#!/usr/bin/env python3
"""Ninth batch: does C2 read the craft section (the claims' causal-separability claim)?"""
import json, os, sys
sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r47/MutExitCodes")
import drive2 as D
from drive2 import sh, put, commit, S, run, green_c2, LANE

W = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-47/w1/MutExitCodes/evidence"
d, base, land = green_c2()
run("c2-separability-control", ["python3", "-I", "-B",
                                os.path.join(d, "tools/round-47/record.py"),
                                "--root", d, "--rev", land, "--no-battery"], 0, "control")
dd = os.path.join(S, "sep-" + os.urandom(3).hex()); os.makedirs(dd)
sh(["git", "-C", dd, "clone", "-q", d, "."], check=True)
for k, v in (("user.email", "fx@round47"), ("user.name", "r47 fixture")):
    sh(["git", "-C", dd, "config", k, v], check=True)
skill = open(os.path.join(dd, "SKILL.md")).read()
craft_marker = "\n## Next\n"
new_rule = ("- **4. A new craft block.** body, see `corpus/lessons/round-46.md:1-5`.\n\n")
put(dd, {"SKILL.md": skill.replace(craft_marker, "\n" + new_rule + "## Next\n", 1)})
rev = commit(dd, "one more craft block (C1's surface), card untouched")
out = os.path.join(dd, "receipt.json")
rec = run("c2-separability-craft-block-added", [
    "python3", "-I", "-B", os.path.join(dd, "tools/round-47/record.py"), "--root", dd,
    "--rev", rev, "--no-battery", "--json-out", out], 0,
    "claims: C2 'never reads the craft section'")
import shutil
shutil.copy(out, os.path.join(W, "c2-separability-craft-block-added.json"))
print(json.dumps({"card_untouched": True, "skill_change": "one craft block appended"}))
with open(os.path.join(S, "receipts9.jsonl"), "w") as fh:
    for x in D.OUT: fh.write(json.dumps(x) + "\n")
