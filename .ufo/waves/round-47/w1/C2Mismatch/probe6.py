#!/usr/bin/env python3
"""C2Mismatch probe 6: at the current landing rev, which correction classes are
actually parsed, and does a fabricated line change the verdict?"""
import hashlib
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, os.path.join(LANE, "tools", "round-47"))
sys.path.insert(0, os.path.join(LANE, "tools", "round-46"))
import record  # noqa: E402

REV = subprocess.run(["git", "-C", LANE, "rev-parse", "HEAD"],
                     capture_output=True, text=True).stdout.strip()


def show(p):
    r = subprocess.run(["git", "-C", LANE, "show", f"{REV}:{p}"],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


CARD = show("SCORECARD.md")
CORR, BODY = record.corrections(CARD)
ALL = [l for l in CARD.splitlines() if l.startswith("- corrects ")]
PARSED = [l for l in ALL if record.CORR.match(l.strip())]
DROPPED = [l for l in ALL if not record.CORR.match(l.strip())]
CASES = []


def run(name, extra, note):
    t = CARD
    if extra:
        t = CARD.replace("\n## Round 47 \u2014", "\n" + extra + "\n## Round 47 \u2014", 1)
    code, rec = record.evaluate_text(t, show, LANE, REV, battery=None)
    CASES.append({"case": name, "note": note, "exit": code,
                  "corrections": rec.get("corrections"),
                  "corrections_bad": [c["detail"] if isinstance(c["detail"], str)
                                      else c["detail"] for c in rec.get("corrections_bad", [])],
                  "mismatches": [(m["class"], m["key"]) for m in rec.get("mismatches", [])],
                  "exempted": [e["key"] for e in rec.get("exempted", [])]})


run("landed-as-committed", "", "the card exactly as committed at this rev")
run("fabricated-axes-depth", "- corrects axes depth: 99/99 \u2014 fabricated\n",
    "an axes correction line is unparseable, so a false one costs nothing")
run("fabricated-axes-coverage", "- corrects axes coverage: 1/1 \u2014 fabricated\n",
    "same for coverage")
run("fabricated-path-statement",
    "- corrects path .ufo/waves/round-46/l1/scores/c1-at-F4.json: fabricated, never checked\n",
    "the path branch ignores the statement, so any text passes")
run("fabricated-seats-total", "- corrects seats round-47: 9 waves, 999 seats total\n",
    "the seats branch is real: a false total is red")

print(json.dumps({"rev": REV, "card_sha256": hashlib.sha256(CARD.encode()).hexdigest(),
                  "corrections_parsed": len(CORR), "every_corrects_line": ALL,
                  "lines_matching_CORR": len(PARSED),
                  "unparsed_lines": DROPPED, "cases": CASES}, indent=1))
