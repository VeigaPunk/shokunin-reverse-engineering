#!/usr/bin/env python3
"""Probe: two prose clauses the frozen v2 counter does not actually bind.

1. "every arm cell names a token from the fixed vocabulary" -> substring match, so
   `uncommitted` passes.
2. "every row's trigger names a routed R45-CL<n> id" -> only the union is checked, so
   a row whose trigger names none passes.

Runs the frozen `attest.score` in-process against a synthetic SKILL text; no repo.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FROZEN = os.path.join(HERE, "frozen")
sys.path.insert(0, FROZEN)
import attest  # noqa: E402

ATTEST_BODY = open(os.path.join(FROZEN, "attest.py")).read()
FILES = {
    "tools/round-46/attest.py": ATTEST_BODY,
    "corpus/lessons/round-45.md": "lesson line\n" * 240,
    "plans/round-46-claims.md": attest.CLAIMS_BODY,
}
files = lambda p: FILES.get(p)  # noqa: E731


def run(tag, rows):
    skill = attest.skill_text(attest.good_block(rows=rows))
    code, rec = attest.score(skill, files, "r46", "v2", "probe", battery=None)
    print(json.dumps({"probe": tag, "exit": code, "rows": rec.get("rows"),
                      "failing": rec.get("failing")}, sort_keys=True))
    return code


base = list(attest.GOOD_ROWS)
run("genuine-13-rows", base)
run("extra-row-no-routed-id",
    base + [("a trigger naming no routed id", "off topic", "commit", "0")])
run("extra-row-arm-substring",
    base + [("R45-CL2", "ghost", "uncommitted", "0")])
run("extra-row-arm-zzz-control",
    base + [("R45-CL2", "ghost", "zzz", "0")])
