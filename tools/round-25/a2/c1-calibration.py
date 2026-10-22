#!/usr/bin/env python3
"""Round 25 (attempt 2) C1: count self-assessment mismatches at one revision.

Five fixed items, each comparing a lane self-assessment statement (SCORECARD,
LOG, SHONEN, QUALITY) with observed repository state or with the recorded
outside verdict of round 24. Reads only Git blobs at --rev; never the work tree.

Usage: python3 -I -B tools/round-25/a2/c1-calibration.py --root <lane> --rev <rev>
Prints one JSON object. Exit 0 when mismatches == 0, 1 when any item
mismatches, 2 when the revision or a required blob cannot be read.
"""
import argparse
import json
import os
import re
import subprocess
import sys

SPOT = "corpus/lessons/round-24-verifier-spotcheck.md"


def git(root, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    return subprocess.run(["git", "-C", root, "--no-replace-objects", *args],
                          capture_output=True, text=True, env=env)


def blob(root, rev, path):
    p = git(root, "cat-file", "blob", f"{rev}:{path}")
    if p.returncode != 0:
        raise LookupError(path)
    return p.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    r = git(a.root, "rev-parse", "--verify", f"{a.rev}^{{commit}}")
    if r.returncode != 0:
        print(json.dumps({"error": "bad_rev", "rev": a.rev}))
        return 2
    rev = r.stdout.strip()
    try:
        score = blob(a.root, rev, "SCORECARD.md")
        log = blob(a.root, rev, "LOG.md")
        shonen = blob(a.root, rev, "SHONEN.md")
        quality = blob(a.root, rev, "corpus/QUALITY.md")
        province = blob(a.root, rev, "PROVINCE.md")
        blob(a.root, rev, SPOT)
    except LookupError as e:
        print(json.dumps({"error": "missing_blob", "path": str(e), "rev": rev}))
        return 2

    items = []

    # I1/I2: the round-24 outside decision is recorded where the lane assesses itself.
    def records_verdict(text):
        return any(SPOT in ln and "rejected-honest-stop" in ln for ln in text.splitlines())
    items.append({"id": "I1", "what": "SCORECARD records the round-24 outside decision (cites the spot-check and rejected-honest-stop on one line)",
                  "match": records_verdict(score)})
    items.append({"id": "I2", "what": "LOG records the round-24 outside decision (same line test)",
                  "match": records_verdict(log)})

    # I3: the round-24 outside disagreement became a QUALITY admission criterion (LEARNING.md discernment rule).
    rows = [ln for ln in quality.splitlines() if re.match(r"^\| \d+ \|", ln)]
    items.append({"id": "I3", "what": "a QUALITY admission-criterion row cites the round-24 spot-check",
                  "match": any(SPOT.split("/")[-1] in ln for ln in rows)})

    # I4: the owned-axes coverage row's N/N equals the knowledge Markdown count at rev.
    lst = git(a.root, "ls-tree", "-r", "--name-only", rev, "corpus/knowledge/")
    count = sum(1 for p in lst.stdout.splitlines() if p.endswith(".md"))
    row = next((ln for ln in score.splitlines() if ln.startswith("| coverage |")), "")
    m = re.search(r"(\d+)/(\d+) knowledge files mapped", row)
    stated = [int(m.group(1)), int(m.group(2))] if m else None
    items.append({"id": "I4", "what": "SCORECARD owned-axes coverage row states N/N knowledge files mapped with N equal to the knowledge Markdown count",
                  "stated": stated, "observed": count,
                  "match": bool(stated) and stated[0] == stated[1] == count})

    # I5: SHONEN's PROVINCE boundary pointer range lies inside PROVINCE's first '## Adjacent' section.
    plines = province.splitlines()
    adj = next((i + 1 for i, ln in enumerate(plines) if ln.strip() == "## Adjacent"), None)
    end = None
    if adj:
        end = next((i for i in range(adj, len(plines)) if plines[i].startswith("## ")), len(plines))
    pm = re.search(r"`PROVINCE\.md:(\d+)-(\d+)`", shonen)
    rng = [int(pm.group(1)), int(pm.group(2))] if pm else None
    items.append({"id": "I5", "what": "SHONEN boundary pointer PROVINCE.md:A-B lies inside the first ## Adjacent section",
                  "stated": rng, "observed": [adj, end],
                  "match": bool(rng and adj) and adj <= rng[0] <= rng[1] <= end})

    mism = sum(1 for i in items if not i["match"])
    print(json.dumps({"rev": rev, "items": len(items), "mismatches": mism, "detail": items}, indent=1))
    return 0 if mism == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
