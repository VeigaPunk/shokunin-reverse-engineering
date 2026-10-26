#!/usr/bin/env python3
"""Leaf-level diff of two REA receipts: what changes between two runs of the SAME bytes.

Run: python3 diff-leaves.py <a.json> <b.json>
"""
import collections, json, re, sys

def load(p):
    d = json.load(open(p, encoding='utf-8')); return d.get('data', d)

def leaves(x, pre=''):
    if isinstance(x, dict):
        for k, v in x.items(): yield from leaves(v, f'{pre}.{k}' if pre else k)
    elif isinstance(x, list):
        for i, v in enumerate(x): yield from leaves(v, f'{pre}[{i}]')
    else: yield pre, x

a, b = load(sys.argv[1]), load(sys.argv[2])
la, lb = dict(leaves(a)), dict(leaves(b))
paths = sorted(set(la) | set(lb))
diff = [p for p in paths if la.get(p) != lb.get(p)]
print('total leaves: %d   differing: %d' % (len(paths), len(diff)))
print('by top-level field: %s' % dict(collections.Counter(p.split('.')[0] for p in diff)))
print('\nby shape (index folded):')
for k, v in collections.Counter(re.sub(r'\[\d+\]', '[]', p) for p in diff).most_common():
    print('  %3d  %s' % (v, k))
print('\nevidence ids: a=%s b=%s' % (a.get('evidence_id'), b.get('evidence_id')))
