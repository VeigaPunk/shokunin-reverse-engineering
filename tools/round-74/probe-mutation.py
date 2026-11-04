#!/usr/bin/env python3
"""probe-mutation.py - round-74 instrument (R74-C1 operability).

Round 73's mutation probe (`MutProbe`) reported six A12 selftest survivors on
`tools/round-73/seam-probe.py`: deleting the genuine-canary conjunct, making an
unreadable `/proc/<pid>/environ` read as an empty environment, keeping only the
first kernel sample, dropping the `canary_present` field, swapping the verdict's
two witnesses and skipping the forged sub-run each left `--selftest` green.
This battery is the frozen scorer for that finding.

Two patch sets, one semantic each:

  r73probe  the same ten defect classes applied to the LANDED round-73 blob
            (the round-73 probe is untouched; the base arm).  Expected: four
            killed by the existing A12 case, the six named survivors green.
  r74probe  the same ten classes applied to the round-74 blob, where each is
            expected KILLED and the failure must name its declared case.

A mutant is killed only when the selftest fails AND its `failures` list names
the declared case: a syntax error, a crash, or a different case is
`killed_wrong_case` and does not count (QUALITY row 108).  The pristine blob
must be green at the registered case count before any mutant is scored
(QUALITY row 109), the patch site must apply exactly once (else exit 2,
unevaluable), and the target blob is pinned by sha256 when `--expect-target-
sha256` is supplied (an absent expectation records the pin as unpinned, never
as matched -- QUALITY row 130).

Exit: 0 the expectation is met (pristine green at the registered case count,
survivor count and -- when given -- survivor names equal, no wrong-case kill);
1 expectation missed, each survivor and wrong-case kill named; 2 could-not-
evaluate (bad argv, unknown revision, patch site absent or ambiguous, pristine
selftest not green, refused --work).
`--validate <receipt>` checks a receipt's structural honesty.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile

SCHEMA = "kaidoku-r74-probe-mutation-v1"

# The ten defect classes round-73's MutProbe applied, expressed as exact-once
# text patches per blob.  Each entry: (name, anchor, replacement, expect_case).
R73 = [
    ("a-drop-forged-detected",
     '    return {"ok": bool(genuine_ok and lie_clean and forged_detected),',
     '    return {"ok": bool(genuine_ok and lie_clean),', None),
    ("a-drop-lie-clean",
     '    return {"ok": bool(genuine_ok and lie_clean and forged_detected),',
     '    return {"ok": bool(genuine_ok and forged_detected),', None),
    ("a-drop-genuine-canary",
     '                  and all(sorted(s.get("keys") or []) == allow\n'
     '                          and not s.get("canary_present")\n'
     '                          and s.get("home_under") is True',
     '                  and all(sorted(s.get("keys") or []) == allow\n'
     '                          and s.get("home_under") is True', None),
    ("a-drop-genuine-rc",
     '    genuine_ok = (genuine.get("rc") == 0\n'
     '                  and {"git", "readelf"} <= set(genuine_kernel)',
     '    genuine_ok = ({"git", "readelf"} <= set(genuine_kernel)', None),
    ("a-any-forged-sample",
     '    forged_detected = bool(forged_kernel) and any(\n'
     '        sorted(s.get("keys") or []) != allow or s.get("canary_present")\n'
     '        for s in forged_kernel.values())',
     '    forged_detected = bool(forged_kernel)', None),
    ("b-unreadable-empty",
     '        with open("/proc/%d/environ" % pid, "rb") as fh:\n'
     '            raw = fh.read()\n'
     '    except OSError:\n'
     '        return None\n'
     '    env = {}',
     '        with open("/proc/%d/environ" % pid, "rb") as fh:\n'
     '            raw = fh.read()\n'
     '    except OSError:\n'
     '        return {}\n'
     '    env = {}', None),
    ("b-first-sample-only",
     '    return list(seen.values())',
     '    return list(seen.values())[:1]', None),
    ("b-drop-canary-field",
     '                "canary_present": "KAIDOKU_ENV_CANARY" in env,\n',
     '', None),
    ("c-swap-verdict-inputs",
     '    verdict = a12_verdict(genuine, forged, CHILD_ENV_KEYS)',
     '    verdict = a12_verdict(forged, genuine, CHILD_ENV_KEYS)', None),
    ("c-skip-forged-subrun",
     '    forged = {"rc": f_rcs, "shims": _parse_shims(f_shims, CHILD_ENV_KEYS),\n'
     '              "kernel": _name_samples(f_samples, os.path.join(f_dir, "shims"))}',
     '    forged = {"rc": [], "shims": {}, "kernel": {}}', None),
]

R74 = [
    ("a-drop-forged-detected",
     '    return {"ok": bool(genuine_ok and lie_clean and forged_detected),',
     '    return {"ok": bool(genuine_ok and lie_clean),', "a12-kernel-cases"),
    ("a-drop-lie-clean",
     '    return {"ok": bool(genuine_ok and lie_clean and forged_detected),',
     '    return {"ok": bool(genuine_ok and forged_detected),', "a12-kernel-cases"),
    ("a-drop-genuine-canary",
     '                  and all(sorted(s.get("keys") or []) == allow\n'
     '                          and not s.get("canary_present")\n'
     '                          and s.get("home_under") is True',
     '                  and all(sorted(s.get("keys") or []) == allow\n'
     '                          and s.get("home_under") is True',
     "a12-genuine-canary-only"),
    ("a-drop-genuine-rc",
     '    genuine_ok = (genuine.get("rc") == 0\n'
     '                  and {"git", "readelf"} <= set(genuine_kernel)',
     '    genuine_ok = ({"git", "readelf"} <= set(genuine_kernel)',
     "a12-kernel-cases"),
    ("a-any-forged-sample",
     '    forged_detected = bool(forged_kernel) and any(\n'
     '        sorted(s.get("keys") or []) != allow or s.get("canary_present")\n'
     '        for s in forged_kernel.values())',
     '    forged_detected = bool(forged_kernel)', "a12-kernel-cases"),
    ("b-unreadable-empty",
     '        with open("/proc/%d/environ" % pid, "rb") as fh:\n'
     '            raw = fh.read()\n'
     '    except OSError:\n'
     '        return None\n'
     '    env = {}',
     '        with open("/proc/%d/environ" % pid, "rb") as fh:\n'
     '            raw = fh.read()\n'
     '    except OSError:\n'
     '        return {}\n'
     '    env = {}', "a12-proc-environ-unreadable"),
    ("b-first-sample-only",
     '    return list(seen.values())',
     '    return list(seen.values())[:1]', "a12-kernel-multiple-samples"),
    ("b-drop-canary-field",
     '                "canary_present": "KAIDOKU_ENV_CANARY" in env,\n',
     '', "a12-kernel-canary-field"),
    ("c-swap-verdict-inputs",
     '    verdict = verdict_fn(genuine, forged, allow)',
     '    verdict = verdict_fn(forged, genuine, allow)', "a12-arm-wiring"),
    ("c-skip-forged-subrun",
     '    spawn = spawn or subprocess.Popen',
     '    return {"rc": [], "shims": {}, "kernel": {}}\n'
     '    spawn = spawn or subprocess.Popen', "a12-arm-forged-executed"),
]

PATCH_SETS = {
    "r73probe": {"tool": "tools/round-73/seam-probe.py", "mutants": R73,
                 "min_pristine_cases": 14},
    "r74probe": {"tool": "tools/round-74/seam-probe.py", "mutants": R74,
                 "min_pristine_cases": 20},
}


class Unevaluable(Exception):
    """Exit-2 class: the battery cannot score, so it claims nothing."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def apply_patch(text: str, anchor: str, replacement: str) -> str:
    """Exact-once text replacement; zero or several sites is unevaluable."""
    count = text.count(anchor)
    if count != 1:
        raise Unevaluable(f"patch site occurs {count} times, need exactly 1")
    return text.replace(anchor, replacement, 1)


