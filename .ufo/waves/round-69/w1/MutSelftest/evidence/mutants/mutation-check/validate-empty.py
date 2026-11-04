#!/usr/bin/env python3
"""mutation-check.py - round-69 instrument (R69-C1, calibration, capability).

The round-68 wave named five route mutants that survive every detector the lane
actually runs (M68-6: `identity_ok` decorative, `recovery_ok` self-comparing,
detection without the section clause, `before_ok` self-comparing, the control
arm dropped).  Round 69 closes them at the gate itself: the instrument's
`--selftest` feeds the pure `evaluate_carrier()` seam a FALSE model per arm, so
each mutant must now fail its own selftest case.

This battery applies the five patches to a scratch copy of the instrument under
test and runs ONLY that instrument's `--selftest`:

  r68 patch set  -> tools/round-68/packed-elf.py (frozen at its own round): the
                    five are expected to SURVIVE (13/13 green)
  r69 patch set  -> tools/round-69/packed-elf.py: each is expected KILLED, and
                    the failure must name the arm-false case that binds it

A mutant that exits non-zero without naming its expected case is
`killed_wrong_case` and does not count as a kill: a syntax error is not a gate.

Exit: 0 the frozen expectation met (r68: survivors 5; r69: survivors 0, no
wrong-case kill, pristine selftest green); 1 expectation missed, each survivor
and wrong-case kill named; 2 could-not-evaluate (unknown revision, patch site
absent or ambiguous, pristine selftest not green, refused --work, bad argv).
`--validate <receipt>` checks a receipt's structural honesty (0 well formed,
1 a named defect, 2 unreadable).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

PATCH_SETS = {
    "r68": [
        ("M1_identity", 'and sha256_file(unpacked) == c["sha256"])', 'and True)', None),
        ("M2_recovery", 'and rec_counts == orig_counts',
         'and rec_counts == rec_counts', None),
        ("M3_detected", 'detected = listing["rc"] == 0 and secs == 0',
         'detected = listing["rc"] == 0 and True', None),
        ("M4_before", 'and before_procedures < floor',
         'and before_procedures == before_procedures', None),
        ("M5_control",
         'fold(carriers, all(c["control"]["list_rc"] != 0 and c["control"]["decompress_rc"] != 0\n'
         + " " * 37 +
         'for c in carriers), len(CARRIERS))',
         'fold(carriers, True, len(CARRIERS))', None),
    ],
    "r69": [
        ("M1_identity",
         'identity_ok = model["unpack_rc"] == 0 and model["unpacked_sha256"] == model["pin"]',
         'identity_ok = True', "arm-pack-identity-false"),
        ("M2_recovery",
         'recovery_ok = bool(model["recovered_counts"]) and model["recovered_counts"] == model["orig_counts"]',
         'recovery_ok = bool(model["recovered_counts"])', "arm-pack-recovery-false"),
        ("M3_detected",
         'detected = model["upx_list_rc"] == 0 and model["section_count"] == 0',
         'detected = model["upx_list_rc"] == 0', "arm-pack-detected-false"),
        ("M4_before",
         'before_ok = model["packed_procedures"] is not None and model["packed_procedures"] <= model["before_max_procedures"]',
         'before_ok = model["packed_procedures"] is not None', "arm-pack-before-false"),
        ("M5_control",
         'control_ok = model["control_list_rc"] != 0 and model["control_decompress_rc"] != 0',
         'control_ok = True', "arm-pack-control-false"),
    ],
}
EXPECTED_SURVIVORS = {"r68": 5, "r69": 0}


class Unevaluable(Exception):
    """Exit-2 class: the battery cannot score, so it claims nothing."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def selftest_json(out: str, err: str) -> dict | None:
    for text in (out, err):
        if not text.strip():
            continue
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict) and "cases" in payload:
            return payload
    return None


def run_selftest(path: str) -> dict:
    proc = subprocess.run([sys.executable, "-I", "-B", path, "--selftest"],
                          capture_output=True, text=True, timeout=300)
    payload = selftest_json(proc.stdout, proc.stderr)
    return {"rc": proc.returncode,
            "cases": (payload or {}).get("cases"),
            "failed": (payload or {}).get("failed"),
            "ok": (payload or {}).get("ok"),
            "stderr_tail": proc.stderr[-400:] if proc.returncode not in (0, 1) else ""}


def git_blob(root: str, rev: str, tool: str) -> bytes:
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{tool}"],
                          capture_output=True)
    if proc.returncode != 0:
        raise Unevaluable(f"git show {rev}:{tool} failed rc={proc.returncode}")
    return proc.stdout


