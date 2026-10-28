#!/usr/bin/env python3
"""Fifth batch: can an axes correction repair a red axes atom (clause 3's axes sentence)?"""
import json, os, sys
sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r47/MutExitCodes")
import drive2 as D
from drive2 import sh, put, commit, S, run, green_c2

def clone(d, prefix):
    dd = os.path.join(S, prefix + os.urandom(3).hex())
    os.makedirs(dd)
    sh(["git", "-C", dd, "clone", "-q", d, "."], check=True)
    for k, v in (("user.email", "fx@round47"), ("user.name", "r47 fixture")):
        sh(["git", "-C", dd, "config", k, v], check=True)
    return dd

def main():
    d, base, land = green_c2()
    card = open(os.path.join(d, "SCORECARD.md")).read()
    red = card.replace("| coverage | 9.72 -> 10.0 | 1/1", "| coverage | 9.72 -> 10.0 | 9/9")
    assert red != card
    for name, line, expect, note in (
        ("red-axes-uncorrected", "", 1, "a red axes row is red"),
        ("red-axes-true-correction", "\n- corrects axes coverage: 1/1\n", 0,
         "clause 3: an axes correction stating 1/1 must exempt and re-derive"),
        ("red-axes-false-correction", "\n- corrects axes coverage: 9/9\n", 1,
         "clause 3: a false axes correction must keep the atom red"),
    ):
        dd = clone(d, "axes2-")
        put(dd, {"SCORECARD.md": red + line})
        rev = commit(dd, "axes " + name)
        rec = run("c2-" + name, ["python3", "-I", "-B",
                                 os.path.join(dd, "tools/round-47/record.py"),
                                 "--root", dd, "--rev", rev, "--no-battery"], expect, note)
        try:
            out = json.loads(rec["stdout"])
            print(json.dumps({"detail": name, "exit": rec["exit"], "corrections": out.get("corrections"),
                              "corrections_bad": out.get("corrections_bad"),
                              "exempted": out.get("exempted"),
                              "mismatch_classes": [m.get("class") for m in out.get("mismatches", [])]}))
        except Exception:
            print(json.dumps({"detail": name, "exit": rec["exit"], "raw": rec["stdout"][:200]}))
    with open(os.path.join(S, "receipts5.jsonl"), "w") as fh:
        for x in D.OUT:
            fh.write(json.dumps(x) + "\n")

main()
