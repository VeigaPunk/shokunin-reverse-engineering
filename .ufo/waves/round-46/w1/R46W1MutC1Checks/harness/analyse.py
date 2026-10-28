#!/usr/bin/env python3
"""Per-case failure deltas: what the mutation removed, and why a case stayed red."""
import json
import sys

S = "/fast/scratch/hyaku/kaidoku-r46/R46W1MutC1Checks"
d = json.load(open(S + "/receipts/summary.json"))
runs, meta = d["runs"], d["meta"]


def why(rec):
    rows = rec.get("case_rows") or []
    return {r["case"]: r.get("failing") for r in rows}


for ver in ("base", "head"):
    base = why(runs[f"{ver}-baseline"])
    print(f"\n######## {ver}  (baseline exit={runs[f'{ver}-baseline']['exit']} "
          f"cases={runs[f'{ver}-baseline']['cases']})")
    for mid in sorted({m["mutant"] for m in meta.values()}):
        rec = runs.get(f"{ver}-{mid}")
        if not rec or rec.get("case_rows") is None:
            print(f"\n-- {mid}: UNPARSED exit={rec and rec.get('exit')}")
            continue
        got = why(rec)
        delta = []
        for case in base:
            b = json.dumps(base[case], sort_keys=True)
            g = json.dumps(got.get(case), sort_keys=True)
            if b != g:
                delta.append((case, base[case], got.get(case)))
        print(f"\n-- {mid}: exit={rec['exit']} failures={rec['failures']}")
        for case, b, g in delta:
            print(f"   {case}\n      base: {b}\n      mut : {g}")
