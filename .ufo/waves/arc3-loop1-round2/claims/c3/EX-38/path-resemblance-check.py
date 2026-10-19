#!/usr/bin/env python3
"""EX-38 citation-resemblance check for new file paths (seat EX-38, c3, r2).

Question: do paths newly added to the repo by EX-31 (the custody-pair tool)
resemble the citation-drift probe's PINNED CITATIONS — i.e. the files named in
`pointer-table.json` (citing files and resolved targets)?

Resemblance classes, each an exact string test (no fuzzy guessing):
  R1 exact_target_collision   new path == a needle file path     [HARD]
  R3 suffix_resemblance       new path endswith a needle path, or vice versa
                                                                  [HARD]
  R2 basename_collision       basename(new) == basename(needle file), other dir
                                                                  [ADVISORY]
  R4 dir_adjacency            new path sits in a dir that also holds a needle file
                                                                 [INFO]
R1/R3 are the citation-grade risks: a shared full path (R1, or a tail long
enough to be mistaken for one) is what the probe itself resolves, so a collision
would put the new file's bytes under a pinned citation. R2 is naming hygiene
only — it fires on any reuse of a generic basename (demonstrated: a proposed
`custody-pair/README.md` fires R2 against `corpus/README.md`), so it is reported
and left for adjudication, never auto-red. R4 is adjacency, not a defect.

Exit: 0 no R1/R3, 1 R1/R3 present, 2 could-not-evaluate.
"""
import argparse
import json
import os
import sys


def needle_set(table):
    """Every file path the probe can read: citing files and non-@ targets."""
    paths = set()
    for entry in list(table.get("entries", [])) + list(table.get("quoted", [])):
        f = entry.get("file")
        if f and not f.startswith("@"):
            paths.add(f)
        t = entry.get("target")
        if t and not t.startswith("@"):
            paths.add(t)
    return paths


def check(new_paths, needles):
    rows = []
    for p in new_paths:
        for n in sorted(needles):
            if p == n:
                rows.append(("R1", p, n, "exact path identity"))
                continue
            # a multi-segment shared tail is the citation-grade resemblance:
            # a bare basename match is only R2 below.
            tail = n if p.endswith("/" + n) else (p if n.endswith("/" + p) else None)
            if tail and "/" in tail:
                rows.append(("R3", p, n, "path-suffix identity on tail %r" % tail))
            elif os.path.basename(p) == os.path.basename(n):
                rows.append(("R2", p, n, "same basename, different directory"))
            elif os.path.dirname(p) == os.path.dirname(n):
                rows.append(("R4", p, n, "same directory"))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", required=True)
    ap.add_argument("--paths-file", required=True,
                    help="one new repo-relative path per line, '#' comments allowed")
    args = ap.parse_args()
    try:
        table = json.load(open(args.table))
        lines = [l.strip() for l in open(args.paths_file)]
    except (OSError, ValueError) as exc:
        print("RESEMBLANCE: could-not-evaluate %s" % exc)
        return 2
    new_paths = [l for l in lines if l and not l.startswith("#")]
    needles = needle_set(table)
    rows = check(new_paths, needles)
    for cls, p, n, why in rows:
        print("RESEMBLANCE: %s new=%s needle=%s (%s)" % (cls, p, n, why))
    hard = [r for r in rows if r[0] in ("R1", "R3")]
    advisory = [r for r in rows if r[0] == "R2"]
    info = [r for r in rows if r[0] == "R4"]
    print("RESEMBLANCE_SUMMARY: new_paths=%d needles=%d hard_findings=%d "
          "(R1/R3) advisory=%d (R2) informational=%d (R4)"
          % (len(new_paths), len(needles), len(hard), len(advisory), len(info)))
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
