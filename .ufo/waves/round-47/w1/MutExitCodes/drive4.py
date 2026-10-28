#!/usr/bin/env python3
"""Fourth batch: is an `axes` correction line parsed, re-derived, and able to make C2 red?"""
import json, os, sys
sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r47/MutExitCodes")
import drive2 as D
from drive2 import sh, put, commit, S, run, green_c2

def main():
    d, base, land = green_c2()
    card = open(os.path.join(d, "SCORECARD.md")).read()
    assert "- corrects seats round-9" in card
    run("c2-green-control", ["python3", "-I", "-B", os.path.join(d, "tools/round-47/record.py"),
                             "--root", d, "--rev", land, "--no-battery"], 0, "control")
    cases = {
        # a false seats correction is binding (control for the probe below)
        "false-seats-correction": ("- corrects seats round-9: 9 waves, 99 seats total\n", 1,
                                   "control: a false seats correction turns the counter red"),
        # clause 3 says an axes correction must state <resolved>/<total>; the parser cannot see it
        "false-axes-correction": ("- corrects axes coverage: 999/999\n", 1,
                                  "clause 3 requires an axes correction to re-derive"),
        "garbage-axes-correction": ("- corrects axes depth: not a fraction at all\n", 1,
                                    "clause 3 requires an axes correction to state <r>/<t>"),
        # an exemption naming an atom that does not exist, in a known class
        "ghost-rev-correction": ("- corrects rev deadbee: nowhere\n", 1, "ghost atom"),
    }
    for name, (line, expect, note) in cases.items():
        dd = os.path.join(S, "axes-" + name + "-" + os.urandom(3).hex())
        sh(["git", "-C", dd, "clone", "-q", d, "."], check=True) if os.makedirs(dd) is None else None
        for k, v in (("user.email", "fx@round47"), ("user.name", "r47 fixture")):
            sh(["git", "-C", dd, "config", k, v], check=True)
        body = open(os.path.join(dd, "SCORECARD.md")).read()
        put(dd, {"SCORECARD.md": body + line})
        rev = commit(dd, "correction " + name)
        rec = run("c2-" + name, ["python3", "-I", "-B",
                                 os.path.join(dd, "tools/round-47/record.py"),
                                 "--root", dd, "--rev", rev, "--no-battery"], expect, note)
        if rec["exit"] != expect:
            print(json.dumps({"detail": name, "corrections": json.loads(rec["stdout"]).get("corrections"),
                              "corrections_bad": json.loads(rec["stdout"]).get("corrections_bad"),
                              "exempted": json.loads(rec["stdout"]).get("exempted")}))
    with open(os.path.join(S, "receipts4.jsonl"), "w") as fh:
        for x in D.OUT:
            fh.write(json.dumps(x) + "\n")

main()
