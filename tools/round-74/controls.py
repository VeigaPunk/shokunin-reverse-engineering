#!/usr/bin/env python3
"""controls.py - round-74 do-nothing and near-miss controls (R74-C1, R74-C2).

Every claim's counter must be shown reachable-by-nothing before its data: a
control that skips the claimed work must miss the target, and a near-miss that
differs only in the declared binding must stay red.  This instrument runs the
four controls against the round-74 instruments and prints one receipt.

Arms:

  c1_base_world        the ten defect classes against the LANDED round-73
                       probe: the four previously-bound mutants die, the six
                       MutProbe survivors survive -- the claim's before-world.
  c1_no_declared_cases the round-74 probe's six new cases renamed (identical
                       assertions, no declared names): the six mutants now
                       fail a case that is NOT the declared one, so the battery
                       scores them killed_wrong_case and no kill.  The case
                       NAMES, not merely a red selftest, are what the claim
                       binds.
  c2_do_nothing        the round-74 record audit at the base revision: every
                       atom added this round is false there, so a do-nothing
                       round cannot reach the target.
  c2_selftest_reds     the audit's own parser selftest, whose red arms (a
                       two-arm claim row without a selection block, a used-by
                       cell naming a sibling entry) must exist and pass.

Exit: 0 every arm met; 1 an arm missed, named with its observation; 2
could-not-evaluate.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
NEW_ATOMS = ("D7b_before_selection", "D8_capability_rows", "D9_s275_used_by",
             "D10_search_log", "D11_rejected_rows", "D12_census_erratum",
             "D13_readme_newline", "D14_runner_binding", "D15_freeze_pins")
RENAMES = {
    "cases[\"a12-genuine-canary-only\"]": "cases[\"x-a12-genuine-canary-only\"]",
    "cases[\"a12-kernel-multiple-samples\"]": "cases[\"x-a12-kernel-multiple-samples\"]",
    "cases[\"a12-kernel-canary-field\"]": "cases[\"x-a12-kernel-canary-field\"]",
    "cases[\"a12-proc-environ-unreadable\"]": "cases[\"x-a12-proc-environ-unreadable\"]",
    "cases[\"a12-arm-wiring\"]": "cases[\"x-a12-arm-wiring\"]",
    "cases[\"a12-arm-forged-executed\"]": "cases[\"x-a12-arm-forged-executed\"]",
}


def load(name: str):
    spec = importlib.util.spec_from_file_location(
        f"r74_{name}", os.path.join(HERE, f"{name}.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git_show(root: str, rev: str, path: str) -> str:
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(f"controls: git show {rev}:{path} failed")
    return proc.stdout


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--base-rev", required=True)
    ap.add_argument("--audit-rev")
    ap.add_argument("--work", required=True)
    ap.add_argument("--json-out")
    args = ap.parse_args(argv)
    work = os.path.abspath(args.work)
    if not os.path.isdir(work):
        print(f"controls: --work is not a directory: {work}", file=sys.stderr)
        return 2
    promut = load("probe-mutation")
    audit = load("record-audit")
    arms = []

    # -- c1_base_world -----------------------------------------------------
    r73_text = git_show(args.root, args.base_rev, promut.PATCH_SETS["r73probe"]["tool"])
    scored = promut.score_text(r73_text, promut.R73, args.root, work, 14)
    survivors = [r["name"] for r in scored["mutants"]
                 if r["verdict"] == "survived"]
    expect = ["a-drop-genuine-canary", "b-unreadable-empty",
              "b-first-sample-only", "b-drop-canary-field",
              "c-swap-verdict-inputs", "c-skip-forged-subrun"]
    arms.append({"arm": "c1_base_world", "met": sorted(survivors) == sorted(expect),
                 "observed": {"survivors": survivors,
                              "pristine_ok": scored["pristine_ok"]},
                 "expects": expect})

    # -- c1_no_declared_cases ---------------------------------------------
    r74_text = git_show(args.root, args.base_rev, promut.PATCH_SETS["r74probe"]["tool"])
    doctored = r74_text
    for old, new in RENAMES.items():
        if doctored.count(old) != 1:
            print(f"controls: rename site {old} occurs "
                  f"{doctored.count(old)} times", file=sys.stderr)
            return 2
        doctored = doctored.replace(old, new, 1)
    scored = promut.score_text(doctored, promut.R74, args.root, work, 20)
    wrong = [r["name"] for r in scored["mutants"]
             if r["verdict"] == "killed_wrong_case"]
    killed = [r["name"] for r in scored["mutants"] if r["verdict"] == "killed"]
    arms.append({"arm": "c1_no_declared_cases",
                 "met": (sorted(wrong) == sorted(expect) and len(killed) == 4),
                 "observed": {"killed_wrong_case": wrong, "killed": killed,
                              "pristine_ok": scored["pristine_ok"]},
                 "expects": {"killed_wrong_case": expect, "killed": 4}})

    # -- c2_do_nothing -----------------------------------------------------
    receipt = audit.audit(args.root, args.audit_rev or args.base_rev)
    mismatches = receipt["mismatches"]
    arms.append({"arm": "c2_do_nothing",
                 "met": all(atom in mismatches for atom in NEW_ATOMS),
                 "observed": {"mismatch_count": receipt["mismatch_count"],
                              "mismatches": mismatches},
                 "expects": {"every_new_atom_false": list(NEW_ATOMS)}})

    # -- c2_selftest_reds --------------------------------------------------
    selftest_copy = os.path.join(tempfile.mkdtemp(prefix="ctl-selftest-", dir=work),
                                 "record-audit.py")
    with open(selftest_copy, "w", encoding="utf-8") as fh:
        fh.write(git_show(args.root, args.base_rev, "tools/round-74/record-audit.py"))
    proc = subprocess.run([sys.executable, "-I", "-B", selftest_copy, "--selftest"],
                          capture_output=True, text=True,
                          env={**os.environ, "TMPDIR": work})
    reds = ("selection-two-arms-red", "used-by-wrong-entry-red")
    ok = False
    observed = {"rc": proc.returncode, "stdout_tail": proc.stdout[-400:]}
    try:
        payload = json.loads(proc.stdout)
        ok = (proc.returncode == 0 and payload.get("failures") == []
              and all(case in (payload.get("case_names") or [])
                      for case in reds))
        observed["case_names"] = payload.get("case_names")
    except json.JSONDecodeError:
        pass
    arms.append({"arm": "c2_selftest_reds", "met": bool(ok),
                 "observed": observed, "expects": list(reds)})

    receipt = {"schema": "kaidoku-r74-controls-v1", "base_rev": args.base_rev,
               "work": tempfile.mkdtemp(prefix="ctl-", dir=work),
               "arms": arms, "met": sum(1 for a in arms if a["met"]),
               "ok": all(a["met"] for a in arms)}
    text = json.dumps(receipt, indent=1, sort_keys=True)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(text)
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
