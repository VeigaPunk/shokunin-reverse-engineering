#!/usr/bin/env python3
"""Render the EX-27 before/after comparison table from the two regress.json files."""
import json
from pathlib import Path

BASE = Path("/var/tmp/ex27-r3/runs/baseline-112d01dc/regress.json")
REV = Path("/var/tmp/ex27-r3/runs/revised-7cd19c3c/regress.json")


def load(p):
    d = json.loads(Path(p).read_text())
    return {r["leg"] + "/" + r["name"]: r for r in d["rows"]}, d


b, bd = load(BASE)
r, rd = load(REV)

keys = list(b.keys())
print("| row | before (112d01dc) | after (%s) | verdict |" % rd["tool_sha"][:12])
print("|---|---|---|---|")


def brief(row):
    if row is None:
        return "—"
    parts = []
    mapping = [("verdict", "v"), ("exit", "exit"), ("sha_same", "sha="), ("sha_only_view", ""),
               ("label_defect", "labels"), ("sha_agree", "sha-agree"), ("cases", "cases"),
               ("read_error", "READ-ERR"), ("clobbered", "clobbered"), ("traceback", "traceback"),
               ("requires5", ""), ("require5_supported", "req5-flag")]
    for k, _ in mapping:
        if k in row and row[k] is not None:
            v = row[k]
            if isinstance(v, bool):
                v = "yes" if v else "no"
            parts.append("%s=%s" % (k, v))
    return " ".join(parts)


for k in keys:
    bb, rr = b.get(k), r.get(k)
    st = rr.get("hold") if rr else None
    verdict = {True: "HOLD", False: "**FAIL**", None: "change(declared)"}[st]
    print("| %s | %s | %s | %s |" % (k, brief(bb), brief(rr), verdict))