#!/usr/bin/env python3
"""depth-blocks.py - round-88 counter (R88-C2, depth).

Implements the depth atom of SCORECARD recipe A as a committed instrument: a
`## Queue-drain craft` rule block counts as resolved only when every
`corpus/knowledge/<name>.md[:line[-line]]` citation it carries exists at the
measured revision and its line range is inside the file.  A block with no
citation is unresolved; a block citing an absent file or an out-of-range line
is unresolved.

Reads committed bytes only (`git show <rev>:<path>`), never the working tree,
unless `--worktree` is passed.

Exit: 0 every block resolved; 1 at least one unresolved; 2 could-not-evaluate
(bad revision, missing SKILL.md, bad argv).

--selftest runs the resolver on an in-memory fixture tree.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

TOOL = "tools/round-88/depth-blocks.py"
PATTERN = r"corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?"


class Unevaluable(Exception):
    pass


def read_at(root: str, rev: str | None, path: str) -> str:
    if rev:
        p = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                           capture_output=True, text=True)
        if p.returncode != 0:
            raise Unevaluable(f"absent at {rev}: {path}: {p.stderr.strip()[:120]}")
        return p.stdout
    full = os.path.join(root, path)
    if not os.path.isfile(full):
        raise Unevaluable(f"absent in worktree: {path}")
    with open(full, encoding="utf-8") as fh:
        return fh.read()


def rule_blocks(skill: str) -> list[str]:
    if "## Queue-drain craft " not in skill:
        raise Unevaluable("SKILL.md carries no '## Queue-drain craft ' section")
    craft = skill.split("## Queue-drain craft ", 1)[1].split("\n## ", 1)[0]
    return re.split(r"(?m)^- \*\*", craft)[1:]


def resolve(rule: str, reader) -> tuple[bool, list[str]]:
    refs = re.findall(PATTERN, rule)
    if not refs:
        return False, ["no-citation"]
    problems = []
    for name, first, last in refs:
        try:
            count = len(reader("corpus/knowledge/" + name).splitlines())
        except Unevaluable as exc:
            problems.append(f"absent:{name}:{exc}")
            continue
        start = int(first or 1)
        end = int(last or first or 1)
        if not (1 <= start <= end <= count):
            problems.append(f"range:{name}:{start}-{end} of {count}")
    return not problems, problems


def count(root: str, rev: str | None) -> dict:
    skill = read_at(root, rev, "SKILL.md")

    def reader(path):
        return read_at(root, rev, path)

    blocks, unresolved = rule_blocks(skill), []
    for i, rule in enumerate(blocks, 1):
        ok, problems = resolve(rule, reader)
        if not ok:
            unresolved.append({"block": i, "problems": problems})
    return {"tool": TOOL, "revision": rev or "worktree", "blocks": len(blocks),
            "resolved": len(blocks) - len(unresolved), "unresolved": unresolved,
            "met_target": not unresolved}


def selftest() -> int:
    fails, ncases = [], 0

    def check(name, cond):
        nonlocal ncases
        ncases += 1
        if not cond:
            fails.append(name)

    tree = {"corpus/knowledge/2026-01-01-a.md": "l1\nl2\nl3\n",
            "corpus/knowledge/2026-01-01-b.md": "x\n"}

    def reader(path):
        if path not in tree:
            raise Unevaluable("absent")
        return tree[path]

    ok, probs = resolve("- **rule**: see corpus/knowledge/2026-01-01-a.md:2-3", reader)
    check("resolved-range", ok and probs == [])
    ok, probs = resolve("- **rule**: see corpus/knowledge/2026-01-01-a.md:3-9", reader)
    check("range-out-of-bounds", not ok and probs[0].startswith("range:"))
    ok, probs = resolve("- **rule**: see corpus/knowledge/2026-01-01-z.md", reader)
    check("absent-file", not ok and probs[0].startswith("absent:"))
    ok, probs = resolve("- **rule**: no citation here", reader)
    check("no-citation", not ok and probs == ["no-citation"])
    ok, probs = resolve("- **rule**: corpus/knowledge/2026-01-01-b.md", reader)
    check("bare-file-line1", ok)
    check("block-split", len(rule_blocks("## Queue-drain craft v9\n- **a** x\n- **b** y\n## next\n")) == 2)
    try:
        rule_blocks("no section")
        fails.append("missing-section")
    except Unevaluable:
        pass
    ncases += 1
    print(f"SELFTEST cases={ncases} failures={len(fails)} {' '.join(fails)}".rstrip())
    return 0 if not fails else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev")
    ap.add_argument("--worktree", action="store_true")
    ap.add_argument("--json-out")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    rev = None if a.worktree else a.rev
    if not a.worktree and not a.rev:
        print("could-not-evaluate: --rev (or --worktree) is required", file=sys.stderr)
        return 2
    try:
        receipt = count(os.path.abspath(a.root), rev)
    except Unevaluable as exc:
        receipt = {"tool": TOOL, "unevaluable": str(exc), "met_target": False}
        print(json.dumps(receipt, sort_keys=True))
        return 2
    if a.json_out:
        with open(a.json_out, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=1, sort_keys=True)
    print(json.dumps({k: receipt[k] for k in ("revision", "blocks", "resolved",
                                              "unresolved", "met_target")}, sort_keys=True))
    return 0 if receipt["met_target"] else 1


if __name__ == "__main__":
    sys.exit(main())
