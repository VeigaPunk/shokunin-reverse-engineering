#!/usr/bin/env python3
"""stub-counter.py -- the byte-clause half of a P40-C1 counter, for validating the
control suite (R40C1Controls). NOT the round-40 counter.

It exists so that every control in suite.json can be *scored today* on a dev mirror,
proving that the clause each control is supposed to trip really fires on the bytes the
overlay writes. It reads only committed bytes of a git repo plus the frozen tools.

It deliberately does NOT implement the rerun binding (it cannot: that needs REA on the
frozen carriers). `rerun_projection_ok` is reported as null, and the rerun column is
measured separately by projection.py (see projection-compare.txt).

Bindings implemented (names as in suite.json):
  carriers_spec_ok carrier_present carrier_pin_ok carrier_marker_ok
  carrier_blocklen_le_ok distinct_carriers_ok oracle_shape_ok oracle_ok
  publication_ok failed_chunk_ok gaps_ok subject_ok evidence_id_ok
  receipt_descends_freeze_ok frozen_paths_clean doc_core_row doc_frontier_note
  doc_frontier_note_consistent doc_entry doc_sources_opened_this_round
  doc_coverage_map doc_control_table_frozen

Usage:
  python3 -I -B stub-counter.py --root R --rev V --freeze F --json-out J
Exit 0 met_target, 1 not met, 2 unevaluable (frozen_path_changed).
"""
import argparse
import hashlib
import json
import os
import struct
import subprocess
import sys
import tempfile

SPEC = '.ufo/waves/round-40/c1/carriers.json'
CONTROLS = '.ufo/waves/round-40/c1/controls.json'
ENTRY_TITLE = 'AVM layout'
PROVINCE = 'PROVINCE.md'
SOURCES = 'corpus/SOURCES.md'
README = 'corpus/README.md'
READER = 'tools/round-40/sqfs-list.py'
CLAIMS = 'plans/round-40-claims.md'
CORE_HEADING = '## Round-40 additions to Core'
NOTE_MARK = 'Round-40 frontier note'
META_MAX = 8192
MASK = 0x8000
ALLOWED_GAPS = ('unpublished-entry', 'extractor-failure')
BINDINGS = (
    'carriers_spec_ok', 'carrier_present', 'carrier_pin_ok', 'carrier_marker_ok',
    'carrier_blocklen_le_ok', 'distinct_carriers_ok', 'oracle_shape_ok', 'oracle_ok',
    'publication_ok', 'failed_chunk_ok', 'gaps_ok', 'subject_ok', 'evidence_id_ok',
    'receipt_descends_freeze_ok', 'frozen_paths_clean', 'doc_core_row',
    'doc_frontier_note', 'doc_frontier_note_consistent', 'doc_entry',
    'doc_sources_opened_this_round', 'doc_coverage_map', 'doc_control_table_frozen',
    'run_provenance_ok',
)


class Unevaluable(Exception):
    def __init__(self, reason):
        super().__init__(reason)
        self.reason = reason


def git(root, *args):
    p = subprocess.run(['git', '-C', root, *args], capture_output=True)
    return p.returncode, p.stdout


def show(root, rev, path):
    rc, out = git(root, 'show', '%s:%s' % (rev, path))
    return out if rc == 0 else None


def first_added(root, rev, path):
    rc, out = git(root, 'log', '--diff-filter=A', '--format=%H', rev, '--', path)
    return out.decode().split()[-1] if rc == 0 and out.split() else None


def is_ancestor(root, a, b):
    return git(root, 'merge-base', '--is-ancestor', a, b)[0] == 0


def decode_carrier(raw):
    """(marker, le_ok) from the image bytes: the two carrier-side tests."""
    if len(raw) < 96 or raw[:4] != b'sqsh':
        return None, None
    mkfs = struct.unpack_from('>I', raw, 8)[0]
    used = struct.unpack_from('>Q', raw, 40)[0]
    inode_tbl = struct.unpack_from('>Q', raw, 64)[0]
    marker = mkfs == used
    if not 96 <= inode_tbl < used or inode_tbl + 2 > len(raw):
        return marker, False
    le = struct.unpack_from('<H', raw, inode_tbl)[0] & ~MASK
    be = struct.unpack_from('>H', raw, inode_tbl)[0] & ~MASK

    def plausible(n):
        return 0 < n <= META_MAX and n <= used

    return marker, bool(plausible(le) and not plausible(be))


