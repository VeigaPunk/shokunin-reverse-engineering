#!/usr/bin/env python3
"""registry-conformance.py - round-68 instrument (R68-C1, calibration).

The lane's self-assessment of its own instrument inventory is SKILL.md's
`<!-- instrument-registry v2 -->` table: one row per gate or probe, with a
verdict map the closure grades against.  The round-67 outside closure found the
table incomplete for the round it had just closed: both round-67 instruments
(`tools/round-67/avm-le-counter.py`, `tools/round-67/mutation-battery.py`) are
named by `plans/round-67-claims.md` and existed at the tip, and neither had a
row.  No lane gate compared the two inventories, so nothing caught it.

This instrument is that comparison, over the registry's own regime:

  scope      every `tools/round-N/<name>.(py|sh|mjs)` path that
             `plans/round-N-claims.md` names for its OWN round N, for N >=
             REGIME_START (41, the round the registry begins at), that EXISTS
             as a blob at --rev.  A plan citing another round's tool cites that
             round's regime, not its own.  Rounds below REGIME_START are
             reported as `legacy_unregistered` and never counted: they predate
             the registry.
  registry   the backticked cell-0 paths of the instrument-registry section of
             SKILL.md at --rev.

mismatches is four named sets, never a bare count:

  unregistered    a scope path with no registry row
  duplicate_rows  a path with more than one row
  row_absent      a row whose path is not a blob at --rev
  thin            a row whose verdict cell does not name all three exit codes
                  (grammar: the code at the start of the cell or after `;`,
                  followed by `=`/`:` or a word - `0=met`, `0 met`, `0 clean`)

`named_but_absent` (a plan names a tool that does not exist at --rev) is
reported and excluded from scope, as the round-46 census does.

Exit: 0 clean (`mismatches == 0`); 1 any mismatch; 2 could-not-evaluate
(unknown revision, absent markers, unreadable SKILL.md or plans, bad argv).

--selftest runs the pure functions over in-memory fixtures and asserts the
registered case inventory (QUALITY #109); it never runs git and never writes
outside an optional --json-out.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

TOOL = "tools/round-68/registry-conformance.py"
REGIME_START = 41
MARK_OPEN = "<!-- instrument-registry v2 -->"
MARK_CLOSE = "<!-- /instrument-registry -->"
PLAN_RE = re.compile(r"^plans/round-(\d+)-claims\.md$")
TOOL_RE = re.compile(r"tools/round-\d+[A-Za-z0-9._/-]*?\.(?:py|sh|mjs)(?![A-Za-z0-9._-])")
ROW_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|")
VERDICT_RE = (re.compile(r"(?:^|[;|]\s*|\s)0\s*(?:[=:]|\s+[A-Za-z(])"),
              re.compile(r"(?:^|[;|]\s*|\s)1\s*(?:[=:]|\s+[A-Za-z(])"),
              re.compile(r"(?:^|[;|]\s*|\s)2\s*(?:[=:]|\s+[A-Za-z(])"))

REGISTERED_CASES = [
    "clean",
    "unregistered",
    "duplicate-rows",
    "row-absent",
    "thin-cell",
    "legacy-excluded",
    "named-but-absent",
    "missing-markers",
    "verdict-grammar",
    "empty-registry",
    "case-inventory",
]


class Unevaluable(Exception):
    """Exit-2 class: the census cannot be computed, so it scores nothing."""


def registry_rows(skill_text: str) -> list[dict]:
    if skill_text.count(MARK_OPEN) != 1 or skill_text.count(MARK_CLOSE) != 1:
        raise Unevaluable("instrument-registry markers absent or doubled")
    body = skill_text.split(MARK_OPEN, 1)[1].split(MARK_CLOSE, 1)[0]
    rows = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        m = ROW_RE.match(line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        rows.append({"path": m.group(1), "cells": len(cells),
                     "verdict": cells[2] if len(cells) > 2 else ""})
    return rows


def plan_scope(plans: dict[str, str]) -> tuple[list[str], list[str], list[str]]:
    """(regime paths, legacy paths, named_but_absent paths) - sorted, distinct."""
    regime, legacy = set(), set()
    named = set()
    for path, text in plans.items():
        m = PLAN_RE.match(path)
        if not m:
            continue
        round_no = int(m.group(1))
        own = f"tools/round-{round_no}/"
        for tool in TOOL_RE.findall(text):
            tool = tool.rstrip(".").rstrip("/")
            if not re.search(r"\.(py|sh|mjs)$", tool):
                continue
            if not tool.startswith(own):
                continue  # a foreign round's tool belongs to that round's regime
            named.add(tool)
            (regime if round_no >= REGIME_START else legacy).add(tool)
    return sorted(regime), sorted(legacy), sorted(named)


def census(plans: dict[str, str], skill_text: str, existing: set[str]) -> dict:
    """Pure census over plan texts + SKILL.md + the blob set at the revision."""
    rows = registry_rows(skill_text)
    regime, legacy, named = plan_scope(plans)
    scope = [p for p in regime if p in existing]
    named_but_absent = sorted(p for p in named if p not in existing)
    by_path: dict[str, list[dict]] = {}
    for row in rows:
        by_path.setdefault(row["path"], []).append(row)
    unregistered = sorted(p for p in scope if p not in by_path)
    duplicate_rows = sorted(p for p, r in by_path.items() if len(r) > 1)
    row_absent = sorted(p for p in by_path if p not in existing)
    thin = sorted(p for p, r in by_path.items()
                  if not all(rx.search(r[0]["verdict"]) for rx in VERDICT_RE))
    legacy_unregistered = sorted(p for p in legacy if p not in by_path and p in existing)
    mismatches = len(unregistered) + len(duplicate_rows) + len(row_absent)
    return {
        "schema": "kaidoku-r68-registry-conformance-v1",
        "claim": "R68-C1",
        "regime_start_round": REGIME_START,
        "scope_size": len(scope),
        "registry_rows": len(rows),
        "registry_paths": len(by_path),
        "unregistered": unregistered,
        "duplicate_rows": duplicate_rows,
        "row_absent": row_absent,
        "thin": thin,
        "legacy_unregistered": legacy_unregistered,
        "named_but_absent": named_but_absent,
        "mismatches": mismatches,
        "ok": mismatches == 0 and len(scope) > 0,
    }


def git(root: str, *argv: str) -> str:
    try:
        return subprocess.run(["git", "-C", root, *argv], check=True,
                              capture_output=True, text=True).stdout
    except subprocess.CalledProcessError as exc:
        raise Unevaluable(f"git {' '.join(argv)} failed: rc={exc.returncode}") from exc


def read_revision(root: str, rev: str) -> tuple[dict[str, str], str, set[str]]:
    try:
        ls = git(root, "ls-tree", "-r", "--name-only", rev, "--", "plans").splitlines()
    except Unevaluable:
        ls = []
    plans = {}
    for path in ls:
        if PLAN_RE.match(path):
            try:
                plans[path] = git(root, "show", f"{rev}:{path}")
            except Unevaluable:
                continue
    try:
        skill = git(root, "show", f"{rev}:SKILL.md")
    except Unevaluable as exc:
        raise Unevaluable("SKILL.md unreadable at --rev") from exc
    existing = set(git(root, "ls-tree", "-r", "--name-only", rev, "--", "tools").splitlines())
    return plans, skill, existing


def run_score(root: str, rev: str, out: str | None) -> int:
    plans, skill, existing = read_revision(root, rev)
    result = census(plans, skill, existing)
    result["rev"] = rev
    result["instrument"] = {
        "path": TOOL,
        "sha256": __import__("hashlib").sha256(open(__file__, "rb").read()).hexdigest(),
        "rev": git(root, "log", "-1", "--format=%H", "--", TOOL).strip() or None,
    }
    text = json.dumps(result, indent=1, sort_keys=True)
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(text)
    return 0 if result["ok"] else 1


def selftest() -> int:
    def skill(rows: list[str]) -> str:
        return "\n".join([MARK_OPEN, "| tool | g | v | s | p | w | o |",
                          "|---|---|---|---|---|---|---|", *rows, MARK_CLOSE, ""])

    def row(path: str, verdict: str = "0=met; 1=not met; 2=could-not-evaluate") -> str:
        return f"| `{path}` | g | {verdict} | s | p | w | o |"

    execs = {f"tools/round-{n}/a.py" for n in (41, 50, 67)}
    cases = []
    plan67 = "plans/round-67-claims.md"
    plan40 = "plans/round-40-claims.md"
    clean_skill = skill([row(p) for p in sorted(execs)])
    clean_plans = {plan67: "uses `tools/round-67/a.py` and tools/round-50/a.py",
                   plan40: "uses tools/round-40/a.py"}
    r = census(clean_plans, clean_skill, execs | {"tools/round-40/a.py"})
    cases.append(("clean", r["ok"] and r["mismatches"] == 0 and r["scope_size"] == 1))

    r = census({plan67: "uses tools/round-67/a.py, tools/round-67/b.py"},
               skill([row("tools/round-67/a.py")]), execs | {"tools/round-67/b.py"})
    cases.append(("unregistered", r["unregistered"] == ["tools/round-67/b.py"]
                  and r["mismatches"] == 1))

    r = census(clean_plans, skill([row("tools/round-67/a.py"),
                                   row("tools/round-67/a.py"),
                                   row("tools/round-50/a.py")]), execs)
    cases.append(("duplicate-rows", r["duplicate_rows"] == ["tools/round-67/a.py"]
                  and r["mismatches"] == 1))

    r = census(clean_plans, skill([row("tools/round-67/a.py"),
                                   row("tools/round-50/a.py"),
                                   row("tools/round-99/gone.py")]),
               execs | {"tools/round-99/other.py"})
    cases.append(("row-absent", r["row_absent"] == ["tools/round-99/gone.py"]
                  and r["mismatches"] == 1))

    r = census(clean_plans, skill([row("tools/round-67/a.py", "0=met; 1=not met"),
                                   row("tools/round-50/a.py")]), execs)
    cases.append(("thin-cell", r["thin"] == ["tools/round-67/a.py"] and r["mismatches"] == 1))

    r = census({plan40: "uses tools/round-40/old.py"}, skill([]),
               {"tools/round-40/old.py"})
    cases.append(("legacy-excluded", r["mismatches"] == 0
                  and r["legacy_unregistered"] == ["tools/round-40/old.py"]
                  and r["scope_size"] == 0))

    r = census({plan67: "uses tools/round-67/a.py and tools/round-67/ghost.py"},
               skill([row("tools/round-67/a.py")]), execs)
    cases.append(("named-but-absent", r["named_but_absent"] == ["tools/round-67/ghost.py"]
                  and r["ok"] and r["scope_size"] == 1))

    try:
        census(clean_plans, "no markers here", execs)
        cases.append(("missing-markers", False))
    except Unevaluable:
        cases.append(("missing-markers", True))

    plain = census(clean_plans, skill([row("tools/round-67/a.py", "0 met (x); 1 not met (y); 2 could-not-evaluate (z)"),
                                       row("tools/round-50/a.py", "0 clean; 1 defect; 2 unevaluable")]),
                   execs)
    cases.append(("verdict-grammar", plain["thin"] == [] and plain["mismatches"] == 0))

    r = census(clean_plans, skill([]), execs)
    cases.append(("empty-registry", r["mismatches"] == 1
                  and r["unregistered"] == ["tools/round-67/a.py"]))

    executed = [name for name, _ in cases] + ["case-inventory"]
    cases.append(("case-inventory", executed == REGISTERED_CASES))

    failed = [name for name, ok in cases if not ok]
    print(json.dumps({"selftest": TOOL, "cases": len(cases), "failed": failed,
                      "ok": not failed}, indent=1))
    return 0 if not failed else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root")
    ap.add_argument("--rev")
    ap.add_argument("--json-out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.root or not args.rev:
        print("registry-conformance: --root and --rev are required", file=sys.stderr)
        return 2
    try:
        return run_score(args.root, args.rev, args.json_out)
    except Unevaluable as exc:
        print(json.dumps({"schema": "kaidoku-r68-registry-conformance-v1",
                          "unevaluable": str(exc), "claim": "R68-C1"}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
