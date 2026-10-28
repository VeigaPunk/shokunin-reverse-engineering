#!/usr/bin/env python3
"""Collect full receipts (not truncated) into the seat dir for the report's key rows."""
import json, os, shutil, subprocess, sys
sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r47/MutExitCodes")
import drive2 as D
from drive2 import sh, put, commit, S, run, LANE, green_c2

W = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-47/w1/MutExitCodes"
EV = os.path.join(W, "evidence")
os.makedirs(EV, exist_ok=True)
HEAD = sh(["git", "-C", LANE, "rev-parse", "HEAD"]).stdout.strip()
A6 = "f54b3b6de9085d3db449ed5d0916296cb29c1f6d"
A2 = "62e33f7dd75c8e3285967b26419842c106f6c965"
F1 = "5017e1f7299c3a812e87e7950148f54313dd279e"
BASE = "13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5"
C1 = os.path.join(LANE, "tools/round-47/exact.py")
C2 = os.path.join(LANE, "tools/round-47/record.py")

def lane(name, args, expect):
    out = os.path.join(EV, name + ".json")
    rec = run("evidence-" + name, ["python3", "-I", "-B"] + args + ["--json-out", out], expect)
    return rec

lane("c1-freeze-A2-at-HEAD", [C1, "--root", LANE, "--freeze", A2, "--rev", HEAD, "--no-battery"], 2)
lane("c1-freeze-F1-at-HEAD", [C1, "--root", LANE, "--freeze", F1, "--rev", HEAD, "--no-battery"], 2)
lane("c1-freeze-A6-at-HEAD", [C1, "--root", LANE, "--freeze", A6, "--rev", HEAD, "--no-battery"], 0)
lane("c1-freeze-A6-at-HEAD-battery", [C1, "--root", LANE, "--freeze", A6, "--rev", HEAD], 0)
lane("c1-freeze-F1-at-F1", [C1, "--root", LANE, "--freeze", F1, "--rev", F1, "--no-battery"], 1)
lane("c2-at-HEAD-battery", [C2, "--root", LANE, "--rev", HEAD], 0)
lane("c2-at-base", [C2, "--root", LANE, "--rev", BASE, "--no-battery"], 1)
lane("c2-at-A2", [C2, "--root", LANE, "--rev", A2, "--no-battery"], 0)

# fixture evidence: C2 over rewritten frozen bytes
d, base, land = green_c2()
for name, patch, expect in (
    ("c2-frozen-counter-tampered",
     lambda dd: put(dd, {"tools/round-47/record.py":
                         open(os.path.join(dd, "tools/round-47/record.py")).read()
                         + "\n# post-freeze tamper of a frozen path\n"}), 2),
    ("c2-frozen-claims-tampered",
     lambda dd: put(dd, {"plans/round-47-claims.md":
                         "# claims\n\n## Frozen paths (exact)\n\n- `plans/round-47-claims.md`\n"}), 2),
):
    dd = os.path.join(S, "ev-" + name + "-")
    dd = dd + os.urandom(3).hex()
    os.makedirs(dd)
    sh(["git", "-C", dd, "clone", "-q", d, "."], check=True)
    for k, v in (("user.email", "fx@round47"), ("user.name", "r47 fixture")):
        sh(["git", "-C", dd, "config", k, v], check=True)
    patch(dd)
    rev = commit(dd, name)
    out = os.path.join(dd, "receipt.json")
    run("evidence-" + name, ["python3", "-I", "-B",
                             os.path.join(dd, "tools/round-47/record.py"), "--root", dd,
                             "--rev", rev, "--no-battery", "--json-out", out], expect)
    shutil.copy(out, os.path.join(EV, name + ".json"))
    diff = sh(["git", "-C", dd, "log", "-1", "--format=%H %s", "-p",
               "--", "tools/round-47/", "plans/round-47-claims.md"]).stdout
    open(os.path.join(EV, name + ".patch"), "w").write(diff)
    open(os.path.join(EV, name + ".fixture.json"), "w").write(json.dumps(
        {"fixture_root": dd, "base": base, "landing": land, "measured": rev,
         "generator": "drive2.green_c2 (receipts reproduce with drive8.py)"}, indent=1))

# fixture evidence: the axes correction class
card = open(os.path.join(d, "SCORECARD.md")).read()
red = card.replace("| coverage | 9.72 -> 10.0 | 1/1", "| coverage | 9.72 -> 10.0 | 9/9")
for name, line, expect in (
    ("c2-axes-false-correction", "\n- corrects axes coverage: 999/999\n", 1),
    ("c2-axes-true-correction-red-atom", "\n- corrects axes coverage: 1/1\n", 0),
):
    dd = os.path.join(S, "ev-" + name + "-" + os.urandom(3).hex())
    os.makedirs(dd)
    sh(["git", "-C", dd, "clone", "-q", d, "."], check=True)
    for k, v in (("user.email", "fx@round47"), ("user.name", "r47 fixture")):
        sh(["git", "-C", dd, "config", k, v], check=True)
    put(dd, {"SCORECARD.md": red + line})
    rev = commit(dd, name)
    out = os.path.join(dd, "receipt.json")
    run("evidence-" + name, ["python3", "-I", "-B",
                             os.path.join(dd, "tools/round-47/record.py"), "--root", dd,
                             "--rev", rev, "--no-battery", "--json-out", out], expect)
    shutil.copy(out, os.path.join(EV, name + ".json"))
    open(os.path.join(EV, name + ".card.md"), "w").write(red + line)

open(os.path.join(EV, "HEAD.json"), "w").write(json.dumps(
    {"lane_head": HEAD, "freezes_measured": {"A2": A2, "A6": A6, "F1": F1, "base": BASE},
     "utc": __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
     .replace(microsecond=0).isoformat()}, indent=1))
with open(os.path.join(S, "receipts8.jsonl"), "w") as fh:
    for x in D.OUT:
        fh.write(json.dumps(x) + "\n")
