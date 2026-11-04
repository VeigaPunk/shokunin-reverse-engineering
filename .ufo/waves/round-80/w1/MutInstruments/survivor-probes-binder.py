#!/usr/bin/env python3
"""Binder survivor proofs: the assertion each surviving mutant escapes.

Each probe returns True only when the module still enforces the rule the
selftest is missing. Run: survivor-probes-binder.py <pristine> <mutant.py>...
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import pathlib
import sys


def load(path: str):
    spec = importlib.util.spec_from_file_location("binder_probe_" + pathlib.Path(path).stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def forged(mod) -> dict:
    digest = hashlib.sha256(pathlib.Path(mod.__file__).read_bytes()).hexdigest()
    return {
        "checks_total": 5, "matched": 5, "mismatches": 0, "unparsed": 0,
        "checked_at": "2026-11-04T00:00:00-03:00", "control": None,
        "duplicates": [],
        "instrument": {"path": "tools/round-80/pointer-bind.py", "sha256": digest},
        "record": {"sha256": "a" * 64, "rev": "b" * 40},
        "ok": True,
        "checks": [{"id": f"c{index}", "matched": True, "unparsed": False,
                    "path_is_declared": True, "line_start": 1, "line_end": 1,
                    "tokens": ["t"], "line_sha256": "b" * 64,
                    "delimiter_evidence": [{"token": "t", "occurrences": 1,
                                            "delimited": True}]}
                   for index in range(5)],
    }


LINES = ["a\n", '        "rea-agents@6.7.0",\n', "c\n", "d\n"]


def b6_delimited_flag(mod) -> bool:
    """Evidence that says `delimited: False` must be a defect."""
    receipt = forged(mod)
    receipt["checks"][0]["delimiter_evidence"][0]["delimited"] = False
    defects = mod.validate_receipt(receipt)["defects"]
    return any("matched without delimiter evidence" in d for d in defects)


def b13_checks_total(mod) -> bool:
    """A receipt whose checks_total disagrees with its check list must be a defect."""
    receipt = forged(mod)
    receipt["checks_total"] = 6
    defects = mod.validate_receipt(receipt)["defects"]
    return any("checks_total does not re-derive" in d for d in defects)


def b9_start_bound(mod) -> bool:
    """A pointer naming line 0 must be refused as not-1-based."""
    return mod.bind("f.json:0", ["x"], LINES)["reason"] == (
        "line range 0-0 is not a forward 1-based range")


PROBES = {"b6-drop-delimited-evidence": b6_delimited_flag,
          "b9-drop-start-bound": b9_start_bound,
          "b13-drop-checks-total": b13_checks_total}


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
