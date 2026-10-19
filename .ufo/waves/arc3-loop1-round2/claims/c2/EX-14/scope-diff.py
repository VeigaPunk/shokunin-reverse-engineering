#!/usr/bin/env python3
"""CR-5 SCOPE-table differ: before vs after census instrument.

Usage: python3 scope-diff.py <before.py> <after.py>
Prints added / removed / changed rows and flags creep signatures:
  - open-ended bound (end >= 9000 or end is the last line of file)
  - CURRENT -> DATED class flip
  - end widened / start moved earlier
Exit 0 if tables identical, 1 if changed (change is not itself a defect).
"""
import re, sys


def parse(path):
    txt = open(path, encoding="utf-8").read()
    m = re.search(r"SCOPE\s*=\s*\[(.*?)\n\]", txt, re.S)
    rows = []
    for mm in re.finditer(r'\(\s*"([^"]+)",\s*(\d+),\s*(\d+),\s*"([A-Z]+)",\s*(None|\d+),\s*(None|r"[^"]*")\s*\)',
                          m.group(1)):
        f, s, e, cls, ml, mr = mm.groups()
        rows.append((f, int(s), int(e), cls,
                     None if ml == "None" else int(ml),
                     None if mr == "None" else mr[1:]))
    return rows


def key(r):
    return (r[0], r[1], r[2])


def main():
    before, after = parse(sys.argv[1]), parse(sys.argv[2])
    bset, aset = {key(r): r for r in before}, {key(r): r for r in after}
    added = [r for k, r in aset.items() if k not in bset]
    removed = [r for k, r in bset.items() if k not in aset]
    changed = [(bset[k], aset[k]) for k in bset.keys() & aset.keys()
               if bset[k] != aset[k]]
    flags = []
    for (f, s, e, cls, ml, mr) in added:
        if e >= 9000:
            flags.append("CREEP open-ended bound: %s %d-%d %s" % (f, s, e, cls))
        if cls == "DATED" and (e - s) > 150:
            flags.append("CREEP wide added DATED row: %s %d-%d (%d lines)" % (f, s, e, e - s + 1))
    for (f, s, e, cls, ml, mr) in added:
        for (f2, s2, e2, cls2, ml2, mr2) in removed:
            if f == f2 and s <= s2 and e >= e2 and (s < s2 or e > e2):
                flags.append("CREEP widen-by-add/remove: %s %d-%d %s replaced %d-%d %s"
                             % (f, s, e, cls, s2, e2, cls2))
    for (b, a) in changed:
        if b[3] == "CURRENT" and a[3] == "DATED":
            flags.append("CREEP class flip CURRENT->DATED: %s %d-%d -> %d-%d" % (b[0], b[1], b[2], a[1], a[2]))
        if a[2] > b[2] and a[3] == "DATED":
            flags.append("CREEP DATED end widened: %s %d-%d -> %d-%d" % (b[0], b[1], b[2], a[1], a[2]))
        if a[1] < b[1] and a[3] == "DATED":
            flags.append("CREEP DATED start moved earlier: %s %d-%d -> %d-%d" % (b[0], b[1], b[2], a[1], a[2]))
    print("rows before=%d after=%d" % (len(before), len(after)))
    print("ADDED (%d):" % len(added))
    for r in added:
        print("  + %s %d-%d %s marker_line=%s marker=%r" % r)
    print("REMOVED (%d):" % len(removed))
    for r in removed:
        print("  - %s %d-%d %s marker_line=%s marker=%r" % r)
    print("CHANGED (%d):" % len(changed))
    for b, a in changed:
        print("  ~ %s %d-%d %s -> %d-%d %s (marker %s->%s)" %
              (b[0], b[1], b[2], b[3], a[1], a[2], a[3], b[4], a[4]))
    print("CREEP FLAGS: %r" % flags)
    return 0 if (not added and not removed and not changed) else 1


if __name__ == "__main__":
    sys.exit(main())
