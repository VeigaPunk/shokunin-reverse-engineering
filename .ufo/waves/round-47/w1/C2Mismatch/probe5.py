#!/usr/bin/env python3
"""C2Mismatch probe 5: (a) the round-45 seats correction becomes a false exemption
once a `## Round 47` section is appended; (b) the seats sum shape counts a third wave."""
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
CORR = ("\n## Record corrections \u2014 round 47\n\n"
        "- corrects seats round-45: 2 waves, 76 seats total\n"
        "- corrects window round-46: empty in 332f4884..13a9e9e -- "
        "tools/round-46 plans/round-46-claims.md\n")


def green(t, corr=CORR):
    t = t.replace("Wave 1: 40 seats; wave 2: 32 seats", "Wave 1: 40 seats; wave 2: 36 seats")
    t = t.replace("0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty",
                  "332f4884..13a9e9e -- tools/round-46 plans/round-46-claims.md` is empty")
    t = t.replace("133/133 knowledge files mapped", "138/138 knowledge files mapped")
    t = t.replace("20/20 queue-drain rule blocks", "23/23 queue-drain rule blocks")
    return t + corr


ROUND47 = ("\n\n## Round 47 \u2014 the exactness matrix and the record counter\n\n"
           "Base `13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5`; freeze "
           "`5017e1f7299c3a812e87e7950148f54313dd279e`. Waves: 30 + 30 = 60 seats.\n")

CASES = []


def run(name, card, note, files=None):
    code, rec = record.evaluate_text(card, files or git_show, LANE, REV, battery=None)
    CASES.append({"case": name, "note": note, "exit": code,
                  "sections": rec.get("sections"),
                  "failing": rec.get("failing"),
                  "mismatches": [(m["class"], m["key"], m["derived"])
                                 for m in rec.get("mismatches", [])],
                  "exempted": [e["key"] for e in rec.get("exempted", [])],
                  "corrections": rec.get("corrections"),
                  "corrections_bad": [c["detail"] for c in rec.get("corrections_bad", [])]})
    return code, rec


run("I1-corrections-at-base-scope", green(CARD),
    "last two sections are 45 and 46; both corrections name live atoms")

# I2: append a round-47 section *before* the corrections section, as a landing would
withr47 = green(CARD.replace("\n## Record corrections \u2014 round 47", ROUND47 +
                             "\n## Record corrections \u2014 round 47"))
run("I2-corrections-after-round47", withr47,
    "the round-45 atom is out of the last-two window; its correction names nothing")
run("I2b-corrections-before-round47",
    green(CARD) + ROUND47 if False else green(CARD).rstrip() + "\n" + ROUND47,
    "round-47 section appended AFTER the corrections section: sections() sees 46 and 47")


# H4: a third wave for round 45; sum line inserted inside the round-45 section
def files3(p):
    if p == ".ufo/waves/round-45/w3-dispatch.json":
        return json.dumps({"counts": {"spawn": 9, "resume": 0, "total": 9}})
    return git_show(p)


base3 = green(CARD).replace("## Round 45 \u2014", "## Round 45 \u2014", 1)
head = "## Round 45 \u2014"
run("H4-sum-counts-wave3", base3.replace(head, head + " Waves: 40 + 36 = 85 seats.",
                                        1), "sum includes the third wave", files=files3)
run("H4-sum-missing-wave3", base3.replace(head, head + " Waves: 40 + 36 = 76 seats.",
                                          1), "sum omits the third wave", files=files3)
run("H4-pair-unaware-of-wave3", base3, "no atom names the third wave", files=files3)

print(json.dumps({"rev": REV, "card_sha256": hashlib.sha256(CARD.encode()).hexdigest(),
                  "cases": CASES}, indent=1))
