#!/usr/bin/env python3
"""Generate `tools/round-48/census2.json`: the instrument census R48-C1 scores against.

Rule (mechanical, re-derivable, never a hand-kept list):

    scope = every path matching `tools/round-4[1-8]/**.{py,sh}` that is named in a
            round-41..48 claim file at `--rev`, restricted to paths that exist there

The round-46 census stopped at round 46, so the registry section grew two rows
(`tools/round-47/exact.py`, `tools/round-47/record.py`) that its own census could not
name; this generator extends the rule through round 48 so the registry and the census
are the same set again.

`census_text(read)` is the pure form the counters re-run: `read(path)` returns the
file's text at the measured revision, or None. It imports nothing, so a counter can
exec it from committed bytes.

    python3 -I -B tools/round-48/census2.py --root . --rev <rev> --out tools/round-48/census2.json
"""
import argparse
import json
import os
import re
import subprocess
import sys

CLAIMS = [f"plans/round-{n}-claims.md" for n in range(41, 49)]
TOOL = re.compile(r"tools/round-4[1-8]/[A-Za-z0-9._/-]+\.(?:py|sh)")
RULE = ("every path matching tools/round-4[1-8]/**.{py,sh} named in a "
        "plans/round-4[1-8]-claims.md at --rev, restricted to paths present there")


def census_text(read):
    """Sorted census paths, plus the per-file naming map, from a text reader."""
    named, per_file = set(), {}
    for path in CLAIMS:
        body = read(path)
        if body is None:
            per_file[path] = {"present": False, "named": []}
            continue
        found = sorted({m.group(0) for m in TOOL.finditer(body)})
        per_file[path] = {"present": True, "named": found}
        named |= set(found)
    present = sorted(p for p in named if read(p) is not None)
    absent = sorted(named - set(present))
    return {"rule": RULE, "paths": present, "named_but_absent": absent,
            "per_claims_file": per_file}


def _git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)


def _read_at(root, rev, path):
    if rev == "WORKTREE":
        full = os.path.join(root, path)
        return open(full).read() if os.path.exists(full) else None
    r = _git(root, "show", f"{rev}:{path}")
    return r.stdout if r.returncode == 0 else None


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", required=True)
    ap.add_argument("--rev", default="main", help="a revision, or WORKTREE")
    ap.add_argument("--out")
    args = ap.parse_args()
    doc = census_text(lambda p: _read_at(args.root, args.rev, p))
    text = json.dumps(doc, indent=1) + "\n"
    if args.out:
        with open(args.out, "w") as fh:
            fh.write(text)
    print(json.dumps({"paths": len(doc["paths"]),
                      "named_but_absent": doc["named_but_absent"],
                      "per_file": {k: len(v["named"])
                                   for k, v in doc["per_claims_file"].items()}},
                     indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
