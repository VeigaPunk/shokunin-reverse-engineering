#!/usr/bin/env python3
"""EX-14 scope-locus map (arc3-loop1-round2, chain c2).

Attributes every census locus (block) and every det (assertion) to the SCOPE
row that owns its primary physical line, then reports per-row and per-file
occupancy so the H3 positive-floor predicate can be tested for false FAILs on
ordinary HEAD runs.

Read-only: imports the census module, never writes to the repo.
"""
import importlib.util
import json
import os
import sys

CENSUS = sys.argv[1] if len(sys.argv) > 1 else "/var/tmp/ex14/census.py"
ROOT = sys.argv[2] if len(sys.argv) > 2 else "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"

spec = importlib.util.spec_from_file_location("census", CENSUS)
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)

live = C.live_pins()
files = sorted({s[0] for s in C.SCOPE})
out = {}
counts = {}
filelines = {}
for f in files:
    try:
        lines = open(os.path.join(ROOT, f), encoding="utf-8", errors="replace").read().splitlines()
    except OSError:
        counts[f] = {"lines": 0, "loci": 0, "readable": False}
        filelines[f] = None
        continue
    filelines[f] = lines
    counts[f] = {"lines": len(lines), "loci": len(C.classify(f, lines, live, out)), "readable": True}

# ---- row occupancy ------------------------------------------------------
rows = []
for idx, (f, s, e, cls, ml, mr) in enumerate(C.SCOPE):
    rec = {"idx": idx, "file": f, "range": "%d-%d" % (s, e), "class": cls,
           "blocks": 0, "dets": 0, "line_hits": [], "disps": {}, "kinds": {},
           "values": [], "gate_only": 0, "lines_in_range": 0}
    lines = filelines.get(f)
    if lines:
        rec["lines_in_range"] = max(0, min(e, len(lines)) - s + 1)
    rows.append(rec)

for disp, recs in out.items():
    if disp in ("g11", "g7"):
        continue
    for r in recs:
        f = r["file"]
        for d in r["asserts"]:
            cls, ml, mr = C.scope_of(f, d["line"])
            for row in rows:
                if row["file"] == f and row["range"] == "%d-%d" % (d["line"] * 0 + 0, 0):
                    pass
            # attribute by row bounds
            for idx, (rf, rs, re_, rcls, rml, rmr) in enumerate(C.SCOPE):
                if rf == f and rs <= d["line"] <= re_:
                    rows[idx]["dets"] += 1
                    rows[idx]["line_hits"].append(d["line"])
                    rows[idx]["disps"][d["disp"]] = rows[idx]["disps"].get(d["disp"], 0) + 1
                    rows[idx]["kinds"][d["kind"]] = rows[idx]["kinds"].get(d["kind"], 0) + 1
                    if len(rows[idx]["values"]) < 8:
                        rows[idx]["values"].append("%s=%s(%s)" % (d["client"], d["value"], d["disp"]))
        # block counted once per row that owns its first det
        if r["asserts"]:
            first = r["asserts"][0]["line"]
            for idx, (rf, rs, re_, rcls, rml, rmr) in enumerate(C.SCOPE):
                if rf == f and rs <= first <= re_:
                    rows[idx]["blocks"] += 1
                    break

# ---- gate-text-only scan (row holds gate vocabulary but no needle) ------
for row in rows:
    lines = filelines.get(row["file"])
    s, e = row["range"].split("-")
    s, e = int(s), int(e)
    if not lines:
        continue
    for i in range(s, min(e, len(lines)) + 1):
        txt = lines[i - 1].strip()
        if txt and C.REA_GATE.search(txt):
            # is this physical line covered by any det?
            if i not in row["line_hits"]:
                row["gate_only"] += 1

report = {
    "census": CENSUS,
    "census_sha256": __import__("hashlib").sha256(open(CENSUS, "rb").read()).hexdigest(),
    "root": ROOT,
    "live": live,
    "counts": counts,
    "rows": rows,
    "row_count": len(rows),
    "zero_det_rows": [r["idx"] for r in rows if r["dets"] == 0],
    "zero_block_rows": [r["idx"] for r in rows if r["blocks"] == 0],
    "zero_locus_files": [f for f, c in counts.items() if c["loci"] == 0],
}
print(json.dumps(report, indent=1))
