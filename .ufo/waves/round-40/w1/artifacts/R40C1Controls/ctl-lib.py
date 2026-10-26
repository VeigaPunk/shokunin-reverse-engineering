#!/usr/bin/env python3
"""ctl-lib.py -- materializer for the P40-C1 pre-freeze control suite (R40C1Controls).

Each control is an *exact file overlay* on top of the honest round-40 tree (checked out
at its scored revision) inside a throwaway scratch clone. The overlay is applied by

    python3 -I -B ctl-lib.py --control CTL-C1-3 --root $D --freeze $FREEZE [--spec PATH]

and then committed by the driver (`run-controls.sh`), which records the commit id and
runs the round-40 C1 counter against it. Nothing outside $D is written.

Two kinds of control exist (see suite.json):

  overlay      the attack is file content; this script makes the content.
  position     the attack is *where* the bytes land relative to the freeze commit;
               this script only marks the files, the driver places the commit.

Contract paths (from plans/round-40-claims.md and R40-C1's draft predicate). `--spec`
overrides the spec path; every other path is fixed by this file and echoed in the
control's `claim_paths` so the L1 can rename paths in one place if the freeze differs.

  spec          .ufo/waves/round-40/c1/carriers.json
  control table .ufo/waves/round-40/c1/controls.json
  carriers      corpus/evidence/round-40/c1/<ID>/{carrier.*,oracle.tsv,symlinks.tsv,after.json}
  entry         corpus/knowledge/2026-10-26-r40-avm-be-squashfs-v4-core.md
  province      PROVINCE.md          sources  corpus/SOURCES.md
  readme        corpus/README.md     tools    tools/round-40/

Exit 0 on success, 2 on an unusable control id or a missing precondition (message on
stderr). Never runs REA, unblob or sasquatch; never touches a carrier that this round
declares frozen in a file it does not rewrite itself.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

SPEC = '.ufo/waves/round-40/c1/carriers.json'
CONTROLS = '.ufo/waves/round-40/c1/controls.json'
ENTRY = 'corpus/knowledge/2026-10-26-r40-avm-be-squashfs-v4-core.md'
STEM = '2026-10-26-r40-avm-be-squashfs-v4-core'
PROVINCE = 'PROVINCE.md'
SOURCES = 'corpus/SOURCES.md'
README = 'corpus/README.md'
TOOLS = 'tools/round-40'
GEN39 = 'tools/round-39/gen-squashfs.py'
R39DIR = 'corpus/evidence/round-39/c1'
GENUINE_AVM = 'GENUINE_AVM'          # spec key: path to the genuine AVM-layout body to strip


def die(msg):
    print('ctl-lib: %s' % msg, file=sys.stderr)
    raise SystemExit(2)


def sh(root, *args):
    p = subprocess.run(['git', '-C', root, *args], capture_output=True)
    if p.returncode != 0:
        die('git %s: %s' % (' '.join(args), p.stderr.decode('utf-8', 'replace').strip()))
    return p.stdout


def show(root, rev, path):
    return sh(root, 'show', '%s:%s' % (rev, path))


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def read_json(root, path):
    return json.loads(open(os.path.join(root, path), 'rb').read())


def write_json(root, path, obj):
    full = os.path.join(root, path)
    os.makedirs(os.path.dirname(full) or '.', exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=1, sort_keys=True)
        f.write('\n')


def write_bytes(root, path, data):
    full = os.path.join(root, path)
    os.makedirs(os.path.dirname(full) or '.', exist_ok=True)
    with open(full, 'wb') as f:
        f.write(data)


def read_bytes(root, path):
    with open(os.path.join(root, path), 'rb') as f:
        return f.read()


def carriers(root, spec_path):
    spec = read_json(root, spec_path)
    out = []
    for c in spec['carriers']:
        out.append(c)
    if not out:
        die('spec has no carriers')
    return out


def tsv(root, path):
    rows = []
    for line in read_bytes(root, path).splitlines():
        if line.strip():
            rows.append([c.decode('utf-8', 'surrogateescape') for c in line.split(b'\t')])
    return rows


def re_mint(env):
    """A fortger's re-mint: the id is a digest of the record's own canonical bytes.

    Measured (measurements.txt §2): two honest runs of one carrier have different ids,
    so the id cannot be a run fingerprint; any self-consistent record re-mints to an id
    the counter's own recompute accepts. The overlay writes the value the recompute
    yields for the fabricated record, which is what a re-mint produces.
    """
    body = json.dumps({k: v for k, v in env.items() if k != 'evidence_id'},
                      sort_keys=True, separators=(',', ':'))
    env['evidence_id'] = 'ev_' + sha256(body.encode('utf-8'))
    return env


def synthesize_receipt(carrier, root='', with_root=None):
    """The CTL-C1-2 forgery: everything a holder of the frozen TSVs can assert."""
    oracle = tsv(carrier['_root'], carrier['oracle'])
    if not carrier.get('output_directory'):
        # a forger writes this round's scratch root, because the provenance clause only
        # asks for a path under /kaidoku-r40/ - it cannot tell a run from a string
        carrier['output_directory'] = '/fast/scratch/hyaku/kaidoku-r40/%s/extract' % (
            carrier.get('id') or 'X')
    rootname = with_root or carrier.get('extract_root') or 'firmware.bin_extract'
    files = []
    for rel, sha, size in oracle:
        files.append({
            'relative_path': '%s/%s' % (rootname, rel),
            'path': '%s/%s/%s' % (carrier.get('output_directory', '$OUT'), rootname, rel),
            'size': int(size), 'sha256': sha, 'reported_sha256': sha,
            'mime_type': None, 'analysis_depth': 1,
            'runtime_address': None, 'original_file_range': None})
    gaps, diags = [], []
    if carrier.get('symlinks') and os.path.exists(os.path.join(carrier['_root'], carrier['symlinks'])):
        for row in tsv(carrier['_root'], carrier['symlinks']):
            if len(row) < 3:
                continue
            rel, target, kind = row[0], row[1], row[2]
            if kind == 'in-tree':
                gaps.append({'kind': 'unpublished-entry',
                             'relative_path': '%s/%s' % (rootname, rel)})
            else:
                diags.append({'input_path': '$input', 'report': {
                    '__typename__': 'MaliciousSymlinkRemoved', 'severity': 'WARNING',
                    'link': '%s/%s/%s' % (carrier.get('output_directory', '$OUT'), rootname, rel),
                    'target': target}})
    env = {
        'evidence_id': 'ev_' + '0' * 64,
        'subject': {'name': os.path.basename(carrier['path']),
                    'digest': {'sha256': carrier['sha256']},
                    'local_path': carrier['abs_path'], 'format': 'file',
                    'architecture': None},
        'provider': {'id': 'unblob', 'name': 'Unblob', 'version': '26.6.4'},
        'analysis_profile': None, 'predicate_type': 'rea.analysis',
        'operation': 'extract_firmware',
        'parameters': {'path': carrier['abs_path'],
                       'output_directory': carrier.get('output_directory', '$OUT'),
                       'max_depth': 3, 'max_output_bytes': 268435456,
                       'max_output_files': 10000},
        'raw_result': None,
        'normalized_result': {
            'engine': {'name': 'unblob', 'version': '26.6.4',
                       'executable_path': carrier.get('unblob_path', '$UNBLOB'),
                       'executable_sha256': carrier.get('unblob_sha256', '0' * 64),
                       'source_revision': None, 'worker_count': 1},
            'selection': {'offset': 0, 'length': carrier['size_bytes'],
                          'sha256': carrier['sha256']},
            'output_directory': carrier.get('output_directory', '$OUT'),
            'coverage': 'partial',
            'files': files, 'unpublished_entries': [],
            'chunks': [{'input_path': '$input', 'provider_id': '0:1',
                        'range': {'offset': 0, 'length': carrier['size_bytes']},
                        'root_file_range': {'offset': 0, 'length': carrier['size_bytes']},
                        'handler': 'squashfs_v4_be', 'encrypted': False,
                        'extraction_failed': False}],
            'derivations': [], 'depth_limited_paths': [],
            'diagnostics': diags, 'extraction_gaps': gaps,
            'extraction_continuations': [],
            'published_bytes': sum(f['size'] for f in files)},
        'confidence': 'observed', 'authority': 'shipped-artifact',
        'environment': None,
        'limitations': ['fabricated for control CTL-C1-2'],
        'relationship_coverage': None,
        'locations': [{'kind': 'file-offset-range', 'start': 0,
                       'end': carrier['size_bytes']}],
        'evidence_links': [],
    }
    return re_mint(env)


def load_or_synth(carrier, root):
    """The honest tip's receipt if it exists, else the CTL-C1-2 synthesis.

    C1-14 and C1-18 mutate an existing receipt; on a tree whose receipts have not
    landed yet (the freeze) they fall back to the synthesized shape so the control
    stays runnable, and the report says which base it used.
    """
    path = os.path.join(root, carrier['receipt'])
    if os.path.exists(path):
        return json.loads(open(path, 'rb').read())
    ctx = attach(carrier, root)
    ctx['extract_root'] = carrier.get('extract_root') or (
        os.path.basename(carrier['path']) + '_extract')
    return synthesize_receipt(ctx)


def attach(spec_carrier, root):
    c = dict(spec_carrier)
    c['_root'] = root
    c.setdefault('symlinks', '')
    c['abs_path'] = os.path.join(os.path.abspath(root), c['path'])
    return c


def overlay_c1_1(root, spec_path):
    """Round-39 K1..K6 receipts copied onto the round-40 receipt paths."""
    for c in carriers(root, spec_path):
        src = os.path.join(R39DIR, c['id'], 'after.json') if c['id'] in (
            'K1', 'K2', 'K3', 'K4', 'K5', 'K6') else None
        if not src or not os.path.exists(os.path.join(root, src)):
            # ids differ in round 40: cycle round-39 receipts onto the round-40 ids
            order = ['K1', 'K2', 'K3', 'K4', 'K5', 'K6']
            src = os.path.join(R39DIR, order[carriers(root, spec_path).index(c) % 6],
                               'after.json')
        data = read_bytes(root, src)
        write_bytes(root, c['receipt'], data)


def overlay_c1_2(root, spec_path):
    for c in carriers(root, spec_path):
        write_json(root, c['receipt'], synthesize_receipt(attach(c, root)))


def workdir():
    """Scratch for generated bodies: TMPDIR if set, else a sibling of the clone.

    Never inside the clone: an overlay must change only the files it names, so a
    control can be diffed against the honest tree.
    """
    base = os.environ.get('TMPDIR') or os.environ.get('HYAKU_SCRATCH') or '/tmp'
    d = os.path.join(base, 'ctl-r40-work')
    os.makedirs(d, exist_ok=True)
    return d


def writer_path(root):
    cand = [os.path.join(root, GEN39), os.environ.get('R40_WRITER', '')]
    for p in cand:
        if p and os.path.exists(p):
            return p
    die('no squashfs writer: looked for %s and $R40_WRITER' % GEN39)


def marker_only_body(root, tree=None, comp='gzip'):
    """Build a marker-only standard-BE body with the lane writer (`--endian avm`)."""
    work = workdir()
    os.makedirs(work, exist_ok=True)
    tree = tree or os.path.join(work, 'tree')
    if not os.path.isdir(tree):
        for d, f, body in ((('bin',), ('run',), b'#!/bin/sh\necho hi\n'),
                           (('docs',), ('a.txt',), b'a\n'),
                           (('docs', 'deep'), ('blob.bin',), b'blob\n')):
            os.makedirs(os.path.join(tree, *d), exist_ok=True)
            with open(os.path.join(tree, *d, *f), 'wb') as fh:
                fh.write(body)
    out = os.path.join(work, 'marker-only.sqsh')
    subprocess.run([sys.executable, '-I', '-B', writer_path(root), tree, out,
                    '--endian', 'avm', '--comp', comp], check=True,
                   capture_output=True)
    with open(out, 'rb') as fh:
        return fh.read()


def stage():
    return os.environ.get('CTL_STAGE', 'all')


def writes_receipts(control):
    st = stage()
    if control in FREEZE_SIDE:
        return st in ('all', 'tip')
    return st in ('all', 'freeze', 'tip')


def overlay_c1_3(root, spec_path):
    """Marker-only standard-BE bodies on every carrier; honest docs; shaped receipts.

    The spec is rewritten to stay consistent with the new bytes (pin, size, oracle
    digest and row count), so no pin/oracle-shape clause fires and the *only* byte
    clause that can refuse this control is the block-length endianness one.
    """
    base_body = marker_only_body(root)
    spec = read_json(root, spec_path)
    for idx, c in enumerate(carriers(root, spec_path)):
        body = base_body + b'\0' * idx          # distinct bytes, bytes_used unchanged
        write_bytes(root, c['path'], body)
        # the oracle must still be a *true* file list for these bytes: standard-BE reader
        # (the lane reader auto-selects endianness from the magic, so a plain run is the
        # real file set of this marker-only body).
        out = os.path.join(workdir(), 'oracle-%s.tsv' % c['id'])
        subprocess.run([sys.executable, '-I', '-B',
                        os.path.join(root, TOOLS, 'sqfs-list.py'),
                        os.path.join(root, c['path']), '--files', out,
                        '--symlinks', os.path.join(workdir(), 'sym-%s.tsv' % c['id'])],
                       check=True, capture_output=True)
        write_bytes(root, c['oracle'], read_bytes(root, out))
        c2 = dict(c)
        c2['sha256'] = sha256(body)
        c2['size_bytes'] = len(body)
        c2['oracle'] = c['oracle']
        for sc in spec['carriers']:
            if sc['id'] == c['id']:
                sc['sha256'] = sha256(body)
                sc['size_bytes'] = len(body)
                sc['oracle_sha256'] = sha256(read_bytes(root, c['oracle'])) \
                    if os.path.exists(os.path.join(root, c['oracle'])) else sc.get('oracle_sha256')
                sc['oracle_files'] = len(tsv(root, c['oracle'])) if os.path.exists(
                    os.path.join(root, c['oracle'])) else sc.get('oracle_files')
        if writes_receipts('CTL-C1-3'):
            ctx = attach(c2, root)
            ctx['extract_root'] = os.path.basename(c['path']) + '_extract'
            # a marker-only body publishes nothing with sasquatch-v4be (no -be); the
            # receipt this control writes asserts success, which is the whole point:
            # the body is not AVM.
            write_json(root, c['receipt'], synthesize_receipt(ctx))
    write_json(root, spec_path, spec)


def overlay_c1_4(root, spec_path):
    """Genuine AVM-layout bodies with mkfs_time normalised, receipts kept truthful-shaped."""
    spec = read_json(root, spec_path)
    src = spec.get(GENUINE_AVM)
    if not src or not os.path.exists(src):
        die('spec key %s must name the genuine AVM-layout body to strip' % GENUINE_AVM)
    raw = bytearray(open(src, 'rb').read())
    if len(raw) < 96:
        die('genuine body too short')
    raw[8:12] = (1700000000).to_bytes(4, 'big')      # mkfs_time != bytes_used
    body = bytes(raw)
    spec = read_json(root, spec_path)
    for idx, c in enumerate(carriers(root, spec_path)):
        cbody = body + b'\0' * idx
        write_bytes(root, c['path'], cbody)
        for sc in spec['carriers']:
            if sc['id'] == c['id']:
                sc['sha256'] = sha256(cbody)
                sc['size_bytes'] = len(cbody)
        if writes_receipts('CTL-C1-4'):
            c2 = dict(c)
            c2['sha256'] = sha256(cbody)
            c2['size_bytes'] = len(cbody)
            ctx = attach(c2, root)
            ctx['extract_root'] = os.path.basename(c['path']) + '_extract'
            write_json(root, c['receipt'], synthesize_receipt(ctx))
    write_json(root, spec_path, spec)


def overlay_c1_6(root, spec_path):
    """PATH shim that forces -be, plus the receipt shape that run really produces."""
    shimdir = os.path.join(root, '.ctl-bin')
    os.makedirs(shimdir, exist_ok=True)
    shim = os.path.join(shimdir, 'sasquatch-v4be')
    with open(shim, 'w', encoding='utf-8') as f:
        f.write('#!/bin/sh\n# CTL-C1-6: force -be, the marker decision inverted\n'
                'exec "%s" -be "$@"\n'
                % os.path.expanduser('~/.local/bin/sasquatch-v4be'))
    os.chmod(shim, 0o755)
    # the shape forced--be produces on a genuine AVM layout is the tested shape of a
    # failed extraction (receipt-markeronly-dev.json): handler squashfs_v4_be,
    # extraction_failed true, 0 files, one extractor-failure gap.
    for c in carriers(root, spec_path):
        env = synthesize_receipt(attach(c, root))
        for ch in env['normalized_result']['chunks']:
            ch['extraction_failed'] = True
        env['normalized_result']['files'] = []
        env['normalized_result']['derivations'] = []
        env['normalized_result']['diagnostics'] = [{'input_path': '$input', 'report': {
            '__typename__': 'ExtractCommandFailedReport', 'severity': 'ERROR'}}]
        env['normalized_result']['extraction_gaps'] = [{
            'kind': 'extractor-failure', 'input_path': '$input', 'relative_path': None,
            'handler': 'squashfs_v4_be', 'provider_id': '0:1',
            'range': {'offset': 0, 'length': c['size_bytes']},
            'root_file_range': {'offset': 0, 'length': c['size_bytes']},
            'dependencies': [], 'continuation_id': '0' * 64}]
        env['normalized_result']['published_bytes'] = 0
        write_json(root, c['receipt'], re_mint(env))
    write_json(root, '.ctl-bin/README.json', {'control': 'CTL-C1-6', 'shim': shim,
                                              'note': 'prepend .ctl-bin to the child PATH'})


def overlay_c1_8(root, spec_path):
    """Four carrier ids, two distinct byte strings: the target is a count."""
    cs = carriers(root, spec_path)
    if len(cs) < 2:
        die('need at least two carriers to duplicate')
    spec = read_json(root, spec_path)
    first, second = cs[0], cs[1]
    alias = [cs[2] if len(cs) > 2 else cs[0], cs[3] if len(cs) > 3 else cs[1]]
    for dst, src in ((alias[0], first), (alias[1], second)):
        body = read_bytes(root, src['path'])
        write_bytes(root, dst['path'], body)
        new_sha = sha256(body)
        for key in ('oracle', 'symlinks'):
            if dst.get(key) and os.path.exists(os.path.join(root, src[key])):
                write_bytes(root, dst[key], read_bytes(root, src[key]))
        for c in spec['carriers']:
            if c['id'] != dst['id']:
                continue
            # a lane that aliases V2=V1 keeps its own spec *consistent*: pin, size,
            # oracle digest and provenance all match the aliased bytes, so no pin
            # binding fires and only the distinctness clause can refuse it.
            c['sha256'] = new_sha
            c['size_bytes'] = len(body)
            c['oracle_sha256'] = src.get('oracle_sha256')
            c['oracle_files'] = src.get('oracle_files')
            if 'provenance' in src:
                c['provenance'] = src['provenance']
    write_json(root, spec_path, spec)
    if writes_receipts('CTL-C1-8'):
        for c in spec['carriers']:
            ctx = attach(c, root)
            ctx['extract_root'] = c.get('extract_root') or (
                os.path.basename(c['path']) + '_extract')
            write_json(root, c['receipt'], synthesize_receipt(ctx))


def overlay_c1_14(root, spec_path):
    """Publication under a wrong root: every oracle row matched by suffix, tree wrong."""
    for c in carriers(root, spec_path):
        env = load_or_synth(c, root)
        for f in env['normalized_result']['files']:
            f['relative_path'] = 'nested/wrong-root/' + f['relative_path']
        for d in env['normalized_result']['derivations']:
            for k in ('parent_path', 'child_path'):
                if d.get(k):
                    d[k] = d[k].replace('$output/', '$output/nested/wrong-root/')
        write_json(root, c['receipt'], re_mint(env))


def overlay_c1_17(root, spec_path):
    """Cite only round-39 SOURCES rows (same calendar date) and add no round-40 row.

    The round-39 counter tested `row date == 2026-10-26`; every round in this lane is on
    that date, so a date test cannot separate rounds. The honest tree's round-40 row is
    removed, the entry and the docs cite S112/S122 instead.
    """
    rows = [ln for ln in read_bytes(root, SOURCES).splitlines()
            if b'2026-10-26-r40-' not in ln]
    rows.append(b'| S112 | unblob SquashFS handler at tag 26.6.4 | code | A | a | b | c '
                b'| mined | 2026-10-26 | 180d | '
                b'corpus/knowledge/2026-10-26-r40-avm-be-squashfs-v4-core.md |')
    write_bytes(root, SOURCES, b'\n'.join(rows) + b'\n')
    path = os.path.join(root, ENTRY)
    entry = (open(path, 'rb').read().decode('utf-8') if os.path.exists(path) else
             '# AVM layout knowledge entry (control)\n')
    entry += ('\nMarker semantics: S112 and S122 (round-39 rows, opened 2026-10-26) carry '
              'the handler and containment facts this entry uses.\n')
    write_bytes(root, ENTRY, entry.encode('utf-8'))


def overlay_c1_18(root, spec_path):
    """Self-fulfilling oracle: keep only the rows the receipt publishes."""
    for c in carriers(root, spec_path):
        if not writes_receipts('CTL-C1-18'):
            # freeze side: trim the oracle to the subset the (post-freeze) receipt shows
            keep_rows = tsv(root, c['oracle'])[:-1]
            write_bytes(root, c['oracle'], b''.join(
                ('\t'.join(r) + '\n').encode('utf-8', 'surrogateescape')
                for r in keep_rows))
            continue
        env = load_or_synth(c, root)
        files = env['normalized_result']['files']
        if len(files) > 1:
            # the extractor "misses" one file and the oracle is trimmed to agree: the
            # attack is a *partial* extraction whose oracle was written from it.
            env['normalized_result']['files'] = files[:-1]
        for d in env['normalized_result']['derivations']:
            pass
        write_json(root, c['receipt'], env)
        published = set()
        for f in env['normalized_result']['files']:
            rel = f['relative_path']
            for row in tsv(root, c['oracle']):
                if rel == row[0] or rel.endswith('/' + row[0]):
                    published.add(row[0])
        keep = [ln for ln in read_bytes(root, c['oracle']).splitlines()
                if ln.split(b'\t')[0].decode('utf-8', 'surrogateescape') in published]
        write_bytes(root, c['oracle'], b'\n'.join(keep) + (b'\n' if keep else b''))


def overlay_c1_21(root, spec_path):
    """Docs complete except the superseding frontier note."""
    text = read_bytes(root, PROVINCE).decode('utf-8')
    out = [ln for ln in text.splitlines(True)
           if not ('Round-40 frontier note' in ln or 'Round-40 frontier' in ln)]
    write_bytes(root, PROVINCE, ''.join(out).encode('utf-8'))


def overlay_c1_22(root, spec_path):
    """A frontier note that is present but says the opposite."""
    text = read_bytes(root, PROVINCE).decode('utf-8')
    out = []
    for ln in text.splitlines(True):
        if 'Round-40 frontier note' in ln:
            ln = ('Round-40 frontier note, 2026-10-26: the AVM part of the '
                  '`- **sasquatch** — …` bullet stays Frontier; genuine AVM-layout '
                  'big-endian bodies remain unmeasured.\n')
        out.append(ln)
    write_bytes(root, PROVINCE, ''.join(out).encode('utf-8'))


def overlay_n1(root, spec_path):
    """Anti-control: the honest tree, untouched. Must pass."""
    return


# Controls that write a frozen path (carrier, oracle, spec) *and* receipts: the driver
# applies the freeze side in the freeze commit and the tip side one commit later, so the
# receipt-descent clause stays true and only the carrier clause can refuse them.
FREEZE_SIDE = {'CTL-C1-3', 'CTL-C1-4', 'CTL-C1-8', 'CTL-C1-18'}


OVERLAYS = {
    'CTL-C1-1': overlay_c1_1,
    # CTL-C1-5 is a commit-position control: its overlay is the synthesized receipt set
    # landing in the freeze commit itself, so the file content is C1-2's.
    'CTL-C1-5': overlay_c1_2,
    # CTL-C1-9 swaps carriers/oracles/receipts after the freeze: content is C1-3's.
    'CTL-C1-9': overlay_c1_3,
    'CTL-C1-2': overlay_c1_2,
    'CTL-C1-3': overlay_c1_3,
    'CTL-C1-4': overlay_c1_4,
    'CTL-C1-6': overlay_c1_6,
    'CTL-C1-8': overlay_c1_8,
    'CTL-C1-14': overlay_c1_14,
    'CTL-C1-17': overlay_c1_17,
    'CTL-C1-18': overlay_c1_18,
    'CTL-C1-21': overlay_c1_21,
    'CTL-C1-22': overlay_c1_22,
    'CTL-C1-N1': overlay_n1,
}

POSITION_ONLY = ('CTL-C1-0', 'CTL-C1-16', 'CTL-C1-N2', 'CTL-C1-6b', 'CTL-C1-19')


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--control', required=True)
    ap.add_argument('--root', required=True)
    ap.add_argument('--freeze', default=None)
    ap.add_argument('--spec', default=SPEC)
    ap.add_argument('--stage', choices=('all', 'freeze', 'tip'), default='all')
    a = ap.parse_args(argv[1:])
    if a.control in POSITION_ONLY:
        print('ctl-lib: %s is a commit-position control; the driver places it '
              '(see suite.json)' % a.control)
        return 0
    fn = OVERLAYS.get(a.control)
    if fn is None:
        die('unknown control %r' % a.control)
    if a.freeze:
        os.environ.setdefault('CTL_FREEZE', a.freeze)
    os.environ['CTL_STAGE'] = a.stage
    fn(a.root, a.spec)
    print('ctl-lib: applied %s to %s' % (a.control, a.root))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
