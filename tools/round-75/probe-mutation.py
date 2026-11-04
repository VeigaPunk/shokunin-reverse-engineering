#!/usr/bin/env python3
"""probe-mutation.py - round-75 instrument (R75-C1 operability).

Round 74's battery closed the six A12 selftest survivors round 73's MutProbe
found.  The round-74 wave then found three further survivors outside that
frozen class set and one cross-binding:

  * `home_under`/`tmpdir_under` are checked with `is True`, but every fixture
    feeds a real boolean, so a truthiness mutation survives;
  * `_name_samples` kept one sample per shim name (first-wins), so a mutation
    to last-wins is invisible -- and either direction can hide a dirty launch
    behind a clean one;
  * `lie_clean`'s exact key-list equality can be replaced by a superset test;
  * dropping the `canary_present` field also failed
    `a12-kernel-multiple-samples`, so the canary-field case was not the sole
    detector its row claimed.

This battery scores the extended class set against the round-75 blob, and
reports for every mutant whether its declared case was the SOLE detector
(`sole_detector`).  Two patch sets:

  r75base  the fourteen classes applied to the LANDED round-74 blob: the four
           classes round 75 closes survive, and `b-drop-canary-field` is not
           killed by its case alone (the cross-binding).
  r75probe the fifteen classes applied to the round-75 blob, where each is
           expected KILLED by its declared case and the canary field's case is
           its sole detector.

A mutant is killed only when the selftest fails AND its `failures` list names
the declared case.  The pristine blob must be green at or above the registered
case count before any mutant is scored.  The target blob is hashed and
pin-compared BEFORE any generated copy executes (round-74 SentinelScope
SS74-2): an unpinned target is recorded as unpinned, never as matched, and a
pinned mismatch is exit 2 with nothing executed.  Each detector runs in its own
process group and is killed on timeout (SS74-4 cleanup).

Exit: 0 the expectation is met; 1 expectation missed, each survivor and
wrong-case kill named; 2 could-not-evaluate.
`--validate <receipt>` checks a receipt's structural honesty.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import signal
import subprocess
import sys
import tempfile

SCHEMA = "kaidoku-r75-probe-mutation-v1"

# The ten defect classes round-73's MutProbe applied, expressed as exact-once
# text patches per blob.  Each entry: (name, anchor, replacement, expect_case).
SHARED = [
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
     '        for s in _samples(forged_kernel))',
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

# The five round-75 classes: the identity twins, both duplicate-drop
# directions, and the superset key test.
HOME_TRUTHY = ("d-home-under-truthy",
               '                          and s.get("home_under") is True',
               '                          and bool(s.get("home_under"))',
               "a12-genuine-field-identity")
TMP_TRUTHY = ("d-tmpdir-under-truthy",
              '                          and s.get("tmpdir_under") is True',
              '                          and bool(s.get("tmpdir_under"))',
              "a12-genuine-field-identity")
NAME_LAST = ("d-name-samples-last-wins",
             '        out.setdefault(name or "?", []).append(sample)',
             '        out[name or "?"] = [sample]',
             "a12-sample-name-merge")
NAME_FIRST = ("d-name-samples-first-wins",
              '        out.setdefault(name or "?", []).append(sample)',
              '        out.setdefault(name or "?", [sample])',
              "a12-sample-name-merge")
LIE_SUPERSET = ("d-lie-clean-superset",
                '        sorted(s.get("keys") or []) == allow and not s.get("canary_present")\n'
                '        for s in forged_shims.values())',
                '        set(s.get("keys") or []) >= set(allow) and not s.get("canary_present")\n'
                '        for s in forged_shims.values())',
                "a12-lie-clean-keys-exact")

R75 = SHARED + [HOME_TRUTHY, TMP_TRUTHY, NAME_LAST, NAME_FIRST, LIE_SUPERSET]

# The base world: the round-74 blob, where `_name_samples` is first-wins by
# construction (one sample per name), so only the last-wins direction is a
# mutation there; the other four closed classes survive.
R75_BASE = list(SHARED)
R75_BASE[R75_BASE.index(("a-any-forged-sample",
                         '    forged_detected = bool(forged_kernel) and any(\n'
                         '        sorted(s.get("keys") or []) != allow or s.get("canary_present")\n'
                         '        for s in _samples(forged_kernel))',
                         '    forged_detected = bool(forged_kernel)', "a12-kernel-cases"))] = (
    "a-any-forged-sample",
    '    forged_detected = bool(forged_kernel) and any(\n'
    '        sorted(s.get("keys") or []) != allow or s.get("canary_present")\n'
    '        for s in forged_kernel.values())',
    '    forged_detected = bool(forged_kernel)', "a12-kernel-cases")
R75_BASE += [
    HOME_TRUTHY, TMP_TRUTHY,
    ("d-name-samples-last-wins",
     '        out.setdefault(name or "?", sample)',
     '        out[name or "?"] = sample',
     "a12-sample-name-merge"),
    LIE_SUPERSET,
]

PATCH_SETS = {
    "r75base": {"tool": "tools/round-74/seam-probe.py", "mutants": R75_BASE,
                "min_pristine_cases": 20},
    "r75probe": {"tool": "tools/round-75/seam-probe.py", "mutants": R75,
                 "min_pristine_cases": 25},
}

RUNNER = "tools/round-75/probe-mutation.py"


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


def classify(rc: int | None, failed: list[str], expect_case: str | None) -> str:
    """A mutant is killed only by a selftest failure naming its declared case."""
    if rc == 0:
        return "survived"
    if expect_case is None:
        return "killed"
    return "killed" if expect_case in (failed or []) else "killed_wrong_case"


def check_pin(expected: str | None, actual: str, where: str = "") -> None:
    """SS74-2: a supplied pin is compared before any generated copy executes."""
    if expected is not None and expected != actual:
        raise Unevaluable(
            f"target pin mismatch before execution: expected {expected}, "
            f"blob at {where or 'target'} is {actual}")


def kill_group(proc: subprocess.Popen) -> None:
    """Exception-safe child cleanup: the detector runs in its own group."""
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    except (ProcessLookupError, PermissionError, OSError):
        pass
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        pass


def run_detector(copy_path: str, cwd: str, work: str) -> dict:
    env = dict(os.environ)
    env["TMPDIR"] = work
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = None
    try:
        proc = subprocess.Popen([sys.executable, "-I", "-B", copy_path,
                                 "--selftest"],
                                cwd=cwd, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True,
                                start_new_session=True)
        stdout, stderr = proc.communicate(timeout=600)
        rc = proc.returncode
    except subprocess.TimeoutExpired:
        if proc is not None:
            kill_group(proc)
        stdout, stderr, rc = "", "detector timed out after 600s", None
    finally:
        if proc is not None and proc.poll() is None:
            kill_group(proc)
    failed: list[str] = []
    cases = None
    try:
        payload = json.loads(stdout)
        failed = payload.get("failures") or []
        cases = payload.get("cases")
    except (json.JSONDecodeError, AttributeError):
        pass
    return {"rc": rc, "failed": failed, "cases": cases,
            "stderr_tail": (stderr or "")[-400:]}


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
        verdict = classify(run["rc"], run["failed"], expect_case)
        sole = (None if expect_case is None
                else (verdict == "killed" and run["failed"] == [expect_case]))
        rows.append({"name": name, "expect_case": expect_case,
                     "rc": run["rc"], "failed": run["failed"],
                     "cases": run["cases"], "verdict": verdict,
                     "sole": sole})
    return {"work": scratch, "pristine": pristine,
            "pristine_ok": pristine_ok, "mutants": rows}


def score(root: str, rev: str, tool: str, patch_set: str, work: str,
          min_pristine_cases: int | None,
          expect_target_sha256: str | None,
          expect_survivors: int | None,
          expect_survivor_names: list[str] | None,
          expect_sole: list[str] | None) -> dict:
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
    # SS74-2: the pin is compared BEFORE any generated copy executes.
    check_pin(expect_target_sha256, target_sha, f"{rev}:{tool}")
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
    sole_map = {r["name"]: r["sole"] for r in rows}
    multi = [r["name"] for r in rows if r["sole"] is False]
    pin = {"expect": expect_target_sha256,
           "matched": (None if expect_target_sha256 is None
                       else expect_target_sha256 == target_sha),
           "pinned": expect_target_sha256 is not None,
           "pinned_before_exec": True}
    # The runner binding is the bytes that actually executed (round-74 routed
    # defect 5: reading the runner at the target revision made the base arm
    # bind null, because a round-75 tool does not exist at the round-74 base).
    try:
        with open(os.path.abspath(__file__), "rb") as fh:
            runner_bytes = fh.read()
        runner = {"path": RUNNER, "sha256": sha256_bytes(runner_bytes)}
    except OSError:
        runner = {"path": RUNNER, "sha256": None}
    ok = bool(pristine_ok and not wrong)
    if expect_survivors is not None:
        ok = ok and len(survivors) == expect_survivors
    if expect_survivor_names is not None:
        ok = ok and sorted(survivors) == sorted(expect_survivor_names)
    if expect_target_sha256 is not None:
        ok = ok and pin["matched"] is True
    for name in (expect_sole or []):
        ok = ok and sole_map.get(name) is True
    return {"schema": SCHEMA, "patch_set": patch_set, "tool": tool, "rev": rev,
            "root": os.path.abspath(root), "work": scratch,
            "target_sha256": target_sha, "target_pin": pin, "runner": runner,
            "min_pristine_cases": floor, "pristine": pristine,
            "pristine_ok": pristine_ok, "mutants": rows,
            "survivor_count": len(survivors), "survivors": survivors,
            "killed": killed, "killed_wrong_case": wrong,
            "sole_detector": sole_map, "multi_detected": multi,
            "expected": {"survivors": expect_survivors,
                         "survivor_names": expect_survivor_names,
                         "sole": expect_sole},
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
    sole = receipt.get("sole_detector") or {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        expect = row.get("expect_case")
        want = (None if expect is None
                else row.get("verdict") == "killed"
                and row.get("failed") == [expect])
        if sole.get(row.get("name")) != want:
            defects.append(f"sole_detector disagrees for {row.get('name')}")
    pin = receipt.get("target_pin") or {}
    if pin.get("pinned_before_exec") is not True:
        defects.append("target_pin does not record pin-before-execution")
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
        apply_patch("a x b x c", "x", "y")
        cases["patch-ambiguous-refused"] = False
    except Unevaluable:
        cases["patch-ambiguous-refused"] = True
    cases["classify-killed"] = (
        classify(1, ["a12-case"], "a12-case") == "killed")
    cases["classify-wrong-case"] = (
        classify(1, ["other"], "a12-case") == "killed_wrong_case")
    cases["classify-survived"] = classify(0, [], "a12-case") == "survived"
    cases["classify-none"] = classify(1, [], None) == "killed"
    try:
        check_pin("aa", "bb", "self")
        cases["pin-mismatch-refused"] = False
    except Unevaluable:
        cases["pin-mismatch-refused"] = True
    cases["pin-unpinned-ok"] = check_pin(None, "bb") is None
    cases["pin-match-ok"] = check_pin("bb", "bb") is None
    print(json.dumps({"selftest": RUNNER, "cases": len(cases),
                      "case_names": sorted(cases),
                      "failures": [k for k, v in cases.items() if not v]},
                     indent=1, sort_keys=True))
    return 0 if all(cases.values()) else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev")
    ap.add_argument("--tool")
    ap.add_argument("--patch-set")
    ap.add_argument("--work")
    ap.add_argument("--min-pristine-cases", type=int)
    ap.add_argument("--expect-target-sha256")
    ap.add_argument("--expect-survivors", type=int)
    ap.add_argument("--expect-survivor-names")
    ap.add_argument("--expect-sole", action="append", default=[])
    ap.add_argument("--json-out")
    ap.add_argument("--validate")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if args.validate:
        return validate(args.validate)
    missing = [name for name in ("rev", "tool", "patch_set", "work")
               if not getattr(args, name)]
    if missing:
        print(json.dumps({"unevaluable": "missing required arguments: "
                                          + ", ".join(missing)}))
        return 2
    try:
        names = (args.expect_survivor_names.split(",")
                 if args.expect_survivor_names else None)
        receipt = score(args.root, args.rev, args.tool, args.patch_set,
                        args.work, args.min_pristine_cases,
                        args.expect_target_sha256, args.expect_survivors,
                        names, args.expect_sole)
    except Unevaluable as exc:
        print(json.dumps({"unevaluable": str(exc)}))
        return 2
    payload = json.dumps(receipt, indent=1, sort_keys=True)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(payload + "\n")
    print(payload)
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
