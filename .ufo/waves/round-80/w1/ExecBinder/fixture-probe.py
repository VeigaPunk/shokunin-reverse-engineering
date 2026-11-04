#!/usr/bin/env python3
"""Score the frozen round-80 strictness fixtures against both binders.

This is the seat's own probe, not the L1's `tools/round-80/strictness-battery.py`:
it exists to show the candidate's behaviour on the exact fixtures the frozen
battery will read, and to reproduce the round-79 control's weakness.

    python3 -I -B fixture-probe.py --root <lane> \
        --candidate <pointer-bind.py> --control tools/round-79/pointer-bind.py \
        --fixtures .ufo/waves/round-80/l1/fixtures/strictness.json \
        [--json-out <receipt>]

A red `bind` case is a false green when the implementation reports `matched`.
A red `record` case is a false green when the appended duplicate cell is
collapsed (fewer than two cells with the fixture's `cell_id`); a candidate that
also declares the id in `parse_record`'s duplicates list is stricter still.
A green control is a refusal when `matched` is false.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import sys


def load(path: str):
    spec = importlib.util.spec_from_file_location(
        "binder_" + pathlib.Path(path).stem.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_record(module, text: str):
    """Accept round 79's 2-tuple and round 80's (checks, unparsed, duplicates)."""
    out = module.parse_record(text)
    if isinstance(out, tuple) and len(out) == 3:
        checks, unparsed, duplicates = out
    else:
        checks, unparsed = out
        counts: dict[str, int] = {}
        for check in checks:
            counts[check.get("id")] = counts.get(check.get("id"), 0) + 1
        duplicates = [key for key, count in counts.items() if count > 1]
    return checks, unparsed, list(duplicates)


def score(module, fixtures: dict) -> dict:
    red: list[dict] = []
    green: list[dict] = []
    for case in fixtures["red_cases"]:
        if case["kind"] == "bind":
            result = module.bind(case["pointer"], case["tokens"], case["lines"])
            refused = not result["matched"]
            detail = {"id": case["id"], "kind": "bind",
                      "matched": result["matched"],
                      "reason": result.get("reason", "")}
        else:
            text = fixtures["record_template"] + case["append_cell"].rstrip("\n") + "\n"
            checks, unparsed, duplicates = parse_record(module, text)
            cells = sum(1 for check in checks if check.get("id") == case["cell_id"])
            collapsed = cells < 2
            declared = case["cell_id"] in duplicates
            refused = not collapsed and declared
            detail = {"id": case["id"], "kind": "record",
                      "checks": len(checks), "cells": cells,
                      "duplicates": duplicates,
                      "collapsed": collapsed, "declared": declared}
        red.append({"id": case["id"], "false_green": not refused, **detail})
    for case in fixtures["green_cases"]:
        result = module.bind(case["pointer"], case["tokens"], case["lines"])
        green.append({"id": case["id"], "refused": not result["matched"],
                      "matched": result["matched"]})
    return {
        "false_greens": sum(1 for item in red if item["false_green"]),
        "green_refusals": sum(1 for item in green if item["refused"]),
        "red": red,
        "green": green,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--control", required=True)
    ap.add_argument("--fixtures", required=True)
    ap.add_argument("--json-out")
    args = ap.parse_args(argv)
    root = pathlib.Path(args.root).resolve()
    fixtures = json.loads((root / args.fixtures).read_text(encoding="utf-8"))
    candidate = score(load(str(root / args.candidate)), fixtures)
    control = score(load(str(root / args.control)), fixtures)
    receipt = {
        "schema": "kaidoku-r80-execbinder-fixture-probe-v1",
        "fixtures": args.fixtures,
        "fixture_sha256": __import__("hashlib").sha256(
            (root / args.fixtures).read_bytes()).hexdigest(),
        "cases": len(fixtures["red_cases"]),
        "green_cases": len(fixtures["green_cases"]),
        "candidate": {key: candidate[key] for key in ("false_greens", "green_refusals")},
        "control": {key: control[key] for key in ("false_greens", "green_refusals")},
        "detail": {"candidate": candidate, "control": control},
    }
    receipt["pass"] = bool(receipt["candidate"]["false_greens"] == 0
                           and receipt["candidate"]["green_refusals"] == 0
                           and receipt["control"]["false_greens"] == 4
                           and receipt["control"]["green_refusals"] == 0
                           and receipt["cases"] == 4
                           and receipt["green_cases"] == 2)
    text = json.dumps(receipt, indent=1, sort_keys=True) + "\n"
    if args.json_out:
        pathlib.Path(args.json_out).write_text(text, encoding="utf-8")
    print(json.dumps({key: receipt[key] for key in
                      ("cases", "green_cases", "candidate", "control", "pass")},
                     sort_keys=True))
    return 0 if receipt["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
