#!/usr/bin/env python3
"""Prove each named 'missing case' would kill its surviving mutant."""

import importlib.util
import json
import os
import sys

S = os.path.dirname(os.path.abspath(__file__))
PRISTINE = {"pointer-bind": os.path.join(S, "pointer-bind.orig.py"),
            "gate-mutation": os.path.join(S, "gate-mutation.orig.py")}
MUT = os.path.join(S, "run", "mutants")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def pb_forged(line_start=1, line_end=1):
    return {"checks_total": 5, "matched": 5, "mismatches": 0, "unparsed": 0,
            "record": {"sha256": "a" * 64}, "ok": True,
            "checks": [{"id": f"c{i}", "matched": True, "unparsed": False,
                        "line_start": line_start if i == 0 else 1,
                        "line_end": line_end if i == 0 else 1,
                        "line_sha256": "b" * 64} for i in range(5)]}


def gm_forged(pristine=None, applied=True, case_absent=False):
    muts = [{"id": f"m{i}", "declared_case": "c", "killed": True,
             "applied": applied, "case_absent": case_absent,
             "failed_cases": ["c"]} for i in range(8)]
    return {"mutants_total": 8, "killed": 8, "survivors": 0, "survivor_ids": [],
            "declared_case_hits": 8,
            "target": {"sha256": "a" * 64},
            "target_pin": {"expected": "a" * 64, "matched": True},
            "pristine": pristine or {"ok": True, "failures": 0},
            "ok": True, "mutants": muts}


RECORD = ("Devin `rea-agents@6.7.0` (`/home/x/devin.json:7`)\n"
          "OMP `rea-agents@6.7.0` (`/home/x/omp.json:8`)\n"
          "Kimi `rea-agents@6.7.0` (`/home/x/kimi.toml:4126`)\n"
          "(`/home/x/.bashrc:28-29` (were `:23-24` before the edit))\n")


def case_pb_e(mod):
    return bool(mod.validate_receipt(pb_forged(0, 0))["defects"])


def case_pb_f(mod):
    mod.git_show = lambda root, rev, path: RECORD.encode()
    receipt = mod.battery(".", "fixture", None)
    ghidra = [c for c in receipt["checks"] if c["id"] == "ghidra-version"][0]
    return ghidra["matched"] is False and ghidra["unparsed"] is True


def case_gm_f(mod):
    return bool(mod.validate_receipt(gm_forged(case_absent=True))["defects"])


def case_gm_g(mod):
    return bool(mod.validate_receipt(
        gm_forged(pristine={"ok": True, "failures": 2}))["defects"])


def case_gm_h(mod):
    return bool(mod.validate_receipt(gm_forged(applied=False))["defects"])


CASES = {
    "pb-e-validate-range-guard": ("pointer-bind", case_pb_e,
                                  "a forged pointer receipt whose matched check "
                                  "sits at line 0 must yield a validate defect"),
    "pb-f-nonparse-matched": ("pointer-bind", case_pb_f,
                              "a record cell that does not parse must come back "
                              "matched False and unparsed True from battery"),
    "gm-f-validate-no-guard": ("gate-mutation", case_gm_f,
                               "a forged gate receipt with killed true, case_absent "
                               "true and its declared case in failed_cases must yield "
                               "a validate defect"),
    "gm-g-pristine-guard": ("gate-mutation", case_gm_g,
                            "a forged gate receipt with pristine.ok true and "
                            "failures 2 must yield a validate defect"),
    "gm-h-applied-guard": ("gate-mutation", case_gm_h,
                           "a forged gate receipt with killed true and applied false "
                           "must yield a validate defect"),
}

BASELINE = {}
for name, path in PRISTINE.items():
    BASELINE[name] = load("base_" + name.replace("-", "_"), path)

rows = []
ok_all = True
for mid, (inst, fn, sentence) in CASES.items():
    base_val = fn(BASELINE[inst])
    mut_val = fn(load("mut_" + mid.replace("-", "_"), os.path.join(MUT, mid + ".py")))
    kills = base_val is True and mut_val is False
    ok_all &= kills
    rows.append({"missing_case_for": mid, "instrument": inst,
                 "case": sentence, "pristine_value": base_val,
                 "mutant_value": mut_val, "would_kill": kills})

print(json.dumps({"schema": "kaidoku-r79-missing-case-proof-v1",
                  "rows": rows, "all_kill": ok_all}, indent=1, sort_keys=True))
sys.exit(0 if ok_all else 1)
