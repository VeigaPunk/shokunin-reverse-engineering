#!/usr/bin/env python3
"""ordercheck.py -- probe whether a proposed v2 row order resolves the measured
feature combinations, using the v2 grammar sketch from the L1 contract.

This is a RECON prototype, not the frozen interpreter: it hard-codes one row list
and prints (label, action) per envelope so the ordering argument in the report is
executable.  Feature extraction mirrors tools/round-39/sqfs-triage.py (and
feat.py): OP=data.operation, PV=data.provider.id, H/G/D/BE/SR/P as in v1.

Usage: python3 -I -B ordercheck.py [--table A|B] ENVELOPE...
  --table A  rows as proposed in R40C2ReconMixed.md (mixed before escaping,
             exact gap sets, domain pinned on every row)
  --table B  same rows but escaping row keeps v1's ``*`` gap/dependency cells
             with mixed still first (must still resolve mixed)
  --table C  escaping row keeps v1's ``*`` cells AND sits before the mixed row
             (the R39-CL2 shape); mixed then mislabels as escaping

Exit 0 always (it is a reporter); rows with no match print ``unclassified``.
"""
import argparse
import fnmatch
import json
import shlex
import sys

ACTIONS = ('install-extractor rerun-fresh expect-absent expect-absent-metadata '
           'repin-marker inspect-chunk ignore-benign')
SYMLINK_TYPENAME = 'MaliciousSymlinkRemoved'

# Each row: (label, operation, provider, handler, gap_kinds, dependencies, be,
#            symlink_removed, published, action)
ROWS_A = [
    ('no-squashfs-chunk', 'extract_firmware', 'unblob', None, '*', '*',
     'n/a', '*', '*', 'inspect-chunk'),
    ('dep-missing-be', 'extract_firmware', 'unblob', 'squashfs_v4_be',
     ('missing-extractor-dependency',), ('sasquatch-v4be',), 'n/a', 'no', '*',
     'install-extractor'),
    ('dep-missing-le', 'extract_firmware', 'unblob', 'squashfs_v4_le',
     ('missing-extractor-dependency',), ('sasquatch',), 'n/a', 'no', '*',
     'install-extractor'),
    ('avm-marker-be-dropped', 'extract_firmware', 'unblob', 'squashfs_v4_be',
     ('extractor-failure',), (), 'no', 'no', '0', 'repin-marker'),
    ('body-extractor-failure', 'extract_firmware', 'unblob', 'squashfs_v4_be',
     ('extractor-failure',), (), 'yes', 'no', '0', 'rerun-fresh'),
    ('partial-body-failure', 'extract_firmware', 'unblob', 'squashfs_v4_*',
     ('extractor-failure',), (), 'yes', 'no', '>0', 'rerun-fresh'),
    ('mixed-symlinks', 'extract_firmware', 'unblob', 'squashfs_v4_*',
     ('unpublished-entry',), (), 'n/a', 'yes', '>0', 'expect-absent-metadata'),
    ('escaping-symlink-removed', 'extract_firmware', 'unblob', 'squashfs_v4_*',
     (), (), 'n/a', 'yes', '>0', 'expect-absent'),
    ('in-tree-symlink-metadata', 'extract_firmware', 'unblob', 'squashfs_v4_*',
     ('unpublished-entry',), (), 'n/a', 'no', '>0', 'ignore-benign'),
    ('clean', 'extract_firmware', 'unblob', 'squashfs_v4_*', (), (),
     'n/a', 'no', '>0', 'ignore-benign'),
    ('clean-empty', 'extract_firmware', 'unblob', 'squashfs_v4_*', (), (),
     'n/a', 'no', '0', 'ignore-benign'),
]

ROWS_B = [row if row[0] != 'escaping-symlink-removed'
          else ('escaping-symlink-removed', 'extract_firmware', 'unblob',
                'squashfs_v4_*', '*', '*', 'n/a', 'yes', '>0', 'expect-absent')
          for row in ROWS_A]


def _esc_v1():
    return ('escaping-symlink-removed', 'extract_firmware', 'unblob',
            'squashfs_v4_*', '*', '*', 'n/a', 'yes', '>0', 'expect-absent')


_ESC = _esc_v1()
ROWS_C = ([row for row in ROWS_A
           if row[0] in ('no-squashfs-chunk', 'dep-missing-be', 'dep-missing-le',
                         'avm-marker-be-dropped', 'body-extractor-failure',
                         'partial-body-failure')]
          + [_ESC]
          + [row for row in ROWS_A
             if row[0] not in ('no-squashfs-chunk', 'dep-missing-be',
                               'dep-missing-le', 'avm-marker-be-dropped',
                               'body-extractor-failure', 'partial-body-failure',
                               'escaping-symlink-removed')])


