#!/usr/bin/env python3
"""Feature table for the four committed round-40 C1 after-receipts (real bytes).

  python3 -I -B real-carrier-features.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin
"""
import argparse, hashlib, json, os

ap = argparse.ArgumentParser()
ap.add_argument('--root', default=os.environ.get('KAIDOKU_ROOT', '.'))
a = ap.parse_args()
base = os.path.join(a.root, 'corpus/evidence/round-40/c1')
cols = ['carrier', 'receipt_sha256', 'OP', 'PR', 'handlers', 'gap_kinds', 'gap_count',
        'deps', 'be', 'SR', 'P', 'unpublished', 'depth_limited', 'max_depth', 'coverage']
print('\t'.join(cols))
for name in ('V1', 'V2', 'L1', 'L2'):
    p = os.path.join(base, name, 'after.json')
    raw = open(p, 'rb').read()
    d = json.loads(raw)
    nr = d.get('normalized_result') or {}
    gaps = nr.get('extraction_gaps') or []
    be = 'n/a'
    for diag in (nr.get('diagnostics') or []):
        c = (diag.get('report') or {}).get('command')
        if isinstance(c, str) and c:
            be = 'yes' if ' -be ' in ' ' + c + ' ' else 'no'
    print('\t'.join([name, hashlib.sha256(raw).hexdigest(), str(d.get('operation')),
        str((d.get('provider') or {}).get('id')),
        ','.join(sorted({c.get('handler') for c in (nr.get('chunks') or []) if c.get('handler')})) or '-',
        ','.join(sorted({g.get('kind') for g in gaps})) or '-', str(len(gaps)),
        ','.join(sorted({x for g in gaps for x in (g.get('dependencies') or [])})) or '-',
        be, str(any((x.get('report') or {}).get('kind') == 'MaliciousSymlinkRemoved'
                    for x in (nr.get('diagnostics') or []))),
        str(len(nr.get('files') or [])), str(len(nr.get('unpublished_entries') or [])),
        ','.join(nr.get('depth_limited_paths') or []) or '-',
        str((d.get('parameters') or {}).get('max_depth')), str(nr.get('coverage'))]))