def reader_rows(tmp, reader_src, carrier_bytes, avm=True):
    os.makedirs(tmp, exist_ok=True)
    tool = os.path.join(tmp, 'sqfs-list.py')
    img = os.path.join(tmp, 'carrier.bin')
    files = os.path.join(tmp, 'files.tsv')
    links = os.path.join(tmp, 'links.tsv')
    with open(tool, 'wb') as f:
        f.write(reader_src)
    with open(img, 'wb') as f:
        f.write(carrier_bytes)
    cmd = [sys.executable, '-I', '-B', tool] + (['--avm'] if avm else []) + [
        img, '--files', files, '--symlinks', links]
    p = subprocess.run(cmd, capture_output=True)
    if p.returncode != 0:
        return None
    rows = []
    with open(files, 'rb') as f:
        for line in f:
            line = line.rstrip(b'\r\n')
            if line:
                rows.append([c.decode('utf-8', 'surrogateescape') for c in line.split(b'\t')])
    return rows


def tsv(raw):
    rows = []
    for line in (raw or b'').splitlines():
        if line.strip():
            rows.append([c.decode('utf-8', 'surrogateescape') for c in line.split(b'\t')])
    return rows


def evidence_id_selfconsistent(env):
    body = json.dumps({k: v for k, v in env.items() if k != 'evidence_id'},
                      sort_keys=True, separators=(',', ':'))
    return env.get('evidence_id') == 'ev_' + hashlib.sha256(body.encode()).hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--freeze', required=True)
    ap.add_argument('--json-out', required=True)
    a = ap.parse_args(argv)
    root, rev, freeze = a.root, a.rev, a.freeze

    spec_raw = show(root, rev, SPEC)
    spec = json.loads(spec_raw) if spec_raw else None
    b = {k: False for k in BINDINGS}
    detail = {}
    res = {'revision': rev, 'freeze': freeze, 'predicate': 'P40-C1',
           'counter': 'stub-counter.py (byte clauses only)'}

    if spec is None:
        res.update({'bindings': b, 'met_target': False, 'reason': 'no_carriers_spec'})
        json.dump(res, open(a.json_out, 'w'), indent=1, sort_keys=True)
        return 1
    cs = spec.get('carriers') or []
    b['carriers_spec_ok'] = len(cs) > 0
    b['distinct_carriers_ok'] = len({c.get('sha256') for c in cs}) == len(cs) and len(cs) > 0

    reader_src = show(root, rev, READER)
    tmp = tempfile.mkdtemp(prefix='stubctl-')
    matched = 0
    per = {}
    for c in cs:
        raw = show(root, rev, c['path'])
        ok = raw is not None
        if not ok:
            per[c['id']] = {'carrier_present': False}
            continue
        pin = hashlib.sha256(raw).hexdigest() == c.get('sha256')
        marker, le_ok = decode_carrier(raw)
        oracle = tsv(show(root, rev, c['oracle']))
        red = reader_rows(tmp, reader_src, raw) if reader_src else None
        red_ok = red is not None and sorted((r[0], r[1]) for r in red) == \
            sorted((r[0], r[1]) for r in oracle)
        env = show(root, rev, c['receipt'])
        env = json.loads(env) if env else None
        row = {'pin': pin, 'marker': marker, 'le': le_ok, 'oracle_rows': len(oracle),
               'carrier_present': True, 'oracle_shape': bool(oracle) and
               len(oracle) == c.get('oracle_files'), 'oracle_rederived': red_ok}
        if env:
            nr = env.get('normalized_result') or {}
            rootp = (c.get('extract_root') or '') + '/'
            pub = set()
            for f in nr.get('files') or []:
                rp = f.get('relative_path') or ''
                pub.add(rp[len(rootp):] if rootp and rp.startswith(rootp) else None)
            want = {r[0] for r in oracle}
            row['publication'] = pub == want and None not in pub
            failed = [ch.get('extraction_failed') for ch in nr.get('chunks') or []]
            row['failed_chunk'] = bool(failed) and not any(failed)
            kinds = [g.get('kind') or '' for g in nr.get('extraction_gaps') or []]
            links = tsv(show(root, rev, c['symlinks'])) if c.get('symlinks') else []
            in_tree = sum(1 for l in links if len(l) > 2 and l[2] == 'in-tree')
            row['gaps'] = (set(kinds) <= set(ALLOWED_GAPS)
                           and kinds.count('unpublished-entry') == in_tree)
            row['subject'] = (env.get('subject') or {}).get('digest', {}).get(
                'sha256') == c.get('sha256')
            row['evidence_id'] = evidence_id_selfconsistent(env)
            # a receipt this round recorded must have been written under this round's
            # scratch root, not carried over from round 39
            od = [(env.get('parameters') or {}).get('output_directory') or '',
                  (nr.get('output_directory') or '')]
            row['provenance'] = all(isinstance(p, str) and p.startswith('/')
                                    and '/kaidoku-r40/' in p for p in od)
            fa = first_added(root, rev, c['receipt'])
            row['descends'] = fa is not None and fa != freeze and is_ancestor(
                root, freeze, fa)
        per[c['id']] = row
        if row.get('publication') and pin and marker and le_ok:
            matched += 1

    # every carrier clause is a conjunction over carriers, not a disjunction
    def agg(key, default=False):
        vals = [r.get(key) for r in per.values()]
        return bool(vals) and all(v is not default for v in vals) and all(
            v for v in vals)

    b['carrier_present'] = agg('carrier_present')
    b['carrier_pin_ok'] = agg('pin')
    b['carrier_marker_ok'] = agg('marker')
    b['carrier_blocklen_le_ok'] = agg('le')
    b['oracle_shape_ok'] = agg('oracle_shape')
    b['oracle_ok'] = agg('oracle_rederived')
    b['publication_ok'] = agg('publication')
    b['failed_chunk_ok'] = agg('failed_chunk')
    b['gaps_ok'] = agg('gaps')
    b['subject_ok'] = agg('subject')
    b['evidence_id_ok'] = agg('evidence_id')
    b['run_provenance_ok'] = agg('provenance')
    b['receipt_descends_freeze_ok'] = agg('descends')

    frozen = [p for p in [SPEC, CLAIMS, READER, CONTROLS] + [
        q for c in cs for q in (c['path'], c['oracle'], c.get('symlinks'))] if p]
    rc, out = git(root, 'log', '--format=%H', '%s..%s' % (freeze, rev), '--', *frozen)
    b['frozen_paths_clean'] = (rc == 0 and not out.strip())
    b['frozen_path_drift'] = out.decode().split() if out.strip() else []

    prov = (show(root, rev, PROVINCE) or b'').decode('utf-8', 'replace')
    entry_path = None
    for tok in prov.split():
        tok = tok.lstrip('`|')
        if 'corpus/knowledge/' in tok and tok.rstrip('`.,)').endswith('.md'):
            entry_path = tok.rstrip('`.,)')
    entry = (show(root, rev, entry_path) if entry_path else None) or b''
    entry = entry.decode('utf-8', 'replace')
    stem = os.path.basename(entry_path)[:-3] if entry_path else ''
    b['doc_core_row'] = CORE_HEADING in prov
    b['doc_entry'] = bool(entry_path) and ENTRY_TITLE.split()[0] in entry
    b['doc_frontier_note'] = NOTE_MARK in prov
    note = '\n'.join(l for l in prov.splitlines() if NOTE_MARK in l)
    b['doc_frontier_note_consistent'] = bool(note) and (
        'stays Frontier' not in note and 'remain' not in note
        and CORE_HEADING.replace('## ', '') in note and stem in note)
    src = (show(root, rev, SOURCES) or b'').decode('utf-8', 'replace')
    opened = []
    if stem:
        # "opened this round" = the row ID is NEW in FREEZE..REV (not present at the
        # freeze) and its used-by cites this entry. A diff of the file alone is not
        # enough: adding a used-by to a round-39 row also shows up as a '+' line.
        def ids(text):
            out = set()
            for line in text.splitlines():
                cells = [x.strip() for x in line.strip().strip('|').split('|')]
                if cells and cells[0].startswith('S'):
                    out.add(cells[0])
            return out
        at_freeze = ids((show(root, freeze, SOURCES) or b'').decode('utf-8', 'replace'))
        rc, diff = git(root, 'diff', '%s..%s' % (freeze, rev), '--', SOURCES)
        added = [l[1:] for l in diff.decode('utf-8', 'replace').splitlines()
                 if l.startswith('+') and not l.startswith('+++')]
        for line in added:
            cells = [x.strip() for x in line.strip().strip('|').split('|')]
            if cells and cells[0].startswith('S') and cells[0] not in at_freeze \
                    and stem in line:
                opened.append(cells[0])
    b['doc_sources_opened_this_round'] = bool(opened)
    readme = (show(root, rev, README) or b'').decode('utf-8', 'replace')
    b['doc_coverage_map'] = bool(stem) and stem in readme
    ctl = show(root, rev, CONTROLS)
    ctl_first = first_added(root, rev, CONTROLS)
    b['doc_control_table_frozen'] = bool(ctl) and ctl_first is not None and (
        ctl_first == freeze or is_ancestor(root, ctl_first, freeze))

    b['rerun_projection_ok'] = None
    b.pop('frozen_path_drift', None)
    res.update({'bindings': b, 'carriers_matched': matched, 'target': len(cs) or 4,
                'carrier_detail': per,
                'frozen_path_drift': [p for p in frozen if p] and
                out.decode().split() or []})
    res['met_target'] = bool(matched == (len(cs) or 4) and matched > 0
                             and all(v for k, v in b.items() if v is not None))
    json.dump(res, open(a.json_out, 'w'), indent=1, sort_keys=True)
    print(json.dumps({k: res[k] for k in ('bindings', 'carriers_matched', 'met_target')},
                     sort_keys=True))
    if res['frozen_path_drift']:
        return 2
    return 0 if res['met_target'] else 1


if __name__ == '__main__':
    sys.exit(main())
