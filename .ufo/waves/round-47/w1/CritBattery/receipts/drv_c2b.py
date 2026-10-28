#!/usr/bin/env python3
"""CritBattery: laundering attacks on the C2 counter (record.py), scored by record.evaluate_text."""
import json
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, LANE + "/tools/round-47")
sys.path.insert(0, LANE + "/tools/round-46")
import gate  # noqa: E402
import record  # noqa: E402

REV = sys.argv[1] if len(sys.argv) > 1 else "1e2c3102"
tip = gate.resolve(LANE, REV)
card = gate.show(LANE, tip, "SCORECARD.md")
files = lambda p: gate.show(LANE, tip, p)  # noqa: E731
BAT = "--battery" in sys.argv


def run(name, text, battery=False):
    code, rec = record.evaluate_text(text, files, LANE, tip,
                                    battery=None)
    if battery:
        code, rec = record.evaluate_text(
            text, files, LANE, tip,
            battery=record.run_battery(text, files, LANE, tip, root_repo=LANE))
    print(json.dumps({"name": name, "changed": text != card, "exit": code,
                      "failing": rec.get("failing"),
                      "mismatches": [m["class"] + "/" + m["key"] for m in rec.get("mismatches") or []],
                      "corrections_bad": rec.get("corrections_bad"),
                      "exempted": [e["class"] + "/" + e["key"] for e in rec.get("exempted") or []],
                      "battery": rec.get("battery") and {
                          "n": rec["battery"]["correction_forgeries"],
                          "green": rec["battery"]["forgeries_green"]}}))


# 0. control
run("genuine", card)

# 1. seats PAIR laundered by the true seats correction of the same round
t = card.replace("Wave 1: 40 seats; wave 2: 32 seats", "Wave 1: 55 seats; wave 2: 17 seats", 1)
run("launder-seats-pair-55-17", t)

# 1b. same, as a forged correction that is true but does not state the split
t1b = card.replace("Wave 1: 40 seats; wave 2: 32 seats", "Wave 1: 55 seats; wave 2: 17 seats", 1)
t1b = t1b.replace("- corrects seats round-45: 2 waves, 76 seats total",
                  "- corrects seats round-45: 2 waves, 76 seats total", 1)
run("launder-seats-pair-with-true-correction", t1b)

# 2. round-46 sum atom falsified, exempted by a NEW true seats correction for round 46
t2 = card.replace("Waves: 40 + 40 = 80 seats", "Waves: 60 + 20 = 80 seats", 1)
t2 = t2.replace("## Record corrections \u2014 round 47\n\n",
                "## Record corrections \u2014 round 47\n\n- corrects seats round-46: 2 waves, 80 seats total\n", 1)
run("launder-seats-sum-60-20-new-correction", t2)

# 3. axes head falsified, exempted by the existing true axes correction
t3 = card.replace("| coverage | 10 \u2192 10 | 138/138", "| coverage | 10 \u2192 10 | 12/138", 1)
if t3 == card:
    import re
    m = re.search(r"(?m)^\|\s*coverage\s*\|.*$", card)
    print(json.dumps({"axes_row": m.group(0)[:300] if m else None}))
    t3 = card[:m.start()] + m.group(0).replace("138/138", "12/138", 1) + card[m.end():]
run("launder-axes-coverage-12-138", t3)

# 4. window atom's concrete base and pathspec falsified; correction is about another window
t4 = card.replace(
    "0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty at every measurement above.",
    "13a9e9e1..<tip> -- SKILL.md` is empty at every measurement above.", 1)
run("launder-window-base-and-pathspec", t4)

# 5. the measured-at revision of the round-47 after-cell replaced by the base revision
t5 = card.replace("| `1e2c310295` |", "| `13a9e9e1` |", 1)
print(json.dumps({"measured_at_replaced": t5 != card}))
run("after-cell-measured-at-swapped-to-base", t5)

# 6. a before-cell revision swapped for another resolving ancestor
t6 = card.replace("`5017e1f7` (plan + both counters)", "`13a9e9e1` (plan + both counters)", 1)
print(json.dumps({"freeze_token_replaced": t6 != card}))
run("freeze-series-token-swapped-to-base", t6)

# 7. NON-EMPTY window forgery redirected: does run_battery still target the correction?
t7 = card.replace(
    "0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty at every measurement above.",
    "0425224..58eb04b6 -- tools/round-46 plans/round-46-claims.md` is empty in"
    " 0425224..58eb04b6 at every measurement above.", 1)
run("battery-window-target-fragility", t7, battery=True)
run("genuine-with-battery", card, battery=True)
