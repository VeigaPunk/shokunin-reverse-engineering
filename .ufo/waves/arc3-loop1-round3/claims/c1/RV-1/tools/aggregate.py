#!/usr/bin/env python3
"""RV-1 r3 — aggregate every recompute leg into one table (markdown + json)."""
import glob
import json
import os

OUT = "/var/tmp/rv1-r3/out"
rows = {}
for f in glob.glob(os.path.join(OUT, "*.txt")) + glob.glob(os.path.join(OUT, "final", "*.txt")):
    label = os.path.basename(f)[:-4]
    text = open(f).read()
    if "# PLANTED_SET_JSON " not in text:
        continue
    d = json.loads([l for l in text.splitlines() if l.startswith("# PLANTED_SET_JSON ")][-1]
                   [len("# PLANTED_SET_JSON "):])
    verdict = {}
    for l in text.splitlines():
        if l.startswith("# A==B:"):
            verdict["abc"] = ("True" in l.split("A==C:")[0]) and ("A==C: True" in l)
        if l.startswith("# planted==A:"):
            verdict["planted"] = l.split("planted==A:")[1].split()[0]
        if l.startswith("# missing_from_recompute="):
            verdict["diff"] = l[len("# missing_from_recompute="):].strip()
        if l.startswith("# runtime ") and "compiled==file:" in l:
            verdict["runtime"] = l.split("compiled==file:")[1].strip()
    rows[label] = {**d, **verdict}

md = ["| leg | contract | K | source sha256 | planted? | runtime compiled==file |",
      "|---|---|---|---|---|---|"]
for label in sorted(rows):
    r = rows[label]
    md.append(f"| {label} | {r.get('contract','')} | {len(r.get('selectors',[]))} | "
              f"`{r.get('source_sha256','')[:16]}…` | {r.get('planted','-')} | {r.get('runtime','-')} |")
open(os.path.join(OUT, "recompute-table.md"), "w").write("\n".join(md) + "\n")
json.dump(rows, open(os.path.join(OUT, "recompute-table.json"), "w"), indent=1, sort_keys=True)
print("\n".join(md))
print(f"legs: {len(rows)}")