#!/usr/bin/env python3
"""R44EntryDraft: byte-diff two files, no external comparator.

The omp shell resolves `cmp` to a built-in (pi-shell) whose exit code does not follow
GNU cmp semantics, so the entry's byte-diff fact is measured here instead: this prints
the byte length of both files and every differing 0-based offset with its two bytes.

Usage: python3 -I -B bytediff.py <fileA> <fileB>
Exit 0 when the run completed (difference or not); the verdict is the printed count.
"""
import sys


def main():
    a, b = sys.argv[1], sys.argv[2]
    x, y = open(a, "rb").read(), open(b, "rb").read()
    n = min(len(x), len(y))
    diffs = [(i, x[i], y[i]) for i in range(n) if x[i] != y[i]]
    print(f"len_a={len(x)} len_b={len(y)} diff_bytes={len(diffs)}")
    for i, p, q in diffs:
        print(f"offset0={i} a=0o{p:o} b=0o{q:o} a_chr={chr(p) if 32 <= p < 127 else '?'} "
              f"b_chr={chr(q) if 32 <= q < 127 else '?'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
