#!/usr/bin/env python3
"""EX-21 diff-surface helper: name which top-level functions/constants changed.

Usage: python3 diff-surface.py <before.py> <after.py> [--diff]

Prints a per-top-level-block status table (added/removed/changed/same) with
sha256 of each block body, so an external audit can state exactly which
functions moved — and, with --diff, the unified diff itself. Blocks are split
on top-level (column-0) `def`/`class`/assignment anchors, which is approximate
by construction; the unified diff is the ground truth and is included whenever
any block is reported changed.
"""
import difflib
import hashlib
import re
import sys

ANCHOR = re.compile(r"(?m)^(?:def\s+(\w+)|class\s+(\w+)|([A-Z_][A-Z0-9_]*)\s*=|@)")


def blocks(path):
    lines = open(path, encoding="utf-8").read().splitlines(True)
    starts = []
    for i, line in enumerate(lines):
        m = ANCHOR.match(line)
        if m:
            name = m.group(1) or m.group(2) or m.group(3) or "@decorator"
            starts.append((i, name))
    out = []
    for n, (i, name) in enumerate(starts):
        end = starts[n + 1][0] if n + 1 < len(starts) else len(lines)
        body = "".join(lines[i:end])
        out.append((name, hashlib.sha256(body.encode()).hexdigest()[:12], i + 1, end))
    return out


def main():
    before, after = blocks(sys.argv[1]), blocks(sys.argv[2])
    bd = {name: (h, s, e) for (name, h, s, e) in before}
    ad = {name: (h, s, e) for (name, h, s, e) in after}
    changed = []
    for name in [n for (n, _h, _s, _e) in after]:
        if name not in bd:
            print("ADDED    %-24s sha=%s lines=%d-%d" % (name, ad[name][0], ad[name][1], ad[name][2]))
            changed.append(name)
        elif bd[name][0] != ad[name][0]:
            print("CHANGED  %-24s %s -> %s  lines %d-%d -> %d-%d"
                  % (name, bd[name][0], ad[name][0], bd[name][1], bd[name][2], ad[name][1], ad[name][2]))
            changed.append(name)
    for name in [n for (n, _h, _s, _e) in before]:
        if name not in ad:
            print("REMOVED  %-24s sha=%s lines=%d-%d" % (name, bd[name][0], bd[name][1], bd[name][2]))
            changed.append(name)
    same = [n for n in ad if n in bd and bd[n][0] == ad[n][0]]
    print("BLOCKS: total_after=%d changed=%d same=%d" % (len(ad), len(changed), len(same)))
    if changed or "--diff" in sys.argv:
        a = open(sys.argv[1], encoding="utf-8").read().splitlines(True)
        b = open(sys.argv[2], encoding="utf-8").read().splitlines(True)
        sys.stdout.writelines(difflib.unified_diff(a, b, fromfile=sys.argv[1], tofile=sys.argv[2], n=3))
    return 0


if __name__ == "__main__":
    sys.exit(main())
