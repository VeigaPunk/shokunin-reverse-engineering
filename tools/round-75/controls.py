#!/usr/bin/env python3
"""controls.py - round-75 do-nothing and near-miss controls (R75-C1, R75-C2).

Every claim's counter must be shown reachable-by-nothing before its data: a
control that skips the claimed work must miss the target, and a near-miss that
differs only in the declared binding must stay red.  This instrument runs the
four controls against the round-75 instruments and prints one receipt.

Arms:

  c1_base_world         the extended class set against the LANDED round-74
                        probe: the four classes round 75 closes survive and the
                        canary field is not the sole detector -- the claim's
                        before-world.
  c1_no_declared_cases  the round-75 probe's new case names renamed (identical
                        assertions, no declared names): the closed mutants now
                        fail a case that is NOT the declared one, so the battery
                        scores `killed_wrong_case` and no kill.  The case
                        NAMES, not merely a red selftest, are what the claim
                        binds.
  c2_do_nothing         the round-75 record audit at the base revision: every
                        atom is false there, so a do-nothing round cannot reach
                        zero mismatches.
  c2_red_fixtures       the audit's four strengthened grammars each reject
                        their red fixture in-process (the cosmetic passes the
                        round-74 wave demonstrated).

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

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_SURVIVORS = ["d-home-under-truthy", "d-tmpdir-under-truthy",
                  "d-name-samples-last-wins", "d-lie-clean-superset"]
RENAMES = [
    'cases["a12-genuine-field-identity"]',
    'cases["a12-sample-name-merge"]',
    'cases["a12-lie-clean-keys-exact"]',
    'cases["a12-kernel-multiple-samples"]',
    'cases["a12-kernel-canary-field"]',
]


def load(name: str):
    spec = importlib.util.spec_from_file_location(
        f"r75_{name}", os.path.join(HERE, f"{name}.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_text(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def git_show(root: str, rev: str, path: str) -> str:
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(f"controls: git show {rev}:{path} failed")
    return proc.stdout


def arm(name: str, ok: bool, observed: dict) -> dict:
    return {"name": name, "ok": bool(ok), "observed": observed}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--base-rev", required=True)
    ap.add_argument("--after-rev")
    ap.add_argument("--work", required=True)
    ap.add_argument("--json-out")
    args = ap.parse_args(argv)
    work = os.path.abspath(args.work)
    if not os.path.isdir(work):
        print(json.dumps({"unevaluable": f"--work is not a directory: {work}"}))
        return 2
    root = os.path.abspath(args.root)
    battery = load("probe-mutation")
    audit_mod = load("record-audit")
    arms = []

    # -- c1_base_world ------------------------------------------------------
    base_text = git_show(root, args.base_rev, "tools/round-74/seam-probe.py")
    base_scored = battery.score_text(base_text, battery.PATCH_SETS["r75base"]["mutants"],
                                     root, work, 20)
    survivors = sorted(r["name"] for r in base_scored["mutants"]
                       if r["verdict"] == "survived")
    canary_row = next((r for r in base_scored["mutants"]
                       if r["name"] == "b-drop-canary-field"), {})
    base_ok = (base_scored["pristine_ok"] and survivors == sorted(BASE_SURVIVORS)
               and canary_row.get("sole") is False
               and len(canary_row.get("failed") or []) > 1)
    arms.append(arm("c1_base_world", base_ok,
                    {"survivors": survivors, "pristine_cases":
                     base_scored["pristine"]["cases"],
                     "canary_failed": canary_row.get("failed"),
                     "canary_sole": canary_row.get("sole")}))

    # -- c1_no_declared_cases ----------------------------------------------
    if args.after_rev:
        after_text = git_show(root, args.after_rev, "tools/round-75/seam-probe.py")
        after_pristine = battery.run_detector(
            _write(work, "after-pristine.py", after_text), root, work)
    else:
        after_text = read_text(os.path.join(root, "tools/round-75/seam-probe.py"))
        after_pristine = battery.run_detector(
            os.path.join(root, "tools/round-75/seam-probe.py"), root, work)
    renamed = after_text
    for anchor in RENAMES:
        renamed = battery.apply_patch(renamed, anchor, anchor.replace('["', '["x-'))
    renamed_path = _write(work, "renamed-cases.py", renamed)
    closed = {"d-home-under-truthy", "d-tmpdir-under-truthy",
              "d-name-samples-last-wins", "d-name-samples-first-wins",
              "d-lie-clean-superset", "b-drop-canary-field",
              "b-first-sample-only"}
    subset = [m for m in battery.PATCH_SETS["r75probe"]["mutants"]
              if m[0] in closed]
    renamed_scored = battery.score_text(renamed, subset, root, work, 25)
    renamed_killed = [r["name"] for r in renamed_scored["mutants"]
                      if r["verdict"] == "killed"]
    renamed_wrong = [r["name"] for r in renamed_scored["mutants"]
                     if r["verdict"] == "killed_wrong_case"]
    no_case_ok = (after_pristine["rc"] == 0 and renamed_scored["pristine_ok"]
                  and not renamed_killed
                  and len(renamed_wrong) >= 6)
    arms.append(arm("c1_no_declared_cases", no_case_ok,
                    {"pristine_rc": after_pristine["rc"],
                     "renamed_pristine_ok": renamed_scored["pristine_ok"],
                     "killed": renamed_killed, "wrong_case": renamed_wrong,
                     "renamed_path": renamed_path}))

    # -- c2_do_nothing ------------------------------------------------------
    if args.after_rev:
        audit_text = git_show(root, args.after_rev, "tools/round-75/record-audit.py")
        audit_path = _write(work, "record-audit-copy.py", audit_text)
    else:
        audit_path = os.path.join(root, "tools/round-75/record-audit.py")
    proc = subprocess.run([sys.executable, "-I", "-B", audit_path,
                           "--root", root, "--rev", args.base_rev],
                          capture_output=True, text=True, cwd=root)
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        payload = {}
    do_nothing_ok = (payload.get("mismatch_count") == len(audit_mod.ATOMS)
                     and payload.get("ok") is False)
    arms.append(arm("c2_do_nothing", do_nothing_ok,
                    {"rc": proc.returncode,
                     "mismatch_count": payload.get("mismatch_count"),
                     "mismatches": payload.get("mismatches"),
                     "stderr_tail": (proc.stderr or "")[-300:]}))

    # -- c2_red_fixtures ----------------------------------------------------
    cases = audit_mod.grammar_cases()
    red_ok = bool(cases) and all(cases.values())
    arms.append(arm("c2_red_fixtures", red_ok, {"cases": cases}))

    ok = all(row["ok"] for row in arms)
    receipt = {"schema": "kaidoku-r75-controls-v1", "base_rev": args.base_rev,
               "after_rev": args.after_rev, "arms": arms, "ok": ok}
    text = json.dumps(receipt, indent=1, sort_keys=True)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(text)
    return 0 if ok else 1


def _write(work: str, name: str, text: str) -> str:
    path = os.path.join(work, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


if __name__ == "__main__":
    sys.exit(main())
