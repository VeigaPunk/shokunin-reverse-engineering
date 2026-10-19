#!/usr/bin/env python3
"""RV-9 independent receipt comparator (NOT custody-pair.py).

Parses v2 receipts (stanza blocks: PATH ... 16 fields) and compares two receipts
field-by-field for shared paths. Prints per-path AGREE/DIFFER and a summary.

usage: receipt-field-diff.py A.txt B.txt
exit 0 = every shared path agrees on every compared field; 1 = a field differs.
"""
import sys

FIELDS = ["EXISTS", "TYPE", "SIZE", "SHA256", "MTIME_EPOCH", "MTIME_NS",
          "MTIME_UTC_RENDER", "MTIME_LOCAL_RENDER", "CTIME_EPOCH", "CTIME_NS",
          "CTIME_UTC_RENDER", "CTIME_LOCAL_RENDER", "INODE", "MODE", "UID", "GID"]

def parse(path):
    stanzas = {}
    cur = None
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if line.startswith("#"):
                continue
            if line.startswith("PATH: "):
                cur = line[6:]
                stanzas[cur] = {}
            elif cur is not None and ": " in line:
                k, _, v = line.partition(": ")
                if k in FIELDS:
                    stanzas[cur][k] = v
    return stanzas

def main():
    a, b = sys.argv[1], sys.argv[2]
    A, B = parse(a), parse(b)
    shared = [p for p in A if p in B]
    print("A: %s  stanzas=%d" % (a, len(A)))
    print("B: %s  stanzas=%d" % (b, len(B)))
    print("shared paths: %d" % len(shared))
    diffs = 0
    for p in shared:
        bad = []
        for k in FIELDS:
            va, vb = A[p].get(k), B[p].get(k)
            if va != vb:
                bad.append("%s: A=%r B=%r" % (k, va, vb))
        status = "AGREE" if not bad else "DIFFER"
        print("PATH %s: %s (%d/%d fields)" % (p, status, len(FIELDS) - len(bad), len(FIELDS)))
        for d in bad:
            print("   %s" % d)
        diffs += len(bad)
    onlyA = sorted(set(A) - set(B)); onlyB = sorted(set(B) - set(A))
    if onlyA: print("only-in-A: %s" % onlyA)
    if onlyB: print("only-in-B: %s" % onlyB)
    print("TOTALFIELD-DIFFS: %d" % diffs)
    return 0 if (diffs == 0 and shared) else 1

if __name__ == "__main__":
    sys.exit(main())