def check(work: str, root: str, rev: str, tool: str, patch_set: str) -> dict:
    if patch_set not in PATCH_SETS:
        raise Unevaluable(f"patch set unknown: {patch_set}")
    if not os.path.isdir(work):
        raise Unevaluable(f"--work is not a directory: {work}")
    data = git_blob(root, rev, tool)
    target_sha = sha256_bytes(data)
    scratch = os.path.join(work, "mutation-check")
    shutil.rmtree(scratch, ignore_errors=True)
    os.makedirs(scratch)
    pristine = os.path.join(scratch, "pristine-" + os.path.basename(tool))
    with open(pristine, "wb") as fh:
        fh.write(data)
    base = run_selftest(pristine)
    if base["rc"] != 0 or base["ok"] is not True:
        raise Unevaluable(f"pristine selftest not green: rc={base['rc']} failed={base['failed']}")
    source = data.decode("utf-8")
    mutants = []
    for mid, old, new, expect_case in PATCH_SETS[patch_set]:
        count = source.count(old)
        if count != 1:
            raise Unevaluable(f"patch site {mid} matched {count} times (want 1)")
        mutant = os.path.join(scratch, f"{patch_set}-{mid}-" + os.path.basename(tool))
        with open(mutant, "w", encoding="utf-8") as fh:
            fh.write(source.replace(old, new, 1))
        result = run_selftest(mutant)
        if result["rc"] == 0:
            verdict = "survived"
        elif result["failed"] is not None and expect_case and expect_case in result["failed"]:
            verdict = "killed"
        elif result["failed"] is None and expect_case is None and result["rc"] not in (0, 1):
            verdict = "unevaluable"
        else:
            verdict = "killed_wrong_case"
        mutants.append({"id": mid, "applied": True, "expect_case": expect_case,
                        "rc": result["rc"], "cases": result["cases"],
                        "failed": result["failed"], "verdict": verdict,
                        "stderr_tail": result["stderr_tail"]})
    survivors = [m["id"] for m in mutants if m["verdict"] == "survived"]
    wrong = [m["id"] for m in mutants if m["verdict"] in ("killed_wrong_case", "unevaluable")]
    expected = EXPECTED_SURVIVORS[patch_set]
    ok = len(survivors) == expected and not wrong
    return {
        "instrument": tool, "rev": rev, "patch_set": patch_set,
        "target_sha256": target_sha, "pristine": base,
        "pristine_ok": True,
        "mutants": mutants, "survivors": survivors,
        "killed": [m["id"] for m in mutants if m["verdict"] == "killed"],
        "killed_wrong_case": [m["id"] for m in mutants
                              if m["verdict"] == "killed_wrong_case"],
        "expected_survivors": expected,
        "survivor_count": len(survivors),
        "ok": ok,
    }


def validate(path: str) -> int:
    try:
        with open(path, encoding="utf-8") as fh:
            receipt = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"validate": "mutation-receipt", "unevaluable": str(exc)}))
        return 2
    defects = []
    mutants = receipt.get("mutants")
    if receipt.get("pristine_ok") is not True:
        defects.append("pristine_ok not true")
    if not isinstance(mutants, list):
        defects.append("mutants absent or empty")
        mutants = []
    for m in mutants:
        if not isinstance(m.get("rc"), int):
            defects.append(f"{m.get('id')}: rc not an int")
        if not isinstance(m.get("failed"), list) and m.get("failed") is not None:
            defects.append(f"{m.get('id')}: failed not a list")
        if m.get("applied") is not True:
            defects.append(f"{m.get('id')}: applied not true")
        if not isinstance(m.get("verdict"), str):
            defects.append(f"{m.get('id')}: verdict absent")
    derived = sorted(str(m.get("id")) for m in mutants
                     if m.get("verdict") == "survived")
    if sorted(str(x) for x in receipt.get("survivors") or []) != derived:
        defects.append("survivors disagree with the mutant rows")
    out = {"validate": "mutation-receipt", "path": path, "ok": not defects,
           "defects": defects, "mutants": len(mutants)}
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0 if not defects else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root")
    ap.add_argument("--rev")
    ap.add_argument("--tool")
    ap.add_argument("--patch-set", choices=sorted(PATCH_SETS))
    ap.add_argument("--work")
    ap.add_argument("--json-out")
    ap.add_argument("--validate")
    args = ap.parse_args(argv)
    if args.validate:
        return validate(args.validate)
    if not (args.root and args.rev and args.tool and args.patch_set and args.work):
        print("mutation-check: --root, --rev, --tool, --patch-set and --work are required",
              file=sys.stderr)
        return 2
    try:
        receipt = check(args.work, args.root, args.rev, args.tool, args.patch_set)
    except Unevaluable as exc:
        print(json.dumps({"schema": "kaidoku-r69-mutation-check-v1",
                          "unevaluable": str(exc)}), file=sys.stderr)
        return 2
    text = json.dumps(receipt, indent=1, sort_keys=True)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(text)
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
