#!/usr/bin/env python3
"""RV-12 rating engine (v3).

Merges: probe replay over history, churn (insert-above-pin events), the honest
edit scenarios S1 reflow / S2 in-phrase reword / S3 insert-above / S6 anchor
reform, and the rename scenarios. Emits a per-entry fragility rating.

usage: rv12-rate.py <prefix> <out.md>
"""
import json
import re
import sys

D = "/var/tmp/rv12"
prefix, out = sys.argv[1], sys.argv[2]

fr = json.load(open("%s/%s-fragility.json" % (D, prefix)))
ch = json.load(open("%s/%s-churn.json" % (D, prefix)))
sc = json.load(open("%s/%s-scenarios.json" % (D, prefix)))
rn = json.load(open("%s/%s-rename.json" % (D, prefix)))

rename_fired = {}
by_path = {}
for e in fr["entries"]:
    for key in ("file", "target"):
        if e.get(key):
            by_path.setdefault(e[key], []).append(e["id"])
for path, r in rn.items():
    for eid in r["fired"]:
        # a renamed citing/target file is reported by the probe under its PATH,
        # not under the entry id: map it back to the entries it pinpoints
        affected = [eid] if eid not in by_path else by_path[eid]
        for a in affected:
            rename_fired.setdefault(a, []).append(path)

OPMUT = ("SCORECARD.md", "PROVINCE.md", "SHONEN.md", "SKILL.md", "LOG.md",
         "README.md")
HEX = re.compile(r"[0-9a-f]{8,}")


def needle_class(e):
    n = e.get("must_match") or ""
    words = [w for w in re.findall(r"[A-Za-z]{3,}", n)
             if w not in ("md", "the", "and", "not", "see")]
    if e.get("kind") == "extracted":
        return "pointer+needle"
    if HEX.search(n) or re.search(r"\d{4}-\d{2}-\d{2}", n):
        return "token"
    if len(words) >= 2:
        return "prose"
    return "token-ish"


rows = []
for e in fr["entries"]:
    eid = e["id"]
    classes, own = [], []
    if eid in rename_fired:
        classes.append("RENAME")
    for scen, tag in (("S6", "REFORM"), ("S3", "SHIFT"), ("S1", "REFLOW"),
                      ("S2", "REWORD")):
        h = sc.get(scen, {}).get(eid)
        if h:
            classes.append(tag)
            if h.get("finding"):
                own.append(tag)
    c = ch.get(eid, {})
    shifts = c.get("shift_events_above_pin") or 0
    revs = c.get("revisions") or 0
    rate = (shifts / revs) if revs else 0.0
    if len(classes) >= 3 or (("REFORM" in classes) and len(classes) >= 2):
        grade = "HIGH"
    elif len(classes) == 2 or (len(classes) == 1 and rate >= 0.25):
        grade = "MED"
    elif classes:
        grade = "LOW"
    else:
        grade = "none-measured"
    if e["kind"] == "anchor" and e.get("line") is None and not classes:
        grade = "LOW (structural)"
    rows.append({
        "id": eid, "kind": e["kind"], "file": e["file"], "line": e["line"],
        "classes": classes, "own": own, "grade": grade,
        "needle": needle_class(e), "shifts": shifts, "revs": revs,
        "rate": round(rate, 2),
        "renamed": rename_fired.get(eid, []),
        "opmut": e["file"].split("/")[-1] in OPMUT,
    })

rows.sort(key=lambda r: ({"HIGH": 0, "MED": 1, "LOW": 2,
                          "LOW (structural)": 3, "none-measured": 4}[r["grade"]],
                         r["id"]))
md = ["| entry | kind | pin | measured honest-edit fire classes | needle | hist insert-above-pin | grade |",
      "|---|---|---|---|---|---|---|"]
for r in rows:
    md.append("| `%s` | %s | %s:%s | %s | %s | %s/%s (%.2f) | **%s** |" %
              (r["id"], r["kind"], r["file"], r["line"],
               ", ".join(r["classes"]) or "-", r["needle"], r["shifts"],
               r["revs"], r["rate"], r["grade"]))
open(out, "w").write("\n".join(md) + "\n")
print("\n".join(md))
from collections import Counter
print("\ngrades:", dict(Counter(r["grade"] for r in rows)))
print("classes:", dict(Counter(c for r in rows for c in r["classes"])))
json.dump(rows, open(out.replace(".md", ".json"), "w"), indent=1)