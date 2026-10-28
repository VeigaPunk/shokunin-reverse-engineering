#!/usr/bin/env python3
"""CritBattery: final C2 attack set, dynamic string targeting. Read-only on the lane."""
import json
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, LANE + "/tools/round-47")
sys.path.insert(0, LANE + "/tools/round-46")
import gate  # noqa: E402
import record  # noqa: E402

REV = sys.argv[1]
tip = gate.resolve(LANE, REV)
card = gate.show(LANE, tip, "SCORECARD.md")
files = lambda p: gate.show(LANE, tip, p)  # noqa: E731


def run(name, text, battery=False):
    code, rec = record.evaluate_text(text, files, LANE, tip, battery=None)
    if battery:
        bat = record.run_battery(text, files, LANE, tip, root_repo=LANE)
        code, rec = record.evaluate_text(text, files, LANE, tip, battery=bat)
    print(json.dumps({
        "name": name, "changed": text != card, "exit": code,
        "failing": rec.get("failing"),
        "mismatches": [m["class"] + "/" + m["key"] for m in rec.get("mismatches") or []],
        "corrections": rec.get("corrections"),
        "corrections_bad": len(rec.get("corrections_bad") or []),
        "exempted": [e["class"] + "/" + e["key"] for e in rec.get("exempted") or []],
        "battery": rec.get("battery") and {k: v for k, v in rec["battery"].items()
                                           if k != "fixtures"}}))


print(json.dumps({"rev": tip,
                  "corr_lines": card.count("\n- corrects "),
                  "parsed": len(record.corrections(card)[0])}))
run("genuine", card)

# 1. seats PAIR laundered: the wave split is false, the correction names only the total
m = re.search(r"Wave 1: (\d+) seats; wave 2: (\d+) seats", card)
a, b = int(m.group(1)), int(m.group(2))
t = card[:m.start()] + f"Wave 1: {a + 15} seats; wave 2: {b - 15} seats" + card[m.end():]
run("launder-seats-pair", t)

# 2. window atom's base revision and pathspec replaced; correction is another window
m = re.search(r"([0-9a-f]{7,40})\.\.<tip> -- [A-Za-z0-9._/ -]+", card)
t = card[:m.start()] + "13a9e9e1..<tip> -- SKILL.md" + card[m.end():]
run("launder-window-base-pathspec", t)

# 3. false axes corrections (a class CORR cannot parse)
t = card.replace("corrects axes coverage: 138/138", "corrects axes coverage: 999/999", 1)
run("false-axes-correction-coverage", t)
t = card.replace("corrects axes depth: 24/24", "corrects axes depth: 999/999", 1)
run("false-axes-correction-depth", t)

# 4. the after-cell's measured revision swapped for another resolving ancestor
cell = re.findall(r"\| `([0-9a-f]{7,40})` \|", card)
print(json.dumps({"measured_at_candidates": cell}))
if cell:
    t = card.replace("| `%s` |" % cell[-1], "| `13a9e9e1` |", 1)
    run("after-cell-measured-at-swapped", t)

# 5. kill rule: the corrections section deleted
t = card.split(record.CORR_HEAD)[0]
run("corrections-section-deleted", t)

# 6. a correction that states the split the atom actually got wrong (the honest repair shape)
m = re.search(r"- corrects seats round-45: (\d+) waves, (\d+) seats total", card)
if m:
    t = card.replace(m.group(0),
                     "- corrects seats round-45: wave 1: 55 seats; wave 2: 17 seats", 1)
    run("correction-states-the-split", t)

# 7. battery with the genuine card, for the record
run("genuine-battery", card, battery=True)
