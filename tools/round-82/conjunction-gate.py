#!/usr/bin/env python3
"""R82-C1: full-conjunction enforcement over the frozen round-81 record counter.

The frozen round-81 counter (tools/round-81/record-integration.py, sha256
52c829c604a5aac9306458cc6291b8cc648d3999ccf2eec0348666e582d524d6) derives its
`killed` verdict from pristine exit, both SELFTEST summaries, mutant exit and
one declared-case detector, and enforces neither a pristine population floor,
nor zero pristine failures, nor the frozen binder digest it records (M81-8:
its `ok` is true on pristine [1,0] and [11,3]; a swapped binder is unchecked).

This gate re-derives that frozen rule from pinned bytes and scores the FULL
declared conjunction on the retained round-81 receipts and forged variants of
them. It is a record-integrity instrument for the lane's own evidence layer;
it grants no domain coverage or REA capability.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

COUNTER_PATH = "tools/round-81/record-integration.py"
COUNTER_SHA256 = "52c829c604a5aac9306458cc6291b8cc648d3999ccf2eec0348666e582d524d6"
BINDER_PATH = "tools/round-80/pointer-bind.py"
BINDER_SHA256 = "a5755ba1884f0c8d695d16289edbf5dff420e72d7552d424c2cc2df7bb94a438"
CASE = "record-fixture-committed-clean"
PRISTINE_FLOOR = 11
WRONG_BINDER = "deadbeef" * 8
ORIGINAL_CASES = [
    "green-strict-refuses-every-red",
    "green-strict-refuses-no-green",
    "red-loose-accepts-reds",
    "red-refuse-all-fails-greens",
    "red-duplicate-without-signal",
    "red-duplicate-signal-with-collapsed-count",
    "green-validate-consistent",
    "red-validate-tampered-false-greens",
    "red-validate-control-not-reproducing",
]
LANDING = ".ufo/waves/round-81/l1/scores/c2-at-landing.json"
FORGED_UNDER = ".ufo/waves/round-81/w1/ExecCounter/undersized-pristine.json"
FORGED_DIRTY = ".ufo/waves/round-81/w1/ExecCounter/dirty-pristine-summary.json"
SCHEMA = "kaidoku-r82-conjunction-gate-v1"

DECLARED_RULES = [
    "binder_digest_mismatch",
    "pristine_exit_nonzero",
    "pristine_failures_nonzero",
    "pristine_cases_below_floor",
    "frozen_rule_not_killed",
    "survivors_not_zero",
    "mutants_not_one",
    "original_cases_absent",
    "detector_absent_or_passing",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def get(root: str, rev: str, path: str) -> bytes:
    return subprocess.check_output(["git", "-C", root, "show", f"{rev}:{path}"])


def load_receipt(root: str, rev: str, path: str):
    return json.loads(get(root, rev, path).decode("utf-8"))


# ---------------------------------------------------------------------------
# the frozen rule, re-derived verbatim from the pinned counter bytes
# ---------------------------------------------------------------------------

def frozen_killed(receipt: dict) -> bool:
    """Byte-equivalent re-implementation of the pinned counter's `killed`.

    tools/round-81/record-integration.py: killed = (pristine.exit == 0
    and pristine.summary is not None and mutant.summary is not None
    and mutant.exit == 1 and len(detector) == 1 and detector[0].pass is False)
    with detector = mutant cases whose `case` == CASE. The rule ignores the
    pristine population, the pristine failure count and the receipt's
    binder_sha256 field -- that is the documented deficiency this gate closes.
    """
    pristine = receipt.get("pristine") or {}
    mutant = receipt.get("mutant") or {}
    cases = mutant.get("cases") or []
    detector = [r for r in cases if isinstance(r, dict) and r.get("case") == CASE]
    return bool(
        pristine.get("exit") == 0
        and pristine.get("summary") is not None
        and mutant.get("summary") is not None
        and mutant.get("exit") == 1
        and len(detector) == 1
        and detector[0].get("pass") is False
    )


def conjunction(receipt: dict) -> tuple[bool, list[str]]:
    """The full declared conjunction, checked in declared order."""
    defects: list[str] = []
    pristine = receipt.get("pristine") or {}
    mutant = receipt.get("mutant") or {}
    cases = pristine.get("cases") or []
    detector = [r for r in (mutant.get("cases") or [])
                if isinstance(r, dict) and r.get("case") == CASE]
    if receipt.get("binder_sha256") != BINDER_SHA256:
        defects.append("binder_digest_mismatch")
    if type(pristine.get("exit")) is not int or pristine.get("exit") != 0:
        defects.append("pristine_exit_nonzero")
    summary = pristine.get("summary")
    if not (isinstance(summary, list) and len(summary) == 2
            and all(type(v) is int for v in summary)):
        defects.append("pristine_failures_nonzero")
    elif summary[1] != 0:
        defects.append("pristine_failures_nonzero")
    if (len(cases) < PRISTINE_FLOOR or not isinstance(summary, list)
            or len(summary) != 2 or type(summary[0]) is not int
            or summary[0] < PRISTINE_FLOOR or summary[0] != len(cases)):
        defects.append("pristine_cases_below_floor")
    if (frozen_killed(receipt) is not True
            or type(receipt.get("killed")) is not int or receipt.get("killed") != 1
            or type(mutant.get("exit")) is not int):
        defects.append("frozen_rule_not_killed")
    if type(receipt.get("survivors")) is not int or receipt.get("survivors") != 0:
        defects.append("survivors_not_zero")
    if type(receipt.get("mutants")) is not int or receipt.get("mutants") != 1:
        defects.append("mutants_not_one")
    names = [r.get("case") for r in cases if isinstance(r, dict)]
    missing = [n for n in ORIGINAL_CASES if n not in names]
    if (missing or any(names.count(n) != 1 for n in ORIGINAL_CASES)
            or len(names) != len(cases)
            or any(not isinstance(n, str) for n in names)
            or len(set(names)) != len(names)
            or any(r.get("pass") is not True for r in cases if isinstance(r, dict))):
        defects.append("original_cases_absent")
    if len(detector) != 1 or detector[0].get("pass") is not False:
        defects.append("detector_absent_or_passing")
    return (not defects), defects


# ---------------------------------------------------------------------------
# battery
# ---------------------------------------------------------------------------

def arm(root: str, rev: str, name: str, path: str, declared: str,
        mutate=None) -> dict:
    receipt = load_receipt(root, rev, path)
    if mutate is not None:
        receipt = mutate(receipt)
    frozen = frozen_killed(receipt)
    ok, defects = conjunction(receipt)
    refused = not ok
    reason = defects[0] if defects else None
    if declared is None:
        met = bool(frozen is True and ok)
    else:
        met = bool(frozen is True and refused and reason == declared)
    return {"arm": name, "receipt_path": path, "declared_reason": declared,
            "frozen_killed": frozen, "conjunction_ok": ok, "defects": defects,
            "reason": reason, "met": met}


def battery(root: str, rev: str, json_out: str | None) -> tuple[dict, int]:
    receipt: dict = {"schema": SCHEMA, "rev": rev,
                     "instrument": {"path": "tools/round-82/conjunction-gate.py",
                                    "sha256": sha256_bytes(Path(__file__).read_bytes())},
                     "counter": {"path": COUNTER_PATH, "sha256": COUNTER_SHA256},
                     "binder": {"path": BINDER_PATH, "sha256": BINDER_SHA256}}
    code = 0
    try:
        counter_digest = sha256_bytes(get(root, rev, COUNTER_PATH))
        binder_digest = sha256_bytes(get(root, rev, BINDER_PATH))
    except (subprocess.CalledProcessError, OSError) as exc:
        receipt.update({"unevaluable": str(exc), "ok": False})
        _write(receipt, json_out)
        print(json.dumps(receipt))
        return receipt, 2
    receipt["counter_sha256_matches"] = counter_digest == COUNTER_SHA256
    receipt["binder_sha256_matches"] = binder_digest == BINDER_SHA256
    if not (receipt["counter_sha256_matches"] and receipt["binder_sha256_matches"]):
        receipt.update({"unevaluable": "pin mismatch on frozen instruments",
                        "ok": False})
        _write(receipt, json_out)
        print(json.dumps(receipt))
        return receipt, 2

    arms = [
        arm(root, rev, "undersized", FORGED_UNDER, "pristine_cases_below_floor"),
        arm(root, rev, "dirty", FORGED_DIRTY, "pristine_failures_nonzero"),
        arm(root, rev, "binder-swap", LANDING, "binder_digest_mismatch",
            mutate=lambda r: {**copy.deepcopy(r), "binder_sha256": WRONG_BINDER}),
        arm(root, rev, "genuine", LANDING, None),
    ]
    forged = [a for a in arms if a["arm"] != "genuine"]
    genuine = arms[-1]
    genuine_ok = bool(genuine["conjunction_ok"] and genuine["frozen_killed"])
    reasons = sorted(a["reason"] for a in forged if a["reason"])
    frozen_accepts = sum(1 for a in forged if a["frozen_killed"])
    control = {"control": "frozen-rule-accepts-forged",
               "expected": "the pinned counter rule alone accepts all three forged states",
               "accepted": frozen_accepts, "met": frozen_accepts == 3}
    receipt.update({
        "arms": arms, "forged_total": len(forged),
        "refused": sum(1 for a in forged if not a["conjunction_ok"]),
        "reasons": reasons, "genuine_ok": genuine_ok,
        "frozen_rule_accepts_forged": frozen_accepts,
        "controls": [control],
    })
    receipt["ok"] = bool(
        receipt["refused"] == 3
        and reasons == sorted(["pristine_cases_below_floor",
                               "pristine_failures_nonzero",
                               "binder_digest_mismatch"])
        and genuine_ok and frozen_accepts == 3
        and all(a["met"] for a in forged)
        and control["met"]
        and receipt["counter_sha256_matches"]
        and receipt["binder_sha256_matches"])
    check = validate_receipt(receipt)
    receipt["validate"] = check
    if check["defects"]:
        receipt["ok"] = False
    code = 0 if receipt["ok"] else 1
    _write(receipt, json_out)
    print(json.dumps({k: receipt[k] for k in
                      ("forged_total", "refused", "reasons", "genuine_ok",
                       "frozen_rule_accepts_forged", "counter_sha256_matches",
                       "binder_sha256_matches", "ok")}, sort_keys=True))
    print(json.dumps({"validate_defects": check["defects"]}, sort_keys=True))
    return receipt, code


def validate_receipt(receipt: dict) -> dict:
    """Internal consistency: the verdict line must re-derive from the arms."""
    defects: list[str] = []
    arms = receipt.get("arms") or []
    forged = [a for a in arms if a.get("arm") != "genuine"]
    genuine = [a for a in arms if a.get("arm") == "genuine"]
    if len(arms) != 4 or len(forged) != 3 or len(genuine) != 1:
        defects.append("arm_shape")
    refused = sum(1 for a in forged if not a.get("conjunction_ok"))
    if receipt.get("refused") != refused:
        defects.append("refused_mismatch")
    if receipt.get("forged_total") != len(forged):
        defects.append("forged_total_mismatch")
    reasons = sorted(a.get("reason") for a in forged if a.get("reason"))
    if receipt.get("reasons") != reasons:
        defects.append("reasons_mismatch")
    genuine_ok = bool(genuine and genuine[0].get("conjunction_ok")
                      and genuine[0].get("frozen_killed"))
    if receipt.get("genuine_ok") != genuine_ok:
        defects.append("genuine_ok_mismatch")
    accepts = sum(1 for a in forged if a.get("frozen_killed"))
    if receipt.get("frozen_rule_accepts_forged") != accepts:
        defects.append("control_mismatch")
    declared = sorted(["pristine_cases_below_floor", "pristine_failures_nonzero",
                       "binder_digest_mismatch"])
    if receipt.get("ok") and reasons != declared:
        defects.append("declared_reason_set")
    if receipt.get("ok") != (receipt.get("refused") == 3 and genuine_ok
                             and receipt.get("frozen_rule_accepts_forged") == 3
                             and all(a.get("met") for a in forged)
                             and receipt.get("counter_sha256_matches") is True
                             and receipt.get("binder_sha256_matches") is True):
        defects.append("verdict_not_rederived")
    return {"defects": defects, "checked": True}


def _write(receipt: dict, json_out: str | None) -> None:
    if json_out:
        Path(json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(json_out).write_text(json.dumps(receipt, indent=1) + "\n")


# ---------------------------------------------------------------------------
# selftest: isolated synthetic receipts only, no real runs
# ---------------------------------------------------------------------------

def synthetic_genuine() -> dict:
    names = ORIGINAL_CASES + [CASE, "record-fixture-committed-duplicate"]
    return {
        "rev": "@synthetic@", "target": "strictness-battery.py",
        "declared_case": CASE,
        "instrument": {"path": COUNTER_PATH, "sha256": COUNTER_SHA256},
        "target_sha256": "a" * 64, "binder_sha256": BINDER_SHA256,
        "pristine": {"exit": 0,
                     "cases": [{"case": n, "pass": True} for n in names],
                     "summary": [11, 0], "stdout": "SELFTEST cases=11 failures=0\n"},
        "mutant": {"exit": 1,
                   "cases": [{"case": n, "pass": True} for n in ORIGINAL_CASES]
                   + [{"case": CASE, "pass": False},
                      {"case": "record-fixture-committed-duplicate",
                       "pass": False}],
                   "summary": [11, 2], "stdout": "SELFTEST cases=11 failures=2\n"},
        "mutants": 1, "killed": 1, "survivors": 0, "ok": True,
    }


def selftest() -> tuple[dict, int]:
    cases: dict[str, bool] = {}

    def check(name: str, cond: bool) -> None:
        cases[name] = bool(cond)

    base = synthetic_genuine()
    ok, defects = conjunction(base)
    check("genuine-synthetic-passes", ok and not defects)
    check("frozen-rule-agrees-genuine", frozen_killed(base) is True)

    under = copy.deepcopy(base)
    under["pristine"]["cases"] = under["pristine"]["cases"][:1]
    under["pristine"]["summary"] = [1, 0]
    ok, defects = conjunction(under)
    check("floor-refused", not ok and defects[0] == "pristine_cases_below_floor")
    check("floor-deficiency-frozen-accepts", frozen_killed(under) is True)

    dirty = copy.deepcopy(base)
    dirty["pristine"]["summary"] = [11, 3]
    ok, defects = conjunction(dirty)
    check("failures-refused", not ok and defects[0] == "pristine_failures_nonzero")
    check("failures-deficiency-frozen-accepts", frozen_killed(dirty) is True)
    short_summary = copy.deepcopy(base)
    short_summary["pristine"]["summary"] = [1, 0]
    ok, defects = conjunction(short_summary)
    check("summary-floor-independent", not ok and
          "pristine_cases_below_floor" in defects)
    bool_summary = copy.deepcopy(base)
    bool_summary["pristine"]["summary"] = [11, False]
    ok, defects = conjunction(bool_summary)
    check("summary-bool-refused", not ok and
          "pristine_failures_nonzero" in defects)

    swap = copy.deepcopy(base)
    swap["binder_sha256"] = WRONG_BINDER
    ok, defects = conjunction(swap)
    check("binder-refused", not ok and defects[0] == "binder_digest_mismatch")
    check("binder-deficiency-frozen-accepts", frozen_killed(swap) is True)

    exit1 = copy.deepcopy(base)
    exit1["pristine"]["exit"] = 1
    ok, defects = conjunction(exit1)
    check("pristine-exit-refused",
          not ok and defects[0] == "pristine_exit_nonzero")

    notkilled = copy.deepcopy(base)
    notkilled["mutant"]["exit"] = 0
    ok, defects = conjunction(notkilled)
    check("frozen-rule-not-killed-refused",
          not ok and "frozen_rule_not_killed" in defects)

    surv = copy.deepcopy(base)
    surv["survivors"] = 1
    ok, defects = conjunction(surv)
    check("survivors-refused", not ok and "survivors_not_zero" in defects)

    mut2 = copy.deepcopy(base)
    mut2["mutants"] = 2
    ok, defects = conjunction(mut2)
    check("mutants-refused", not ok and "mutants_not_one" in defects)

    nonames = copy.deepcopy(base)
    nonames["pristine"]["cases"] = [c for c in nonames["pristine"]["cases"]
                                    if c["case"] != ORIGINAL_CASES[3]]
    ok, defects = conjunction(nonames)
    check("original-names-refused",
          not ok and "original_cases_absent" in defects)

    nodetect = copy.deepcopy(base)
    nodetect["mutant"]["cases"] = [c for c in nodetect["mutant"]["cases"]
                                   if c["case"] != CASE]
    ok, defects = conjunction(nodetect)
    check("detector-absent-refused",
          not ok and "detector_absent_or_passing" in defects)

    passing = copy.deepcopy(base)
    for r in passing["mutant"]["cases"]:
        if r["case"] == CASE:
            r["pass"] = True
    ok, defects = conjunction(passing)
    check("detector-passing-refused",
          not ok and "detector_absent_or_passing" in defects)

    dup = copy.deepcopy(base)
    dup["mutant"]["cases"] = dup["mutant"]["cases"] + [
        {"case": CASE, "pass": False}]
    ok, defects = conjunction(dup)
    check("detector-nonunique-refused",
          not ok and "detector_absent_or_passing" in defects)

    # rule order is deterministic on a state failing two conjuncts
    both = copy.deepcopy(base)
    both["binder_sha256"] = WRONG_BINDER
    both["pristine"]["summary"] = [11, 3]
    ok, defects = conjunction(both)
    check("first-declared-defect-binder", defects[0] == "binder_digest_mismatch")

    # validate_receipt agrees with a hand-consistent receipt
    good_receipt = {"schema": SCHEMA, "arms": [
        {"arm": "undersized", "conjunction_ok": False, "frozen_killed": True,
         "reason": "pristine_cases_below_floor", "met": True},
        {"arm": "dirty", "conjunction_ok": False, "frozen_killed": True,
         "reason": "pristine_failures_nonzero", "met": True},
        {"arm": "binder-swap", "conjunction_ok": False, "frozen_killed": True,
         "reason": "binder_digest_mismatch", "met": True},
        {"arm": "genuine", "conjunction_ok": True, "frozen_killed": True,
         "reason": None, "met": True}],
        "forged_total": 3, "refused": 3,
        "reasons": sorted(["pristine_cases_below_floor",
                           "pristine_failures_nonzero",
                           "binder_digest_mismatch"]),
        "genuine_ok": True, "frozen_rule_accepts_forged": 3,
        "counter_sha256_matches": True, "binder_sha256_matches": True,
        "ok": True}
    check("validate-consistent-clean",
          validate_receipt(good_receipt)["defects"] == [])

    bad = copy.deepcopy(good_receipt)
    bad["refused"] = 2
    check("validate-refused-mismatch",
          "refused_mismatch" in validate_receipt(bad)["defects"])

    failures = sorted(k for k, v in cases.items() if not v)
    summary = {"selftest": "tools/round-82/conjunction-gate.py",
               "cases": len(cases), "case_names": sorted(cases),
               "failures": failures}
    print(json.dumps(summary, indent=1, sort_keys=True))
    print(f"SELFTEST cases={len(cases)} failures={len(failures)}")
    return summary, 0 if not failures else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--battery", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--cli-selftest", action="store_true")
    ap.add_argument("--work")
    ap.add_argument("--json-out")
    a = ap.parse_args()
    if a.cli_selftest:
        if not a.work:
            ap.error("--cli-selftest requires --work")
        argv = [sys.executable, "-I", "-B", str(Path(__file__).with_name("cli-fixtures.py")),
                "--root", a.root, "--rev", a.rev, "--work", a.work,
                "--which", "conjunction"]
        if a.json_out:
            argv += ["--json-out", a.json_out]
        return subprocess.run(argv).returncode
    if a.selftest:
        _, code = selftest()
        return code
    if a.battery:
        _, code = battery(a.root, a.rev, a.json_out)
        return code
    print("usage: --battery | --selftest", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
