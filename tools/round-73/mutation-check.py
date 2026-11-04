#!/usr/bin/env python3
"""mutation-check.py - round-72 instrument (R72-C2 calibration; R69-C1 retained).

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

Round 72 adds the A10 self-mutant the round-71 wave reported as survivor i
(`binding_ok = True` in the seam probe): the r71 patch set applies it to
tools/round-71/seam-probe.py and must see it SURVIVE (the probe never bound
its verdict to the checker), and the r72 patch set applies it to
tools/round-72/seam-probe.py and must see it KILLED naming
`a10-binding-from-checker`.

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
import tempfile

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
PATCH_SETS["r70"] = list(PATCH_SETS["r69"])
# R72-C2: the A10 self-mutant the round-71 wave's MutReaders reported as
# survivor i (probe:471, `binding_ok = True`) scored against the two probes.
# On the round-71 probe it must SURVIVE (the probe never had a case that binds
# the verdict to the checker); on the round-72 probe it must be KILLED, and the
# failure must name `a10-binding-from-checker`.
PATCH_SETS["r71"] = [
    ("A10_binding_force_true",
     'binding_ok = (receipt or {}).get("run_binding") == want_binding',
     'binding_ok = True', None),
]
PATCH_SETS["r72"] = [
    ("A10_binding_force_true",
     'binding_ok = clauses.get("run_binding") is True and present',
     'binding_ok = True', "a10-binding-from-checker"),
]
# Round 73 (R73-C3): the three reader seams the round-72 MutReaders probe
# reported as selftest survivors (a git-reader env, b checker-readelf env, c
# implicit-capsule derivation).  On tools/round-73/packed-elf.py each is killed
# by its named case; on the round-72 bytes the same defect classes survive,
# which is the base arm (`r73base`).
PATCH_SETS["r73"] = [
    ("git_reader_env_dropped",
     '        proc = run(["git", "-C", root, "show", f"{rev}:{path}"], timeout=120,\n'
     '                   env=env, capture=capture)',
     '        proc = run(["git", "-C", root, "show", f"{rev}:{path}"], timeout=120,\n'
     '                   env=None, capture=capture)',
     "git-reader-allowlisted-exec"),
    ("readelf_env_dropped",
     '            rh = readelf_header(row["source"], env=cenv, capture=capture)',
     '            rh = readelf_header(row["source"], capture=capture)',
     "checker-readelf-allowlisted-exec"),
    ("implicit_capsule_dropped",
     '    if not isinstance(observed, dict) or not isinstance(observed.get("log"), str):\n'
     '        return out\n'
     '    cand = observed["log"]',
     '    if not isinstance(observed, dict) or not isinstance(observed.get("log"), str):\n'
     '        return out\n'
     '    return out\n'
     '    cand = observed["log"]',
     "implicit-capsule-polluted-raw-log"),
]
PATCH_SETS["r73base"] = [
    ("git_reader_env_dropped",
     '        proc = run(["git", "-C", root, "show", f"{rev}:{path}"], timeout=120,\n'
     '                   env=env, capture=capture)',
     '        proc = run(["git", "-C", root, "show", f"{rev}:{path}"], timeout=120,\n'
     '                   env=None, capture=capture)', None),
    ("readelf_env_dropped",
     '            rh = run(["readelf", "-h", row["source"]], env=cenv, capture=capture)',
     '            rh = run(["readelf", "-h", row["source"]], capture=capture)', None),
    ("implicit_capsule_dropped",
     '    if capsule_path is None and isinstance(observed, dict) \\\n'
     '            and isinstance(observed.get("log"), str):',
     '    if False and isinstance(observed, dict) \\\n'
     '            and isinstance(observed.get("log"), str):', None),
]
EXPECTED_SURVIVORS = {"r68": 5, "r69": 0, "r70": 0, "r71": 1, "r72": 0,
                      "r73": 0, "r73base": 3}


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
    payload = selftest_json(proc.stdout, proc.stderr) or {}
    # Two selftest schemas in this lane: the route prints `failed`, the probe
    # prints `failures` and no `ok`.  Normalise both (R72-C2 needs the probe).
    failed = payload["failed"] if "failed" in payload else payload.get("failures")
    ok = payload["ok"] if "ok" in payload else (
        isinstance(failed, list) and not failed)
    return {"rc": proc.returncode,
            "cases": payload.get("cases"),
            "failed": failed,
            "ok": ok,
            "stderr_tail": proc.stderr[-400:] if proc.returncode not in (0, 1) else ""}


def git_blob(root: str, rev: str, tool: str) -> bytes:
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{tool}"],
                          capture_output=True)
    if proc.returncode != 0:
        raise Unevaluable(f"git show {rev}:{tool} failed rc={proc.returncode}")
    return proc.stdout


def check(work: str, root: str, rev: str, tool: str, patch_set: str,
          expect_target_sha256: str | None = None,
          min_pristine_cases: int | None = None) -> dict:
    if patch_set not in PATCH_SETS:
        raise Unevaluable(f"patch set unknown: {patch_set}")
    if not os.path.isdir(work):
        raise Unevaluable(f"--work is not a directory: {work}")
    data = git_blob(root, rev, tool)
    target_sha = sha256_bytes(data)
    # Per-run scratch: a mkdtemp of our own for every invocation, so two runs
    # sharing one --work never clobber each other (round-69 M69-11).
    scratch = tempfile.mkdtemp(prefix="mutation-check-", dir=work)
    pristine = os.path.join(scratch, "pristine-" + os.path.basename(tool))
    with open(pristine, "wb") as fh:
        fh.write(data)
    # The tool may import a sibling lane module (round-72's packed-elf imports
    # capsule_audit.py); every scratch copy needs it or the selftest dies at
    # import and the battery reports an unevaluable world.
    srcdir = os.path.join(os.path.abspath(root), os.path.dirname(tool))
    for mod in ("capsule_audit.py",):
        src = os.path.join(srcdir, mod)
        if os.path.isfile(src):
            shutil.copy(src, os.path.join(scratch, mod))
    base = run_selftest(pristine)
    if base["rc"] != 0 or base["ok"] is not True:
        raise Unevaluable(f"pristine selftest not green: rc={base['rc']} failed={base['failed']}")
    target_pin_matched = True
    pristine_floor_met = True
    floor_defect = None
    pin_defect = None
    if expect_target_sha256 is not None and expect_target_sha256 != target_sha:
        target_pin_matched = False
        pin_defect = (f"target pin mismatch: computed {target_sha} != "
                      f"declared {expect_target_sha256}")
    if min_pristine_cases is not None:
        if not isinstance(base.get("cases"), int):
            pristine_floor_met = False
            floor_defect = f"pristine.cases {base.get('cases')} not an int"
        elif base["cases"] < min_pristine_cases:
            pristine_floor_met = False
            floor_defect = (f"pristine.cases {base['cases']} < "
                            f"declared floor {min_pristine_cases}")
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
    ok = (len(survivors) == expected and not wrong
          and target_pin_matched and pristine_floor_met)
    return {
        "instrument": tool, "rev": rev, "patch_set": patch_set,
        "target_sha256": target_sha, "pristine": base,
        "pristine_ok": True,
        "work_dir": scratch,
        "target_pin": {"expect": expect_target_sha256, "matched": target_pin_matched,
                       "defect": pin_defect},
        "pristine_floor": {"min": min_pristine_cases, "met": pristine_floor_met,
                           "defect": floor_defect},
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
    if not isinstance(receipt.get("target_sha256"), str) or not receipt.get("target_sha256"):
        defects.append("target_sha256 absent")
    if not isinstance(receipt.get("work_dir"), str) or not receipt.get("work_dir"):
        defects.append("work_dir absent")
    if not isinstance(mutants, list) or not mutants:
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
        if m.get("verdict") == "killed" and m.get("rc") == 0:
            defects.append(f"{m.get('id')}: killed with a green rc")
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
    ap.add_argument("--expect-target-sha256")
    ap.add_argument("--min-pristine-cases", type=int)
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
        receipt = check(args.work, args.root, args.rev, args.tool, args.patch_set,
                        args.expect_target_sha256, args.min_pristine_cases)
    except Unevaluable as exc:
        print(json.dumps({"schema": "kaidoku-r72-mutation-check-v1",
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
