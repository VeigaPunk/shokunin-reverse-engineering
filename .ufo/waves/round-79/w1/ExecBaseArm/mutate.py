#!/usr/bin/env python3
"""Independent re-derivation of R79-C1's base arm.

This applier does NOT import `tools/round-79/gate-mutation.py`.  It re-reads the
frozen MUTANTS table as *data* (an AST literal from the freeze revision) and
brings its own applier, its own selftest-output parser and its own kill judge:

  * exactly one occurrence of an anchor, else REFUSE (never apply);
  * a mutant is KILLED only when its declared case is present in the mutated
    copy's `--selftest` output AND fails there;
  * an absent declared case is a SURVIVOR, never a pass;
  * a copy with no `SELFTEST cases=N failures=M` line is INCONCLUSIVE.

Measured arm here is the BASE revision (default 29d2ca30b8); the freeze arm is
the claimant's, not this seat's.

Usage:
  python3 -I -B mutate.py --root <lane> [--rev <rev>] --work <scratch>
                        [--freeze <rev>] --json-out <receipt>
Exit: 0 when the measured base arm reproduces (8 total, 5 killed, 3 survivors
named m03/m05/m08 and all three declared cases absent from the pristine case
list); 1 when it does not; 2 on could-not-evaluate.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys

BASE_REV = "29d2ca30b83a6a0d85b0aa979de0138fde1660e6"
FREEZE_REV = "ed68cd0a6cc790cca342380a2d80d1927a668c8c"
TARGET = "tools/round-78/attack-gate.py"
TOOL = "tools/round-79/gate-mutation.py"
EXPECT_SURVIVORS = ["m03-near-miss-re-dead", "m05-atom-absent-bound",
                    "m08-validate-no-refusal-guard"]
SELFTEST_LINE = re.compile(r"^SELFTEST cases=(?P<cases>\d+) failures=(?P<failures>\d+)$")

# Hand transcription of the eight frozen mutants, typed from the freeze blob
# rather than produced by the parser below.  If these two disagree the arm is
# unevaluable, so a mis-transcription can never masquerade as a measurement.
TRANSCRIBED = [
    ("m01-auth-dead",
     '    out: list[dict] = []\n    r = receipt.get("rev")\n',
     '    return []\n    out: list[dict] = []\n    r = receipt.get("rev")\n',
     "red-receipt-auth"),
    ("m02-qualified-atom-dead",
     'QUALIFIED_ATOM_RE = re.compile(r"^[A-Z][0-9][0-9A-Za-z_]*:")\n',
     'QUALIFIED_ATOM_RE = re.compile(r"(?!)")\n',
     "red-qualified-atom"),
    ("m03-near-miss-re-dead",
     'NEAR_MISS_RE = re.compile(\n'
     '    r"^(?:mismatch|survivor|atom|pristine|validate|match|matches)\\s+\\S+$")\n',
     'NEAR_MISS_RE = re.compile(r"(?!)")\n',
     "red-near-miss-unparsed"),
    ("m04-negation-dead",
     'NEGATION_RE = re.compile(r"\\b(not|no|none|never|neither)\\b", re.IGNORECASE)\n',
     'NEGATION_RE = re.compile(r"(?!)")\n',
     "red-negated"),
    ("m05-atom-absent-bound",
     '            if not isinstance(atoms, list):\n'
     '                return False, "defect", {"reason": "no_atoms", "field": field}\n',
     '            if not isinstance(atoms, list):\n'
     '                return True, "bound", {"reason": "no_atoms", "field": field}\n',
     "red-atom-absent"),
    ("m06-near-miss-stems-empty",
     'NEAR_MISS_STEMS = {"mismatch", "mismatches", "survivor", "survivors", "atom",\n'
     '                   "atoms", "pristine", "validate", "match", "matches"}\n',
     'NEAR_MISS_STEMS = set()\n',
     "red-near-miss-plural"),
    ("m07-mode-ok-always",
     '    return mode in FILE_MODES and kind == "blob"\n',
     '    return True\n',
     "red-mode-tree"),
    ("m08-validate-no-refusal-guard",
     '        if fixture.get("refused") and not fixture.get("reasons"):\n'
     "            defects.append(f\"{fixture.get('id')}: refused without a reason\")\n",
     '',
     "red-validate-refused-no-reason"),
]


class Unevaluable(Exception):
    """The arm cannot be scored, so it claims nothing."""


def git_bytes(root: str, rev: str, path: str) -> bytes | None:
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                          capture_output=True)
    return proc.stdout if proc.returncode == 0 else None


def read_mutants(root: str, freeze: str) -> list[dict]:
    """Parse the frozen MUTANTS table as data; the tool is never executed."""
    blob = git_bytes(root, freeze, TOOL)
    if blob is None:
        raise Unevaluable(f"{TOOL} absent at {freeze}")
    tree = ast.parse(blob.decode("utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "MUTANTS" for t in node.targets):
            table = ast.literal_eval(node.value)
            if not isinstance(table, list) or len(table) != 8:
                raise Unevaluable(f"MUTANTS is not an 8-entry list at {freeze}")
            for entry in table:
                for key in ("id", "anchor", "replace", "declared_case"):
                    if key not in entry:
                        raise Unevaluable(f"mutant entry missing {key!r}")
            return table
    raise Unevaluable(f"MUTANTS assignment not found at {freeze}")


def apply_once(text: str, mutant: dict) -> tuple[str | None, str, int]:
    """Apply one exact single-occurrence edit; REFUSE 0 or >1 occurrences."""
    anchor, hits = mutant["anchor"], text.count(mutant["anchor"])
    if hits != 1:
        return None, f"REFUSED: anchor occurs {hits} times, want exactly 1", hits
    mutated = text.replace(anchor, mutant["replace"], 1)
    if mutated == text:
        return None, "REFUSED: edit is a no-op (replace equals anchor)", hits
    return mutated, "applied", hits


def parse_selftest(stdout: str) -> tuple[dict[str, bool], int | None, int | None,
                                         str | None]:
    """Own parser: case JSON lines plus the SELFTEST summary line."""
    cases: dict[str, bool] = {}
    cases_n = failures_n = None
    summary = None
    for line in stdout.splitlines():
        stripped = line.strip()
        if stripped.startswith("{"):
            try:
                entry = json.loads(stripped)
            except json.JSONDecodeError:
                continue
            if isinstance(entry, dict) and isinstance(entry.get("case"), str):
                cases[entry["case"]] = entry.get("pass") is True
            continue
        match = SELFTEST_LINE.match(stripped)
        if match:
            cases_n = int(match.group("cases"))
            failures_n = int(match.group("failures"))
            summary = stripped
    return cases, cases_n, failures_n, summary


def run_selftest(path: str, env: dict, cwd: str) -> tuple[int, str, str]:
    proc = subprocess.run([sys.executable, "-I", "-B", path, "--selftest"],
                          capture_output=True, text=True, env=env, cwd=cwd,
                          timeout=300)
    return proc.returncode, proc.stdout, proc.stderr


def judge(mutant: dict, cases: dict[str, bool]) -> dict:
    """Killed iff the declared case is present and fails; absent is a survivor."""
    declared = mutant["declared_case"]
    absent = declared not in cases
    failed = sorted(name for name, ok in cases.items() if not ok)
    killed = (not absent) and cases[declared] is False
    return {
        "declared_case": declared,
        "declared_case_present": not absent,
        "case_absent": absent,
        "killed": killed,
        "declared_case_in_failed_list": declared in failed,
        "failed_cases": failed,
        "detector_count": len(failed),
        "sole_detector": killed and len(failed) == 1,
    }


def refusal_control(text: str, mutants: list[dict]) -> dict:
    """Show the applier refuses an anchor that occurs twice (never applies).

    The hit count in the source text, not a "already applied" flag, decides.
    Three genuine refusals plus one recorded non-refusal that proves the point:
    `m01`'s replacement re-emits its own anchor verbatim, so its anchor still
    occurs exactly once after the edit and a *second* application is a valid
    second insertion, not a duplicate.  That check is expected to apply, and it
    is excluded from `all_refused` on purpose.
    """
    embedding = mutants[0]        # m01: replacement contains the anchor
    consuming = next(m for m in mutants if m["anchor"] not in m["replace"])
    checks: list[dict] = []

    doubled = embedding["anchor"] + text       # two literal occurrences
    got, note, hits = apply_once(doubled, embedding)
    checks.append({"case": "source-with-two-anchors", "expect": "refuse",
                   "refused": got is None, "hits": hits, "note": note})

    once, note1, hits1 = apply_once(text, consuming)
    if once is None:
        raise Unevaluable(f"control precondition failed: {note1}")
    again, note2, hits2 = apply_once(once, consuming)
    checks.append({"case": "reapply-consumed-anchor", "expect": "refuse",
                   "mutant": consuming["id"], "refused": again is None,
                   "hits": hits2, "note": note2})

    gone, note3, hits3 = apply_once("no anchor in this text\n", embedding)
    checks.append({"case": "anchor-absent", "expect": "refuse",
                   "refused": gone is None, "hits": hits3, "note": note3})

    second, note4, hits4 = apply_once(text, embedding)
    if second is None:
        raise Unevaluable(f"control precondition failed: {note4}")
    embed_again, note5, hits5 = apply_once(second, embedding)
    checks.append({"case": "reapply-embedding-anchor", "expect": "apply-again",
                   "refused": embed_again is None, "hits": hits5, "note": note5,
                   "informational": True})

    refusals = [c for c in checks if not c.get("informational")]
    return {"checks": checks, "all_refused": all(c["refused"] for c in refusals),
            "informational_note": "reapply-embedding-anchor applies by design: "
                                  "m01's replacement re-emits the anchor exactly once"}


def cross_check(parsed: list[dict], text: str) -> dict:
    """Hand transcription vs parsed table vs base blob: all three must agree."""
    mismatches: list[str] = []
    if len(parsed) != len(TRANSCRIBED):
        mismatches.append(f"entry count parsed={len(parsed)} typed={len(TRANSCRIBED)}")
    by_id = {m["id"]: m for m in parsed}
    for mid, anchor, replace, declared in TRANSCRIBED:
        got = by_id.get(mid)
        if got is None:
            mismatches.append(f"{mid}: absent from parsed table")
            continue
        for field, want in (("anchor", anchor), ("replace", replace),
                            ("declared_case", declared)):
            if got[field] != want:
                mismatches.append(f"{mid}.{field}: parsed != typed")
        hits = text.count(anchor)
        if hits != 1:
            mismatches.append(f"{mid}: typed anchor occurs {hits} times in base blob")
    return {"entries": len(TRANSCRIBED), "mismatches": mismatches,
            "agree": not mismatches}


def battery(root: str, rev: str, freeze: str, work: str) -> dict:
    blob = git_bytes(root, rev, TARGET)
    if blob is None:
        raise Unevaluable(f"{TARGET} absent at {rev}")
    text = blob.decode("utf-8")
    mutants = read_mutants(root, freeze)
    agreement = cross_check(mutants, text)
    if not agreement["agree"]:
        raise Unevaluable("typed/parsed mutant tables disagree: "
                          + "; ".join(agreement["mismatches"]))
    run_root = os.path.join(work, f"arm-{rev[:8]}")
    os.makedirs(run_root, exist_ok=True)
    env = {k: os.environ.get(k, "") for k in ("HOME", "LANG", "PATH", "TMPDIR")}
    env["TMPDIR"] = work

    pristine_path = os.path.join(run_root, "pristine-base.py")
    with open(pristine_path, "wb") as handle:
        handle.write(blob)
    p_exit, p_out, p_err = run_selftest(pristine_path, env, run_root)
    p_cases, p_cases_n, p_failures, p_summary = parse_selftest(p_out)
    if p_cases_n is None:
        raise Unevaluable(
            f"base pristine selftest produced no summary line (exit {p_exit}): "
            f"{p_err.strip().splitlines()[-1:] or ['<no stderr>']}")

    results: list[dict] = []
    for mutant in mutants:
        mutated, note, hits = apply_once(text, mutant)
        entry: dict = {"id": mutant["id"], "edit": mutant["edit"],
                       "declared_case": mutant["declared_case"],
                       "anchor_occurrences": hits, "apply_note": note,
                       "applied": mutated is not None, "exit": None,
                       "case_absent": True, "killed": False,
                       "declared_case_present": False,
                       "declared_case_in_failed_list": False,
                       "failed_cases": [], "detector_count": 0,
                       "sole_detector": False, "inconclusive": False}
        if mutated is None:
            entry["inconclusive"] = True
            results.append(entry)
            continue
        copy = os.path.join(run_root, f"{mutant['id']}.py")
        with open(copy, "w", encoding="utf-8") as handle:
            handle.write(mutated)
        entry["mutated_bytes"] = len(mutated.encode("utf-8"))
        entry["mutated_sha256"] = hashlib.sha256(mutated.encode("utf-8")).hexdigest()
        entry["copy_differs_from_pristine"] = mutated != text
        m_exit, m_out, m_err = run_selftest(copy, env, run_root)
        m_cases, m_cases_n, m_failures, m_summary = parse_selftest(m_out)
        entry["exit"] = m_exit
        entry["selftest_summary"] = m_summary
        if m_cases_n is None:
            entry["inconclusive"] = True
            entry["stderr_tail"] = m_err.strip().splitlines()[-1:] or []
            results.append(entry)
            continue
        entry.update(judge(mutant, m_cases))
        entry["cases_total"] = m_cases_n
        entry["failures_total"] = m_failures
        results.append(entry)

    killed_ids = [m["id"] for m in results if m["killed"]]
    survivor_ids = sorted(m["id"] for m in results if not m["killed"])
    absent_ids = sorted(m["id"] for m in results if m["case_absent"])
    absent_in_pristine = sorted(m["id"] for m in results
                                if m["declared_case"] not in p_cases)
    control = refusal_control(text, mutants)

    reproduces = (len(results) == 8
                  and len(killed_ids) == 5
                  and survivor_ids == EXPECT_SURVIVORS
                  and absent_ids == EXPECT_SURVIVORS
                  and absent_in_pristine == EXPECT_SURVIVORS
                  and all(m["applied"] and not m["inconclusive"] for m in results)
                  and control["all_refused"]
                  and agreement["agree"])
    return {
        "schema": "kaidoku-r79-execbasearm-mutation-v1",
        "seat": "ExecBaseArm",
        "claim": "R79-C1 (base arm only; freeze arm re-derived by nobody here)",
        "method": "independent applier/parser/judge; MUTANTS read as AST data from "
                  f"{TOOL}@{freeze[:8]}; gate-mutation.py never imported or executed",
        "base": {
            "rev": rev,
            "path": TARGET,
            "bytes": len(blob),
            "sha256": hashlib.sha256(blob).hexdigest(),
            "selftest": {"exit": p_exit, "cases": p_cases_n,
                         "failures": p_failures, "summary_line": p_summary,
                         "failed_cases": sorted(n for n, ok in p_cases.items() if not ok),
                         "case_names": sorted(p_cases)},
            "mutants_total": len(results),
            "killed": len(killed_ids),
            "killed_ids": killed_ids,
            "survivors": len(survivor_ids),
            "survivor_ids": survivor_ids,
            "declared_case_absent_ids": absent_ids,
            "declared_case_absent_in_pristine_ids": absent_in_pristine,
            "mutants": results,
        },
        "mutants_frozen_at": {"rev": freeze, "tool": TOOL,
                              "count": len(mutants),
                              "ids": [m["id"] for m in mutants]},
        "mutant_table_cross_check": agreement,
        "refusal_control": control,
        "control": "two-anchor source, consumed-anchor reapply and anchor-absent refusals",
        "reproduces_expected_base_arm": reproduces,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev", default=BASE_REV)
    ap.add_argument("--freeze", default=FREEZE_REV)
    ap.add_argument("--work", required=True)
    ap.add_argument("--json-out")
    args = ap.parse_args(argv)
    work = os.path.abspath(args.work)
    os.makedirs(work, exist_ok=True)
    try:
        receipt = battery(os.path.abspath(args.root), args.rev, args.freeze, work)
    except Unevaluable as exc:
        print(json.dumps({"ok": False, "unevaluable": str(exc)}))
        return 2
    text = json.dumps(receipt, indent=1, sort_keys=True)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
    print(text)
    return 0 if receipt["reproduces_expected_base_arm"] else 1


if __name__ == "__main__":
    sys.exit(main())
