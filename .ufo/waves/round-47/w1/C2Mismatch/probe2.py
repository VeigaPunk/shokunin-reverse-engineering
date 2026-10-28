#!/usr/bin/env python3
"""C2Mismatch probe 2: decisive variants for the frozen R47-C2 predicate."""
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


def git_show(p):
    r = subprocess.run(["git", "-C", LANE, "show", f"{REV}:{p}"],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


CARD = git_show("SCORECARD.md")
SEATS_FIX = ("Wave 1: 40 seats; wave 2: 32 seats", "Wave 1: 40 seats; wave 2: 36 seats")
WIN_FIX = ("0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty",
           "332f4884..13a9e9e -- tools/round-46 plans/round-46-claims.md` is empty")
CORR2 = ("\n## Record corrections \u2014 round 47\n\n"
         "- corrects seats round-45: 2 waves, 76 seats total\n"
         "- corrects window round-46: empty in 332f4884..13a9e9e -- "
         "tools/round-46 plans/round-46-claims.md\n")


def green(axes_cov="138/138", axes_dep="23/23", corrections=CORR2):
    t = CARD.replace(*SEATS_FIX).replace(*WIN_FIX)
    t = t.replace("133/133 knowledge files mapped", axes_cov + " knowledge files mapped")
    t = t.replace("20/20 queue-drain rule blocks", axes_dep + " queue-drain rule blocks")
    return t + corrections


CASES = []


def run(name, card, note, files=None):
    fs = files or git_show
    code, rec = record.evaluate_text(card, fs, LANE, REV, battery=None)
    CASES.append({"case": name, "note": note, "exit": code,
                  "failing": rec.get("failing"),
                  "mismatches": [(m["class"], m["key"], m["atom"][:70])
                                 for m in rec.get("mismatches", [])],
                  "exempted": len(rec.get("exempted", [])),
                  "corrections": rec.get("corrections"),
                  "corrections_bad": [c["detail"] for c in rec.get("corrections_bad", [])],
                  "atoms_by_class": rec.get("atoms_by_class")})
    return code, rec


run("A-green-baseline", green(), "in-place fixes + the two documented corrections")

# B2: the documented axes correction is the only repair for a stale depth row
stale = CARD.replace(*SEATS_FIX).replace(*WIN_FIX).replace("133/133", "138/138")
run("B2-axes-correction-dropped", stale + CORR2 + "- corrects axes depth: 20/20\n",
    "claims file says an axes correction may state <resolved>/<total>; CORR regex has no 'axes'")

# C2: delete the coverage row outright, everything else green
out = []
for line in green().splitlines(True):
    if line.lstrip().startswith("| coverage |") and "138/138" in line:
        continue
    out.append(line)
run("C2-coverage-row-deleted-green", "".join(out),
    "no coverage atom, axes class still non-empty -> the vacuous repair scores met")

# D2: two true but inert path corrections stand in for the two repairs
inert = ("\n## Record corrections \u2014 round 47\n\n"
         "- corrects path .ufo/waves/round-45/r45-w2-results.json: present at the revision\n"
         "- corrects path .ufo/waves/round-45/r45-w1-results.json: present at the revision\n")
run("D2-inert-corrections", green(corrections=inert),
    "corrections exempt two already-green path atoms; the real repairs are in-place edits")

# E2: block 24 landing changes the depth observable
skill = git_show("SKILL.md")
tail = ("\n- **24. Exactness table.** <!-- exactness-table v3 --> A synthetic block used "
        "only to measure the depth observable's sensitivity; its citation is "
        "`tools/round-47/record.py:1-10`.\n")
skill24 = skill.rstrip("\n") + "\n" + tail


def files24(p):
    if p == "SKILL.md":
        return skill24
    return git_show(p)


code, rec = run("E2-depth-sensitivity", green(axes_dep="23/23"), "block 24 appended",
                files=files24)
code23, rec23 = run("E2-depth-baseline", green(axes_dep="23/23"), "no block 24")
depth_atom = [m for m in rec["mismatches"] if m["class"] == "axes"]
CASES[-2]["depth_derived"] = depth_atom[0]["derived"] if depth_atom else None
CASES[-1]["depth_derived"] = None

# F2: the built-in battery on a green card
bat = record.run_battery(green(), git_show, LANE, REV)
CASES.append({"case": "F2-battery-on-green", "battery": bat})

# G2: the battery on the recorded before state (no corrections section)
bat_before = record.run_battery(CARD, git_show, LANE, REV)
CASES.append({"case": "G2-battery-on-before", "battery": bat_before})

print(json.dumps({"rev": REV, "card_sha256": hashlib.sha256(CARD.encode()).hexdigest(),
                  "cases": CASES}, indent=1))
