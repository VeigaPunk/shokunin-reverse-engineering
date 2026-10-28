#!/usr/bin/env python3
"""Round-47 C2: real-card variants. Frozen record.py @5017e1f against the lane's own
committed SCORECARD.md, on a read-only clone, with the drafted round-47 corrections.

V1 as committed (seats + window + 2 axes corrections)
V2 window correction line deleted
V3 V1 + a decoy degenerate window atom in the round-46 section, correction pair set to it
V4 V1 with both `- corrects axes` lines deleted (are they parseable at all?)
"""
import json
import os
import re
import subprocess
import sys
import time

S = os.environ["HYAKU_SCRATCH"]
L = os.path.join(S, "lane-copy")
RECORD = os.environ.get("RECORD_OVERRIDE") or os.path.join(S, "inst/tools/round-47/record.py")
OUT = os.environ.get("REALCARD_OUT") or os.path.join(S, "realcard.json")


def run(args, cwd=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


def g(*args):
    return run(["git", "-C", L, *args])


def must(*args):
    r = g(*args)
    if r.returncode != 0:
        raise SystemExit("git %s -> %s %s" % (" ".join(args), r.returncode, r.stderr))
    return r.stdout.strip()


def measure(tag):
    rev = must("rev-parse", "HEAD")
    cmd = [sys.executable, "-I", "-B", RECORD, "--root", L, "--rev", rev]
    utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    r = run(cmd)
    try:
        rec = json.loads(r.stdout)
    except ValueError:
        rec = {"unparsable": r.stdout[:400]}
    return {"variant": tag, "rev": rev,
            "command": "python3 -I -B $S/inst/tools/round-47/record.py --root $L "
                       "--rev " + rev,
            "utc": utc, "exit": r.returncode,
            "stdout_sha256": __import__("hashlib").sha256(r.stdout.encode()).hexdigest(),
            "failing": rec.get("failing"),
            "mismatches": [(m["class"], str(m["key"]), json.dumps(m["derived"])[:200])
                           for m in (rec.get("mismatches") or [])],
            "corrections": rec.get("corrections"),
            "corrections_bad": rec.get("corrections_bad"),
            "exempted": [(e["class"], e["atom"][:80]) for e in (rec.get("exempted") or [])],
            "battery": rec.get("battery")}


def drop_block(text, prefix):
    """Drop a `- corrects ...` entry and its continuation lines."""
    lines = text.splitlines(True)
    out, skip = [], False
    for line in lines:
        if line.startswith(prefix):
            skip = True
            continue
        if skip and line.startswith("  ") and not line.lstrip().startswith("- "):
            continue
        skip = False
        out.append(line)
    return "".join(out)


def main():
    must("reset", "--hard", "-q")
    base = must("rev-parse", "HEAD")
    orig = g("show", "HEAD:SCORECARD.md").stdout
    rows = []

    # V1: as committed
    rows.append(measure("V1-as-committed"))

    # V2: window correction deleted
    v2 = drop_block(orig, "- corrects window round-46:")
    assert v2 != orig
    open(os.path.join(L, "SCORECARD.md"), "w").write(v2)
    must("add", "SCORECARD.md")
    must("commit", "-q", "-m", "V2: window correction removed")
    rows.append(measure("V2-no-window-correction"))

    # V3: decoy degenerate atom in the round-46 section + correction pair moved to it
    must("reset", "--hard", "-q", base)
    decoy = "`git log 58eb04b6..58eb04b6 -- tools/round-46 plans/round-46-claims.md` is empty."
    v3 = orig.replace("## Record corrections \u2014 round 47",
                      decoy + "\n\n## Record corrections \u2014 round 47", 1)
    v3 = v3.replace(
        "- corrects window round-46: empty in 332f4884..58eb04b6 -- "
        "tools/round-46 plans/round-46-claims.md",
        "- corrects window round-46: empty in 58eb04b6..58eb04b6 -- "
        "tools/round-46 plans/round-46-claims.md", 1)
    assert v3 != orig and "58eb04b6..58eb04b6 --" in v3
    open(os.path.join(L, "SCORECARD.md"), "w").write(v3)
    must("add", "SCORECARD.md")
    must("commit", "-q", "-m", "V3: decoy degenerate window atom")
    rows.append(measure("V3-decoy-degenerate-pair"))

    # V4: axes correction lines deleted from V1
    must("reset", "--hard", "-q", base)
    v4 = orig
    for pref in ("- corrects axes coverage:", "- corrects axes depth:"):
        v4 = drop_block(v4, pref)
    assert v4 != orig
    open(os.path.join(L, "SCORECARD.md"), "w").write(v4)
    must("add", "SCORECARD.md")
    must("commit", "-q", "-m", "V4: axes corrections removed")
    rows.append(measure("V4-no-axes-corrections"))

    # V5: V1 + an A3-era historical correction for a round that has no atom at all,
    #     over a degenerate window and a pathspec that does not exist
    must("reset", "--hard", "-q", base)
    v5 = orig.rstrip("\n") + ("\n- corrects window round-3: empty in 58eb04b6..58eb04b6 -- tools/none/\n")
    open(os.path.join(L, "SCORECARD.md"), "w").write(v5)
    must("add", "SCORECARD.md")
    must("commit", "-q", "-m", "V5: historical correction for a round with no atom")
    rows.append(measure("V5-historical-no-atom-correction"))

    must("reset", "--hard", "-q", base)
    out = {"lane_clone": L, "base": base, "record_py_sha256":
           __import__("hashlib").sha256(open(RECORD, "rb").read()).hexdigest(),
           "variants": rows}
    print(json.dumps(out, indent=1, sort_keys=True))
    open(OUT, "w").write(json.dumps(out, indent=1, sort_keys=True) + "\n")


main()
