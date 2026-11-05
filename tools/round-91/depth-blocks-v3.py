#!/usr/bin/env python3
"""depth-blocks-v3.py - round-91 counter (R91-C2, depth).

Supersedes `tools/round-89/depth-blocks-v2.py` on one count, routed by the
round-90 non-author spot-check and written here before data (QUALITY 175):

1. **The block's shape is part of the predicate.** v2 proves that block N
   exists, resolves its `corpus/knowledge/` citations and clears a word/backtick
   floor; a *prose* block citing a real knowledge line still scores 30/30. v3
   additionally requires every block at or after `--shape-from` (default 31) to
   carry a Markdown decision table: a header row, a separator row and at least
   `MIN_TABLE_ROWS` body rows, each with at least `MIN_TABLE_CELLS` cells. Blocks
   below the boundary keep v2's rule, because retrofitting 19 historical blocks
   would rewrite history rather than measure it — the boundary is declared, not
   inferred.
2. **The shape-blind predecessor is a measured control.** `--prose-proof` runs
   v2's resolution and v3's on the same two fixtures: a prose block (v2 accepts,
   v3 refuses) and a shaped block (both accept). The claim's receipt carries
   both verdicts, so "the predecessor false-greens this fixture" is printed,
   not asserted.

Citations are `corpus/knowledge/<stem>.md[:start[-end]]` and are read at the
revision named by `--rev` (never the moving worktree unless `--worktree`).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys

TOOL = "tools/round-91/depth-blocks-v3.py"
V2 = "tools/round-89/depth-blocks-v2.py"
PATTERN = r"corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?"
MIN_WORDS = 25
MIN_SPANS = 2
MIN_TABLE_ROWS = 3
MIN_TABLE_CELLS = 4
SEPARATOR = re.compile(r"^\|[\s:|-]+\|$")


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


def load_module(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rule_blocks(skill: str) -> list[str]:
    if "## Queue-drain craft " not in skill:
        raise Unevaluable("SKILL.md carries no '## Queue-drain craft ' section")
    craft = skill.split("## Queue-drain craft ", 1)[1].split("\n## ", 1)[0]
    return re.split(r"(?m)^- \*\*", craft)[1:]


def shape(rule: str) -> tuple[bool, list[str]]:
    """v2's floor: words and backticked spans."""
    problems = []
    words = len(rule.split())
    spans = len(re.findall(r"`[^`\n]+`", rule))
    if words < MIN_WORDS:
        problems.append(f"shape:words:{words}<{MIN_WORDS}")
    if spans < MIN_SPANS:
        problems.append(f"shape:spans:{spans}<{MIN_SPANS}")
    return not problems, problems


def table_shape(rule: str) -> tuple[bool, dict, list[str]]:
    """A decision table: header, separator and >=3 body rows of >=4 cells."""
    lines = [ln.strip() for ln in rule.splitlines()]
    best = {"rows": 0, "min_cells": 0}
    for i in range(len(lines) - 1):
        head = lines[i]
        if not (head.startswith("|") and head.endswith("|") and len(head) > 2):
            continue
        if not SEPARATOR.match(lines[i + 1] or ""):
            continue
        rows, cells = [], []
        j = i + 2
        while j < len(lines) and lines[j].startswith("|") and lines[j].endswith("|"):
            rows.append(lines[j])
            cells.append(len(lines[j].strip("|").split("|")))
            j += 1
        if len(rows) > best["rows"]:
            best = {"rows": len(rows), "min_cells": min(cells) if cells else 0}
    problems = []
    if best["rows"] < MIN_TABLE_ROWS:
        problems.append(f"table:rows:{best['rows']}<{MIN_TABLE_ROWS}")
    if best["min_cells"] < MIN_TABLE_CELLS:
        problems.append(f"table:cells:{best['min_cells']}<{MIN_TABLE_CELLS}")
    return not problems, best, problems


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


def count(root: str, rev: str | None, expect: int, shape_from: int) -> dict:
    skill = read_at(root, rev, "SKILL.md")

    def reader(path):
        return read_at(root, rev, path)

    blocks, unresolved, per_block = rule_blocks(skill), [], []
    shaped = 0
    for i, rule in enumerate(blocks, 1):
        ok, problems = resolve(rule, reader)
        if ok:
            ok, problems = shape(rule)
        tok, tinfo, tproblems = table_shape(rule)
        if tok:
            shaped += 1
        rec = {"block": i, "resolved": ok, "table": tok, "table_rows": tinfo["rows"],
               "required_shape": i >= shape_from}
        if rec["required_shape"] and not tok:
            ok = False
            problems = problems + tproblems
        rec["problems"] = problems
        per_block.append(rec)
        if not ok:
            unresolved.append({"block": i, "problems": problems})
    resolved = len(blocks) - len(unresolved)
    required = [r for r in per_block if r["required_shape"]]
    shaped_required = sum(1 for r in required if r["table"])
    met = (len(blocks) == expect and resolved == expect and not unresolved
           and shaped_required == len(required))
    return {"tool": TOOL, "revision": rev or "worktree", "blocks": len(blocks),
            "resolved": resolved, "shaped": shaped,
            "shape_from": shape_from, "shaped_required": shaped_required,
            "required_blocks": len(required), "unresolved": unresolved,
            "blocks_detail": per_block,
            "expect_blocks": expect,
            "floors": {"min_words": MIN_WORDS, "min_spans": MIN_SPANS,
                       "min_table_rows": MIN_TABLE_ROWS,
                       "min_table_cells": MIN_TABLE_CELLS},
            "met_target": met,
            "label": (f"blocks {len(blocks)}, resolved {resolved}, "
                      f"required-shaped {shaped_required}/{len(required)}")}


