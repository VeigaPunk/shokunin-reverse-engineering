#!/usr/bin/env python3
"""EX-05 (c1, round 2): JSON delta between two census v10 runs.

Compares the --json output of a baseline root against a treated root and
prints every difference except the declared-benign `counts.<file>.lines`
growth (line-count changes are expected when a rule block is appended).
Any new locus record, verdict change, or count change other than `lines`
is printed as a DELTA and makes exit 1.

Usage: python3 census-delta.py baseline.json treated.json
"""
import json
import sys

KEYS = ("stale", "ambiguous", "undeclared", "unresolved", "scope_errors",
        "g11", "g7", "unreadable", "declared_fail_classes")


def fingerprint(rec):
    if isinstance(rec, dict):
        return "%s %s [%s] %s" % (rec.get("file"), rec.get("block"),
                                 rec.get("disp"),
                                 ";".join("%s=%s" % (a.get("kind"), a.get("value"))
                                          for a in rec.get("asserts", [])))
    return str(rec)


def main(basef, treatf):
    base = json.load(open(basef))
    treat = json.load(open(treatf))
    deltas = 0
    if base["verdict"] != treat["verdict"]:
        print("DELTA verdict: %s -> %s" % (base["verdict"], treat["verdict"]))
        deltas += 1
    for f in sorted(set(base["counts"]) | set(treat["counts"])):
        b, t = base["counts"].get(f, {}), treat["counts"].get(f, {})
        if b.get("lines") != t.get("lines"):
            print("lines %-14s %s -> %s (benign: appended rule block)"
                  % (f, b.get("lines"), t.get("lines")))
        if b.get("loci") != t.get("loci"):
            print("DELTA loci %-14s %s -> %s" % (f, b.get("loci"), t.get("loci")))
            deltas += 1
    for k in KEYS:
        b = [fingerprint(r) for r in base.get(k, [])]
        t = [fingerprint(r) for r in treat.get(k, [])]
        for r in t:
            if r not in b:
                print("DELTA %s new: %s" % (k, r))
                deltas += 1
        for r in b:
            if r not in t:
                print("DELTA %s lost: %s" % (k, r))
                deltas += 1
    for k in ("historical", "current_ok"):
        b = {fingerprint(r) for r in base.get(k, [])}
        t = {fingerprint(r) for r in treat.get(k, [])}
        for r in sorted(t - b):
            print("DELTA %s new: %s" % (k, r))
            deltas += 1
        for r in sorted(b - t):
            print("DELTA %s lost: %s" % (k, r))
            deltas += 1
    print("DELTAS=%d" % deltas)
    return 1 if deltas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
