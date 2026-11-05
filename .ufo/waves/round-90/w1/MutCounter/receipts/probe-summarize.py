#!/usr/bin/env python3
"""summarize.py - turn the mutant-run receipts into the evidence table.

For every $S/runs/<id>/receipt.json print: label, met_target, exit, per
population counts, the controls that are false, and the killing case:
 * the first scored cell that is not recovered, else
 * the first re-scored carrier-blind cell that is not recovered (that is the
   arm that rejects a source-bound cheat once the repair scores every cell).
Also dump the isolation box listings and the repair sha256 (which ties the run
to the exact cheat bytes).
"""

import glob
import json
import os

S = "/fast/scratch/hyaku/kaidoku-r90/MutCounter"


def bad_arms(arms):
    return [k for k, v in arms.items() if v is not None and v is not True]


def killer(r):
    for pop in ("P1-later-block", "P2-first-block", "P3-zeroed"):
        for c in r["cases"][pop]:
            if not c["recovered"]:
                return {"where": f"{pop}/{c['carrier']}/{c.get('direction')}",
                        "rc": c["rc"], "failing_arms": bad_arms(c["arms"]),
                        "box_after": c["box_after"]}
    bc = r["controls"]["carrier_blind"]
    if not r["controls_ok"]["carrier_blind"]:
        for c in bc["cases"]:
            if not c["recovered"]:
                return {"where": f"carrier_blind/{c['carrier']}/{c.get('direction')}",
                        "rc": c["rc"], "failing_arms": bad_arms(c["arms"]),
                        "box_after": c["box_after"]}
        return {"where": "carrier_blind/probe", "rc": None,
                "failing_arms": ["blind_ok"], "box_after": None}
    return None


rows = []
for path in sorted(glob.glob(f"{S}/runs/*/receipt.json")):
    rid = os.path.basename(os.path.dirname(path))
    r = json.load(open(path))
    rec = {"run": rid, "label": r["label"], "met_target": r["met_target"],
           "exit": r["exit"], "recovered": r["recovered"],
           "expect": r["expect"],
           "controls_false": [k for k, v in r["controls_ok"].items() if not v],
           "controls_ok": r["controls_ok"],
           "repair_sha256": (r["repair"] or {}).get("sha256"),
           "shell_exit": open(os.path.join(os.path.dirname(path),
                                           "exit.txt")).read().strip(),
           "killing_case": killer(r),
           "isolation_listings": sorted({tuple(x["box_after"])
                                         for x in r["controls"]["isolation"]}),
           "blind_recovered": sum(1 for c in r["controls"]["carrier_blind"]["cases"]
                                  if c["recovered"]),
           "blind_cases": len(r["controls"]["carrier_blind"]["cases"])}
    rows.append(rec)
    print(f"{rid:34s} met={str(r['met_target']):5s} exit={r['exit']} "
          f"shell={rec['shell_exit']} {r['label']}  false={','.join(rec['controls_false']) or '-'}")
    k = rec["killing_case"]
    if k:
        print(f"{'':34s} killer {k['where']} rc={k['rc']} arms={','.join(k['failing_arms'])}")
    if len(rec["isolation_listings"]) > 1 or any("leak" in t for t in rec["isolation_listings"]):
        print(f"{'':34s} isolation listings {rec['isolation_listings']} "
              f"ok={rec['controls_ok']['isolation']}")
json.dump(rows, open(f"{S}/summary.json", "w"), indent=1)
print(f"{len(rows)} runs summarised -> {S}/summary.json")
