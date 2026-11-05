#!/usr/bin/env python3
"""depth-blocks-v4.py - round-97 counter (R97-C2, depth).

Supersedes `tools/round-91/depth-blocks-v3.py` on one count, routed by the round-96
CriticC2 attack d (`_table_rows` merged every `|` line of a block, so a padded decoy
table satisfied the shape floor while the block's own table was junk) and frozen before
data:

**The shape floor counts only the block's first table.** v3 picked the table with the
most body rows anywhere in the block (`best`), so a padded decoy could carry the floor
for a junk table. v4 evaluates header + separator + >= MIN_TABLE_ROWS body rows of
>= MIN_TABLE_CELLS cells on the FIRST table of the block (header at the earliest
`|` line followed by a separator); later tables neither rescue nor count. The
decoy-vs-real discrimination is measured by `--decoy-proof`: v3 accepts the decoy
fixture, v4 refuses it, and both accept the real table.

Everything else is unchanged from v3 (citations read at `--rev`, word/backtick floor,
`--shape-from` boundary, expect/label arithmetic). `--selftest` adds the decoy cases.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys

TOOL = "tools/round-97/depth-blocks-v4.py"
V3 = "tools/round-91/depth-blocks-v3.py"
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
    if "## Queue-drain craft " not in skill and "## Queue-drain craft" not in skill:
        raise Unevaluable("SKILL.md carries no '## Queue-drain craft' section")
    craft = skill.split("## Queue-drain craft", 1)[1].split("\n## ", 1)[0]
    return re.split(r"(?m)^- \*\*", craft)[1:]


def shape(rule: str) -> tuple[bool, list[str]]:
    """v2's floor: words and backticked spans."""
    problems = []
    words = len(rule.split())
    spans = len(re.findall(r"`[^`\n]+`", rule))
    if words < MIN_WORDS:
        problems.append(f"shape:words:{words}<{MIN_WORDS}")
    if spans < MIN_SPANS:
        problems.append(f"shape:spans:{spans}<MIN_SPANS".replace("MIN_SPANS", str(MIN_SPANS)))
    return not problems, problems


def first_table(rule: str) -> tuple[bool, dict, list[str]]:
    """The block's FIRST table must satisfy the floor; padded decoys do not count."""
    lines = [ln.strip() for ln in rule.splitlines()]
    first = None
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
        first = {"rows": len(rows), "min_cells": min(cells) if cells else 0}
        break
    if first is None:
        return False, {"rows": 0, "min_cells": 0}, ["first-table:absent"]
    problems = []
    if first["rows"] < MIN_TABLE_ROWS:
        problems.append(f"first-table:rows:{first['rows']}<{MIN_TABLE_ROWS}")
    if first["min_cells"] < MIN_TABLE_CELLS:
        problems.append(f"first-table:cells:{first['min_cells']}<{MIN_TABLE_CELLS}")
    return not problems, first, problems


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
        tok, tinfo, tproblems = first_table(rule)
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
DECOY = ("- **rule**: this block states a threshold of 3 and a refusal "
         "signature and `alpha` and `beta` corpus/knowledge/2026-01-01-a.md:2-3\n"
         "  | class | signature |\n"
         "  |---|---|\n"
         "  | a | `x` |\n"
         "  | b | `y` |\n"
         "\n"
         "  The table below pads the floor in v3's best-table view.\n"
         "  | pad1 | pad2 | pad3 | pad4 |\n"
         "  |---|---|---|---|\n"
         "  | f | `p` | guard | criterion |\n"
         "  | g | `q` | guard | criterion |\n"
         "  | h | `r` | guard | criterion |\n")


def decoy_proof(root: str) -> dict:
    """v3 and v4 on the same fixtures: the padded-decoy false-green is measured,
    not claimed."""
    v3 = load_module(os.path.join(root, V3), "depthv4proof_v3")
    out = {}
    for name, text in (("real", TABLE), ("decoy", DECOY)):
        results = {}
        for label, mod, fn in (("v3", v3, v3.table_shape), ("v4", sys.modules[__name__],
                                                           first_table)):
            ok, _info, _probs = fn(text)
            results[label] = bool(ok)
        out[name] = {"v3_accepts": results["v3"], "v4_accepts": results["v4"]}
    out["control_killed"] = (out["real"]["v3_accepts"] is True
                             and out["real"]["v4_accepts"] is True
                             and out["decoy"]["v3_accepts"] is True
                             and out["decoy"]["v4_accepts"] is False)
    return out


def selftest() -> int:
    fails, ncases = [], 0

    def check(name, cond):
        nonlocal ncases
        ncases += 1
        if not cond:
            fails.append(name)

    ok, info, probs = first_table(TABLE)
    check("table-accepted", ok and info["rows"] == 3 and probs == [])
    ok, info, probs = first_table(PROSE)
    check("prose-refused", not ok and probs == ["first-table:absent"])
    two = TABLE.replace("  | c | `z` | g3 | QUALITY 3 |\n", "")
    ok, info, probs = first_table(two)
    check("two-rows-refused", not ok and info["rows"] == 2)
    narrow = TABLE.replace("  | c | `z` | g3 | QUALITY 3 |\n",
                           "  | c | `z` | g3 |\n")
    ok, info, probs = first_table(narrow)
    check("three-cells-refused", not ok and info["min_cells"] == 3)
    # the decoy: a junk first table (2 cells) plus a padded second table; v3's
    # best-table merge accepted it, v4 refuses on the first table.
    ok, info, probs = first_table(DECOY)
    check("decoy-refused", not ok and info["rows"] == 2
          and any(p.startswith("first-table:rows:") for p in probs))
    v3 = load_module(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "..", "round-91", "depth-blocks-v3.py"), "st_v3")
    v3_ok, _i, _p = v3.table_shape(DECOY)
    check("v3-accepts-decoy", v3_ok)
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
    ap.add_argument("--decoy-proof", action="store_true")
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
    if a.decoy_proof:
        receipt = {"tool": TOOL, "proof": decoy_proof(root)}
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
