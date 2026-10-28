#!/usr/bin/env python3
"""RevC2Exempt — attack the R47-C2 exemption path of the frozen record.py.

Every panel calls the frozen instrument's own evaluate_text() with a card variant and
files read from the REAL lane at a fixed rev (read-only git). No lane byte is written.
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

S = "/fast/scratch/hyaku/kaidoku-r47/RevC2Exempt"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
INST = os.path.join(S, "inst-62e33f7d", "round-47", "record.py")
REV = "e856beb5"
BASE = "13a9e9e1"

spec = importlib.util.spec_from_file_location("rec47", INST)
rec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rec)
gate = rec.gate


def show(rev, path):
    return gate.show(LANE, rev, path)


CARD = show(REV, "SCORECARD.md")
if CARD is None:
    sys.exit("no card at rev")
FILES = lambda p: show(REV, p)  # noqa: E731

CORR_HEAD = "## Record corrections — round 47"
SEAT45 = "Wave 1: 40 seats; wave 2: 32 seats"
SEAT46 = "Waves: 40 + 40 = 80 seats."
WINDOW46 = "0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty"


def with_corr(card, lines):
    """Replace (or append) the corrections section body with `lines`."""
    head_at = card.find(CORR_HEAD)
    if head_at >= 0:
        card = card[:head_at]
    return card + CORR_HEAD + "\n\n" + "\n".join(lines) + "\n"


def strip_corr(card):
    head_at = card.find(CORR_HEAD)
    return card[:head_at] if head_at >= 0 else card


def run(name, card, expect, note="", battery=True):
    bat = None
    code, receipt = rec.evaluate_text(card, FILES, LANE, REV, battery=None)
    if battery and code in (0, 1):
        b = rec.run_battery(card, FILES, LANE, REV)
        code, receipt = rec.evaluate_text(card, FILES, LANE, REV, battery=b)
    out = {"panel": name, "expect_exit": expect, "exit": code,
           "ok": code == expect, "note": note,
           "failing": receipt.get("failing"),
           "mismatches": [{"class": m["class"], "key": m["key"],
                           "atom": m["atom"][:120]} for m in receipt.get("mismatches", [])],
           "exempted": [{"class": a["class"], "key": a["key"],
                         "atom": a["atom"][:120]} for a in receipt.get("exempted", [])],
           "corrections": receipt.get("corrections"),
           "corrections_bad": receipt.get("corrections_bad"),
           "battery": receipt.get("battery"),
           "card_sha256": hashlib.sha256(card.encode()).hexdigest()}
    print(json.dumps(out, indent=1))
    return out


C_TRUE_SEATS45 = ("- corrects seats round-45: 2 waves, 76 seats total — "
                  "`w2-dispatch.json` reports `counts.spawn 36`.")
C_TRUE_SEATS46 = "- corrects seats round-46: 2 waves, 80 seats total"
C_TRUE_WIN46 = ("- corrects window round-46: empty in 332f4884..58eb04b6 -- "
                "tools/round-46 plans/round-46-claims.md")
C_PATH = "- corrects path .ufo/waves/round-46/w1/R46W1CritC1: landed"

results = []

# ---- panel 0: the landed card, sanity -------------------------------------------------
results.append(run("P0-landed-card", CARD, 0, "instrument agrees with the lane's own landing"))

# ---- panel 1: assignment fixture — 3 exemptions hide 3 false atoms --------------------
false46 = CARD.replace(SEAT46, "Waves: 41 + 40 = 81 seats.")
assert false46 != CARD
p1 = with_corr(false46, [C_TRUE_SEATS45, C_TRUE_SEATS46, C_TRUE_WIN46])
results.append(run("P1-three-exemptions-three-false-atoms", p1, 0,
                   "round-45 still says 'wave 2: 32 seats', round-46 now says "
                   "'41 + 40 = 81', round-46 window still names <tip>: counter green"))

# ---- panel 1b: same, plus a FOURTH false atom the cap cannot cover --------------------
p1b = with_corr(false46, [C_TRUE_SEATS45, C_TRUE_SEATS46, C_TRUE_WIN46])
p1b = p1b.replace(SEAT46.replace("40", "41"),  # the falsified line, now present
                  "Waves: 41 + 40 = 81 seats. Receipt `.ufo/waves/round-46/w9/ghost.json`.")
p1b_card = p1b.replace(
    "Waves: 41 + 40 = 81 seats.",
    "Waves: 41 + 40 = 81 seats. Receipt `.ufo/waves/round-46/w9/ghost.json`.")
assert ".ufo/waves/round-46/w9/ghost.json" in p1b_card
results.append(run("P1b-fourth-false-atom-beyond-cap", p1b_card, 1,
                   "three exemptions spent, the fourth false atom must stay red"))

# ---- panel 2: scope shift — a new ## Round 47 heading drops round 45 from scope -------
r47 = ("\n## Round 47 — landing pad for the C2 window\n\nWaves: 75 + 0 = 75 seats. Base "
       "`13a9e9e1`. Control `.ufo/waves/round-47/controls/ctl-c2-0-do-nothing.json`. "
       "`git log 13a9e9e1..13a9e9e1 -- tools/round-47/` is empty.\n")
p2 = with_corr(CARD, [C_TRUE_SEATS45, C_TRUE_SEATS46, C_TRUE_WIN46]) + r47
results.append(run("P2-round47-heading-retains-seats45-correction", p2, 1,
                   "the landed seats-45 correction becomes a ghost the moment the round's "
                   "own section lands"))
p2b = with_corr(CARD, [C_TRUE_WIN46, C_PATH]) + r47
results.append(run("P2b-round47-heading-drops-seats45-correction", p2b, 0,
                   "round-45 'wave 2: 32 seats' is now outside the last-two window and is "
                   "never examined: no correction of it exists"))

# ---- panel 3: vacuous window pathspec -------------------------------------------------
p3 = with_corr(CARD, [C_TRUE_SEATS45,
                      "- corrects seats round-46: 2 waves, 80 seats total",
                      "- corrects window round-46: empty in 13a9e9e1..e856beb5 -- "
                      "corpus/no-such-tree/"])
results.append(run("P3-vacuous-window-pathspec", p3, 0,
                   "a pathspec matching no file re-derives 'empty' and exempts the <tip> atom"))
p3b = with_corr(CARD, [C_TRUE_SEATS45,
                       "- corrects seats round-46: 2 waves, 80 seats total",
                       "- corrects window round-46: empty in 13a9e9e1..e856beb5 -- "
                       ".ufo/waves/round-46"])
results.append(run("P3b-real-pathspec-nonempty-window", p3b, 1,
                   "control: the same window over a real pathspec is not empty"))
p3c = with_corr(CARD, [C_TRUE_SEATS45,
                       "- corrects seats round-46: 2 waves, 80 seats total",
                       "- corrects window round-46: empty in 13a9e9e1..e856beb5 -- "
                       ".ufo/waves/round-46."])
results.append(run("P3c-trailing-dot-pathspec", p3c, 0,
                   "a trailing period in the pathspec selects nothing -> 'empty' again"))

# ---- panel 4: one correction line, many false atoms (key collision) -------------------
multi = CARD.replace(SEAT45, "Wave 1: 40 seats; wave 2: 32 seats. Waves: 40 + 32 = 72 seats.")
multi = with_corr(multi, [C_TRUE_SEATS45,
                          "- corrects seats round-46: 2 waves, 80 seats total",
                          C_TRUE_WIN46])
results.append(run("P4-one-line-hides-three-false-seat-atoms", multi, 0,
                   "pair + sum atoms in round 45 share key '45': one line exempts both; "
                   "exempted counts atoms, the clause text says 'more atoms than the record "
                   "defects it names'"))
multi4 = CARD.replace(SEAT45, "Wave 1: 40 seats; wave 2: 32 seats. Waves: 40 + 32 = 72 seats. "
                              "Wave 1: 39 seats; wave 2: 36 seats.")
multi4 = with_corr(multi4, [C_TRUE_SEATS45,
                            "- corrects seats round-46: 2 waves, 80 seats total",
                            C_TRUE_WIN46])
results.append(run("P4b-four-false-seat-atoms", multi4, 1,
                   "cap holds: exempted 4 > 3"))

# ---- panel 5: corrections >= 2 is satisfiable by two no-ops ---------------------------
repaired = CARD.replace(SEAT45, "Wave 1: 40 seats; wave 2: 36 seats")
repaired = repaired.replace(WINDOW46, "332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md` is empty")
repaired_corr = with_corr(repaired, [C_TRUE_SEATS45,
                                     "- corrects window round-46: empty in "
                                     "332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md"])
results.append(run("P5-noop-corrections-after-in-place-repair", repaired_corr, 0,
                   "record edited in place, corrections exempt nothing, clause 3 satisfied"))
results.append(run("P5b-repaired-record-no-corrections", strip_corr(repaired), 1,
                   "a CLEAN record cannot pass: corrections 0 < 2"))

# ---- panel 6: battery is green while it scores nothing --------------------------------
base_card = show(BASE, "SCORECARD.md")
results.append(run("P6-base-card-no-corrections-section", base_card, 1,
                   "battery reports 3 forgeries with error 'no corrections section' and "
                   "forgeries_green 0: the battery clause is satisfied without scoring any"))

# ---- panel 7: class-wide placeholder exemption ---------------------------------------
two_win = CARD.replace(
    WINDOW46,
    WINDOW46 + ". `git log 13a9e9e1..<tip> -- corpus/knowledge/` is empty")
two_win = with_corr(two_win, [C_TRUE_SEATS45,
                              "- corrects seats round-46: 2 waves, 80 seats total",
                              "- corrects window round-46: empty in 13a9e9e1..e856beb5 -- "
                              "corpus/no-such-tree/"])
results.append(run("P7-one-window-line-exempts-every-placeholder", two_win, 0,
                   "a placeholder atom with NO concrete pair is exempted by any window "
                   "correction, whatever its pathspec"))

with open(os.path.join(S, "out", "attack-panels.json"), "w") as fh:
    json.dump({"rev": REV, "instrument_sha256":
               hashlib.sha256(open(INST, "rb").read()).hexdigest(),
               "panels": results}, fh, indent=1, sort_keys=True)
bad = [r["panel"] for r in results if not r["ok"]]
print(json.dumps({"panels": len(results), "unexpected": bad}, indent=1))
