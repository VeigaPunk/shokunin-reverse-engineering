#!/usr/bin/env python3
"""CritC2Scope probe 2: what the out-of-scope 95.8% of SCORECARD.md contains, atom-wise."""
import json
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, os.path.join(LANE, "tools", "round-47"))
sys.path.insert(0, os.path.join(LANE, "tools", "round-46"))
import record  # noqa: E402

REV = sys.argv[1] if len(sys.argv) > 1 else "2e4ae434"


def files(path):
    r = subprocess.run(["git", "-C", LANE, "show", f"{REV}:{path}"],
                       capture_output=True, text=True)
    return None if r.returncode != 0 else r.stdout


CARD = files("SCORECARD.md")
heads = [(m.start(), m.group(1)) for m in re.finditer(r"(?m)^## (.+)$", CARD)]
buckets = {"front": [], "luna": [], "arc": [], "round": [], "corrections": []}
per = []
for i, (pos, title) in enumerate(heads):
    end = heads[i + 1][0] if i + 1 < len(heads) else len(CARD)
    body = CARD[pos:end]
    nlines = body.count("\n")
    atoms = record.collect(body, "0", files, LANE, REV)
    if title.startswith("Round "):
        b = "round"
    elif title.startswith("luna-"):
        b = "luna"
    elif title.startswith("arc2") or title.startswith("arc3") or title.startswith("Post-review"):
        b = "arc"
    elif title.startswith("Record corrections"):
        b = "corrections"
    else:
        b = "front"
    buckets[b].append({"title": title[:60], "line": CARD[:pos].count("\n") + 1,
                       "lines": nlines, "atoms": len(atoms),
                       "by_class": {c: sum(1 for a in atoms if a["class"] == c)
                                    for c in record.CLASSES}})

summ = {}
for b, rows in buckets.items():
    summ[b] = {"sections": len(rows), "lines": sum(r["lines"] for r in rows),
               "atoms": sum(r["atoms"] for r in rows),
               "by_class": {c: sum(r["by_class"][c] for r in rows)
                            for c in record.CLASSES}}
print(json.dumps({"rev": REV, "total_lines": CARD.count("\n"),
                  "buckets": summ,
                  "front_detail": buckets["front"],
                  "round_sections": len(buckets["round"]),
                  "luna_and_arc_titles": [r["title"] for r in buckets["luna"] + buckets["arc"]][:8]},
                 indent=1))
