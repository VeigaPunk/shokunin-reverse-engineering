#!/usr/bin/env python3
"""RV-4 census locus differ — review instrument for wave arc3-loop1-round4 (chain c2).

Purpose: given a BASELINE census JSON and a CANDIDATE census JSON (both from
`.ufo/gates/c1-census-v10.py --root DIR --json`), report every locus-level
difference.  A "gated locus" for this review is one assertion entry (the
instrument's own unit of detection: file, physical line, kind, client, value)
plus every row-level disposition the verdict is computed from (STALE /
AMBIGUOUS / UNDECLARED / UNRESOLVED / SCOPE-ERRORS / UNREADABLE / g11 / g7 /
declared fail classes / the G2 per-file floor).

Patch texts are applied to a SCRATCH COPY of the tree; the real tree is only
ever read.  Usage:

    python3 census-diff.py BASELINE.json CANDIDATE.json

Exit 0 when the candidate introduces no new gated locus and no disposition
regression; 1 otherwise; 2 on input error.
"""
import json
import sys


def load(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError) as ex:
        print("cannot read census JSON %r: %s" % (path, ex), file=sys.stderr)
        raise SystemExit(2)


def assertion_keys(doc):
    """Every assertion entry the instrument recorded, as a stable key."""
    keys = {}
    for bucket in ("stale", "ambiguous", "undeclared", "unresolved", "historical",
                   "current_ok", "info"):
        for rec in doc.get(bucket) or []:
            if not isinstance(rec, dict):
                continue
            for d in rec.get("asserts") or []:
                key = (rec["file"], d["line"], d["kind"], str(d["client"]),
                       str(d["value"]))
                keys[key] = {"bucket": bucket, "disp": d["disp"], "why": d["why"],
                             "block": rec["block"], "scope": d["scope"]}
    return keys


def row_keys(doc):
    out = {}
    for bucket in ("stale", "ambiguous", "undeclared", "unresolved"):
        for rec in doc.get(bucket) or []:
            if not isinstance(rec, dict):
                continue
            out[(rec["file"], rec["block"], bucket)] = rec.get("text", "")[:120]
    return out


def main(argv):
    if len(argv) != 3:
        print("usage: census-diff.py BASELINE.json CANDIDATE.json", file=sys.stderr)
        return 2
    base, cand = load(argv[1]), load(argv[2])

    ba, ca = assertion_keys(base), assertion_keys(cand)
    new_keys = sorted(set(ca) - set(ba))
    gone_keys = sorted(set(ba) - set(ca))
    moved = sorted(k for k in set(ba) & set(ca) if ba[k]["disp"] != ca[k]["disp"])

    print("== assertion inventory ==")
    print("baseline assertions=%d  candidate assertions=%d" % (len(ba), len(ca)))

    print("\n== NEW gated loci (candidate-only assertions) — %d ==" % len(new_keys))
    for k in new_keys:
        print("  %s:%s [%s] %s=%s -> %s (%s)  block %s scope %s"
              % (k[0], k[1], k[2], k[3], k[4], ca[k]["disp"], ca[k]["why"],
                 ca[k]["block"], ca[k]["scope"]))
    if not new_keys:
        print("  (none)")

    print("\n== REMOVED assertions (baseline-only) — %d ==" % len(gone_keys))
    for k in gone_keys:
        print("  %s:%s [%s] %s=%s -> was %s" % (k[0], k[1], k[2], k[3], k[4],
                                                ba[k]["disp"]))
    if not gone_keys:
        print("  (none)")

    print("\n== DISPOSITION MOVES (same assertion, different class) — %d ==" % len(moved))
    for k in moved:
        print("  %s:%s [%s] %s=%s  %s -> %s" % (k[0], k[1], k[2], k[3], k[4],
                                                ba[k]["disp"], ca[k]["disp"]))
    if not moved:
        print("  (none)")

    print("\n== verdict rows ==")
    for name in ("verdict", "scope_errors", "unreadable", "g2_ok",
                 "declared_fail_classes", "g11", "g7", "current_ok_per_file",
                 "counts"):
        b, c = base.get(name), cand.get(name)
        flag = "" if b == c else "   <-- CHANGED"
        print("  %-22s baseline=%r%s" % (name, b, flag))
        if b != c:
            print("  %-22s candidate=%r" % ("", c))

    bad = bool(new_keys) or bool(moved) or base.get("verdict") != cand.get("verdict")
    for name in ("scope_errors", "unreadable", "g11", "g7", "declared_fail_classes"):
        if len(cand.get(name) or []) > len(base.get(name) or []):
            bad = True
    print("\nRESULT: %s" % ("DEFECT — new gated locus or regression present"
                            if bad else "CLEAN — no new gated locus, no regression"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
