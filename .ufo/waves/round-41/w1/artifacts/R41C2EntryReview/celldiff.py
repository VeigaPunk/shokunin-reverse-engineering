#!/usr/bin/env python3
"""Verify R40-CL5 M1 sub-claims at 49096c7e against working bytes (== base, tree clean)."""
import hashlib, re, sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'

def cells(line):
    parts = [c.strip() for c in line.strip().strip('|').split('|')]
    return parts

def rows_from(path, first, last):
    with open(path, encoding='utf-8') as fh:
        lines = fh.read().splitlines()
    out = {}
    for n in range(first, last + 1):
        line = lines[n - 1]
        if line.lstrip().startswith('| ') and not line.lstrip().startswith('| ---') \
           and not line.lstrip().startswith('| label'):
            cs = cells(line)
            out[cs[0]] = (n, cs)
    return out

def sha(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()

skill = LANE + '/SKILL.md'
py40 = LANE + '/tools/round-40/sqfs-triage-v2.py'
py39 = LANE + '/tools/round-39/sqfs-triage.py'

print('sha256 SKILL.md                ', sha(skill))
print('sha256 tools/round-40/sqfs-triage-v2.py', sha(py40))
print('sha256 tools/round-39/sqfs-triage.py    ', sha(py39))

# ---- v2: SKILL rows 365-375 vs TABLE_BLOCK rows 176-186 -------------------------
sk = rows_from(skill, 363, 375)
tb = rows_from(py40, 174, 186)
print('\n== v2 SKILL table vs v2 TABLE_BLOCK ==')
print('skill rows:', sorted(sk), '\ntable_block rows:', sorted(tb))
assert set(sk) == set(tb), 'row label sets differ'
header_sk = cells(open(skill).read().splitlines()[362])
header_tb = cells(open(py40).read().splitlines()[173])
print('header equal:', header_sk == header_tb, len(header_sk), 'cells')
divs = []
for label in sorted(sk):
    a, b = sk[label][1], tb[label][1]
    if len(a) != len(b):
        divs.append((label, 'CELLCOUNT', len(a), len(b)))
        continue
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            divs.append((label, header_sk[i], x, y))
if not divs:
    print('no cell divergence')
for label, col, x, y in divs:
    print(f'DIVERGENT row={label} col={col}')
    print(f'  SKILL  : {x}')
    print(f'  TABLE  : {y}')

# ---- v1: SKILL v1 rows 339-346 vs round-39 TABLE_BLOCK rows 134-141 -------------
sk1 = rows_from(skill, 337, 346)
tb1 = rows_from(py39, 132, 141)
print('\n== v1 SKILL table vs round-39 TABLE_BLOCK ==')
print('skill rows:', sorted(sk1), '\ntable_block rows:', sorted(tb1))
h1sk = cells(open(skill).read().splitlines()[336])
h1tb = cells(open(py39).read().splitlines()[131])
print('header equal:', h1sk == h1tb, len(h1sk), 'cells')
for label in sorted(set(sk1) & set(tb1)):
    a, b = sk1[label][1], tb1[label][1]
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y and i < 7:  # decision cells only (handler..published files)
            print(f'DIVERGENT(decision) row={label} col={h1sk[i]}')
            print(f'  SKILL  : {x}')
            print(f'  TABLE  : {y}')

# ---- escaping-row G cell and selftest TABLE_BLOCK usage -------------------------
esc_sk = cells(open(skill).read().splitlines()[371])
print('\nescaping row (SKILL:372) decision cells:', esc_sk[:9])
with open(py40, encoding='utf-8') as fh:
    t40 = fh.read()
print('_skel(TABLE_BLOCK) uses in v2 selftest:', t40.count('_skel(TABLE_BLOCK)'))
with open(py39, encoding='utf-8') as fh:
    t39 = fh.read()
print('_skel(TABLE_BLOCK) uses in v1 selftest:', t39.count('_skel(TABLE_BLOCK)'))
print('contains-operator present in v2 py:', bool(re.search(r"kind == 'contains'|'contains'", t40)))
