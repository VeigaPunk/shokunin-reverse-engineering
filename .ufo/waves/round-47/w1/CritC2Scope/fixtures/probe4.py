#!/usr/bin/env python3
"""CritC2Scope probe 4: self-exclusion by heading string; in-scope atom inventory."""
import json
import os
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
out = {}

# inventory of what the counter actually derives, per in-scope section
inv = {}
for rnd, text in record.sections(CARD):
    rows = []
    for a in record.collect(text, rnd, files, LANE, REV):
        ok, detail = record.derive(a, files, LANE, REV, lambda r: record.dispatch_counts(files, r))
        rows.append({"class": a["class"], "key": str(a["key"])[:70],
                     "ok": ok, "detail": detail})
    inv["round-" + rnd] = rows
out["inventory"] = inv
out["axes_atoms"] = record.collect_axes(CARD)


def run(name, card):
    code, rec = record.evaluate_text(card, files, LANE, REV, battery=None)
    out[name] = {"exit": code, "sections": rec.get("sections"),
                 "atoms": rec.get("atoms"),
                 "mismatches": [m["atom"][:80] for m in rec.get("mismatches", [])],
                 "failing": rec.get("failing") or rec.get("reason")}
    return code, rec


# E12: the round writes its own section under a heading the pattern does not match.
self_excluded = CARD + (
    "\n## r47 — the two frozen counters, measured at `deadbee3`\n\n"
    "Waves: 900 + 900 = 1800 seats\n\n"
    "`git log deadbee3..deadbee3 -- plans/` is empty\n")
run("E12_self_excluded_heading_with_false_atoms", self_excluded)

# E13: same atoms under `## Round 47` — now in scope, and must go red.
in_scope = CARD + (
    "\n## Round 47 — the two frozen counters, measured at `deadbee3`\n\n"
    "Waves: 900 + 900 = 1800 seats\n\n"
    "`git log deadbee3..deadbee3 -- plans/` is empty\n")
run("E13_same_atoms_under_Round_47", in_scope)

print(json.dumps(out, indent=1))
