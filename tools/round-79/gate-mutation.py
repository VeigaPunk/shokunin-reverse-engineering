#!/usr/bin/env python3
"""Round-79 selftest mutation battery: the round-78 gate's survivors close.

The round-78 wave's mutation seat (MutGate) ran eight textual mutants of
`tools/round-78/attack-gate.py` against the gate's own detectors and reported
two survivors: `m03` (the near-miss regex made dead; no selftest case exercises
the unparsable spelling) and `m08` (`validate_receipt`'s refused-without-a-reason
guard removed; no selftest case calls `validate_receipt`).  This battery freezes
that question: eight mutants, each with ONE declared selftest case, run against
the target instrument's `--selftest` at a measured revision.

    --battery   run the pristine target and every mutant; write a receipt.
    --selftest  unit cases for the battery's own helpers.
    --validate  re-derive a receipt's counts from its own mutant list.
    --control   empty-set: the do-nothing control (no mutants, cannot pass).

A mutant is KILLED only when its declared case is present in the mutant's
selftest output and fails there.  An absent declared case is a SURVIVOR, never
a pass (that is exactly the round-78 defect: a detector that does not exist
cannot catch anything).  A mutant whose anchor does not occur exactly once, or
whose copy does not produce a SELFTEST summary, is INCONCLUSIVE and never
counted as killed.

Exit: 0 every mutant killed by its declared case, pristine green, target pinned;
1 otherwise; 2 could-not-evaluate.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

ROUND = 79
TARGET = "tools/round-78/attack-gate.py"
TARGET_SHA256 = "4e4baf00ef0cb34c5615155abd0a746b7e12a6a997340d32ce72c5402d32d2bf"
PREDICATE = (
    "R79-C1 is verified iff `python3 -I -B tools/round-79/gate-mutation.py --root . "
    "--rev <measured> --work <scratch> --battery --json-out <receipt>` exits 0 with "
    "`mutants_total 8`, `killed 8`, `survivors 0`, `declared_case_hits 8`, "
    "`target_pin.matched true`, a pristine selftest of 29 cases and 0 failures, and a "
    "defect-free `validate`; each mutant's declared case is present and fails in that "
    "mutant's selftest and the three mutants `m03`, `m05` and `m08` (the two round-78 "
    "survivors plus the atom-absent conjunct) are detected by that one case alone, "
    "while at base `29d2ca30` the same battery exits 1 with `survivors 3` naming "
    "`m03`, `m05` and `m08`."
)

# Each mutant: one exact single-occurrence edit and the one case that must fail.
MUTANTS = [
    {
        "id": "m01-auth-dead",
        "edit": "auth_findings returns [] before any check (dead rule)",
        "anchor": '    out: list[dict] = []\n'
                  '    r = receipt.get("rev")\n',
        "replace": '    return []\n'
                   '    out: list[dict] = []\n'
                   '    r = receipt.get("rev")\n',
        "declared_case": "red-receipt-auth",
    },
    {
        "id": "m02-qualified-atom-dead",
        "edit": "QUALIFIED_ATOM_RE matches nothing",
        "anchor": 'QUALIFIED_ATOM_RE = re.compile(r"^[A-Z][0-9][0-9A-Za-z_]*:")\n',
        "replace": 'QUALIFIED_ATOM_RE = re.compile(r"(?!)")\n',
        "declared_case": "red-qualified-atom",
    },
    {
        "id": "m03-near-miss-re-dead",
        "edit": "NEAR_MISS_RE matches nothing (round-78 survivor)",
        "anchor": 'NEAR_MISS_RE = re.compile(\n'
                  '    r"^(?:mismatch|survivor|atom|pristine|validate|match|matches)'
                  '\\s+\\S+$")\n',
        "replace": 'NEAR_MISS_RE = re.compile(r"(?!)")\n',
        "declared_case": "red-near-miss-unparsed",
    },
    {
        "id": "m04-negation-dead",
        "edit": "NEGATION_RE matches nothing",
        "anchor": 'NEGATION_RE = re.compile(r"\\b(not|no|none|never|neither)\\b", '
                  're.IGNORECASE)\n',
        "replace": 'NEGATION_RE = re.compile(r"(?!)")\n',
        "declared_case": "red-negated",
    },
    {
        "id": "m05-atom-absent-bound",
        "edit": "the atom branch returns (True, bound) when the receipt has no atoms table",
        "anchor": '            if not isinstance(atoms, list):\n'
                  '                return False, "defect", {"reason": "no_atoms", '
                  '"field": field}\n',
        "replace": '            if not isinstance(atoms, list):\n'
                   '                return True, "bound", {"reason": "no_atoms", '
                   '"field": field}\n',
        "declared_case": "red-atom-absent",
    },
    {
        "id": "m06-near-miss-stems-empty",
        "edit": "NEAR_MISS_STEMS emptied (the parsed-field branch goes blind)",
        "anchor": 'NEAR_MISS_STEMS = {"mismatch", "mismatches", "survivor", "survivors", '
                  '"atom",\n                   "atoms", "pristine", "validate", "match", '
                  '"matches"}\n',
        "replace": 'NEAR_MISS_STEMS = set()\n',
        "declared_case": "red-near-miss-plural",
    },
    {
        "id": "m07-mode-ok-always",
        "edit": "mode_ok accepts any object mode",
        "anchor": '    return mode in FILE_MODES and kind == "blob"\n',
        "replace": '    return True\n',
        "declared_case": "red-mode-tree",
    },
    {
        "id": "m08-validate-no-refusal-guard",
        "edit": "validate_receipt skips the refused-without-a-reason guard "
                "(round-78 survivor)",
        "anchor": '        if fixture.get("refused") and not fixture.get("reasons"):\n'
                  '            defects.append(f"{fixture.get(\'id\')}: refused without '
                  'a reason")\n',
        "replace": '',
        "declared_case": "red-validate-refused-no-reason",
    },
]

SELFTEST_LINE = re.compile(r"^SELFTEST cases=(?P<cases>\d+) failures=(?P<failures>\d+)$")


class Unevaluable(Exception):
    """Exit-2 class: the battery cannot score, so it claims nothing."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_show(root: str, rev: str, path: str) -> bytes | None:
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                          capture_output=True)
    return proc.stdout if proc.returncode == 0 else None


