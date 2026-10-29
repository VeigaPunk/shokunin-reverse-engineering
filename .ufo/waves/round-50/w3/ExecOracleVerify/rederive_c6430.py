#!/usr/bin/env python3
"""Re-derive the c6430 oracle table the way the frozen counter does.

`tools/round-50/c1-counter.py::rederive_oracle` extracts the carrier bytes
with `/usr/bin/unsquashfs` (flags -no-xattrs -no-progress -f -no-exit-code)
into a fresh scratch tree, walks it and hashes every regular file; symlinks,
directories and device nodes are left out.  This script does exactly that and
compares the result, in both directions, with the frozen table
`tools/round-50/oracle/c6430.oracle.tsv`.

Exit 0 = full agreement; 1 = disagreement; 2 = could not evaluate.
"""
import hashlib
import json
import os
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
SCRATCH = os.path.dirname(os.path.abspath(__file__))
TREE = os.path.join(SCRATCH, 'tree')
ORACLE = os.path.join(LANE, 'tools/round-50/oracle/c6430.oracle.tsv')
OUT = os.path.join(SCRATCH, 'rederive.json')

if not os.path.isdir(TREE):
    print('no extracted tree at %s' % TREE)
    sys.exit(2)

oracle = {}
with open(ORACLE, 'r', encoding='utf-8') as fh:
    for line in fh:
        if not line.strip():
            continue
        rel, sha, size = line.rstrip('\n').split('\t')
        oracle[rel] = (sha.strip().lower(), int(size.strip()))

rows = []
for dirpath, _dirs, names in os.walk(TREE):
    for name in names:
        full = os.path.join(dirpath, name)
        if os.path.islink(full) or not os.path.isfile(full):
            continue
        h = hashlib.sha256()
        size = 0
        with open(full, 'rb') as fh:
            for blk in iter(lambda: fh.read(1 << 20), b''):
                h.update(blk)
                size += len(blk)
        rel = os.path.relpath(full, TREE).replace(os.sep, '/')
        rows.append((rel, h.hexdigest(), size))
rows.sort()

derived = {r[0]: (r[1], r[2]) for r in rows}
want, got = set(oracle), set(derived)
frozen_only = sorted(want - got)
derived_only = sorted(got - want)
differing = sorted(p for p in (want & got) if oracle[p] != derived[p])

out = {
    'source': 'unsquashfs -no-xattrs -no-progress -f -no-exit-code -d tree carrier.bin + sha256 walk',
    'oracle_rows': len(oracle),
    'derived_rows': len(derived),
    'frozen_only': frozen_only[:10],
    'n_frozen_only': len(frozen_only),
    'derived_only': derived_only[:10],
    'n_derived_only': len(derived_only),
    'differing': differing[:10],
    'n_differing': len(differing),
    'equal': not (frozen_only or derived_only or differing),
}
with open(OUT, 'w', encoding='utf-8') as fh:
    json.dump(out, fh, indent=1, sort_keys=True)
print(json.dumps({k: v for k, v in out.items()
                  if k not in ('frozen_only', 'derived_only', 'differing')},
                 sort_keys=True))
sys.exit(0 if out['equal'] else 1)
