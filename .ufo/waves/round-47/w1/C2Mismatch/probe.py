#!/usr/bin/env python3
"""C2Mismatch probe: run the frozen R47-C2 predicate (record.evaluate_text) over
forged/card variants of the SCORECARD at 13a9e9e. Read-only on the lane."""
import hashlib
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = "13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5"
sys.path.insert(0, os.path.join(LANE, "tools", "round-47"))
sys.path.insert(0, os.path.join(LANE, "tools", "round-46"))
import record  # noqa: E402


def show(p):
    r = subprocess.run(["git", "-C", LANE, "show", f"{REV}:{p}"],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


CARD = show("SCORECARD.md")
assert CARD

# a card that is already green except for the two axes rows: fix the record text in
# place and add the two corrections the claims file documents.
def base_green():
    t = CARD
    t = t.replace("Wave 1: 40 seats; wave 2: 32 seats", "Wave 1: 40 seats; wave 2: 36 seats")
    t = t.replace("0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty",
                  "332f4884..13a9e9e -- tools/round-46 plans/round-46-claims.md` is empty")
    t += ("\n## Record corrections \u2014 round 47\n\n"
          "- corrects seats round-45: 2 waves, 76 seats total\n"
          "- corrects window round-46: empty in 332f4884..13a9e9e -- tools/round-46 plans/round-46-claims.md\n")
    return t


def fix_axes(t, cov="138/138", dep="23/23"):
    t = t.replace("133/133 knowledge files mapped", cov + " knowledge files mapped")
    t = t.replace("20/20 queue-drain rule blocks", dep + " queue-drain rule blocks")
    return t


def drop_coverage_row(t):
    out = []
    for line in t.splitlines(True):
        if line.lstrip().startswith("| coverage |") and "133/133" in line:
            continue
        out.append(line)
    return "".join(out)


def add_axes_correction(t):
    return t + ("- corrects axes depth: 20/20\n")


CASES = []


def run(name, card, note):
    code, rec = record.evaluate_text(card, show, LANE, REV, battery=None)
    CASES.append({"case": name, "note": note, "exit": code,
                  "failing": rec.get("failing"),
                  "mismatch_classes": [(m["class"], m["key"]) for m in rec.get("mismatches", [])],
                  "exempted": len(rec.get("exempted", [])),
                  "corrections": rec.get("corrections"),
                  "atoms_by_class": rec.get("atoms_by_class")})
    return code


g = fix_axes(base_green())
run("A-genuine-repaired", g, "all atoms true, both documented corrections")
run("B-axes-correction-unparseable", g + "- corrects axes depth: 20/20\n",
    "claims file documents an axes correction; CORR regex omits 'axes'")
t = base_green()
t = t.replace("138/138", "133/133").replace("23/23", "20/20")
run("C-coverage-row-deleted", drop_coverage_row(t),
    "coverage row removed: axes class still has 1 atom, clause 'classes' passes")
run("D-pathspec-typo", fix_axes(CARD.replace("Wave 1: 40 seats; wave 2: 32 seats",
                                             "Wave 1: 40 seats; wave 2: 36 seats")
                                .replace("0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty",
                                         "0425224..13a9e9e -- tools/round-46x plans/round-46-claims.md` is empty")
                                .replace("133/133", "138/138").replace("20/20", "23/23")
                                + "\n## Record corrections \u2014 round 47\n\n"
                                  "- corrects seats round-45: 2 waves, 76 seats total\n"
                                  "- corrects window round-46: empty in 0425224..13a9e9e -- tools/round-46x plans/round-46-claims.md\n"),
    "window over a pathspec no commit touches scores green although tools/round-46 changed")
run("E-reversed-window", fix_axes(CARD.replace("Wave 1: 40 seats; wave 2: 32 seats",
                                               "Wave 1: 40 seats; wave 2: 36 seats")
                                  .replace("0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty",
                                           "13a9e9e..7bf33e31 -- tools/round-46 plans/round-46-claims.md` is empty")
                                  .replace("133/133", "138/138").replace("20/20", "23/23")
                                  + "\n## Record corrections \u2014 round 47\n\n"
                                    "- corrects seats round-45: 2 waves, 76 seats total\n"
                                    "- corrects window round-46: empty in 13a9e9e..7bf33e31 -- tools/round-46 plans/round-46-claims.md\n"),
    "descendant..ancestor window is vacuously empty")
run("F-placeholder-window-invisible", fix_axes(CARD.replace("Wave 1: 40 seats; wave 2: 32 seats",
                                                            "Wave 1: 40 seats; wave 2: 36 seats")
                                               .replace("133/133", "138/138").replace("20/20", "23/23")
                                               + "\n## Record corrections \u2014 round 47\n\n"
                                                 "- corrects seats round-45: 2 waves, 76 seats total\n"
                                                 "- corrects window round-46: empty in 332f4884..13a9e9e -- tools/round-46 plans/round-46-claims.md\n"),
    "placeholder window atom has pair None so any window correction exempts it")
run("G-three-waves-unclaimed", fix_axes(CARD.replace("Wave 1: 40 seats; wave 2: 32 seats",
                                                    "Wave 1: 40 seats; wave 2: 36 seats; wave 3: 9 seats")
                                       .replace("133/133", "138/138").replace("20/20", "23/23")
                                       + "\n## Record corrections \u2014 round 47\n\n"
                                         "- corrects seats round-45: 2 waves, 76 seats total\n"
                                         "- corrects window round-46: empty in 332f4884..13a9e9e -- tools/round-46 plans/round-46-claims.md\n"),
    "a wave-3 seat claim matches no regex and no atom")

out = {"rev": REV, "card_sha256": hashlib.sha256(CARD.encode()).hexdigest(),
       "cases": CASES}
print(json.dumps(out, indent=1))
