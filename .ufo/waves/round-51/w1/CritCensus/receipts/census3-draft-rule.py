#!/usr/bin/env python3
"""DRAFT `tools/round-50/census3.py` (seat C2RegCensus, round 50 wave 1) - generate `census3.json`.

Rule (mechanical; census2's rule extended; never a hand-kept list):

    scope = (a) every path matching `tools/round-4[1-9]/**.{py,sh}` named in a
                `plans/round-4[1-9]-claims.md` at --rev, restricted to paths present there
          U (b) every `.py`/`.sh` path under `tools/round-49/` at --rev
                (the round-49 instrument directory is registered whole, atom B9)
          U (c) every `.py`/`.sh` path under `tools/round-50/` at --rev, excluding
                `tools/round-50/control-fixtures/` (the round-50 directory is registered whole)

Why (b)/(c) and not only (a): at the base the plan-naming rule reaches 3 of the 6
round-49 `.py`/`.sh` files (`c1-counter.py`, `c1-run.sh`, `c2-mismatch.py`); the other three
(`c1-controls.py`, `c1-oracle.py`, `c1-run.py`) are named by no claims file. The round-50
draft plan names `c1-counter.py`, `c1-run.sh`, `c2-record.py`, `selftest-r49-c2.py` but not
`c1-controls.py`. A "named in a plan" rule therefore leaves instruments unregistered by construction.

`census_text(read, ls)` is the pure form a counter re-runs: `read(path)` -> text or None,
`ls(prefix)` -> sorted paths below `prefix` at the measured revision. Imports nothing.

    python3 -I -B tools/round-50/census3.py --root <LANE> --rev <rev> --out tools/round-50/census3.json
"""
import argparse
import json
import re
import subprocess
import sys

CLAIMS = [f"plans/round-{n}-claims.md" for n in range(41, 51)]
TOOL = re.compile(r"tools/round-4[1-9]/[A-Za-z0-9._/-]+\.(?:py|sh)")
SCRIPT = re.compile(r"\.(?:py|sh)$")
WHOLE_DIRS = ("tools/round-49/", "tools/round-50/")
SKIP = ("tools/round-50/control-fixtures/",)
RULE = ("every path matching tools/round-4[1-9]/**.{py,sh} named in a plans/round-4[1-9]-claims.md "
        "or plans/round-50-claims.md at --rev, restricted to paths present there; plus every "
        ".py/.sh path under tools/round-49/ and under tools/round-50/ (not control-fixtures/) at --rev")


def census_text(read, ls):
    named, per_file = set(), {}
    for path in CLAIMS:
        body = read(path)
        if body is None:
            per_file[path] = {"present": False, "named": []}
            continue
        found = sorted({m.group(0) for m in TOOL.finditer(body)})
        per_file[path] = {"present": True, "named": found}
        named |= set(found)
    whole = set()
    for d in WHOLE_DIRS:
        whole |= {p for p in ls(d) if SCRIPT.search(p) and not p.startswith(SKIP)}
    present = sorted({p for p in named if read(p) is not None} | whole)
    absent = sorted(named - set(present))
    return {"rule": RULE, "paths": present, "named_but_absent": absent,
            "whole_directory_additions": sorted(whole - named),
            "per_claims_file": per_file}


def _git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--out")
    args = ap.parse_args()

    def read(p):
        r = _git(args.root, "show", f"{args.rev}:{p}")
        return r.stdout if r.returncode == 0 else None

    def ls(prefix):
        r = _git(args.root, "ls-tree", "-r", "--name-only", args.rev, "--", prefix)
        return sorted(r.stdout.split()) if r.returncode == 0 else []

    doc = census_text(read, ls)
    text = json.dumps(doc, indent=1) + "\n"
    if args.out:
        with open(args.out, "w") as fh:
            fh.write(text)
    print(json.dumps({"paths": len(doc["paths"]), "named_but_absent": doc["named_but_absent"],
                      "whole_directory_additions": doc["whole_directory_additions"]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
