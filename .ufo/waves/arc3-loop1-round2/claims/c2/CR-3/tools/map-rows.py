#!/usr/bin/env python3
"""CR-3 (c2 critic) — per-SCOPE-row locus map at HEAD.

Imports the frozen census v10 instrument (READ-ONLY) and aggregates, for every
declared SCOPE row, the number of (a) blocks whose physical span intersects the
row and (b) per-assert physical lines lying inside the row. Emits JSON.
"""
import collections
import importlib.util
import json
import os
import sys

GATE = sys.argv[1] if len(sys.argv) > 1 else \
    "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/c1-census-v10.py"
ROOT = sys.argv[2] if len(sys.argv) > 2 else \
    "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"

spec = importlib.util.spec_from_file_location("census", GATE)
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)

live = C.live_pins()
if not all(live.values()):
    print("ANCHOR-FAIL %r" % live)
    sys.exit(2)

files = sorted({s[0] for s in C.SCOPE})
filelines, out, counts = {}, {}, {}
loci_by_file = {}
for f in files:
    p = os.path.join(ROOT, f)
    try:
        lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
    except OSError:
        filelines[f] = None
        counts[f] = {"lines": 0, "loci": 0}
        continue
    filelines[f] = lines
    loci = C.classify(f, lines, live, out)
    loci_by_file[f] = loci
    counts[f] = {"lines": len(lines), "loci": len(loci)}

rows = []
for (f, s, e, cls, ml, mr) in C.SCOPE:
    lines = filelines.get(f)
    in_bounds = lines is not None and s <= len(lines)
    span = lines[s - 1:e] if in_bounds else []
    nonblank = sum(1 for ln in span if ln.strip())
    assert_lines, assert_kinds, blocks = [], collections.Counter(), []
    for rec in loci_by_file.get(f, []):
        a, b = [int(x) for x in rec["block"].split("-")]
        if not (b < s or a > e):
            blocks.append({"block": rec["block"], "disp": rec["disp"],
                           "intersects": True})
        for d in rec["asserts"]:
            if s <= d["line"] <= e:
                assert_lines.append(d["line"])
                assert_kinds[d["disp"]] += 1
    rows.append({
        "row": "%s:%d-%d" % (f, s, e), "file": f, "start": s, "end": e,
        "class": cls, "marker_line": ml,
        "file_lines": (len(lines) if lines is not None else None),
        "in_bounds": in_bounds,
        "nonblank_lines_in_row": nonblank,
        "blocks_intersecting": len(blocks),
        "assert_lines": sorted(assert_lines),
        "assert_count": len(assert_lines),
        "assert_disps": dict(assert_kinds),
        "ZERO_LOCUS": len(assert_lines) == 0,
    })

undeclared_lines = []
for f in files:
    lines = filelines.get(f)
    if not lines:
        continue
    for rec in loci_by_file.get(f, []):
        for d in rec["asserts"]:
            if C.scope_of(f, d["line"])[0] is None:
                undeclared_lines.append("%s:%d" % (f, d["line"]))

summary = {
    "gate": GATE, "root": ROOT, "live": live, "counts": counts,
    "verdict": ("PASS" if (not out.get("STALE") and not out.get("AMBIGUOUS")
                and not out.get("UNDECLARED") and not out.get("UNRESOLVED")
                and not C.assert_markers(filelines) and not out.get("g11"))
                else "FAIL"),
    "current_ok_loci": len(out.get("current-ok", [])),
    "historical_loci": len(out.get("historical", [])),
    "zero_locus_rows": [r["row"] for r in rows if r["ZERO_LOCUS"]],
    "zero_locus_files": [f for f, c in counts.items() if c["loci"] == 0],
    "undeclared_assert_lines": undeclared_lines,
    "rows": rows,
}

print(json.dumps(summary, indent=1))
