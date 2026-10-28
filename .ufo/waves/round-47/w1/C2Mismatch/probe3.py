#!/usr/bin/env python3
"""C2Mismatch probe 3: inert corrections with real keys, block-24 depth sensitivity,
three-wave seats omission."""
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
INERT = ("\n## Record corrections \u2014 round 47\n\n"
         "- corrects path .ufo/waves/round-45/l1/scores/c1-at-A2.json: present at the revision\n"
         "- corrects path .ufo/waves/round-45/l1/scores/c2-at-A3.json: present at the revision\n")

CASES = []


def green(t):
    t = t.replace(*SEATS_FIX).replace(*WIN_FIX)
    t = t.replace("133/133 knowledge files mapped", "138/138 knowledge files mapped")
    t = t.replace("20/20 queue-drain rule blocks", "23/23 queue-drain rule blocks")
    return t


def run(name, card, note, files=None):
    code, rec = record.evaluate_text(card, files or git_show, LANE, REV, battery=None)
    CASES.append({"case": name, "note": note, "exit": code,
                  "failing": rec.get("failing"),
                  "mismatches": [(m["class"], m["key"], m["atom"][:60],
                                  m["derived"]) for m in rec.get("mismatches", [])],
                  "exempted": rec.get("exempted"),
                  "corrections": rec.get("corrections"),
                  "corrections_bad": [c["detail"] for c in rec.get("corrections_bad", [])],
                  "atoms_by_class": rec.get("atoms_by_class")})
    return code, rec


# D3: two true corrections that exempt only already-green path atoms
run("D3-inert-corrections-real-keys", green(CARD) + INERT,
    "the two 'corrections' exempt atoms that were never false; the repairs are in-place")

# E3: insert a synthetic rule block 24 at the end of the craft section
skill = git_show("SKILL.md")
marker = "\n## Config custody for live-probe rounds (SOP)"
assert marker in skill
block = ("- **24. Exactness table.** <!-- exactness-table v3 --> Synthetic block, inserted "
         "only to measure the depth observable; cites `tools/round-47/exact.py:1-12` "
         "and `corpus/lessons/round-46.md:1-20`.\n")
skill24 = skill.replace(marker, "\n" + block + marker, 1)


def files24(p):
    return skill24 if p == "SKILL.md" else git_show(p)


code, rec = run("E3-block24-depth", green(CARD), "block 24 present at the measured rev",
                files=files24)
CASES[-1]["depth_derived"] = [m["derived"] for m in rec.get("mismatches", [])
                              if m["class"] == "axes"]
run("E3-baseline-depth", green(CARD), "no block 24")


# H3: a three-wave round — the pair shape never reads wave 3
def files3(p):
    if p == ".ufo/waves/round-45/w3-dispatch.json":
        return json.dumps({"counts": {"spawn": 9, "resume": 0, "total": 9}})
    return git_show(p)


code, rec = run("H3-pair-ignores-wave3", green(CARD), "round-45 has a wave 3 of 9 seats",
                files=files3)
code, rec = run("H3-sum-includes-wave3",
                green(CARD).replace("Waves: 40 + 40 = 80 seats", "Waves: 40 + 36 = 76 seats"),
                "sum shape adds wave 3 into C", files=files3)
CASES[-1]["seats_derived"] = [m["derived"] for m in rec.get("mismatches", [])
                              if m["class"] == "seats"]

print(json.dumps({"rev": REV, "card_sha256": hashlib.sha256(CARD.encode()).hexdigest(),
                  "skill_sha256": hashlib.sha256(skill.encode()).hexdigest(),
                  "cases": CASES}, indent=1))
