#!/usr/bin/env python3
"""RevC2Exempt — second panel set: clause-level (battery=None) truth plus battery shape."""
import hashlib
import importlib.util
import json
import os

S = "/fast/scratch/hyaku/kaidoku-r47/RevC2Exempt"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
INST = os.path.join(S, "inst-62e33f7d", "round-47", "record.py")
REV = "e856beb5"

spec = importlib.util.spec_from_file_location("rec47b", INST)
rec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rec)

CARD = rec.gate.show(LANE, REV, "SCORECARD.md")
FILES = lambda p: rec.gate.show(LANE, REV, p)  # noqa: E731
CORR_HEAD = "## Record corrections — round 47"
SEAT45 = "Wave 1: 40 seats; wave 2: 32 seats"
WINDOW46 = "0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty"


def with_corr(card, lines):
    at = card.find(CORR_HEAD)
    return (card[:at] if at >= 0 else card) + CORR_HEAD + "\n\n" + "\n".join(lines) + "\n"


def run(name, card, expect, note, battery=False):
    code, receipt = rec.evaluate_text(card, FILES, LANE, REV, battery=None)
    if battery and code in (0, 1):
        b = rec.run_battery(card, FILES, LANE, REV)
        code, receipt = rec.evaluate_text(card, FILES, LANE, REV, battery=b)
    out = {"panel": name, "battery": battery, "exit": code, "expect_exit": expect,
           "ok": code == expect, "note": note, "failing": receipt.get("failing"),
           "mismatches": [{"class": m["class"], "key": m["key"], "atom": m["atom"][:120]}
                          for m in receipt.get("mismatches", [])],
           "exempted": [{"class": a["class"], "key": a["key"]} for a in receipt.get("exempted", [])],
           "corrections": receipt.get("corrections"),
           "corrections_bad": [b["detail"] if isinstance(b, dict) else b
                               for b in (receipt.get("corrections_bad") or [])],
           "card_sha256": hashlib.sha256(card.encode()).hexdigest()}
    print(json.dumps(out, indent=1))
    return out


C45 = "- corrects seats round-45: 2 waves, 76 seats total"
C46 = "- corrects seats round-46: 2 waves, 80 seats total"
CW = ("- corrects window round-46: empty in 332f4884..58eb04b6 -- "
      "tools/round-46 plans/round-46-claims.md")
out = []

# clause-level vacuous pathspec: the exemption is granted on a window over a path that
# never existed, so the atom's own pathspec is never re-derived.
out.append(run("Q1-vacuous-pathspec-clause-level",
               with_corr(CARD, [C45, C46,
                                "- corrects window round-46: empty in 13a9e9e1..e856beb5 -- "
                                "corpus/no-such-tree/"]),
               0, "clauses 1-5 green on a vacuous pathspec"))
out.append(run("Q2-trailing-dot-pathspec-clause-level",
               with_corr(CARD, [C45, C46,
                                "- corrects window round-46: empty in 13a9e9e1..e856beb5 -- "
                                ".ufo/waves/round-46."]),
               0, "a trailing period makes the pathspec select nothing -> 'empty'"))
out.append(run("Q3-control-real-pathspec-nonempty-window",
               with_corr(CARD, [C45, C46,
                                "- corrects window round-46: empty in 13a9e9e1..e856beb5 -- "
                                ".ufo/waves/round-47"]),
               1, "control: real pathspec in the same window is not empty"))
# content-blind seats exemption: the atom states 90, the correction states 76, still green
out.append(run("Q4-content-blind-seats-exemption",
               with_corr(CARD.replace(SEAT45, "Wave 1: 40 seats; wave 2: 90 seats"),
                         [C45, CW]),
               0, "the exemption never compares the correction to the atom's own numbers"))
# forced shape: only path/rev corrections -> every battery forgery is a no-op -> clause 6 red
repaired = CARD.replace(SEAT45, "Wave 1: 40 seats; wave 2: 36 seats")
repaired = repaired.replace(WINDOW46,
                            "332f4884..58eb04b6 -- tools/round-46 "
                            "plans/round-46-claims.md` is empty")
out.append(run("Q5-path-only-corrections-battery",
               with_corr(repaired, [
                   "- corrects path .ufo/waves/round-46/controls/ctl-c1-0-do-nothing.json: landed",
                   "- corrects rev 781e19ae: measured"]),
               1, "forced shape: no seats line and no window line makes two forgeries no-ops",
               battery=True))
out.append(run("Q6-path-only-corrections-clause-level",
               with_corr(repaired, [
                   "- corrects path .ufo/waves/round-46/controls/ctl-c1-0-do-nothing.json: landed",
                   "- corrects rev 781e19ae: measured"]),
               0, "clauses 1-5 are green for the same card: only the battery is red"))
# the landed card's own battery, for reference
out.append(run("Q7-landed-card-battery", CARD, 0, "landed card through the full CLI path",
               battery=True))

with open(os.path.join(S, "out", "attack-panels2.json"), "w") as fh:
    json.dump({"rev": REV, "panels": out}, fh, indent=1, sort_keys=True)
print(json.dumps({"unexpected": [p["panel"] for p in out if not p["ok"]]}, indent=1))
