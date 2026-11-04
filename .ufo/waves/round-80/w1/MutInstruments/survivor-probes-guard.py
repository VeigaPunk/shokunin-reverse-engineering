#!/usr/bin/env python3
"""Guard-battery survivor proofs: the five assertions its selftest omits.

Each probe returns True only when the module still enforces the rule the
selftest is missing. Run: survivor-probes-guard.py <pristine> <mutant.py>...
"""

from __future__ import annotations

import importlib.util
import json
import pathlib
import sys


def load(path: str):
    spec = importlib.util.spec_from_file_location("guard_probe_" + pathlib.Path(path).stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def g3_prefix_binds_other(mod) -> bool:
    """A row whose prefix matches one clause that is not the declared one is a defect."""
    clauses = [
        {"clause_id": "G01", "message": "alpha beta", "bound": False, "killed": False},
        {"clause_id": "G02", "message": "beta gamma", "bound": False, "killed": False},
    ]
    rows = [{"id": "G01-x", "clause_id": "G01", "slug": "x", "trigger": "t",
             "prefix": "beta", "case": "red-x", "block_line": 1}]
    binding = mod.bind_rows([dict(c) for c in clauses], rows,
                            'case("red-x", 1, 1)\n')
    return any("binds G02, not G01" in defect for defect in binding["defects"])


def g8_absent_case_reason(mod) -> bool:
    """An absent declared case is reported as absent, not as a passing case."""
    entry = mod.judge_mutant("red-alpha", True, 0, ({"other": False}, 1, 1))
    return entry["reason"] == "declared case absent from the mutant output"


def g9_verdict_rows(mod) -> bool:
    """A row count that disagrees with the guard count must fail the verdict."""
    return mod.verdict_exit(2, 1, 2, 0, 0) == 1


def g10_verdict_survivors(mod) -> bool:
    """One surviving clause must fail the verdict."""
    return mod.verdict_exit(1, 1, 1, 1, 0) == 1


def g12_target_pin(mod) -> bool:
    """target_pin.matched must re-derive from expected/actual."""
    receipt, blobs = mod.synthetic_receipt()
    receipt["target_pin"]["matched"] = False  # expected == actual, so re-derive is True
    receipt["ok"] = False                     # keep ok re-derivable so only the pin guard fires
    defects = mod.validate_receipt(receipt, blobs=blobs, recheck_pristine=False)["defects"]
    return any("target_pin.matched does not re-derive" in defect for defect in defects)


def g13_guards_rederive(mod) -> bool:
    """`guards` must re-derive from the clause list."""
    receipt, blobs = mod.synthetic_receipt()
    receipt["guards"] = 99
    defects = mod.validate_receipt(receipt, blobs=blobs, recheck_pristine=False)["defects"]
    return any("guards does not re-derive from the clause list" in defect
               for defect in defects)


PROBES = {"g3-drop-prefix-binds-other": g3_prefix_binds_other,
          "g8-drop-case-present": g8_absent_case_reason,
          "g9-verdict-drop-rows": g9_verdict_rows,
          "g10-verdict-drop-survivors": g10_verdict_survivors,
          "g12-drop-target-pin": g12_target_pin,
          "g13-drop-guards-rederive": g13_guards_rederive}


def main(argv: list[str]) -> int:
    pristine = load(argv[0])
    rows = []
    for path in argv[1:]:
        mutant = load(path)
        mid = pathlib.Path(path).stem
        probe = PROBES[mid]
        before = bool(probe(pristine))
        after = bool(probe(mutant))
        rows.append({"mutant": mid, "pristine_asserts_correct": before,
                     "mutant_asserts_correct": after, "proved": before and not after})
    for row in rows:
        print(json.dumps(row, sort_keys=True))
    print("PROBES proved=%d/%d" % (sum(1 for r in rows if r["proved"]), len(rows)))
    return 0 if all(r["proved"] for r in rows) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
