#!/usr/bin/env python3
"""depth-blocks-v2.py - round-89 counter (R89-C2, depth).

Supersedes `tools/round-88/depth-blocks.py` on two counts, both routed by the
round-88 non-author spot-check (QUALITY 157 / M88-7 and the M88-9 separability
note) and both declared here before data:

1. **The target is an argument.** `--expect-blocks N` is required and
   `met_target` is `blocks == N and resolved == blocks and not unresolved`.
   The round-88 counter reported `met_target true` at 27 blocks (base) and on a
   one-line stub at 28, because `met_target` was only `not unresolved`.
2. **A block has a shape floor.** A rule block counts as resolved only if its
   citations resolve AND it carries at least `MIN_WORDS` words and `MIN_SPANS`
   backticked spans: a citation-only stub is not a decision block. Every
   pre-existing block (1..28 at the round-89 base) clears both floors; the
   stub, the empty block and the junk-citation block are red selftest arms.

Citations are `corpus/knowledge/<stem>.md[:start[-end]]` and are read at the
revision named by `--rev` (never the moving worktree unless `--worktree`).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

TOOL = "tools/round-89/depth-blocks-v2.py"
PATTERN = r"corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?"
MIN_WORDS = 25
MIN_SPANS = 2


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


def shape(rule: str) -> tuple[bool, list[str]]:
    problems = []
    words = len(rule.split())
    spans = len(re.findall(r"`[^`\n]+`", rule))
    if words < MIN_WORDS:
        problems.append(f"shape:words:{words}<{MIN_WORDS}")
    if spans < MIN_SPANS:
        problems.append(f"shape:spans:{spans}<{MIN_SPANS}")
    return not problems, problems


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


def count(root: str, rev: str | None, expect: int) -> dict:
    skill = read_at(root, rev, "SKILL.md")

    def reader(path):
        return read_at(root, rev, path)

    blocks, unresolved = rule_blocks(skill), []
    for i, rule in enumerate(blocks, 1):
        ok, problems = resolve(rule, reader)
        if ok:
            ok, problems = shape(rule)
        if not ok:
            unresolved.append({"block": i, "problems": problems})
    resolved = len(blocks) - len(unresolved)
    met = len(blocks) == expect and resolved == expect and not unresolved
    return {"tool": TOOL, "revision": rev or "worktree", "blocks": len(blocks),
            "resolved": resolved, "unresolved": unresolved,
            "expect_blocks": expect, "shape_floor": {"min_words": MIN_WORDS,
                                                     "min_spans": MIN_SPANS},
            "met_target": met}


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

    long_body = ("this rule names `alpha` and `beta` and states the threshold 3 "
                 "with a decision row and a refusal signature so that the block "
                 "carries a real rule rather than a pointer")
    ok, probs = resolve("- **rule**: " + long_body + " corpus/knowledge/2026-01-01-a.md:2-3", reader)
    check("resolved-range", ok and probs == [])
    ok, probs = resolve("- **rule**: " + long_body + " corpus/knowledge/2026-01-01-a.md:3-9", reader)
    check("range-out-of-bounds", not ok and probs[0].startswith("range:"))
    ok, probs = resolve("- **rule**: " + long_body + " corpus/knowledge/2026-01-01-z.md", reader)
    check("absent-file", not ok and probs[0].startswith("absent:"))
    ok, probs = resolve("- **rule**: " + long_body + " no citation here", reader)
    check("no-citation", not ok and probs == ["no-citation"])
    ok, probs = resolve("- **rule**: " + long_body + " corpus/knowledge/2026-01-01-b.md", reader)
    check("bare-file-line1", ok)
    # The round-88 stub: one line, one citation, one span -> shape floor red.
    stub = " stub corpus/knowledge/2026-01-01-a.md:1-2 `x`"
    ok, probs = shape(stub)
    check("stub-refused-by-shape", not ok and any(p.startswith("shape:words:") for p in probs))
    ok, probs = shape("- **rule**: `a` `b` corpus/knowledge/2026-01-01-a.md")
    check("two-spans-short-refused", not ok and any(p.startswith("shape:words:") for p in probs))
    check("block-split",
          len(rule_blocks("## Queue-drain craft v9\n- **a** x\n- **b** y\n## next\n")) == 2)
    try:
        rule_blocks("no section")
        fails.append("missing-section")
    except Unevaluable:
        pass
    ncases += 1
    # target arithmetic: base-style world of 2 blocks with expect 3 is not met
    skill = ("## Queue-drain craft v9\n- **a** " + long_body
             + " corpus/knowledge/2026-01-01-a.md\n- **b** " + long_body
             + " corpus/knowledge/2026-01-01-a.md\n## next\n")
    blocks = rule_blocks(skill)
    check("target-encodes-count", len(blocks) == 2)
    print(f"SELFTEST cases={ncases} failures={len(fails)} {' '.join(fails)}".rstrip())
    return 0 if not fails else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev")
    ap.add_argument("--worktree", action="store_true")
    ap.add_argument("--expect-blocks", type=int)
    ap.add_argument("--json-out")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    rev = None if a.worktree else a.rev
    if not a.worktree and not a.rev:
        print("could-not-evaluate: --rev (or --worktree) is required", file=sys.stderr)
        return 2
    if a.expect_blocks is None:
        print("could-not-evaluate: --expect-blocks N is required (QUALITY 157)",
              file=sys.stderr)
        return 2
    try:
        receipt = count(os.path.abspath(a.root), rev, a.expect_blocks)
    except Unevaluable as exc:
        receipt = {"tool": TOOL, "unevaluable": str(exc), "met_target": False}
    receipt["exit"] = 0 if receipt["met_target"] else 1
    if a.json_out:
        with open(a.json_out, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=1, sort_keys=True)
    print(f"blocks {receipt.get('blocks')} resolved {receipt.get('resolved')} "
          f"expect {receipt.get('expect_blocks')} "
          f"unresolved {len(receipt.get('unresolved') or [])} "
          f"met={receipt['met_target']} exit={receipt['exit']}")
    return receipt["exit"]


if __name__ == "__main__":
    sys.exit(main())
