#!/usr/bin/env python3
"""Independent re-derivation of the R68-C1 registry-conformance census.

Written from the regime prose (plan + atom A4) only; it does not import,
exec, or read the frozen instrument's functions.  It reads git objects at a
revision with `git -C <root> ls-tree` / `git -C <root> show`.

Grammar choices (deliberately simpler than the instrument):
  * plan text -> tool paths:  tools/round-<N>/<anything>.{py,sh,mjs} with a
    word boundary after the extension.  The captured <N> is the round the
    path belongs to; scope only keeps <N> == the plan's own round.
  * registry rows: lines inside the two markers whose first cell is backticked.
  * thin: verdict cell must show each of 0, 1, 2 in "verdict position"
    (start of cell, or after ; | or whitespace, followed by =/: or a word).
    A loose grammar (bare code mention anywhere in the cell) is also reported
    so a divergence between the two is visible.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

MARK_OPEN = "<!-- instrument-registry v2 -->"
MARK_CLOSE = "<!-- /instrument-registry -->"
PLAN_RE = re.compile(r"^plans/round-(\d+)-claims\.md$")
# own extractor grammar
TOOL_RE = re.compile(r"tools/round-(\d+)/[A-Za-z0-9._/-]*?\.(?:py|sh|mjs)\b")
ROW_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|")
CODE_POS = re.compile(r"(?:^|[;|]|\s)([012])(?=[=:]|\s+[A-Za-z(])")


def sh(root: str, *argv: str) -> str:
    p = subprocess.run(["git", "-C", root, *argv], capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(f"git {' '.join(argv)} rc={p.returncode}: {p.stderr.strip()}")
    return p.stdout


def read_rev(root: str, rev: str):
    plans = {}
    for path in sh(root, "ls-tree", "-r", "--name-only", rev, "--", "plans").splitlines():
        m = PLAN_RE.match(path)
        if m:
            plans[path] = sh(root, "show", f"{rev}:{path}")
    skill = sh(root, "show", f"{rev}:SKILL.md")
    existing = set(sh(root, "ls-tree", "-r", "--name-only", rev, "--", "tools").splitlines())
    return plans, skill, existing


def rows_of(skill: str):
    if skill.count(MARK_OPEN) != 1 or skill.count(MARK_CLOSE) != 1:
        raise SystemExit("markers absent or doubled")
    body = skill.split(MARK_OPEN, 1)[1].split(MARK_CLOSE, 1)[0]
    rows = []
    for line in body.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        m = ROW_RE.match(s)
        if not m:
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        rows.append({"path": m.group(1),
                     "verdict": cells[2] if len(cells) > 2 else "",
                     "cells": len(cells)})
    return rows


def codes(cell: str):
    return {int(m.group(1)) for m in CODE_POS.finditer(cell)}


def loose_codes(cell: str):
    return {int(c) for c in "012" if re.search(rf"(?<![\w.]){c}(?![\w.])", cell)}


def named_paths(plans):
    """{plan_round: {path: [source plans]}} for own-round paths only."""
    own, foreign = {}, {}
    for plan_path, text in plans.items():
        m = PLAN_RE.match(plan_path)
        if not m:
            continue
        rnd = int(m.group(1))
        for pm in TOOL_RE.finditer(text):
            path = pm.group(0)
            bro = int(pm.group(1))
            if bro == rnd and path.startswith(f"tools/round-{rnd}/"):
                own.setdefault(rnd, {}).setdefault(path, []).append(plan_path)
            else:
                foreign.setdefault(rnd, {}).setdefault(path, set()).add(plan_path)
    return own, foreign


def census(plans, skill, existing, extra_rows=()):
    rows = rows_of(skill)
    for p in extra_rows:
        rows.append({"path": p, "verdict": "0=met; 1=not met; 2=could-not-evaluate",
                     "cells": 7, "simulated": True})
    own, foreign = named_paths(plans)
    regime_all = sorted({p for rnd, d in own.items() if rnd >= 41 for p in d})
    legacy_all = sorted({p for rnd, d in own.items() if rnd < 41 for p in d})
    scope = [p for p in regime_all if p in existing]
    legacy_existing = [p for p in legacy_all if p in existing]
    absent_named = sorted(p for p in regime_all + legacy_all if p not in existing)

    by_path = {}
    for r in rows:
        by_path.setdefault(r["path"], []).append(r)
    unregistered = [p for p in scope if p not in by_path]
    duplicates = sorted(p for p, r in by_path.items() if len(r) > 1)
    row_absent = sorted(p for p in by_path if p not in existing)
    thin_strict = sorted(p for p, r in by_path.items() if codes(r[0]["verdict"]) != {0, 1, 2})
    thin_loose = sorted(p for p, r in by_path.items() if loose_codes(r[0]["verdict"]) != {0, 1, 2})
    legacy_unregistered = [p for p in legacy_existing if p not in by_path]
    mismatches = len(unregistered) + len(duplicates) + len(row_absent) + len(thin_strict)
    return {
        "scope_size": len(scope),
        "registry_rows": len(rows),
        "registry_paths": len(by_path),
        "unregistered": unregistered,
        "duplicate_rows": duplicates,
        "row_absent": row_absent,
        "thin_strict": thin_strict,
        "thin_loose": thin_loose,
        "legacy_unregistered": legacy_unregistered,
        "named_but_absent": absent_named,
        "mismatches": mismatches,
        "ok": mismatches == 0 and len(scope) > 0,
        "per_round_scope": {str(r): sorted(p for p in d if p in existing)
                            for r, d in sorted(own.items()) if r >= 41},
        "foreign_citations": {str(r): {p: sorted(s) for p, s in sorted(d.items())}
                              for r, d in sorted(foreign.items())},
        "multi_named": {p: sorted(set(src)) for r, d in own.items()
                        for p, src in d.items() if len(set(src)) > 1},
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--json-out")
    ap.add_argument("--simulate-repair", action="store_true",
                    help="add the four rows atom A5 names and recompute (simulation)")
    args = ap.parse_args()
    plans, skill, existing = read_rev(args.root, args.rev)
    extra = ()
    if args.simulate_repair:
        extra = ("tools/round-67/avm-le-counter.py",
                 "tools/round-67/mutation-battery.py",
                 "tools/round-68/registry-conformance.py",
                 "tools/round-68/packed-elf.py")
        extra = tuple(p for p in extra if p not in {r["path"] for r in rows_of(skill)})
    res = census(plans, skill, existing, extra)
    res["rev"] = args.rev
    res["simulated_extra_rows"] = list(extra)
    text = json.dumps(res, indent=1, sort_keys=True)
    if args.json_out:
        open(args.json_out, "w", encoding="utf-8").write(text + "\n")
    print(text)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