def classify(rc: int, failed: list[str], expect_case: str | None) -> str:
    """A mutant is killed only by a selftest failure naming its declared case."""
    if rc == 0:
        return "survived"
    if expect_case is None:
        return "killed"
    return "killed" if expect_case in (failed or []) else "killed_wrong_case"


def run_detector(copy_path: str, cwd: str, work: str) -> dict:
    env = dict(os.environ)
    env["TMPDIR"] = work
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run([sys.executable, "-I", "-B", copy_path, "--selftest"],
                          cwd=cwd, env=env, capture_output=True, text=True,
                          timeout=600)
    failed: list[str] = []
    cases = None
    try:
        payload = json.loads(proc.stdout)
        failed = payload.get("failures") or []
        cases = payload.get("cases")
    except json.JSONDecodeError:
        pass
    return {"rc": proc.returncode, "failed": failed, "cases": cases,
            "stderr_tail": (proc.stderr or "")[-400:]}


def score_text(text: str, mutants, root: str, work: str,
               floor: int) -> dict:
    """Score a mutant set against one instrument text (controls reuse this)."""
    scratch = tempfile.mkdtemp(prefix="mut-text-", dir=work)
    pristine_path = os.path.join(scratch, "pristine.py")
    with open(pristine_path, "w", encoding="utf-8") as fh:
        fh.write(text)
    pristine = run_detector(pristine_path, root, scratch)
    pristine_ok = (pristine["rc"] == 0 and pristine["failed"] == []
                   and isinstance(pristine["cases"], int)
                   and pristine["cases"] >= floor)
    rows = []
    for name, anchor, replacement, expect_case in mutants:
        mutated = apply_patch(text, anchor, replacement)
        path = os.path.join(scratch, f"{name}.py")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(mutated)
        run = run_detector(path, root, scratch)
        rows.append({"name": name, "expect_case": expect_case,
                     "rc": run["rc"], "failed": run["failed"],
                     "cases": run["cases"],
                     "verdict": classify(run["rc"], run["failed"], expect_case)})
    return {"work": scratch, "pristine": pristine,
            "pristine_ok": pristine_ok, "mutants": rows}


