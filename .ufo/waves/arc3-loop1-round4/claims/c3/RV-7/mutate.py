#!/usr/bin/env python3
"""RV-7 mutation driver — revert individual fix hunks of a revised tool.

Seat RV-7 (chain c3, reviewer), wave arc3-loop1-round4, 2026-10-19.

Given the base revision (pre-fix) and the revised revision (post-fix), this
driver lists the diff hunks between them and builds mutants that revert a
selected subset of hunks — one mutant per named residual (a)(b)(c). The claim
under test is load-bearing: reverting fix (a) alone must bring back exactly
(a)'s before-behavior (and so on).

  mutate.py list   <base.py> <revised.py>
  mutate.py revert <base.py> <revised.py> <hunk-indices-comma-sep> <out.py>

Reverting a hunk = restoring the base-side lines of that hunk in place of the
revised-side lines, in the revised file. Implemented with difflib opcodes so it
is byte-exact and does not depend on `patch` context heuristics.
"""
import difflib
import hashlib
import sys
from pathlib import Path


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def opcodes(base_lines, rev_lines):
    sm = difflib.SequenceMatcher(a=base_lines, b=rev_lines, autojunk=False)
    return sm.get_opcodes()


def show(base, rev):
    base_lines = Path(base).read_text().splitlines(keepends=True)
    rev_lines = Path(rev).read_text().splitlines(keepends=True)
    ops = opcodes(base_lines, rev_lines)
    idx = 0
    for tag, i1, i2, j1, j2 in ops:
        if tag == "equal":
            continue
        print("HUNK %d  %s  base[%d:%d] -> rev[%d:%d]" % (idx, tag, i1, i2, j1, j2))
        for ln in base_lines[i1:i2]:
            print("  -%s" % ln.rstrip("\n"))
        for ln in rev_lines[j1:j2]:
            print("  +%s" % ln.rstrip("\n"))
        print()
        idx += 1
    print("TOTAL HUNKS: %d" % idx)
    print("base    %s  %d bytes  %d lines" % (sha256(base), Path(base).stat().st_size, len(base_lines)))
    print("revised %s  %d bytes  %d lines" % (sha256(rev), Path(rev).stat().st_size, len(rev_lines)))


def revert(base, rev, indices, out):
    base_lines = Path(base).read_text().splitlines(keepends=True)
    rev_lines = Path(rev).read_text().splitlines(keepends=True)
    ops = opcodes(base_lines, rev_lines)
    non_eq = [(tag, i1, i2, j1, j2) for (tag, i1, i2, j1, j2) in ops if tag != "equal"]
    want = set(int(x) for x in indices.split(",") if x.strip())
    out_lines = []
    cursor = 0
    for idx, (tag, i1, i2, j1, j2) in enumerate(non_eq):
        out_lines.extend(rev_lines[cursor:j1])
        if idx in want:
            out_lines.extend(base_lines[i1:i2])  # revert to base side
        else:
            out_lines.extend(rev_lines[j1:j2])
        cursor = j2
    out_lines.extend(rev_lines[cursor:])
    Path(out).write_text("".join(out_lines))
    print("wrote %s  sha256=%s  bytes=%d" % (out, sha256(out), Path(out).stat().st_size))
    print("reverted hunks: %s" % sorted(want))
    print("mutant == base? %s" % (sha256(out) == sha256(base)))


def main():
    cmd = sys.argv[1]
    if cmd == "list":
        show(sys.argv[2], sys.argv[3])
    elif cmd == "revert":
        revert(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        raise SystemExit("usage: mutate.py list|revert ...")


if __name__ == "__main__":
    main()
