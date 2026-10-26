#!/usr/bin/env python3
"""R41C2ReconDepth -- development recon for the C2 `depth-limited` class (round 41 wave 1).

Builds fresh dev SquashFS carriers whose trees hold a regular file that is itself a
SquashFS image, runs REA 6.5.0 `extract-firmware` at `--max-depth 1`, `--max-depth 2`
and the schema default (3), and records for every envelope:

  * the frozen v2 feature tuple (OP, PV, H, G, D, BE, SR, P) via the lane
    interpreter's own `features()` (loaded by path, never modified);
  * every extraction gap verbatim (kind, input_path, dependencies, relative_path,
    handler, range, continuation_id);
  * the published file list (relative_path, sha256, reported_sha256,
    analysis_depth), `depth_limited_paths`, `chunks`, `diagnostics`, `coverage`;
  * the label the committed v2 interpreter gives the envelope;
  * the label my own direct transcription of the DRAFT v3 precedence text gives
    it (`v3_precedence`, section 5) -- a transcription for attack, not an
    independent evaluator.

Nothing here is frozen; the L1 integrates.  Every carrier is authored in scratch
and is a fresh tree: no vendor image, no reserved carrier, no round-40 carrier and
no held-out carrier is opened, copied or hashed by this script.

Usage
    python3 -I -B mkdev.py --work DIR --out DIR --lane LANE [--only id,id]
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True

REA_PACKAGE = 'rea-agents@6.5.0'
SKILL_REL = 'SKILL.md'
INTERP_REL = 'tools/round-40/sqfs-triage-v2.py'
GEN_REL = 'tools/round-40/gen-squashfs.py'
LIST_REL = 'tools/round-40/sqfs-list.py'
RECIPE_REL = 'tools/round-40/heldout-gen-v2.py'

# ---------------------------------------------------------------- determinism ---
def blob(tag, size):
    """Deterministic bytes: sha256 counter stream keyed by tag."""
    out = bytearray()
    counter = 0
    while len(out) < size:
        out += hashlib.sha256(('%s:%d' % (tag, counter)).encode()).digest()
        counter += 1
    return bytes(out[:size])


def write_file(root, rel, data):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as handle:
        handle.write(data)


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for block in iter(lambda: handle.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def run(cmd, cwd=None, env=None):
    proc = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit('command failed (%d): %s\nstdout=%s\nstderr=%s'
                         % (proc.returncode, ' '.join(cmd),
                            proc.stdout[-2000:], proc.stderr[-2000:]))
    return proc


def build_tree_image(work, name, mode, gen, entries, links=()):
    """Author a tree (entries: rel -> bytes; links: (rel, target)) and squash it."""
    tree = os.path.join(work, 'tree-' + name)
    shutil.rmtree(tree, ignore_errors=True)
    os.makedirs(tree)
    for rel, data in entries:
        write_file(tree, rel, data)
    for rel, target in links:
        path = os.path.join(tree, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        os.symlink(target, path)
    out = os.path.join(work, name + '.sqsh')
    run([sys.executable, '-I', '-B', gen, tree, out, '--endian', mode,
         '--comp', 'gzip'])
    return out, tree


LINK_VARIANTS = {
    'alone': [],
    'intree': [('etc/link_rel', '../usr/share/data.bin')],
    'escaping': [('esc_link', '../outside-target')],
    'both': [('etc/link_rel', '../usr/share/data.bin'),
             ('esc_link', '../outside-target')],
}


def oracle_files(tree):
    rows = []
    for root, dnames, fnames in os.walk(tree):
        dnames.sort()
        for name in sorted(fnames):
            path = os.path.join(root, name)
            if os.path.islink(path):
                continue
            rows.append((os.path.relpath(path, tree), sha256_file(path),
                         os.path.getsize(path)))
    rows.sort()
    return rows


def oracle_links(tree):
    rows = []
    for root, dnames, fnames in os.walk(tree):
        dnames.sort()
        for name in sorted(fnames) + sorted(dnames):
            path = os.path.join(root, name)
            if os.path.islink(path):
                rows.append((os.path.relpath(path, tree), os.readlink(path)))
    rows.sort()
    return rows


# ------------------------------------------------------------------- tooling ---
def rea_env():
    env = dict(os.environ)
    env['REA_UNBLOB_COMMAND'] = os.path.join(
        os.path.expanduser('~'), '.local', 'bin', 'unblob')
    return env


def rea_run(work, carrier, max_depth):
    """One REA extract-firmware run; returns (full envelope, argv, exit code)."""
    case_dir = os.path.join(work, 'rea')
    os.makedirs(case_dir, exist_ok=True)
    outdir = os.path.join(case_dir, 'out')  # REA refuses an existing outdir
    argv = [REA_PACKAGE, 'extract-firmware', '--format', 'json', '--full-output']
    if max_depth is not None:
        argv += ['--max-depth', str(max_depth)]
    argv += [carrier, outdir]
    proc = subprocess.run(['npx', '-y'] + argv, cwd=case_dir, env=rea_env(),
                          capture_output=True, text=True)
    text = (proc.stdout or '').strip()
    full = None
    if text:
        try:
            full = json.loads(text)
        except json.JSONDecodeError:
            start = text.find('{')
            if start >= 0:
                try:
                    full = json.loads(text[start:])
                except json.JSONDecodeError:
                    full = None
    return full, argv, proc.returncode, (proc.stderr or '')[-800:]


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ------------------------------------------------- 5. draft v3 precedence text ---
def v3_precedence(feat):
    """Direct transcription of the DRAFT round-41 `## Label precedence` text.

    Labels only: the draft states no action vocabulary, so the action column is
    reported as None (a gap this recon flags).  Written from the plan text alone.
    """
    op, pv = feat['OP'], feat['PV']
    handlers, gaps = feat['H'], set(feat['G'])
    deps, be, sr, published = set(feat['D']), feat['BE'], feat['SR'], feat['P']
    if op != 'extract_firmware' or pv != 'unblob':
        return 'unclassified'
    if not any(h.startswith('squashfs_v4_') for h in handlers):
        return 'no-squashfs-chunk'
    if 'missing-extractor-dependency' in gaps:
        if 'sasquatch-v4be' in deps:
            return 'dep-missing-be'
        if 'sasquatch' in deps:
            return 'dep-missing-le'
    if 'extractor-failure' in gaps and published > 0:
        return 'partial-body-failure'
    if ('extractor-failure' in gaps and published == 0 and be == 'no'
            and 'squashfs_v4_be' in handlers):
        return 'avm-marker-be-dropped'
    if 'extractor-failure' in gaps and published == 0:
        return 'body-extractor-failure'
    if 'depth-limited' in gaps:
        return 'depth-limited-nested'
    if sr == 'yes' and 'unpublished-entry' in gaps:
        return 'mixed-symlinks'
    if sr == 'yes' and not gaps:
        return 'escaping-symlink-removed'
    if gaps == {'unpublished-entry'}:
        return 'in-tree-symlink-metadata'
    if not gaps:
        return 'clean' if published > 0 else 'clean-empty'
    return 'unclassified'


# --------------------------------------------------------------------- driver ---
def case_table(modes=('le', 'be')):
    """(id, mode, chain, variant, max_depth) for every probe.

    chain: 'shallow'  nested image holds two regular files, no nesting
           'deep'     nested image holds another squashfs (3 levels total)
           'links'    nested image holds a squashfs *and* both link kinds
           'partial'  outer holds a damaged squashfs beside the deep chain
    """
    cases = []
    for mode in modes:
        for variant in ('alone', 'intree', 'escaping', 'both'):
            for depth in (1, 2, 3):
                cases.append(('sh-%s-%s-d%d' % (variant, mode, depth), mode,
                              'shallow', variant, depth))
        for depth in (3, 2):
            cases.append(('dp-alone-%s-d%d' % (mode, depth), mode, 'deep',
                          'alone', depth))
        cases.append(('lk-links-%s-d3' % mode, mode, 'links', 'alone', 3))
        for depth in (1, 2):
            cases.append(('tw-two-%s-d%d' % (mode, depth), mode, 'two',
                          'alone', depth))
        cases.append(('pf-partial-%s-d3' % mode, mode, 'partial', 'alone', 3))
        cases.append(('my-unknown-%s-d3' % mode, mode, 'mystery', 'alone', 3))
        cases.append(('ta-tail-%s-d3' % mode, mode, 'tail', 'alone', 3))
    return cases


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--lane', required=True)
    ap.add_argument('--only', default=None)
    ns = ap.parse_args(argv)

    gen = os.path.join(ns.lane, GEN_REL)
    lister = os.path.join(ns.lane, LIST_REL)
    interp_path = os.path.join(ns.lane, INTERP_REL)
    recipe_path = os.path.join(ns.lane, RECIPE_REL)
    skill = os.path.join(ns.lane, SKILL_REL)
    interp = load_module(interp_path, 'sqfs_triage_v2')
    recipe = load_module(recipe_path, 'heldout_gen_v2')

    os.makedirs(ns.work, exist_ok=True)
    os.makedirs(ns.out, exist_ok=True)

    # innermost image per endianness (two regular files, no nesting)
    inner, inner_tree = {}, {}
    for mode in ('le', 'be'):
        base = os.path.join(ns.work, mode)
        os.makedirs(base, exist_ok=True)
        inner[mode], inner_tree[mode] = build_tree_image(
            base, 'inner', mode, gen,
            [('payload/hello.txt', b'inner payload hello\n'),
             ('payload/deep/leaf.bin', blob('leaf', 700))])
    # middle image per endianness: holds inner.sqsh as a regular file
    middle = {}
    for mode in ('le', 'be'):
        base = os.path.join(ns.work, mode)
        middle[mode] = build_tree_image(
            base, 'middle', mode, gen,
            [('mid/note.txt', b'middle note\n'),
             ('inner2.sqsh', open(inner[mode], 'rb').read())])[0]
    # link-bearing middle: a nested squashfs *and* both link kinds one level down
    middle_links = {}
    for mode in ('le', 'be'):
        base = os.path.join(ns.work, mode)
        middle_links[mode] = build_tree_image(
            base, 'middlelinks', mode, gen,
            [('mid/note.txt', b'middle note\n'),
             ('inner2.sqsh', open(inner[mode], 'rb').read())],
            links=[('mid/keep_link', 'note.txt'),
                   ('mid/esc_link', '../../outside-target')])[0]
    # damaged image for the partial probe: zeroed id-table metadata block
    damaged = {}
    for mode in ('le', 'be'):
        base = os.path.join(ns.work, mode)
        payload = bytearray(open(inner[mode], 'rb').read())
        damaged[mode] = os.path.join(base, 'damaged.sqsh')
        with open(damaged[mode], 'wb') as handle:
            handle.write(recipe.corruption_zero_id_table(payload, mode))

    records = []
    for cid, mode, chain, variant, depth in case_table():
        if ns.only and cid not in {item.strip() for item in ns.only.split(',')}:
            continue
        work = os.path.join(ns.work, cid)
        os.makedirs(work, exist_ok=True)
        nested = {'shallow': inner[mode], 'deep': middle[mode],
                  'links': middle_links[mode], 'partial': middle[mode],
                  'two': inner[mode], 'mystery': middle[mode],
                  'tail': middle[mode]}[chain]
        entries = [('etc/banner.txt', b'outer banner v1\n'),
                   ('usr/share/data.bin', blob('data', 2048))]
        if chain == 'two':
            entries += [('inner_a.sqsh', open(nested, 'rb').read()),
                        ('inner_b.sqsh', open(nested, 'rb').read())]
        else:
            entries.append(('inner.sqsh', open(nested, 'rb').read()))
        if chain == 'partial':
            entries.append(('damaged.sqsh', open(damaged[mode], 'rb').read()))
        if chain == 'mystery':
            entries.append(('mystery.bin', blob('mystery', 4096)))
        if chain == 'tail':
            # a valid squashfs chunk with an unknown trailing region in one file
            entries.append(('padded.sqsh',
                            open(inner[mode], 'rb').read() + blob('tail', 4096)))
        carrier, tree = build_tree_image(work, 'outer', mode, gen, entries,
                                        LINK_VARIANTS[variant])
        inspect = run([sys.executable, '-I', '-B', lister, carrier,
                       '--layout', 'auto', '--inspect',
                       '--files', os.path.join(work, 'list.tsv'),
                       '--nonregular', os.path.join(work, 'nonregular.tsv')]).stdout
        full, rea_argv, exit_code, stderr_tail = rea_run(work, carrier, depth)
        record = {
            'id': cid, 'mode': mode, 'chain': chain, 'variant': variant,
            'max_depth': depth,
            'carrier_sha256': sha256_file(carrier),
            'carrier_size': os.path.getsize(carrier),
            'rea_argv': rea_argv, 'rea_exit_code': exit_code,
            'rea_stderr_tail': stderr_tail,
            'oracle_files': oracle_files(tree),
            'oracle_links': oracle_links(tree),
            'sqfs_list_layout': [line.strip() for line in inspect.splitlines()
                                 if '"layout"' in line or '"avm_marker"' in line],
        }
        if full is None or not isinstance(full.get('data'), dict):
            record['error'] = 'no JSON envelope on stdout'
            records.append(record)
            continue
        data = full['data']
        nr = data.get('normalized_result') or {}
        feat = interp.features(data)
        record['ok'] = full.get('ok')
        record['features'] = feat
        record['coverage'] = nr.get('coverage')
        record['depth_limited_paths'] = nr.get('depth_limited_paths')
        record['gaps'] = nr.get('extraction_gaps')
        record['unpublished_entries'] = nr.get('unpublished_entries')
        record['published'] = [
            {'relative_path': f.get('relative_path'),
             'sha256': f.get('sha256'),
             'reported_sha256': f.get('reported_sha256'),
             'analysis_depth': f.get('analysis_depth'),
             'size': f.get('size')}
            for f in nr.get('files') or []]
        record['chunks'] = [
            {'input_path': c.get('input_path'), 'handler': c.get('handler'),
             'extraction_failed': c.get('extraction_failed')}
            for c in nr.get('chunks') or []]
        record['diagnostics'] = [
            {'input_path': d.get('input_path'),
             'typename': (d.get('report') or {}).get('__typename__')}
            for d in nr.get('diagnostics') or []]
        record['subject_sha256'] = ((data.get('subject') or {}).get('digest')
                                    or {}).get('sha256')
        record['digest_matches_carrier'] = (
            record['subject_sha256'] == record['carrier_sha256'])
        record['v3_precedence_label'] = v3_precedence(feat)
        dest = os.path.join(ns.out, 'envelopes', cid)
        os.makedirs(dest, exist_ok=True)
        env_path = os.path.join(dest, 'envelope.json')
        with open(env_path, 'w', encoding='utf-8') as handle:
            json.dump(data, handle, indent=2, sort_keys=True)
            handle.write('\n')
        proc = subprocess.run([sys.executable, '-I', '-B', interp_path,
                               '--skill', skill, '--json', env_path],
                              capture_output=True, text=True)
        record['v2_interpreter_exit'] = proc.returncode
        if proc.returncode == 0:
            payload = json.loads(proc.stdout)
            result = payload['results'][0]
            record['v2_label'] = result['label']
            record['v2_action'] = result['action']
            record['v2_rule'] = result['rule']
        else:
            record['v2_label'] = None
            record['v2_action'] = None
            record['v2_stderr'] = proc.stderr[-400:]
        records.append(record)
        shutil.rmtree(os.path.join(work, 'rea'), ignore_errors=True)
        print('%-22s d=%d H=%s G=%s D=%s BE=%s SR=%s P=%s v2=%s v3=%s'
              % (cid, depth, feat['H'], feat['G'], feat['D'], feat['BE'],
                 feat['SR'], feat['P'], record.get('v2_label'),
                 record.get('v3_precedence_label')), flush=True)

    summary = {
        'generator': 'R41C2ReconDepth/mkdev.py',
        'rea_package': REA_PACKAGE,
        'interpreter': INTERP_REL,
        'interpreter_sha256': sha256_file(interp_path),
        'skill': SKILL_REL,
        'skill_sha256': sha256_file(skill),
        'writer': GEN_REL,
        'writer_sha256': sha256_file(gen),
        'damage_recipe': RECIPE_REL + ' corruption_zero_id_table',
        'cases': records,
    }
    with open(os.path.join(ns.out, 'summary.json'), 'w', encoding='utf-8') as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write('\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
