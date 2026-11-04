#!/usr/bin/env python3
"""Survivor proofs: a case that returns True on the pristine module and False on
the mutant, for every mutant the target's own `--selftest` failed to kill.

Each probe is `asserts_correct(mod) -> bool`: it encodes the assertion the
selftest is missing, and returns True only when the module still enforces it.

Usage: survivor-probes.py <pristine.py> <mutant.py> [<mutant.py> ...]
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import pathlib
import sys


def load(path: str):
    spec = importlib.util.spec_from_file_location("probe_" + pathlib.Path(path).stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


LINES = ["a\n", '        "rea-agents@6.7.0",\n', "c\n", "d\n"]


def forged(mod) -> dict:
    """The selftest's own green forged receipt, rebuilt against this module."""
    digest = hashlib.sha256(pathlib.Path(mod.__file__).read_bytes()).hexdigest()
    return {"checks_total": 5, "matched": 5, "mismatches": 0, "unparsed": 0,
            "checked_at": "2026-11-04T00:00:00-03:00", "control": None,
            "instrument": {"path": "tools/round-79/pointer-bind.py", "sha256": digest},
            "record": {"sha256": "a" * 64, "rev": "b" * 40}, "ok": True,
            "checks": [{"id": f"c{i}", "matched": True, "unparsed": False,
                        "path_is_declared": True, "line_start": 1, "line_end": 1,
                        "line_sha256": "b" * 64} for i in range(5)]}


def m3_start_bound(mod) -> bool:
    """A pointer naming line 0 must be refused as not-1-based, not rescanned."""
    return mod.bind("f.json:0", ["x"], LINES)["reason"] == (
        "line range 0-0 is not a forward 1-based range")


def m8_range_order(mod) -> bool:
    """A 'matched' check whose line range runs backwards must be a defect."""
    receipt = forged(mod)
    receipt["checks"][0]["line_start"], receipt["checks"][0]["line_end"] = 3, 2
    defects = mod.validate_receipt(receipt)["defects"]
    return any("matched without a 1-based line range" in d for d in defects)


def m9_unparsed_overlap(mod) -> bool:
    """A check that is both matched and unparsed must be a defect."""
    receipt = forged(mod)
    receipt["checks"][0]["unparsed"] = True
    receipt["unparsed"] = 1
    defects = mod.validate_receipt(receipt)["defects"]
    return any("matched and unparsed" in d for d in defects)


PROBES = {"m3-drop-start-bound": m3_start_bound,
          "m8-drop-range-order": m8_range_order,
          "m9-drop-unparsed-overlap": m9_unparsed_overlap}


def main(argv: list[str]) -> int:
    pristine = load(argv[0])
    rows = []
    for path in argv[1:]:
        mutant = load(path)
        mid = pathlib.Path(path).stem
        probe = PROBES[mid]
        rows.append({"mutant": mid,
                     "pristine_asserts_correct": bool(probe(pristine)),
                     "mutant_asserts_correct": bool(probe(mutant)),
                     "proved": bool(probe(pristine)) and not bool(probe(mutant))})
    for row in rows:
        print(json.dumps(row, sort_keys=True))
    print("PROBES proved=%d/%d" % (sum(1 for r in rows if r["proved"]), len(rows)))
    return 0 if all(r["proved"] for r in rows) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
