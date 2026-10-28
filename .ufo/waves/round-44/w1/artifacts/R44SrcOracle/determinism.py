#!/usr/bin/env python3
"""Determinism: the run-2 manifest's {path,bytes,sha256} must equal the run-1 snapshot."""
import json
import sys

W = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-44/w1/R44SrcOracle"
ORACLE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-44/oracle/manifest.json"


def load_tsv(path):
    out = {}
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            sha, size, p = line.split("\t")
            out[p] = (sha, int(size))
    return out


def main():
    run1 = load_tsv(f"{W}/digests.run1.tsv")
    m = json.load(open(ORACLE))
    run2 = {r["path"]: (r["sha256"], r["bytes"]) for r in m["files"]}
    diffs = [p for p in sorted(set(run1) | set(run2)) if run1.get(p) != run2.get(p)]
    print(f"run1_members={len(run1)} run2_members={len(run2)} differing={len(diffs)}")
    for p in diffs:
        print(f"  DIFF {p}: run1={run1.get(p)} run2={run2.get(p)}")
    print("failures_in_run2:", m["counts"]["failures"])
    print(f"deterministic={not diffs and m['counts']['failures'] == 0}")
    return 0 if (not diffs and m["counts"]["failures"] == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
