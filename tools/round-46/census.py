#!/usr/bin/env python3
"""Generate `tools/round-46/census.json`: the instrument census R46-C2 scores against.

Rule (mechanical, re-derivable, never a hand-kept list):

    scope = every path matching `tools/round-4[1-6]/**.{py,sh}` that is named in a
            round-41..46 claim file at `--rev`, restricted to paths that exist there

The claims files are the lane's own record of which tools compute a claim's target,
so the census is a property of committed bytes and not of anyone's memory.  A path
that is named but absent at `--rev` is reported under `named_but_absent` and does not
enter the scope (R45-CL2: a registry row whose tool does not exist is a ghost).

    python3 -I -B tools/round-46/census.py --root . --rev <rev> --out tools/round-46/census.json
"""
import argparse
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gate  # noqa: E402

CLAIMS = [f"plans/round-{n}-claims.md" for n in range(41, 47)]
TOOL = re.compile(r"tools/round-4[1-6]/[A-Za-z0-9._/-]+\.(?:py|sh)")


def _read(root, rev, path):
    if rev == "WORKTREE":
        full = os.path.join(root, path)
        return open(full).read() if os.path.exists(full) else None
    return gate.show(root, rev, path)


def census(root, rev):
    named, per_file = set(), {}
    for path in CLAIMS:
        body = _read(root, rev, path)
        if body is None:
            per_file[path] = {"present": False, "named": []}
            continue
        found = sorted({m.group(0) for m in TOOL.finditer(body)})
        per_file[path] = {"present": True, "named": found}
        named |= set(found)
    if rev == "WORKTREE":
        present = sorted(p for p in named if os.path.exists(os.path.join(root, p)))
    else:
        present = sorted(p for p in named if gate.blob(root, rev, p) is not None)
    absent = sorted(named - set(present))
    return {
        "rule": ("every path matching tools/round-4[1-6]/**.{py,sh} named in a "
                 "plans/round-4[1-6]-claims.md at --rev, restricted to paths present there"),
        "paths": present,
        "named_but_absent": absent,
        "per_claims_file": per_file,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", required=True)
    ap.add_argument("--rev", default="main", help="a revision, or WORKTREE")
    ap.add_argument("--out")
    args = ap.parse_args()
    doc = census(args.root, args.rev)
    text = json.dumps(doc, indent=1) + "\n"
    if args.out:
        with open(args.out, "w") as fh:
            fh.write(text)
    print(json.dumps({"paths": len(doc["paths"]), "named_but_absent": doc["named_but_absent"],
                      "per_file": {k: len(v["named"]) for k, v in doc["per_claims_file"].items()}},
                     indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