def apply_mutant(text: str, mutant: dict) -> tuple[str | None, str]:
    """Apply one exact single-occurrence edit; refuse 0 or >1 occurrences."""
    anchor = mutant["anchor"]
    hits = text.count(anchor)
    if hits != 1:
        return None, f"anchor occurs {hits} times, want exactly 1"
    return text.replace(anchor, mutant["replace"], 1), "applied"


def parse_selftest(stdout: str) -> tuple[dict[str, bool], int | None, int | None]:
    """Read the case JSON lines and the SELFTEST summary."""
    cases: dict[str, bool] = {}
    cases_n = failures_n = None
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            match = SELFTEST_LINE.match(line)
            if match:
                cases_n = int(match.group("cases"))
                failures_n = int(match.group("failures"))
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(entry, dict) and isinstance(entry.get("case"), str):
            cases[entry["case"]] = bool(entry.get("pass"))
    return cases, cases_n, failures_n


def run_selftest(path: str, env: dict, cwd: str) -> tuple[int, str, str]:
    proc = subprocess.run([sys.executable, "-I", "-B", path, "--selftest"],
                          capture_output=True, text=True, env=env, cwd=cwd,
                          timeout=300)
    return proc.returncode, proc.stdout, proc.stderr


def judge(mutant: dict, cases: dict[str, bool]) -> dict:
    declared = mutant["declared_case"]
    absent = declared not in cases
    failed = sorted(name for name, ok in cases.items() if not ok)
    killed = (not absent) and cases[declared] is False
    return {
        "declared_case": declared,
        "case_absent": absent,
        "killed": killed,
        "killed_by_declared": killed,
        "failed_cases": failed,
        "detector_count": len(failed),
        "sole_detector": killed and len(failed) == 1,
    }


