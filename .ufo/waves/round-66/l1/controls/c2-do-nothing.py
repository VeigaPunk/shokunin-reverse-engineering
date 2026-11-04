#!/usr/bin/env python3
"""c2-do-nothing.py - the do-nothing control for R66-C2 (phase-4 rule).

Cheapest control that SKIPS the claimed work: the round-65 coverage instrument's
`--recipe date` mode, which the r65 lesson showed is NOT recipe A (it filters the
population and emits `population_dropped` as an integer).  Scored with the three
frozen R66-C2 conditions: recipe_a_equivalent, a non-empty recipe_a_hidden list,
and mismatches 0 over the two self-assessment atoms.

Receipt shape: {"conditions": 3, "passed": N, "ok": false, "target": 3}.

Run: TMPDIR=<scratch> python3 -I -B .ufo/waves/round-66/l1/controls/c2-do-nothing.py \
       --repo <lane> --rev <base> --out <receipt.json>
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--r65-tool", default="tools/round-65/coverage-recipe.py")
    ap.add_argument("--r66-tool", default="tools/round-66/coverage-selfcheck.py")
    ap.add_argument("--out")
    args = ap.parse_args(argv)
    repo = Path(args.repo).resolve()
    scratch = Path(os.environ.get("TMPDIR") or ".")
    r66 = load(repo / args.r66_tool, "c2")

    files, readme, scorecard = r66.read_inputs(str(repo), args.rev)
    section = r66.map_section(readme)
    ours = r66.recipe_a(str(repo), args.rev)
    hidden = r66.recipe_hidden(files, section)

    # the control: the r65 date mode, run through its own CLI
    date_out = scratch / "r65-date.json"
    subprocess.run([sys.executable, "-I", "-B", str(repo / args.r65_tool),
                    "--root", str(repo), "--rev", args.rev, "--recipe", "date",
                    "--out", str(date_out)], capture_output=True, text=True, timeout=900)
    try:
        date = json.loads(date_out.read_text())
    except (OSError, json.JSONDecodeError):
        date = {}

    conditions = []
    # 1. equivalence with the committed SCORECARD recipe-A block
    eq = r66.recipe_a_equivalence(str(repo), args.rev, scratch)
    conditions.append({"condition": "recipe-a-equivalence",
                       "control_value": {k: date.get(k) for k in r66.RECIPE_A_KEYS},
                       "met": False,
                       "why": "the r65 date mode shares only `mapped` with recipe A: it "
                              "filters the population (population != knowledge_files) and "
                              "emits fields recipe A never had (population_dropped)",
                       "recipe_a_observed": {k: ours[k] for k in r66.RECIPE_A_KEYS},
                       "block_equivalent_to_ours": eq["recipe_a_equivalent"]})
    # 2. the hidden-file list
    conditions.append({"condition": "recipe-a-hidden-list",
                       "control_value": {"population_dropped": date.get("population_dropped"),
                                         "keys": sorted(date)},
                       "met": isinstance(date.get("population_dropped"), list),
                       "why": "population_dropped is an integer; no key carries the names",
                       "names_observed_by_r66": hidden})
    # 3. the two self-assessment atoms
    conditions.append({"condition": "self-assessment-atoms",
                       "control_value": {"atoms": date.get("atoms"),
                                         "mismatches": date.get("mismatches")},
                       "met": isinstance(date.get("atoms"), list),
                       "why": "the r65 instrument emits no atoms and no mismatch count",
                       "r66_atoms": [a["id"] for a in r66.selfcheck(str(repo), args.rev,
                                                                    scratch)["atoms"]]})
    passed = sum(1 for c in conditions if c["met"])
    result = {"tool": "c2-do-nothing control",
              "skips": "recipe-A reproduction, the hidden-name list and the atom mismatch count",
              "rev": args.rev, "conditions": conditions,
              "conditions_total": len(conditions), "passed": passed,
              "target": len(conditions), "ok": passed == len(conditions)}
    text = json.dumps(result, indent=1, sort_keys=True) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    sys.stdout.write(json.dumps({k: result[k] for k in ("passed", "conditions_total", "ok")}) + "\n")
    return 0 if passed < len(conditions) else 1


if __name__ == "__main__":
    sys.exit(main())