def score(root: str, rev: str, tool: str, patch_set: str, work: str,
          min_pristine_cases: int | None,
          expect_target_sha256: str | None,
          expect_survivors: int | None,
          expect_survivor_names: list[str] | None) -> dict:
    if not os.path.isdir(work):
        raise Unevaluable(f"--work is not a directory: {work}")
    spec = PATCH_SETS.get(patch_set)
    if spec is None:
        raise Unevaluable(f"unknown patch set {patch_set}")
    if tool != spec["tool"]:
        raise Unevaluable(f"patch set {patch_set} targets {spec['tool']}, "
                          f"not {tool}")
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{tool}"],
                          capture_output=True)
    if proc.returncode != 0:
        raise Unevaluable(f"git show {rev}:{tool} failed")
    blob = proc.stdout
    target_sha = sha256_bytes(blob)
    text = blob.decode("utf-8")
    floor = min_pristine_cases or spec["min_pristine_cases"]
    scored = score_text(text, spec["mutants"], root, work, floor)
    scratch = scored["work"]
    pristine = scored["pristine"]
    pristine_ok = scored["pristine_ok"]
    rows = scored["mutants"]
    survivors = [r["name"] for r in rows if r["verdict"] == "survived"]
    killed = [r["name"] for r in rows if r["verdict"] == "killed"]
    wrong = [r["name"] for r in rows if r["verdict"] == "killed_wrong_case"]
    pin = {"expect": expect_target_sha256,
           "matched": (None if expect_target_sha256 is None
                       else expect_target_sha256 == target_sha),
           "pinned": expect_target_sha256 is not None}
    runner_blob = subprocess.run(
        ["git", "-C", root, "show", f"{rev}:tools/round-74/probe-mutation.py"],
        capture_output=True)
    runner = {"path": "tools/round-74/probe-mutation.py",
              "sha256": (sha256_bytes(runner_blob.stdout)
                         if runner_blob.returncode == 0 else None)}
    ok = bool(pristine_ok and not wrong)
    if expect_survivors is not None:
        ok = ok and len(survivors) == expect_survivors
    if expect_survivor_names is not None:
        ok = ok and sorted(survivors) == sorted(expect_survivor_names)
    if expect_target_sha256 is not None:
        ok = ok and pin["matched"] is True
    return {"schema": SCHEMA, "patch_set": patch_set, "tool": tool, "rev": rev,
            "root": os.path.abspath(root), "work": scratch,
            "target_sha256": target_sha, "target_pin": pin, "runner": runner,
            "min_pristine_cases": floor, "pristine": pristine,
            "pristine_ok": pristine_ok, "mutants": rows,
            "survivor_count": len(survivors), "survivors": survivors,
            "killed": killed, "killed_wrong_case": wrong,
            "expected": {"survivors": expect_survivors,
                         "survivor_names": expect_survivor_names},
            "ok": ok}