def _as_list(v):
    return v if isinstance(v, list) else []


def _iter_dicts(obj):
    stack = [obj]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            yield cur
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)


def _tokens(cmd):
    if isinstance(cmd, str):
        try:
            return shlex.split(cmd)
        except ValueError:
            return cmd.split()
    if isinstance(cmd, (list, tuple)):
        return [t for t in cmd if isinstance(t, str)]
    return None


def _features(data):
    nr = data['normalized_result']
    handlers, gaps, deps = set(), set(), set()
    for c in _as_list(nr.get('chunks')):
        h = c.get('handler') if isinstance(c, dict) else None
        if isinstance(h, str) and h.startswith('squashfs'):
            handlers.add(h)
    for g in _as_list(nr.get('extraction_gaps')):
        if not isinstance(g, dict):
            continue
        if isinstance(g.get('kind'), str):
            gaps.add(g['kind'])
        for d in _as_list(g.get('dependencies')):
            if isinstance(d, str):
                deps.add(d)
    cmds = []
    for source in (nr.get('diagnostics'), data.get('diagnostics')):
        for diag in _as_list(source):
            rep = diag.get('report') if isinstance(diag, dict) else None
            if isinstance(rep, dict) and 'command' in rep:
                cmds.append(rep['command'])
    for d in _iter_dicts(data.get('raw_result')):
        if 'command' in d:
            cmds.append(d['command'])
    sas = [c for c in cmds if any(
        t.rsplit('/', 1)[-1].startswith('sasquatch') for t in (_tokens(c) or []))]
    if not sas:
        be = 'n/a'
    elif any('-be' in (_tokens(c) or []) for c in sas):
        be = 'yes'
    else:
        be = 'no'
    sr = 'no'
    for diag in _as_list(nr.get('diagnostics')):
        rep = diag.get('report') if isinstance(diag, dict) else None
        if isinstance(rep, dict) and rep.get('__typename__') == SYMLINK_TYPENAME:
            sr = 'yes'
    if sr == 'no':
        sr = 'yes' if any(d.get('__typename__') == SYMLINK_TYPENAME
                          for d in _iter_dicts(data.get('raw_result'))) else 'no'
    prov = data.get('provider') if isinstance(data.get('provider'), dict) else {}
    return {'OP': data.get('operation'), 'PV': prov.get('id'),
            'H': sorted(handlers), 'G': sorted(gaps), 'D': sorted(deps),
            'BE': be, 'SR': sr, 'P': len(_as_list(nr.get('files')))}


def _set_cell(cell, values):
    if cell == '*':
        return True
    if cell == ():
        return not values
    return frozenset(values) == frozenset(cell)


def _match(row, f):
    _, op, pv, handler, gaps, deps, be, sr, published, _action = row
    if op != '*' and f['OP'] != op:
        return False
    if pv != '*' and f['PV'] != pv:
        return False
    if handler is None:
        if f['H']:
            return False
    elif not any(fnmatch.fnmatchcase(h, handler) for h in f['H']):
        return False
    if not _set_cell(gaps, f['G']):
        return False
    if not _set_cell(deps, f['D']):
        return False
    if be != '*' and be != f['BE']:
        return False
    if sr != '*' and sr != f['SR']:
        return False
    if published == '0' and f['P'] != 0:
        return False
    if published == '>0' and f['P'] <= 0:
        return False
    return True


def classify(rows, f):
    for i, row in enumerate(rows, 1):
        if _match(row, f):
            return row[0], row[9], i
    return 'unclassified', 'none', None


def _data(obj):
    if isinstance(obj.get('normalized_result'), dict):
        return obj
    inner = obj.get('data')
    if isinstance(inner, dict) and isinstance(inner.get('normalized_result'), dict):
        return inner
    raise SystemExit('no normalized_result')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--table', choices=['A', 'B', 'C'], default='A')
    ap.add_argument('paths', nargs='+')
    ns = ap.parse_args()
    rows = {'A': ROWS_A, 'B': ROWS_B, 'C': ROWS_C}[ns.table]
    print('table %s actions: %s' % (ns.table, ACTIONS))
    for p in ns.paths:
        with open(p, 'r', encoding='utf-8') as fh:
            f = _features(_data(json.load(fh)))
        label, action, idx = classify(rows, f)
        print('%-28s %-26s %-18s rule=%-4s H=%s G=%s BE=%s SR=%s P=%s OP=%s PV=%s'
              % (p.rsplit('/', 2)[-2], label, action, idx,
                 ','.join(f['H']) or '-', ','.join(f['G']) or '-', f['BE'],
                 f['SR'], f['P'], f['OP'], f['PV']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
