#!/usr/bin/env python3
"""C2Mismatch probe 4: inert corrections that clear the counter; the seats sum shape
vs a three-wave round."""
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
INERT = ("\n## Record corrections \u2014 round 47\n\n"
         "- corrects path .ufo/waves/round-45/l1/scores/c1-at-A2.json: present at the revision\n"
         "- corrects path .ufo/waves/round-45/l1/scores/c2-at-1f4b27f8.json: "
         "present at the revision\n")


def green(t):
    t = t.replace("Wave 1: 40 seats; wave 2: 32 seats", "Wave 1: 40 seats; wave 2: 36 seats")
    t = t.replace("0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty",
                  "332f4884..13a9e9e -- tools/round-46 plans/round-46-claims.md` is empty")
    t = t.replace("133/133 knowledge files mapped", "138/138 knowledge files mapped")
    t = t.replace("20/20 queue-drain rule blocks", "23/23 queue-drain rule blocks")
    return t


CASES = []


def run(name, card, note, files=None):
    code, rec = record.evaluate_text(card, files or git_show, LANE, REV, battery=None)
    CASES.append({"case": name, "note": note, "exit": code,
                  "failing": rec.get("failing"),
                  "mismatches": [(m["class"], m["key"], m["derived"])
                                 for m in rec.get("mismatches", [])],
                  "exempted": [e["key"] for e in rec.get("exempted", [])],
                  "corrections": rec.get("corrections"),
                  "corrections_bad": [c["detail"] for c in rec.get("corrections_bad", [])]})
    return code, rec


run("D4-inert-corrections-real-keys", green(CARD) + INERT,
    "two true corrections that exempt only atoms which were never false")

# H4: round-45 gains a wave 3 of nine seats; the pair shape cannot see it,
# the sum shape counts it.
def files3(p):
    if p == ".ufo/waves/round-45/w3-dispatch.json":
        return json.dumps({"counts": {"spawn": 9, "resume": 0, "total": 9}})
    return git_show(p)


run("H4-pair-unaware-of-wave3", green(CARD) + INERT,
    "a third wave exists and no atom mentions it", files=files3)
sumline = "\nWaves: 40 + 36 = 85 seats.\n"
run("H4-sum-counts-wave3", green(CARD).replace("## Round 45", "## Round 45" , 1) + sumline + INERT,
    "the sum shape adds wave 3 into C", files=files3)
run("H4-sum-missing-wave3", green(CARD) + "\nWaves: 40 + 36 = 76 seats.\n" + INERT,
    "the sum shape rejects a total that omits wave 3", files=files3)

print(json.dumps({"rev": REV, "card_sha256": hashlib.sha256(CARD.encode()).hexdigest(),
                  "cases": CASES}, indent=1))