def validate(path: str) -> int:
    """A saved battery receipt is scoreable only when its rows agree."""
    try:
        with open(path, encoding="utf-8") as fh:
            receipt = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"defects": [f"receipt unreadable: {exc}"]}))
        return 1
    defects = []
    rows = receipt.get("mutants")
    if not isinstance(rows, list) or not rows:
        defects.append("mutants absent or empty")
        rows = []
    verdicts = [r.get("verdict") for r in rows if isinstance(r, dict)]
    survivors = [r.get("name") for r in rows
                 if isinstance(r, dict) and r.get("verdict") == "survived"]
    killed = [r.get("name") for r in rows
              if isinstance(r, dict) and r.get("verdict") == "killed"]
    wrong = [r.get("name") for r in rows
             if isinstance(r, dict) and r.get("verdict") == "killed_wrong_case"]
    if sorted(receipt.get("survivors") or []) != sorted(survivors):
        defects.append("survivors disagree with the mutant rows")
    if receipt.get("survivor_count") != len(survivors):
        defects.append("survivor_count disagrees with the mutant rows")
    if sorted(receipt.get("killed") or []) != sorted(killed):
        defects.append("killed disagrees with the mutant rows")
    if sorted(receipt.get("killed_wrong_case") or []) != sorted(wrong):
        defects.append("killed_wrong_case disagrees with the mutant rows")
    if any(v not in {"survived", "killed", "killed_wrong_case"} for v in verdicts):
        defects.append("an unknown mutant verdict")
    pin = receipt.get("target_pin") or {}
    if isinstance(pin.get("expect"), str):
        if pin.get("matched") is not (pin["expect"] == receipt.get("target_sha256")):
            defects.append("target_pin disagrees with target_sha256")
    elif pin.get("matched") is not None:
        defects.append("an unpinned target records a matched value")
    if receipt.get("ok") is True and (wrong or not receipt.get("pristine_ok")):
        defects.append("ok true with a wrong-case kill or a red pristine run")
    print(json.dumps({"validate": path, "defects": defects}, indent=1))
    return 0 if not defects else 1


def selftest() -> int:
    cases = {}
    cases["patch-exact-once"] = (
        apply_patch("a x b", "x", "y") == "a y b")
    try:
        apply_patch("a b", "x", "y")
        cases["patch-absent-refused"] = False
    except Unevaluable:
        cases["patch-absent-refused"] = True
    try:
        apply_patch("x x", "x", "y")
        cases["patch-ambiguous-refused"] = False
    except Unevaluable:
        cases["patch-ambiguous-refused"] = True
    cases["classify-survived"] = classify(0, [], "c") == "survived"
    cases["classify-killed-named"] = (
        classify(1, ["a", "c"], "c") == "killed")
    cases["classify-wrong-case"] = (
        classify(1, ["a"], "c") == "killed_wrong_case")
    cases["classify-crash-no-name"] = (
        classify(1, [], "c") == "killed_wrong_case")
    cases["classify-base-kill"] = classify(1, ["a12-kernel-cases"], None) == "killed"
    print(json.dumps({"selftest": "tools/round-74/probe-mutation.py",
                      "cases": len(cases), "case_names": sorted(cases),
                      "failures": [k for k, v in cases.items() if not v]},
                     indent=1, sort_keys=True))
    return 0 if all(cases.values()) else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root")
    ap.add_argument("--rev")
    ap.add_argument("--tool")
    ap.add_argument("--patch-set")
    ap.add_argument("--work")
    ap.add_argument("--min-pristine-cases", type=int)
    ap.add_argument("--expect-target-sha256")
    ap.add_argument("--expect-survivors", type=int)
    ap.add_argument("--expect-survivor-names")
    ap.add_argument("--json-out")
    ap.add_argument("--validate")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if args.validate:
        return validate(args.validate)
    missing = [name for name, value in (
        ("--root", args.root), ("--rev", args.rev), ("--tool", args.tool),
        ("--patch-set", args.patch_set), ("--work", args.work)) if not value]
    if missing:
        print("probe-mutation: " + ", ".join(missing) + " required",
              file=sys.stderr)
        return 2
    names = (args.expect_survivor_names.split(",")
             if args.expect_survivor_names else None)
    try:
        receipt = score(args.root, args.rev, args.tool, args.patch_set,
                        args.work, args.min_pristine_cases,
                        args.expect_target_sha256, args.expect_survivors,
                        names)
    except Unevaluable as exc:
        print(json.dumps({"schema": SCHEMA, "unevaluable": str(exc)}),
              file=sys.stderr)
        return 2
    text = json.dumps(receipt, indent=1, sort_keys=True)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(text)
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
