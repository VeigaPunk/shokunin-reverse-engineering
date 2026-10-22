#!/usr/bin/env python3
"""Round 25 (attempt 2) C2: knowledge entries and the sourced EVM selector-name entry at one revision.

Prints the knowledge Markdown count under corpus/knowledge/ and whether the named
entry exists with a `source:` line citing at least one corpus/SOURCES.md row that
is `mined`, `opened` 2026-10-22, and whose `used-by` names the entry path.
Reads only Git blobs at --rev.

Usage: python3 -I -B tools/round-25/a2/c2-coverage.py --root <lane> --rev <rev>
Exit 0 when the entry is present and sourced, 1 when not, 2 on unreadable input.
"""
import argparse
import json
import os
import re
import subprocess
import sys

ENTRY = "corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md"
OPENED = "2026-10-22"


def git(root, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    return subprocess.run(["git", "-C", root, "--no-replace-objects", *args],
                          capture_output=True, text=True, env=env)


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
    lst = git(a.root, "ls-tree", "-r", "--name-only", rev, "corpus/knowledge/")
    if lst.returncode != 0:
        print(json.dumps({"error": "ls_tree_failed", "rev": rev}))
        return 2
    count = sum(1 for p in lst.stdout.splitlines() if p.endswith(".md"))
    src = git(a.root, "cat-file", "blob", f"{rev}:corpus/SOURCES.md")
    if src.returncode != 0:
        print(json.dumps({"error": "missing_blob", "path": "corpus/SOURCES.md", "rev": rev}))
        return 2
    rows = {}
    for ln in src.stdout.splitlines():
        cells = [c.strip() for c in ln.split("|")]
        if len(cells) >= 13 and re.fullmatch(r"S\d{3}", cells[1]):
            rows[cells[1]] = {"status": cells[8], "opened": cells[9], "used_by": cells[11]}
    ent = git(a.root, "cat-file", "blob", f"{rev}:{ENTRY}")
    present = ent.returncode == 0
    cited, qualifying = [], []
    if present:
        src_line = next((ln for ln in ent.stdout.splitlines() if ln.startswith("source:")), "")
        cited = sorted(set(re.findall(r"\bS\d{3}\b", src_line)))
        for sid in cited:
            row = rows.get(sid)
            if row and row["status"] == "mined" and row["opened"] == OPENED and ENTRY in row["used_by"]:
                qualifying.append(sid)
    sourced = 1 if (present and qualifying) else 0
    print(json.dumps({"rev": rev, "knowledge_md": count, "entry": ENTRY, "entry_present": present,
                      "cited_rows": cited, "qualifying_rows": qualifying, "entry_sourced": sourced}, indent=1))
    return 0 if sourced else 1


if __name__ == "__main__":
    sys.exit(main())