def validate_receipt(receipt: dict) -> dict:
    defects: list[str] = []
    mutants = receipt.get("mutants") or []
    ids = [m.get("id") for m in mutants]
    if len(ids) != len(set(ids)):
        defects.append("duplicate mutant id")
    if len(mutants) != receipt.get("mutants_total"):
        defects.append("mutants_total does not re-derive from the mutant list")
    for mutant in mutants:
        if not mutant.get("declared_case"):
            defects.append(f"{mutant.get('id')}: no declared case")
        if mutant.get("killed") and (
                mutant.get("case_absent")
                or mutant.get("declared_case") not in (mutant.get("failed_cases") or [])):
            defects.append(f"{mutant.get('id')}: killed without its declared case failing")
        if mutant.get("killed") and mutant.get("applied") is not True:
            defects.append(f"{mutant.get('id')}: killed without an applied edit")
    killed = sum(1 for m in mutants if m.get("killed"))
    if killed != receipt.get("killed"):
        defects.append("killed does not re-derive from the mutant list")
    survivors = sorted(m.get("id") for m in mutants if not m.get("killed"))
    if survivors != sorted(receipt.get("survivor_ids") or []):
        defects.append("survivor_ids do not re-derive from the mutant list")
    if receipt.get("survivors") != len(survivors):
        defects.append("survivors does not re-derive from the mutant list")
    hits = sum(1 for m in mutants
               if m.get("killed") and m.get("declared_case") in (m.get("failed_cases") or []))
    if hits != receipt.get("declared_case_hits"):
        defects.append("declared_case_hits does not re-derive from the mutant list")
    target = receipt.get("target") or {}
    if not isinstance(target.get("sha256"), str) or len(target.get("sha256") or "") != 64:
        defects.append("target sha256 is not a 64-hex digest")
    pin = receipt.get("target_pin") or {}
    if pin.get("matched") and pin.get("expected") != target.get("sha256"):
        defects.append("target_pin.matched with a non-equal expected digest")
    pristine = receipt.get("pristine") or {}
    if pristine.get("ok") and pristine.get("failures") != 0:
        defects.append("pristine.ok with nonzero failures")
    ok = bool(receipt.get("ok"))
    if ok and (len(mutants) != len(MUTANTS) or survivors or not pin.get("matched")
               or not pristine.get("ok")):
        defects.append("ok true but the frozen target is not met")
    return {"defects": defects, "mutants": len(mutants), "survivors": len(survivors)}


def battery(root: str, rev: str, work: str, control: str | None) -> dict:
    blob = git_show(root, rev, TARGET)
    if blob is None:
        raise Unevaluable(f"{TARGET} absent at {rev}")
    text = blob.decode("utf-8")
    actual = sha256_bytes(blob)
    os.makedirs(work, exist_ok=True)
    run_root = tempfile.mkdtemp(prefix="gate-mutation-", dir=work)
    env = {k: os.environ.get(k, "") for k in ("HOME", "LANG", "PATH", "TMPDIR")}
    results: list[dict] = []
    pristine_path = os.path.join(run_root, "pristine.py")
    with open(pristine_path, "wb") as handle:
        handle.write(blob)
    p_exit, p_out, p_err = run_selftest(pristine_path, env, run_root)
    p_cases, p_cases_n, p_failures = parse_selftest(p_out)
    pristine_ok = p_exit == 0 and p_failures == 0 and p_cases_n is not None
    mutants = [] if control == "empty-set" else MUTANTS
    for mutant in mutants:
        mutated, note = apply_mutant(text, mutant)
        entry: dict = {"id": mutant["id"], "edit": mutant["edit"],
                       "declared_case": mutant["declared_case"],
                       "applied": mutated is not None, "apply_note": note,
                       "exit": None, "failed_cases": [], "case_absent": True,
                       "killed": False, "killed_by_declared": False,
                       "detector_count": 0, "sole_detector": False,
                       "inconclusive": False}
        if mutated is None:
            entry["inconclusive"] = True
            results.append(entry)
            continue
        copy = os.path.join(run_root, f"{mutant['id']}.py")
        with open(copy, "w", encoding="utf-8") as handle:
            handle.write(mutated)
        m_exit, m_out, m_err = run_selftest(copy, env, run_root)
        m_cases, m_cases_n, m_failures = parse_selftest(m_out)
        entry["exit"] = m_exit
        if m_cases_n is None:
            entry["inconclusive"] = True
            entry["stderr_tail"] = m_err.strip().splitlines()[-1:] or []
            results.append(entry)
            continue
        entry.update(judge(mutant, m_cases))
        results.append(entry)
    survivors = sorted(m["id"] for m in results if not m["killed"])
    killed = sum(1 for m in results if m["killed"])
    hits = sum(1 for m in results
               if m["killed"] and m["declared_case"] in m["failed_cases"])
    pin = {"expected": TARGET_SHA256, "actual": actual,
           "matched": TARGET_SHA256 == actual}
    receipt = {
        "schema": "kaidoku-r79-gate-mutation-v1",
        "round": ROUND,
        "predicate": PREDICATE,
        "measured_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "target": {"path": TARGET, "rev": rev, "bytes": len(blob),
                   "sha256": actual},
        "target_pin": pin,
        "pristine": {"exit": p_exit, "cases": p_cases_n,
                     "failures": p_failures, "ok": bool(pristine_ok),
                     "failed_cases": sorted(n for n, ok in p_cases.items() if not ok)},
        "mutants_total": len(results),
        "killed": killed,
        "survivors": len(survivors),
        "survivor_ids": survivors,
        "declared_case_hits": hits,
        "control": control,
        "mutants": results,
    }
    receipt["ok"] = bool(pristine_ok and pin["matched"] and results
                         and not survivors and hits == len(results)
                         and all(m["applied"] and not m["inconclusive"] for m in results)
                         and len(results) == len(MUTANTS))
    return receipt