PROSE = ("- **rule**: this block states a threshold of 3 and a refusal "
         "signature and `alpha` and `beta` corpus/knowledge/2026-01-01-a.md:2-3 "
         "and carries no table at all so the shape-blind counter resolves it")
TABLE = ("- **rule**: this block states a threshold of 3 and a refusal "
         "signature and `alpha` and `beta` corpus/knowledge/2026-01-01-a.md:2-3\n"
         "  | class | signature | guard | criterion |\n"
         "  |---|---|---|---|\n"
         "  | a | `x` | g1 | QUALITY 1 |\n"
         "  | b | `y` | g2 | QUALITY 2 |\n"
         "  | c | `z` | g3 | QUALITY 3 |\n")


def prose_proof(root: str) -> dict:
    """v2 and v3 on the same fixtures: the false-green is measured, not claimed."""
    v2 = load_module(os.path.join(root, V2), "depthv2")
    tree = {"corpus/knowledge/2026-01-01-a.md": "l1\nl2\nl3\n"}
    reader = lambda p: tree[p]  # noqa: E731
    out = {}
    for name, text in (("prose", PROSE), ("table", TABLE)):
        oks = []
        for mod in (v2, sys.modules[__name__]):
            ok, _ = mod.resolve(text, reader)
            if ok:
                ok, _ = mod.shape(text)
            oks.append(ok)
        t_ok, t_info, t_problems = table_shape(text)
        oks[1] = oks[1] and t_ok  # v3 adds the table clause for required blocks
        out[name] = {"v2_accepts": oks[0], "v3_accepts": oks[1],
                     "v3_table": t_ok, "v3_table_problems": t_problems,
                     "rows": t_info["rows"]}
    out["control_killed"] = (out["prose"]["v2_accepts"] is True
                             and out["prose"]["v3_accepts"] is False
                             and out["table"]["v3_accepts"] is True)
    return out


def selftest() -> int:
    fails, ncases = [], 0

    def check(name, cond):
        nonlocal ncases
        ncases += 1
        if not cond:
            fails.append(name)

    ok, info, probs = table_shape(TABLE)
    check("table-accepted", ok and info["rows"] == 3 and probs == [])
    ok, info, probs = table_shape(PROSE)
    check("prose-refused", not ok and any(p.startswith("table:rows:") for p in probs))
    two = TABLE.replace("  | c | `z` | g3 | QUALITY 3 |\n", "")
    ok, info, probs = table_shape(two)
    check("two-rows-refused", not ok and info["rows"] == 2)
    narrow = TABLE.replace("  | c | `z` | g3 | QUALITY 3 |\n",
                           "  | c | `z` | g3 |\n")
    ok, info, probs = table_shape(narrow)
    check("three-cells-refused", not ok and info["min_cells"] == 3)
    check("block-split",
          len(rule_blocks("## Queue-drain craft v9\n- **a** x\n- **b** y\n## next\n")) == 2)
    tree = {"corpus/knowledge/2026-01-01-a.md": "l1\nl2\nl3\n"}
    ok, probs = resolve(PROSE, lambda p: tree[p])
    check("prose-resolves-like-v2", ok and probs == [])
    print(f"SELFTEST cases={ncases} failures={len(fails)} {' '.join(fails)}".rstrip())
    return 0 if not fails else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--prose-proof", action="store_true")
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev")
    ap.add_argument("--worktree", action="store_true")
    ap.add_argument("--expect-blocks", type=int)
    ap.add_argument("--shape-from", type=int, default=31)
    ap.add_argument("--expect", help="frozen label")
    ap.add_argument("--json-out")
    a = ap.parse_args(argv)
    root = os.path.abspath(a.root)
    if a.selftest:
        return selftest()
    if a.prose_proof:
        receipt = {"tool": TOOL, "proof": prose_proof(root)}
        if a.json_out:
            with open(a.json_out, "w", encoding="utf-8") as fh:
                json.dump(receipt, fh, indent=1, sort_keys=True)
        print(json.dumps(receipt["proof"], sort_keys=True))
        return 0 if receipt["proof"]["control_killed"] else 1
    rev = None if a.worktree else a.rev
    if not a.worktree and not a.rev:
        print("could-not-evaluate: --rev (or --worktree) is required", file=sys.stderr)
        return 2
    if a.expect_blocks is None:
        print("could-not-evaluate: --expect-blocks N is required (QUALITY 157)",
              file=sys.stderr)
        return 2
    try:
        receipt = count(root, rev, a.expect_blocks, a.shape_from)
    except Unevaluable as exc:
        receipt = {"tool": TOOL, "unevaluable": str(exc), "met_target": False}
    receipt["exit"] = 0 if receipt["met_target"] else 1
    if a.expect is not None:
        receipt["expect"] = a.expect
        receipt["met_target"] = receipt["met_target"] and receipt["label"] == a.expect
        receipt["exit"] = 0 if receipt["met_target"] else 1
    if a.json_out:
        with open(a.json_out, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=1, sort_keys=True)
    print(f"{receipt.get('label')} expect {receipt.get('expect_blocks')} "
          f"shaped_required {receipt.get('shaped_required')}/{receipt.get('required_blocks')} "
          f"unresolved {len(receipt.get('unresolved') or [])} "
          f"met={receipt['met_target']} exit={receipt['exit']}")
    return receipt["exit"]


if __name__ == "__main__":
    sys.exit(main())
