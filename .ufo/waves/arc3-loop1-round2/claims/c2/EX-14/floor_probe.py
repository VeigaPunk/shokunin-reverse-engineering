#!/usr/bin/env python3
"""EX-14 floor probe — evaluates candidate H3 positive-floor predicates.

Variants:
  A global   current-ok dets > 0                (CR-5's minimal patch)
  B per-file current-ok dets > 0                 (each readable scoped file)
  C global   loci (blocks) > 0
  D per-row  dets >= 1                           (all 20 rows)
  E per-row  dets >= 1, CURRENT rows only
  F per-row  current-ok dets >= 1                (all 20 rows)

Environments:
  head    — repo as-is
  blind   — needles neutered (CR-5 H3 attack)
  skilly  — SKILL.md absent in a scratch root (RV-11 H1 attack)
Read-only wrt the repo.
"""
import importlib.util
import os
import re
import sys

CENSUS = "/var/tmp/ex14/census.py"
ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"


def load():
    spec = importlib.util.spec_from_file_location("census", CENSUS)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def fresh():
    """Reload so needle monkey-patches never leak between environments."""
    return load()


def run(C, root, blind=False):
    if blind:
        never = re.compile(r"(?!x)x")
        C.PIN, C.VER, C.PTR = never, never, never
    live = C.live_pins()
    files = sorted({s[0] for s in C.SCOPE})
    out, counts, readable = {}, {}, {}
    for f in files:
        try:
            lines = open(os.path.join(root, f), encoding="utf-8", errors="replace").read().splitlines()
        except OSError:
            counts[f] = {"lines": 0, "loci": 0}
            readable[f] = False
            continue
        readable[f] = True
        counts[f] = {"lines": len(lines), "loci": len(C.classify(f, lines, live, out))}
    return live, counts, out, readable


def evaluate(C, root, blind=False):
    live, counts, out, readable = run(C, root, blind)
    dets = []
    for disp, recs in out.items():
        if disp in ("g11", "g7"):
            continue
        for r in recs:
            for d in r["asserts"]:
                dets.append((r["file"], d["line"], d["disp"], d["kind"], d["value"]))
    cur_ok = [d for d in dets if d[2] == "current-ok"]
    total_blocks = sum(c["loci"] for c in counts.values())

    def rows_of(fname, lo, hi):
        return [d for d in dets if d[0] == fname and lo <= d[1] <= hi]

    res = {}
    res["A_global_current_ok"] = len(cur_ok) > 0
    res["B_perfile_current_ok"] = all(
        any(d[2] == "current-ok" and d[0] == f for d in dets) for f in counts if readable[f])
    res["B2_perfile_incl_unreadable"] = all(
        any(d[2] == "current-ok" and d[0] == f for d in dets) for f in counts)
    res["C_global_loci"] = total_blocks > 0
    res["D_row_any_det"] = all(rows_of(f, s, e) for (f, s, e, cls, ml, mr) in C.SCOPE)
    res["E_row_det_currentclass"] = all(
        rows_of(f, s, e) for (f, s, e, cls, ml, mr) in C.SCOPE if cls == "CURRENT")
    res["F_row_current_ok"] = all(
        any(d[2] == "current-ok" for d in rows_of(f, s, e)) for (f, s, e, cls, ml, mr) in C.SCOPE)
    per_file = {f: sum(1 for d in cur_ok if d[0] == f) for f in counts}
    per_file_rows = {f: sum(1 for (ff, s, e, cls, ml, mr) in C.SCOPE if ff == f and any(d[2] == "current-ok" for d in rows_of(ff, s, e))) for f in counts}
    empty_rows = [i for i, (f, s, e, cls, ml, mr) in enumerate(C.SCOPE) if not rows_of(f, s, e)]
    return {"counts": counts, "readable": readable, "per_file_current_ok": per_file,
            "per_file_rows_with_current_ok": per_file_rows, "dets": len(dets), "current_ok": len(cur_ok),
            "blocks": total_blocks, "empty_rows": empty_rows,
            "empty_row_specs": ["%d:%s %d-%d %s" % (i, C.SCOPE[i][0], C.SCOPE[i][1], C.SCOPE[i][2], C.SCOPE[i][3])
                                for i in empty_rows],
            "variants": res}


C = load()
print("census sha256:", __import__("hashlib").sha256(open(CENSUS, "rb").read()).hexdigest())
for label, root, blind in (("head", ROOT, False),
                           ("blind", ROOT, True),
                           ("skilly", "/var/tmp/ex14/atk-missing", False),
                           ("nullskill", "/var/tmp/ex14/atk-nullskill", False)):
    r = evaluate(fresh(), root, blind)
    print("\n== ENV %s (root=%s blind=%s) ==" % (label, root, blind))
    print("  counts: %s" % r["counts"])
    print("  readable: %s" % r["readable"])
    print("  dets=%d current-ok=%d blocks=%d" % (r["dets"], r["current_ok"], r["blocks"]))
    print("  per-file current-ok dets: %s" % r["per_file_current_ok"])
    print("  per-file rows with a current-ok det: %s" % r["per_file_rows_with_current_ok"])
    print("  empty rows (%d): %s" % (len(r["empty_rows"]), r["empty_row_specs"]))
    for k, v in r["variants"].items():
        print("    %-28s %s" % (k, "PASS" if v else "FAIL"))
