#!/usr/bin/env python3
"""R39-C1 counter (coverage: standard big-endian SquashFS v4 -> Core).

Predicate P39-C1 (draft; the sentence that freezes in plans/round-39-claims.md):
  At the measured revision, for each of the six frozen big-endian SquashFS v4
  carriers, the committed round-39 REA extract-firmware after-receipt (rea-agents
  6.5.0, unblob 26.6.4, sasquatch-v4be 4.5.1 reachable on the child PATH), first
  added in a commit that descends from the freeze, names the `squashfs_v4_be`
  handler with no failed chunk, publishes every regular file of the frozen
  independent oracle (same relative-path suffix, same sha256), carries extraction
  gaps of kind `unpublished-entry` exactly on the frozen oracle's in-tree symlinks
  and no other gap, publishes no path for the oracle's escaping symlinks, has a
  subject digest equal to the frozen carrier pin, and recomputes to its stored
  evidence id under the rea-agents 6.5.0 rule; PROVINCE.md holds a
  `## Round-39 additions to Core` row naming `squashfs_v4_be` that cites the
  round-39 knowledge entry, which cites a SOURCES.md row opened 2026-10-26 whose
  used-by lists that entry; a round-39 frontier note supersedes the big-endian
  part of the Frontier bullet; corpus/README.md holds a coverage-map row naming
  the entry stem; and no frozen C1 path changed after the freeze.

Target: carriers_matched == 6 and every binding true.

Per-carrier clauses (all must hold):
  carrier_present        the carrier file exists at REV
  carrier_pin_ok         sha256(bytes at REV) == the frozen pin
  oracle_ok              oracle.tsv parses and holds >= 1 regular file
  symlinks_ok            symlinks.tsv parses; every kind is in-tree|escaping
  receipt_present        corpus/evidence/round-39/c1/<id>/after.json parses
  receipt_fresh          its first-add commit at REV is a strict descendant of --freeze
  subject_pin_ok         subject.digest.sha256 == the frozen pin
  operation_ok           operation == extract_firmware and provider.id == unblob
  handler_ok             a chunk names squashfs_v4_be
  chunks_ok              no chunk carries extraction_failed: true
  oracle_hits            every oracle regular file is published (same relative-path
                         suffix, same sha256)
  gaps_ok                the extraction_gaps multiset is exactly one
                         `unpublished-entry` on each in-tree symlink and nothing else
  escaping_ok            no published file path ends with an escaping symlink path
  run_provenance_ok      parameters.output_directory names this round's scratch
                         segment (/kaidoku-r39/): the receipt is a run of this round,
                         not a byte copy of an earlier round's receipt. `parameters`
                         is inside the hashed 6.5.0 semanticProjection, so the field
                         cannot be edited without breaking evidence_id_ok
  evidence_id_ok         stored evidence id == id recomputed under the frozen
                         rea-agents 6.5.0 rule (tools/round-27/xpin-attribute.mjs)

Non-vacuity bindings (properties of the frozen carrier/symlink/oracle set, so they
cannot be gamed after the freeze):
  symlink_coverage       across the six symlinks.tsv files: >= 2 in-tree rows,
                         >= 2 escaping rows, and >= 1 carrier with >= 2 in-tree rows
                         (so the per-link gap cardinality is exercised, not just
                         "a gap exists somewhere")
  xz_leg                 >= 1 carrier whose own superblock is BE SquashFS v4
                         (magic `sqsh`, major 4, minor 0) with the xz compression id
                         (2 = this lane's tools/round-37/gen-squashfs.py `--comp xz`,
                         4 = upstream squashfs-tools XZ), so the xz decompressor leg
                         is bound and not only gzip
  carriers_spec_ok       six distinct ids K1..K6 with six distinct pins and the
                         id/path/sha256/oracle/symlinks fields present

Freeze-drift binding (routed defect R38-CL4): if any commit in FREEZE..REV touches
one of plans/round-39-claims.md, tools/round-39/c1-counter.py,
tools/round-39/c1-run.sh, .ufo/waves/round-39/c1/carriers.json, or any carrier,
oracle or symlinks file that carriers.json lists, the counter exits 2 with
reason `frozen_path_changed` and never reports met.

Usage:
  c1-counter.py --root LANE --rev REV --freeze FREEZE --pkg65 REA650_PKG_ROOT [--json-out PATH]
  c1-counter.py --selftest --pkg65 REA650_PKG_ROOT
Exit: 0 target met, 1 target not met, 2 unevaluable (bad args, git/node failure,
frozen path changed). Reads lane bytes only through git objects (git show
REV:path); writes only a private scratch dir under
$HYAKU_SCRATCH (default /fast/scratch/hyaku)/kaidoku-r39/counter and --json-out.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

CARRIERS = '.ufo/waves/round-39/c1/carriers.json'
AFTERDIR = 'corpus/evidence/round-39/c1'
ENTRY = 'corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md'
STEM = '2026-10-26-r39-be-squashfs-v4-core'
CORE_HEADING = '## Round-39 additions to Core'
FRONTIER_MARK = 'Round-39 frontier note'
HANDLER = 'squashfs_v4_be'
XPIN = 'tools/round-27/xpin-attribute.mjs'
OPENED = '2026-10-26'
TARGET = 6
IDS = ('K1', 'K2', 'K3', 'K4', 'K5', 'K6')
FROZEN_PATHS = (
    'plans/round-39-claims.md',
    'tools/round-39/c1-counter.py',
    'tools/round-39/c1-run.sh',
    CARRIERS,
)
HANDLER_RE = re.compile(r'(?<![A-Za-z0-9_-])' + HANDLER + r'(?![A-Za-z0-9_-])')
SID_RE = re.compile(r'(?<![0-9A-Za-z])(S\d{3,})(?![0-9A-Za-z])')
BINDINGS = ('province_core_section', 'province_core_row', 'frontier_note',
            'entry_present', 'sourced', 'coverage_map_row', 'carriers_spec_ok',
            'symlink_coverage', 'xz_leg')
CLAUSES = ('carrier_present', 'carrier_pin_ok', 'oracle_ok', 'symlinks_ok',
           'receipt_present', 'receipt_fresh', 'subject_pin_ok', 'operation_ok',
           'handler_ok', 'chunks_ok', 'gaps_ok', 'escaping_ok',
           'run_provenance_ok', 'evidence_id_ok')
PROV_SEGMENT = '/kaidoku-r39/'
XZ_COMPRESSION_IDS = (2, 4)


class Unevaluable(Exception):
    reason = 'unevaluable'


class FrozenPathChanged(Unevaluable):
    reason = 'frozen_path_changed'

    def __init__(self, paths):
        self.paths = list(paths)
        super().__init__('frozen path changed after freeze: ' + ', '.join(self.paths))


def git(root, *args, check=True):
    p = subprocess.run(['git', '-C', root, *args], capture_output=True)
    if check and p.returncode != 0:
        raise Unevaluable('git ' + ' '.join(args) + ': ' + p.stderr.decode(errors='replace').strip())
    return p


def show(root, rev, path):
    p = git(root, 'show', f'{rev}:{path}', check=False)
    return p.stdout if p.returncode == 0 else None


def scratch_root():
    d = os.path.join(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'),
                     'kaidoku-r39', 'counter')
    os.makedirs(d, exist_ok=True)
    return d


def section(text, heading):
    lines = text.splitlines()
    try:
        i = lines.index(heading)
    except ValueError:
        return None
    out = []
    for line in lines[i + 1:]:
        if line.startswith('## '):
            break
        out.append(line)
    return out


def cells(row):
    return [c.strip() for c in row.strip().strip('|').split('|')]


def sid_tokens(text):
    return set(SID_RE.findall(text))


def evidence_ids(root, freeze, pkg65, envelopes, work):
    tool = show(root, freeze, XPIN)
    if tool is None:
        raise Unevaluable('xpin tool absent at freeze')
    tpath = os.path.join(work, 'xpin-attribute.mjs')
    open(tpath, 'wb').write(tool)
    paths = []
    for name, env in envelopes.items():
        p = os.path.join(work, name.replace('/', '_') + '.wrapped.json')
        json.dump({'data': env}, open(p, 'w'))
        paths.append((name, p))
    if not paths:
        return {}
    r = subprocess.run(['node', tpath, '--pkg65', pkg65, '--pkg67', pkg65] + [p for _, p in paths],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise Unevaluable('xpin: ' + r.stderr.strip())
    out = {}
    lines = [l for l in r.stdout.splitlines() if l]
    if len(lines) != len(paths):
        raise Unevaluable('xpin line count mismatch')
    for (name, _), line in zip(paths, lines):
        f = line.split('\t')
        if len(f) < 3:
            raise Unevaluable('xpin bad line: ' + line)
        out[name] = (f[1], f[2])
    return out


def parse_tsv(raw, width):
    """Return (rows, error). Paths and hashes keep their bytes (only CR is dropped);
    the trailing kind cell of symlinks.tsv is normalised."""
    rows = []
    if raw is None:
        return None, 'absent'
    for line in raw.decode().splitlines():
        if not line.strip():
            continue
        f = [c.rstrip('\r') for c in line.split('\t')]
        if len(f) != width:
            return None, 'row %r has %d fields, want %d' % (line, len(f), width)
        if width == 3 and f[2].strip() in ('in-tree', 'escaping'):
            f[2] = f[2].strip()
        rows.append(f)
    return rows, None


def provenance_ok(output_directory):
    """A receipt run by this round: absolute, inside the kaidoku-r39 scratch
    segment, and without a `..` segment that could leave it."""
    if not isinstance(output_directory, str) or not os.path.isabs(output_directory):
        return False
    if PROV_SEGMENT not in output_directory:
        return False
    return '..' not in output_directory.split('/')


def same_rel(candidate, rel):
    return bool(candidate) and bool(rel) and (candidate == rel or candidate.endswith('/' + rel))


def resolve_kind(rel, target):
    """Class of a link under unblob 26.6.4's rule, for a per-carrier diagnostic.

    unblob/extractor.py:50 fix_symlink + file_utils.py:34 is_safe_path: an absolute
    target loses its leading `/` and is resolved from the extraction root; a relative
    target is resolved against the link's own directory. A resolved path that still
    begins with `..` leaves the root (escaping). No normaliser clamping: this is the
    convention seat R39C1SymlinkK1K4 froze (`../hello.txt` at depth 0 escapes).

    Diagnostic only: it never gates the target. A disagreement with the frozen
    symlinks.tsv kind is reported per carrier as symlink_kind_recompute_mismatch."""
    base = rel.rsplit('/', 1)[0] if ('/' in rel and not target.startswith('/')) else ''
    t = target.lstrip('/') if target.startswith('/') else target
    joined = os.path.normpath(os.path.join(base, t) if base else t)
    if joined == '..' or joined.startswith('../'):
        return 'escaping'
    return 'in-tree'


def published(env):
    nr = env.get('normalized_result') or {}
    out = []
    for f in (nr.get('files') or []):
        if isinstance(f, dict):
            out.append((f.get('relative_path') or '', f.get('sha256') or ''))
    return out


def chunk_handlers(env):
    nr = env.get('normalized_result') or {}
    return [c.get('handler') for c in (nr.get('chunks') or []) if isinstance(c, dict)]


def chunk_failed(env):
    nr = env.get('normalized_result') or {}
    return any(isinstance(c, dict) and c.get('extraction_failed') for c in (nr.get('chunks') or []))


def gaps(env):
    nr = env.get('normalized_result') or {}
    return list(nr.get('extraction_gaps') or [])


def oracle_hits(oracle, files):
    hits = 0
    for row in oracle:
        rel, sha = row[0], row[1]
        if any(sha == fs and same_rel(fp, rel) for fp, fs in files):
            hits += 1
    return hits


def gaps_ok(gaps_list, in_tree):
    """Exactly one `unpublished-entry` gap per in-tree symlink, nothing else."""
    seen = []
    for g in gaps_list:
        if not isinstance(g, dict):
            return False, 'non-object gap'
        kind = g.get('kind')
        if kind != 'unpublished-entry':
            return False, 'unexpected gap kind %r' % (kind,)
        rp = g.get('relative_path') or ''
        hits = [r for r in in_tree if same_rel(rp, r)]
        if len(hits) != 1:
            return False, 'gap path %r matches %d in-tree symlinks' % (rp, len(hits))
        seen.append(hits[0])
    if sorted(seen) != sorted(in_tree):
        return False, '%d gaps on %d in-tree symlinks' % (len(seen), len(in_tree))
    return True, '%d gaps == %d in-tree symlinks' % (len(seen), len(in_tree))


def escaping_published(files, escaping):
    hits = []
    for fp, _ in files:
        for e in escaping:
            if same_rel(fp, e):
                hits.append(fp)
    return hits


def first_add(root, rev, path):
    p = git(root, 'log', '--diff-filter=A', '--format=%H', rev, '--', path, check=False)
    if p.returncode != 0:
        return None
    lines = [l.strip() for l in p.stdout.decode().splitlines() if l.strip()]
    return lines[-1] if lines else None


def superblock_compression(raw):
    """Compression id of a BE SquashFS v4 superblock, or None (diagnostic + xz_leg)."""
    if not raw or len(raw) < 32 or raw[0:4] != b'sqsh':
        return None
    major = int.from_bytes(raw[28:30], 'big')
    minor = int.from_bytes(raw[30:32], 'big')
    if (major, minor) != (4, 0):
        return None
    return int.from_bytes(raw[20:22], 'big')


def is_ancestor(root, ancestor, descendant):
    p = git(root, 'merge-base', '--is-ancestor', ancestor, descendant, check=False)
    return p.returncode == 0


def frozen_drift(root, freeze, rev, spec):
    """Commits in FREEZE..REV that touch a frozen C1 path (freeze-drift binding)."""
    frozen = set(FROZEN_PATHS)
    for c in spec.get('carriers') or []:
        for key in ('path', 'oracle', 'symlinks'):
            v = c.get(key)
            if isinstance(v, str) and v:
                frozen.add(v)
    p = git(root, 'log', '--pretty=format:', '--name-only', '--no-renames',
            f'{freeze}..{rev}', check=False)
    if p.returncode != 0:
        raise Unevaluable('git log freeze..rev failed')
    touched = sorted({l.strip() for l in p.stdout.decode(errors='replace').splitlines()
                      if l.strip() and l.strip() in frozen})
    return touched


def carriers_spec(spec):
    """(ids, problems) for the frozen carrier list."""
    probs = []
    cs = spec.get('carriers')
    if not isinstance(cs, list):
        return [], ['carriers is not a list']
    ids = [c.get('id') for c in cs if isinstance(c, dict)]
    if len(ids) != TARGET:
        probs.append('carriers has %d entries, want %d' % (len(ids), TARGET))
    if len(set(ids)) != len(ids):
        probs.append('duplicate carrier ids %r' % (ids,))
    if set(ids) != set(IDS):
        probs.append('carrier ids %r != %r' % (sorted(map(str, ids)), list(IDS)))
    pins = [c.get('sha256') for c in cs if isinstance(c, dict)]
    if len(set(pins)) != len(pins):
        probs.append('duplicate carrier pins')
    for c in cs:
        if not isinstance(c, dict):
            probs.append('non-object carrier entry')
            continue
        for key in ('id', 'path', 'sha256', 'oracle', 'symlinks'):
            if not isinstance(c.get(key), str) or not c.get(key):
                probs.append('carrier %r lacks %s' % (c.get('id'), key))
    return ids, probs


def measure(root, rev, freeze, pkg65):
    res = {'revision': rev, 'freeze': freeze, 'predicate': 'P39-C1', 'target': TARGET}
    git(root, 'cat-file', '-e', f'{rev}^{{commit}}')
    git(root, 'cat-file', '-e', f'{freeze}^{{commit}}')
    frozen = show(root, freeze, CARRIERS)
    if frozen is None:
        raise Unevaluable('carriers.json absent at freeze')
    spec = json.loads(frozen)
    cur = show(root, rev, CARRIERS)
    res['carriers_unchanged'] = cur == frozen

    drift = frozen_drift(root, freeze, rev, spec)
    res['frozen_path_changed'] = drift
    if drift:
        raise FrozenPathChanged(drift)

    ids, spec_probs = carriers_spec(spec)
    res['carriers_spec_problems'] = spec_probs

    work = tempfile.mkdtemp(prefix='c1-counter.', dir=scratch_root())
    try:
        per = {}
        envs = {}
        for c in spec.get('carriers') or []:
            if not isinstance(c, dict):
                continue
            k = c.get('id')
            d = {'id': k}
            pin = c.get('sha256')
            cpath = c.get('path')
            opath = c.get('oracle')
            spath = c.get('symlinks')
            rpath = c.get('receipt') or f'{AFTERDIR}/{k}/after.json'

            raw = show(root, rev, cpath) if cpath else None
            d['carrier_present'] = raw is not None
            d['carrier_pin_ok'] = raw is not None and hashlib.sha256(raw).hexdigest() == pin
            d['superblock_compression'] = superblock_compression(raw)

            oracle, oerr = parse_tsv(show(root, rev, opath) if opath else None, 3)
            d['oracle_error'] = oerr
            oracle = oracle or []
            d['oracle_files'] = len(oracle)
            d['oracle_ok'] = oerr is None and len(oracle) > 0

            links, serr = parse_tsv(show(root, rev, spath) if spath else None, 3)
            d['symlinks_error'] = serr
            links = links or []
            bad_kind = [l for l in links if l[2] not in ('in-tree', 'escaping')]
            d['symlinks_ok'] = serr is None and not bad_kind
            in_tree = [l[0] for l in links if l[2] == 'in-tree']
            escaping = [l[0] for l in links if l[2] == 'escaping']
            d['in_tree_symlinks'] = len(in_tree)
            d['escaping_symlinks'] = len(escaping)
            d['symlink_kind_recompute_mismatch'] = [
                [l[0], l[2], resolve_kind(l[0], l[1])] for l in links
                if l[2] in ('in-tree', 'escaping') and resolve_kind(l[0], l[1]) != l[2]]

            raw_receipt = show(root, rev, rpath)
            try:
                env = json.loads(raw_receipt) if raw_receipt else None
            except json.JSONDecodeError:
                env = None
            if not isinstance(env, dict):
                env = None
            d['receipt_path'] = rpath
            d['receipt_present'] = env is not None

            add = first_add(root, rev, rpath) if raw_receipt is not None else None
            d['receipt_first_add'] = add
            d['receipt_fresh'] = bool(add) and add != freeze and is_ancestor(root, freeze, add)

            if env is not None:
                envs[f'{k}/after'] = env
                nr_sub = env.get('subject') or {}
                d['subject_pin_ok'] = ((nr_sub.get('digest') or {}).get('sha256')
                                      if isinstance(nr_sub, dict) else None) == pin
                prov = env.get('provider') or {}
                d['operation_ok'] = (env.get('operation') == 'extract_firmware'
                                     and isinstance(prov, dict) and prov.get('id') == 'unblob')
                d['handler_ok'] = HANDLER in chunk_handlers(env)
                d['chunks_ok'] = not chunk_failed(env)
                files = published(env)
                d['published_files'] = len(files)
                d['oracle_hits'] = oracle_hits(oracle, files)
                ok, why = gaps_ok(gaps(env), in_tree)
                d['gaps_ok'] = ok
                d['gaps_note'] = why
                esc = escaping_published(files, escaping)
                d['escaping_ok'] = not esc
                d['escaping_published'] = esc[:5]
                params = env.get('parameters') or {}
                od = params.get('output_directory') if isinstance(params, dict) else None
                d['output_directory'] = od
                d['run_provenance_ok'] = provenance_ok(od)
            per[k] = d

        ev = evidence_ids(root, freeze, pkg65, envs, work)
        matched = 0
        for k, d in per.items():
            key = f'{k}/after'
            d['evidence_id_ok'] = (key in ev and ev[key][0] == ev[key][1]
                                   and ev[key][0].startswith('ev_'))
            ok = (
                d.get('carrier_present') and d.get('carrier_pin_ok')
                and d.get('oracle_ok') and d.get('symlinks_ok')
                and d.get('receipt_present') and d.get('receipt_fresh')
                and d.get('subject_pin_ok') and d.get('operation_ok')
                and d.get('handler_ok') and d.get('chunks_ok')
                and d.get('gaps_ok') and d.get('escaping_ok')
                and d.get('run_provenance_ok') and d.get('evidence_id_ok')
                and d.get('oracle_hits') == d.get('oracle_files')
            )
            d['matched'] = bool(ok)
            matched += bool(ok)
        res['carrier_ids'] = ids
        res['carriers'] = per
        res['carriers_matched'] = matched
    finally:
        shutil.rmtree(work, ignore_errors=True)

    b = {}
    prov = show(root, rev, 'PROVINCE.md')
    prov_text = prov.decode(errors='replace') if prov else ''
    sec = section(prov_text, CORE_HEADING) if prov else None
    b['province_core_section'] = sec is not None
    rows = [l for l in (sec or []) if l.lstrip().startswith('|')]
    b['province_core_row'] = any(
        HANDLER_RE.search(cells(r)[0]) and ENTRY in r for r in rows)
    b['frontier_note'] = any(FRONTIER_MARK in l and STEM in l for l in prov_text.splitlines())
    ent = show(root, rev, ENTRY)
    b['entry_present'] = ent is not None
    src_ids = set()
    if ent:
        for line in ent.decode(errors='replace').splitlines():
            if line.startswith('source:'):
                src_ids |= sid_tokens(line)
    b['entry_source_ids'] = sorted(src_ids)
    reg = show(root, rev, 'corpus/SOURCES.md')
    ok_ids = []
    if reg:
        for line in reg.decode(errors='replace').splitlines():
            if not re.match(r'^ {0,3}\|\s*S\d{3,}\s*\|', line):
                continue
            c = cells(line)
            if len(c) != 11:
                continue
            used = c[10]
            if c[0] in src_ids and c[8] == OPENED and (ENTRY in used or STEM in used):
                ok_ids.append(c[0])
    b['opened_source_rows'] = sorted(ok_ids)
    b['sourced'] = bool(ok_ids)
    readme = show(root, rev, 'corpus/README.md')
    cm = section(readme.decode(errors='replace'), '## Coverage map') if readme else None
    b['coverage_map_row'] = bool(cm) and any(
        STEM in l for l in cm if l.lstrip().startswith('|'))
    b['carriers_spec_ok'] = not spec_probs
    per = res.get('carriers') or {}
    in_tree_total = sum(v.get('in_tree_symlinks') or 0 for v in per.values())
    escaping_total = sum(v.get('escaping_symlinks') or 0 for v in per.values())
    max_in_tree = max([v.get('in_tree_symlinks') or 0 for v in per.values()] or [0])
    b['symlink_coverage'] = (in_tree_total >= 2 and escaping_total >= 2 and max_in_tree >= 2)
    b['symlink_coverage_detail'] = {'in_tree': in_tree_total,
                                    'escaping': escaping_total,
                                    'max_in_tree_per_carrier': max_in_tree}
    b['xz_leg'] = any(v.get('superblock_compression') in XZ_COMPRESSION_IDS
                      for v in per.values())
    b['xz_leg_detail'] = {k: v.get('superblock_compression') for k, v in per.items()}
    res['bindings'] = b
    res['met_target'] = bool(res['carriers_unchanged'] and res['carriers_matched'] == TARGET
                             and all(b[x] for x in BINDINGS))
    return res


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--root')
    ap.add_argument('--rev')
    ap.add_argument('--freeze')
    ap.add_argument('--pkg65')
    ap.add_argument('--json-out')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest(a.pkg65)
    if not (a.root and a.rev and a.freeze and a.pkg65):
        print('usage: --root --rev --freeze --pkg65 required', file=sys.stderr)
        return 2
    try:
        res = measure(a.root, a.rev, a.freeze, a.pkg65)
    except Unevaluable as e:
        res = {'unevaluable': str(e), 'reason': e.reason, 'argv': sys.argv}
        if isinstance(e, FrozenPathChanged):
            res['frozen_path_changed'] = e.paths
        print(json.dumps({'reason': e.reason, 'detail': str(e),
                          'frozen_path_changed': res.get('frozen_path_changed', [])},
                         sort_keys=True))
        if a.json_out:
            json.dump(res, open(a.json_out, 'w'), indent=1, sort_keys=True)
        return 2
    res['argv'] = sys.argv
    print(json.dumps({k: res[k] for k in ('revision', 'freeze', 'carriers_matched',
                                          'carriers_unchanged', 'frozen_path_changed',
                                          'bindings', 'met_target')}, sort_keys=True))
    if a.json_out:
        json.dump(res, open(a.json_out, 'w'), indent=1, sort_keys=True)
    return 0 if res['met_target'] else 1


# ---------------------------------------------------------------- selftest

def find_xpin(here):
    """Locate tools/round-27/xpin-attribute.mjs from a checkout or an artifact dir."""
    for d in [here] + [os.path.dirname(here)] + \
            [os.path.abspath(os.path.join(here, *(['..'] * n))) for n in range(2, 9)]:
        for rel in ('round-27/xpin-attribute.mjs', 'tools/round-27/xpin-attribute.mjs'):
            p = os.path.join(d, rel)
            if os.path.isfile(p):
                return p
    raise SystemExit('xpin-attribute.mjs not found from ' + here)


def sb_blocks(compression, tag=b'', major=4, minor=0):
    """A 96-byte BE SquashFS v4 superblock prefix with the given compression id.

    `tag` fills the tail so distinct fixture carriers do not share a pin."""
    b = bytearray(96)
    b[0:4] = b'sqsh'
    b[12:16] = (4096).to_bytes(4, 'big')
    b[20:22] = compression.to_bytes(2, 'big')
    b[28:30] = major.to_bytes(2, 'big')
    b[30:32] = minor.to_bytes(2, 'big')
    b[64:64 + len(tag)] = tag
    return bytes(b)


def mint_many(work, xpin_path, pkg65, envs):
    paths = []
    for k, env in envs.items():
        p = os.path.join(work, 'mint-%s.json' % k.replace('/', '_'))
        json.dump({'data': env}, open(p, 'w'))
        paths.append((k, p))
    r = subprocess.run(['node', xpin_path, '--pkg65', pkg65, '--pkg67', pkg65]
                       + [p for _, p in paths], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit('xpin mint failed: ' + r.stderr.strip())
    lines = [l for l in r.stdout.splitlines() if l]
    if len(lines) != len(paths):
        raise SystemExit('xpin mint line count mismatch')
    out = {}
    for (k, _), line in zip(paths, lines):
        out[k] = line.split('\t')[2]
    return out


def selftest(pkg65):
    here = os.path.dirname(os.path.abspath(__file__))
    fx = os.path.join(here, 'selftest')
    sroot = scratch_root()
    xpin_path = find_xpin(here)
    xpin = open(xpin_path, 'rb').read()
    dev = json.load(open(os.path.join(fx, 'dev-after.json')))
    oracle = open(os.path.join(fx, 'dev-oracle.tsv')).read()
    symlinks = open(os.path.join(fx, 'dev-symlinks.tsv')).read()
    r38 = open(os.path.join(fx, 'r38-k2-after.json'), 'rb').read()
    work = tempfile.mkdtemp(prefix='c1-selftest-work.', dir=sroot)

    blobs = {k: ('fixture carrier %s\n' % k).encode() for k in IDS}
    blobs.update({'K1': sb_blocks(1, b'K1-gzip'), 'K2': sb_blocks(1, b'K2-gzip'),
                  'K5': sb_blocks(1, b'K5-gzip'), 'K6': sb_blocks(2, b'K6-xz')})
    pins = {k: hashlib.sha256(blobs[k]).hexdigest() for k in IDS}

    def env_for(k, with_links):
        e = json.loads(json.dumps(dev))
        e['subject']['name'] = k.lower() + '.sqsh'
        e['subject']['digest']['sha256'] = pins[k]
        e['subject']['local_path'] = '/fixture/' + k.lower() + '.sqsh'
        e['parameters']['output_directory'] = (
            '/fast/scratch/hyaku/kaidoku-r39/R39C1Counter/selftest/%s-after' % k.lower())
        if not with_links:
            e['normalized_result']['extraction_gaps'] = []
            e['normalized_result']['unpublished_entries'] = []
        return e

    green_envs = {k: env_for(k, k != 'K1') for k in IDS}
    for k, i in mint_many(work, xpin_path, pkg65, green_envs).items():
        green_envs[k]['evidence_id'] = i

    def receipt_path(k):
        return f'{AFTERDIR}/{k}/after.json'

    def receipts(envs):
        return {receipt_path(k): json.dumps(e) for k, e in envs.items()}

    def spec_json(pin_map=None, drop=None):
        pm = pin_map or pins
        cs = []
        for k in IDS:
            if drop and k in drop:
                continue
            cs.append({'id': k,
                       'path': f'{AFTERDIR}/{k}/carrier.sqsh',
                       'sha256': pm[k],
                       'oracle': f'{AFTERDIR}/{k}/oracle.tsv',
                       'symlinks': f'{AFTERDIR}/{k}/symlinks.tsv',
                       'receipt': receipt_path(k)})
        return json.dumps({'claim': 'R39-C1', 'carriers': cs}, indent=1)

    def province(row=True, heading=CORE_HEADING, cell='`squashfs_v4_be`',
                 note=True, cited=ENTRY):
        r = f'| {cell} | x | `{cited}` |\n' if row else ''
        fn = (f'- {FRONTIER_MARK}, 2026-10-26: the Frontier bullet\'s big-endian '
              f'part is superseded by `{STEM}`.\n') if note else ''
        return (f'# P\n\n{heading}\n\n| Surface | a | Entry |\n|---|---|---|\n{r}\n'
                f'## Next\n{fn}\n')

    def entry(sid='S1121'):
        return f'# E\n\nsource: {sid} - x\n'

    def registry(sid='S1121', opened=OPENED, used=ENTRY):
        rows = (f'| {sid} | s | docs | A | s | a | t | mined | {opened} | 180d | {used} |\n')
        if sid != 'S112':
            rows += (f'| S112 | s | docs | A | s | a | t | mined | {OPENED} | 180d | {ENTRY} |\n')
        return ('# S\n\n## Registry\n\n| id | source | kind | tier | scope | anchor | teaches '
                '| status | opened | recheck | used-by |\n'
                '|---|---|---|---|---|---|---|---|---|---|---|\n' + rows)

    def readme(stem=STEM):
        return f'# R\n\n## Coverage map\n\n| a | b |\n|---|---|\n| x | `{stem}` |\n\n## Other\n'

    def frozen_files(blob_map=None, pin_map=None, link_map=None, **over):
        bm = blob_map or blobs
        pm = pin_map or pins
        lm = link_map or {k: (symlinks if k != 'K1' else '') for k in IDS}
        f = {XPIN: xpin,
             CARRIERS: spec_json(pin_map=pm),
             'plans/round-39-claims.md': b'# plan\n',
             'tools/round-39/c1-counter.py': open(os.path.abspath(__file__), 'rb').read(),
             'tools/round-39/c1-run.sh': b'#!/bin/sh\nexit 0\n',
             'PROVINCE.md': province(),
             ENTRY: entry(),
             'corpus/SOURCES.md': registry(),
             'corpus/README.md': readme()}
        for k in IDS:
            f[f'{AFTERDIR}/{k}/carrier.sqsh'] = bm[k]
            f[f'{AFTERDIR}/{k}/oracle.tsv'] = oracle
            f[f'{AFTERDIR}/{k}/symlinks.tsv'] = lm[k]
        f.update(over)
        return f

    def build(blob_over=None, link_over=None, env_over=None, receipt_over=None):
        """A pin-consistent (frozen files, receipts) pair for one variant."""
        bm = dict(blobs)
        bm.update(blob_over or {})
        pm = {k: hashlib.sha256(bm[k]).hexdigest() for k in IDS}
        lm = {k: (symlinks if k != 'K1' else '') for k in IDS}
        lm.update(link_over or {})
        envs = json.loads(json.dumps(green_envs))
        remint = set()
        for k in IDS:
            if bm[k] != blobs[k]:
                envs[k]['subject']['digest']['sha256'] = pm[k]
                remint.add(k)
        for k, fn in (env_over or {}).items():
            fn(envs[k])
            remint.add(k)
        if remint:
            for k, i in mint_many(work, xpin_path, pkg65,
                                  {k: envs[k] for k in sorted(remint)}).items():
                envs[k]['evidence_id'] = i
        r = receipts(envs)
        for p, content in (receipt_over or {}).items():
            if content is None:
                r.pop(p, None)
            else:
                r[p] = content
        return frozen_files(blob_map=bm, pin_map=pm, link_map=lm), r

    def mutant(k, fn, remint=True):
        e = json.loads(json.dumps(green_envs[k]))
        fn(e)
        if remint:
            e['evidence_id'] = mint_many(work, xpin_path, pkg65, {'m': e})['m']
        envs = dict(green_envs)
        envs[k] = e
        return receipts(envs)

    def add(name, steps, freeze_index, want, reason=None):
        cases.append({'name': name, 'steps': steps, 'freeze': freeze_index,
                      'want': want, 'reason': reason})

    cases = []
    def r38_provenance(e):
        e['parameters']['output_directory'] = (
            '/fast/scratch/hyaku/kaidoku-r38/l1-receipts/K1-after')
    strong_frozen, strong_receipts = build(
        env_over={k: r38_provenance for k in ('K1', 'K2', 'K3', 'K4')})
    add('strong copy: round-38-provenance receipts for K1-K4, genuine K5/K6',
        [strong_frozen, strong_receipts], 0, 1)

    def climbing_provenance(e):
        e['parameters']['output_directory'] = (
            '/fast/scratch/hyaku/kaidoku-r39/../kaidoku-r38/l1-receipts/K1-after')
    climb_frozen, climb_receipts = build(
        env_over={k: climbing_provenance for k in ('K1', 'K2', 'K3', 'K4')})
    add('provenance path climbs out of the round-39 segment with ..',
        [climb_frozen, climb_receipts], 0, 1)

    noxz_frozen, noxz_receipts = build(blob_over={'K6': sb_blocks(1, b'K6-gzip')})
    add('no xz carrier (every superblock gzip)', [noxz_frozen, noxz_receipts], 0, 1)

    in_tree_only = ''.join(l + '\n' for l in symlinks.splitlines() if l.endswith('\tin-tree'))
    nolink_frozen, nolink_receipts = build(
        link_over={k: in_tree_only for k in IDS if k != 'K1'})
    add('no escaping symlink row anywhere',
        [nolink_frozen, nolink_receipts], 0, 1)

    one_in_tree = ('var/lib/run-link\t../../a/run.sh\tin-tree\n'
                   'var/lib/escape-link\t../../../../etc/passwd\tescaping\n')

    def drop_notice_gap(e):
        nr = e['normalized_result']
        nr['extraction_gaps'] = [g for g in nr['extraction_gaps']
                                 if not (g.get('relative_path') or '').endswith('notice-link')]
        nr['unpublished_entries'] = [u for u in nr['unpublished_entries']
                                     if not (u.get('relative_path') or '').endswith('notice-link')]
    one_frozen, one_receipts = build(
        link_over={k: one_in_tree for k in IDS if k != 'K1'},
        env_over={k: drop_notice_gap for k in ('K2', 'K3', 'K4', 'K5', 'K6')})
    add('no carrier exercises two in-tree symlinks', [one_frozen, one_receipts], 0, 1)

    good_receipts = receipts(green_envs)
    frozen = frozen_files()

    add('green', [frozen, good_receipts], 0, 0)
    add('do-nothing (freeze files only)', [frozen], 0, 1)
    add('receipt missing (K6)', [frozen, {k: v for k, v in good_receipts.items()
                                          if '/K6/' not in k}], 0, 1)
    add('receipt added at freeze', [{**frozen, **good_receipts}], 0, 1)
    add('receipt added before freeze', [frozen, good_receipts, {}, {}], 2, 1)
    add('round-38 receipts copied, K5/K6 absent',
        [frozen, {receipt_path(k): (r38.decode() if k == 'K1' else json.dumps(
            {**json.loads(r38.decode()),
             'evidence_id': green_envs[k]['evidence_id']})) for k in ('K2', 'K3', 'K4')}],
        0, 1)
    add('materialised in-tree symlink (published file, no gap)',
        [frozen, mutant('K2', lambda e: (
            e['normalized_result']['extraction_gaps'].pop(
                [i for i, g in enumerate(e['normalized_result']['extraction_gaps'])
                 if g['relative_path'].endswith('usr/share/doc/notice-link')][0]),
            e['normalized_result']['files'].append(
                {'relative_path': 'firmware.bin_extract/usr/share/doc/notice-link',
                 'sha256': '0' * 64})))], 0, 1)
    add('extra gap kind (extractor-failure)',
        [frozen, mutant('K3', lambda e: e['normalized_result']['extraction_gaps'].append(
            {'kind': 'extractor-failure', 'input_path': '$input', 'relative_path': None,
             'handler': HANDLER, 'dependencies': []}))], 0, 1)
    add('missing gap for an in-tree symlink',
        [frozen, mutant('K4', lambda e: e['normalized_result']['extraction_gaps'].pop(0))], 0, 1)
    add('escaping symlink published',
        [frozen, mutant('K5', lambda e: e['normalized_result']['files'].append(
            {'relative_path': 'firmware.bin_extract/var/lib/escape-link',
             'sha256': '1' * 64}))], 0, 1)
    add('wrong chunk handler (LE)',
        [frozen, mutant('K6', lambda e: [c.__setitem__('handler', 'squashfs_v4_le')
                                         for c in e['normalized_result']['chunks']])], 0, 1)
    add('failed chunk',
        [frozen, mutant('K1', lambda e: e['normalized_result']['chunks'][0]
                        .__setitem__('extraction_failed', True))], 0, 1)
    add('subject digest mismatch',
        [frozen, mutant('K2', lambda e: e['subject']['digest']
                        .__setitem__('sha256', '2' * 64))], 0, 1)
    add('carrier bytes changed after freeze',
        [frozen, {**good_receipts,
                  f'{AFTERDIR}/K5/carrier.sqsh': b'changed carrier\n'}], 0, 2,
        'frozen_path_changed')
    add('oracle changed after freeze',
        [frozen, {**good_receipts,
                  f'{AFTERDIR}/K3/oracle.tsv': oracle + 'extra.txt\t' + '3' * 64 + '\t1\n'}],
        0, 2, 'frozen_path_changed')
    add('carriers.json changed after freeze',
        [frozen, {**good_receipts, CARRIERS: spec_json(drop=('K6',))}], 0, 2,
        'frozen_path_changed')
    add('counter edited after freeze',
        [frozen, {**good_receipts,
                  'tools/round-39/c1-counter.py': b'#!/usr/bin/env python3\nprint(0)\n'}],
        0, 2, 'frozen_path_changed')
    bad_pins = dict(pins)
    bad_pins['K1'] = '4' * 64
    add('frozen pin wrong (carrier untouched)',
        [{**frozen, CARRIERS: spec_json(pin_map=bad_pins)}, good_receipts], 0, 1)
    add('edited files list breaks evidence id',
        [frozen, mutant('K3', lambda e: e['normalized_result']['files'].append(
            {'relative_path': 'firmware.bin_extract/extra.txt', 'sha256': '5' * 64}),
            remint=False)], 0, 1)
    add('province row outside round-39 section',
        [{**frozen, 'PROVINCE.md': province(heading='## Round-38 additions to Core')},
         good_receipts], 0, 1)
    add('province row without handler in first cell',
        [{**frozen, 'PROVINCE.md': province(cell='squashfs_v4_le')}, good_receipts], 0, 1)
    add('province row absent', [{**frozen, 'PROVINCE.md': province(row=False)},
                                good_receipts], 0, 1)
    add('province row cites another entry',
        [{**frozen, 'PROVINCE.md': province(cited='corpus/knowledge/2026-10-26-r38-other.md')},
         good_receipts], 0, 1)
    add('frontier note absent', [{**frozen, 'PROVINCE.md': province(note=False)},
                                 good_receipts], 0, 1)
    add('S-id substring S1120',
        [{**frozen, ENTRY: entry('S1120')}, good_receipts], 0, 1)
    add('source row opened earlier',
        [{**frozen, 'corpus/SOURCES.md': registry(opened='2026-10-25')}, good_receipts], 0, 1)
    add('used-by lacks entry',
        [{**frozen, 'corpus/SOURCES.md': registry(used='corpus/lessons/round-39.md')},
         good_receipts], 0, 1)
    add('coverage map lacks stem',
        [{**frozen, 'corpus/README.md': readme(stem='2026-10-26-r39-other')},
         good_receipts], 0, 1)

    fails = []
    green = red = 0
    for c in cases:
        d = tempfile.mkdtemp(prefix='c1-selftest.', dir=sroot)
        try:
            subprocess.run(['git', '-C', d, 'init', '-q'], check=True)
            top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'],
                                 capture_output=True, text=True).stdout.strip()
            if os.path.realpath(top) != os.path.realpath(d):
                raise SystemExit('fixture toplevel mismatch')
            ident = ['-c', 'user.name=fx', '-c', 'user.email=fx@fx']
            revs = []
            for step, files in enumerate(c['steps']):
                for p, content in files.items():
                    full = os.path.join(d, p)
                    if content is None:
                        if os.path.exists(full):
                            os.remove(full)
                        continue
                    os.makedirs(os.path.dirname(full) or d, exist_ok=True)
                    data = content if isinstance(content, bytes) else content.encode()
                    open(full, 'wb').write(data)
                subprocess.run(['git', '-C', d, 'add', '-A'], check=True)
                subprocess.run(['git', '-C', d] + ident +
                               ['commit', '-qm', 'step%d' % step, '--allow-empty'],
                               check=True)
                revs.append(subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'],
                                           capture_output=True, text=True).stdout.strip())
            fz = revs[c['freeze']]
            rv = revs[-1]
            try:
                res = measure(d, rv, fz, pkg65)
                got = 0 if res['met_target'] else 1
                why = None
            except FrozenPathChanged as e:
                got, why = 2, e.reason
                res = None
            except Unevaluable as e:
                got, why = 2, e.reason
                res = None
            if os.environ.get('C1_SELFTEST_DETAIL'):
                if res is None:
                    detail = {'exit': got, 'reason': why}
                else:
                    detail = {
                        'exit': got,
                        'carriers_matched': res['carriers_matched'],
                        'failed_clauses': {
                            k: sorted(x for x in CLAUSES if not v.get(x))
                            for k, v in res['carriers'].items()
                            if any(not v.get(x) for x in CLAUSES)
                            or v.get('oracle_hits') != v.get('oracle_files')},
                        'bindings_false': sorted(x for x in BINDINGS if not res['bindings'][x]),
                        'drift': res['frozen_path_changed'],
                    }
                print('DETAIL\t%s\t%s' % (c['name'], json.dumps(detail)), file=sys.stderr)
            if got == c['want'] and (c['reason'] is None or why == c['reason']):
                green += got == 0
                red += got != 0
            else:
                detail = '' if why is None else ' (%s)' % why
                fails.append('%s: want %d got %d%s' % (c['name'], c['want'], got, detail))
        finally:
            shutil.rmtree(d, ignore_errors=True)
    shutil.rmtree(work, ignore_errors=True)
    print(json.dumps({'selftest': 'c1-counter', 'cases': len(cases),
                      'green_ok': green, 'red_ok': red, 'failures': fails}))
    return 0 if not fails else 1


if __name__ == '__main__':
    sys.exit(main())
