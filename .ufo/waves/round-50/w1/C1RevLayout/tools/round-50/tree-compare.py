#!/usr/bin/env python3
"""tree-compare.py -- per-file comparison of an extracted tree with a sqfs-list TSV oracle.

Usage: tree-compare.py TREE ORACLE_TSV [--json-out FILE]
ORACLE_TSV rows: relpath TAB sha256 TAB size (the round-41 sqfs-list.py --files grammar).
Counts oracle rows missing from TREE, rows whose sha256 or size differ, and regular
files in TREE that no oracle row names. Symlinks are not followed and not counted as
regular files. Exit 0 when no row is missing or different; 1 otherwise; 2 on a bad input.
"""
import hashlib
import json
import os
import sys


def tree_regular(root):
    m = {}
    for dp, _dn, fn in os.walk(root):
        for f in fn:
            p = os.path.join(dp, f)
            if os.path.islink(p) or not os.path.isfile(p):
                continue
            rel = os.path.relpath(p, root)
            with open(p, 'rb') as fh:
                h = hashlib.sha256(fh.read()).hexdigest()
            m[rel] = (h, os.path.getsize(p))
    return m


def oracle(path):
    m = {}
    with open(path) as fh:
        for line in fh:
            rel, sha, size = line.rstrip('\n').split('\t')
            m[rel] = (sha, int(size))
    return m


def main(argv):
    if len(argv) < 3:
        print(__doc__, file=sys.stderr)
        return 2
    tree, tsv = argv[1], argv[2]
    out = argv[argv.index('--json-out') + 1] if '--json-out' in argv else None
    t, o = tree_regular(tree), oracle(tsv)
    missing = sorted(k for k in o if k not in t)
    diff = sorted(k for k in o if k in t and t[k] != o[k])
    extra = sorted(k for k in t if k not in o)
    rec = {'tree': tree, 'oracle': tsv, 'oracle_rows': len(o), 'tree_regular': len(t),
           'missing_in_tree': len(missing), 'sha_or_size_mismatch': len(diff),
           'extra_regular_in_tree': len(extra), 'sample_missing': missing[:3],
           'sample_extra': extra[:3]}
    print(json.dumps(rec, indent=1))
    if out:
        with open(out, 'w') as fh:
            json.dump(rec, fh, indent=1)
    return 0 if not missing and not diff else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