def selftest() -> int:
    cases: list[dict] = []

    def case(name, got, want):
        cases.append({"case": name, "got": got, "want": want, "pass": got == want})

    mutant = MUTANTS[2]
    good, _ = apply_mutant("x\n" + mutant["anchor"] + "y\n", mutant)
    case("green-apply", isinstance(good, str), True)
    case("red-anchor-absent", apply_mutant("x\n", mutant)[1],
         "anchor occurs 0 times, want exactly 1")
    case("red-anchor-twice", apply_mutant(mutant["anchor"] * 2, mutant)[1],
         "anchor occurs 2 times, want exactly 1")
    killed = judge(mutant, {"red-near-miss-unparsed": False})
    case("green-killed", killed["killed"], True)
    case("green-sole", killed["sole_detector"], True)
    absent = judge(mutant, {"red-near-miss-unparsed": True})
    case("red-case-present-but-passes", absent["killed"], False)
    gone = judge(mutant, {"other": False})
    case("red-case-absent", (gone["killed"], gone["case_absent"]), (False, True))
    multi = judge(mutant, {"red-near-miss-unparsed": False, "other": False})
    case("red-not-sole", multi["sole_detector"], False)
    parsed_cases, cases_n, failures_n = parse_selftest(
        '{"case": "a", "got": 1, "want": 1, "pass": true}\n'
        '{"case": "b", "got": 1, "want": 2, "pass": false}\n'
        "SELFTEST cases=2 failures=1\n")
    case("green-parse", (cases_n, failures_n, sorted(parsed_cases)),
         (2, 1, ["a", "b"]))
    forged = {"mutants_total": 8, "killed": 8, "survivors": 0, "survivor_ids": [],
              "declared_case_hits": 8,
              "target": {"sha256": "a" * 64},
              "target_pin": {"expected": "a" * 64, "matched": True},
              "pristine": {"ok": True, "failures": 0},
              "ok": True,
              "mutants": [{"id": f"m{i}", "declared_case": "c", "killed": True,
                           "applied": True, "failed_cases": []} for i in range(8)]}
    case("red-forged-kill", bool(validate_receipt(forged)["defects"]), True)
    empty = dict(forged, mutants=[], mutants_total=0, killed=0,
                 declared_case_hits=0, ok=False)
    case("green-empty-battery-refused", validate_receipt(empty)["defects"], [])
    failures = [c for c in cases if not c["pass"]]
    for case_ in cases:
        print(json.dumps(case_, sort_keys=True))
    print(f"SELFTEST cases={len(cases)} failures={len(failures)}")
    return 0 if not failures else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev")
    ap.add_argument("--work")
    ap.add_argument("--json-out")
    ap.add_argument("--battery", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--validate")
    ap.add_argument("--control", choices=("empty-set",))
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    root = os.path.abspath(args.root)
    if args.validate:
        receipt = json.loads(open(args.validate, encoding="utf-8").read())
        result = validate_receipt(receipt)
        print(json.dumps(result, sort_keys=True))
        return 0 if not result["defects"] else 1
    if not args.battery:
        print("usage: --battery --rev <rev> [--work <dir>] [--json-out <path>]",
              file=sys.stderr)
        return 2
    rev = args.rev
    if rev is None:
        print("--rev is required for --battery", file=sys.stderr)
        return 2
    work = args.work or tempfile.mkdtemp(prefix="gate-mutation-work-")
    try:
        receipt = battery(root, rev, work, args.control)
    except Unevaluable as exc:
        print(json.dumps({"ok": False, "unevaluable": str(exc)}))
        return 2
    text = json.dumps(receipt, indent=1, sort_keys=True) + "\n"
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as handle:
            handle.write(text)
    print(json.dumps({"exit": 0 if receipt["ok"] else 1,
                      "mutants_total": receipt["mutants_total"],
                      "killed": receipt["killed"],
                      "survivors": receipt["survivors"],
                      "survivor_ids": receipt["survivor_ids"],
                      "declared_case_hits": receipt["declared_case_hits"],
                      "pin_matched": receipt["target_pin"]["matched"],
                      "ok": receipt["ok"]}, sort_keys=True))
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
