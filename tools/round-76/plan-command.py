#!/usr/bin/env python3
"""plan-command.py - round-76 instrument (R76-C2 operability).

Makes a round's PRINTED counting command load-bearing: the command a plan or
report shows a reader must be executable as printed, not a sketch.

Round 75's report printed its R75-C1 counter as
`... --expect-target-sha256 1fc1c8fc… --expect-sole b-drop-canary-field`
(an abbreviated hash with a Unicode ellipsis, no `--work`): pasted as printed
it cannot run, and the round-75 spot-check routed that as defect 4.  This gate
reads a fenced `sh` block between `<!-- counting-command: NAME -->` markers out
of a committed plan, refuses every unbound placeholder, executes the argv with
no shell (shlex.split) under a four-key child environment, and compares the
receipt's counter to the declared target.

Modes
  --block C1 --run       execute one plan block and score its counter
  --battery              three arms: plan-c1 (green), r75-printed (static
                         refusal), r75-argv (execution refusal)
  --control NAME         one do-nothing control, each expected to fail
  --selftest             the control set as cases

Exit: 0 every arm/check met; 1 a defect (named); 2 could-not-evaluate
(missing plan, block, fixture or script); 3 refused (unsafe argv, escape).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile

PLAN76 = "plans/round-76-claims.md"
FIXTURES = ".ufo/waves/round-76/pre/fixtures"
ALLOWED_VARS = {"REV", "WORK", "OUT", "ROOT"}
SAFE_SCRIPT_PREFIX = "tools/round-76/"
ENV_KEYS = ("PATH", "HOME", "TMPDIR", "LANG")
METACHARS = (";", "|", "&", "$(", "`", ">", "<")
BLOCK_RE = re.compile(
    r"<!--\s*counting-command:\s*(?P<name>[A-Za-z0-9_-]+)\s*-->(?P<body>.*?)"
    r"<!--\s*/counting-command\s*-->", re.S)
FENCE_RE = re.compile(r"```(?:sh|bash)\n(?P<cmd>.*?)```", re.S)
ELLIPSIS = ("\u2026", "...")
UNBOUND_RE = re.compile(r"<[^>\n]{1,120}>")
VAR_RE = re.compile(r"\$(?:\{([A-Z_]+)\}|([A-Z_]+))")
SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")


class Refused(Exception):
    """Exit-3 class: the block is unsafe or escapes its work root."""


class Unevaluable(Exception):
    """Exit-2 class: nothing to score."""


# --------------------------------------------------------------------------
# block extraction and static grammar
# --------------------------------------------------------------------------

def read_plan(root: str, rev: str, path: str) -> str:
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise Unevaluable(f"plan absent at {rev}: {path}")
    return proc.stdout


def extract_block(text: str, name: str) -> str:
    for match in BLOCK_RE.finditer(text):
        if match.group("name") != name:
            continue
        fence = FENCE_RE.search(match.group("body"))
        if not fence:
            raise Unevaluable(f"block {name} carries no sh fence")
        return fence.group("cmd").strip()
    raise Unevaluable(f"block {name} absent")


def static_defects(command: str) -> list[str]:
    """Placeholders, unbound variables and shell metacharacters."""
    defects = []
    if UNBOUND_RE.search(command):
        defects.append(
            "PLACEHOLDER_UNBOUND: " + UNBOUND_RE.search(command).group(0))
    for ell in ELLIPSIS:
        if ell in command:
            defects.append(f"PLACEHOLDER_UNBOUND: abbreviation {ell!r}")
    for var in VAR_RE.finditer(command):
        name = var.group(1) or var.group(2)
        if name not in ALLOWED_VARS:
            defects.append(f"VARIABLE_UNBOUND: ${name}")
    for token in METACHARS:
        if token in command:
            defects.append(f"SHELL_METACHAR: {token}")
    return defects


def build_argv(command: str, rev: str, work: str, out: str,
               root: str) -> list[str]:
    joined = command.replace("\\\n", " ")
    argv = shlex.split(joined)
    argv = [tok.replace("$REV", rev).replace("${REV}", rev)
               .replace("$WORK", work).replace("${WORK}", work)
               .replace("$OUT", out).replace("${OUT}", out)
               .replace("$ROOT", root).replace("${ROOT}", root)
            for tok in argv]
    if len(argv) < 4:
        raise Refused(f"argv too short: {argv}")
    if argv[0:3] != ["python3", "-I", "-B"]:
        raise Refused(f"argv is not `python3 -I -B <script>`: {argv[0:3]}")
    script = argv[3]
    if not script.startswith(SAFE_SCRIPT_PREFIX):
        raise Refused(f"script outside {SAFE_SCRIPT_PREFIX}: {script}")
    return argv


def containment(path: str, work_root: str) -> str:
    real = os.path.realpath(path)
    base = os.path.realpath(work_root)
    if os.path.commonpath([real, base]) != base:
        raise Refused(f"path escapes the work root: {path}")
    return real


def child_env(work: str) -> dict:
    home = os.path.join(work, "home")
    tmp = os.path.join(work, "tmp")
    os.makedirs(home, exist_ok=True)
    os.makedirs(tmp, exist_ok=True)
    return {"PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "HOME": home, "TMPDIR": tmp, "LANG": "C.UTF-8"}


# --------------------------------------------------------------------------
# execution
# --------------------------------------------------------------------------

def run_block(root: str, rev: str, command: str, work: str, out: str,
              counter_field: str, expect_counter: str) -> dict:
    """Score one command block: static grammar, then execution, then counter."""
    defects = static_defects(command)
    result = {"command": command, "static_defects": defects,
              "executed": False, "rc": None, "stderr_tail": "",
              "stdout_tail": "", "counter": None, "defects": list(defects)}
    if defects:
        return result
    try:
        argv = build_argv(command, rev, work, out, root)
        out_real = containment(out, work)
        work_real = containment(work, work)
    except Refused as exc:
        result["defects"].append(f"REFUSED: {exc}")
        return result
    env = child_env(work_real)
    proc = subprocess.run(argv, cwd=root, env=env, capture_output=True,
                          text=True, timeout=300)
    result.update({"argv": argv, "executed": True, "rc": proc.returncode,
                   "stderr_tail": proc.stderr[-2000:],
                   "stdout_tail": proc.stdout[-2000:]})
    if proc.returncode != 0:
        result["defects"].append(
            f"EXECUTION_FAILED: rc {proc.returncode}: "
            f"{proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else ''}")
        return result
    try:
        with open(out_real, encoding="utf-8") as fh:
            receipt = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        result["defects"].append(f"RECEIPT_UNREADABLE: {exc}")
        return result
    value = receipt
    for part in counter_field.split("."):
        value = value.get(part) if isinstance(value, dict) else None
    result["counter"] = {"field": counter_field, "value": value,
                         "expected": expect_counter,
                         "matched": str(value) == expect_counter}
    if str(value) != expect_counter:
        result["defects"].append(
            f"COUNTER_MISMATCH: {counter_field} {value!r} != {expect_counter!r}")
    return result


# --------------------------------------------------------------------------
# arms and controls
# --------------------------------------------------------------------------

def arm_plan_c1(root: str, rev: str, work: str) -> dict:
    out = os.path.join(work, "c1-receipt.json")
    try:
        command = extract_block(read_plan(root, rev, PLAN76), "C1")
    except Unevaluable as exc:
        return {"arm": "plan-c1", "expected": "rc 0, mismatch_count 0",
                "observed": f"BLOCK_ABSENT: {exc}", "met": False}
    row = run_block(root, rev, command, work, out, "mismatch_count", "0")
    return {"arm": "plan-c1", "expected": "rc 0, mismatch_count 0",
            "observed": ("rc 0, mismatch_count 0" if not row["defects"]
                         else "; ".join(row["defects"])),
            "met": not row["defects"], "row": row}


def arm_fixture(root: str, rev: str, work: str, name: str,
                counter_field: str, expect: str) -> dict:
    path = f"{FIXTURES}/{name}"
    out = os.path.join(work, name.replace(".md", "-receipt.json"))
    try:
        command = extract_block(read_plan(root, rev, path), "r75")
    except Unevaluable as exc:
        return {"arm": name, "expected": "fixture scored",
                "observed": f"FIXTURE_ABSENT: {exc}", "met": False}
    row = run_block(root, rev, command, work, out, counter_field, expect)
    return {"arm": name, "row": row, "met": None, "expected": None,
            "observed": "; ".join(row["defects"]) or "clean"}


def battery(root: str, rev: str, work: str) -> dict:
    os.makedirs(work, exist_ok=True)
    plan = arm_plan_c1(root, rev, os.path.join(work, "plan"))
    printed = arm_fixture(root, rev, os.path.join(work, "printed"),
                          "r75-printed.md", "survivor_count", "0")
    argv_arm = arm_fixture(root, rev, os.path.join(work, "argv"),
                           "r75-argv.md", "survivor_count", "0")
    printed_expect = "PLACEHOLDER_UNBOUND, no execution"
    argv_expect = "EXECUTION_FAILED, rc 2, missing required arguments: work"
    printed_met = bool(printed.get("row")) and (
        any(d.startswith("PLACEHOLDER_UNBOUND")
            for d in printed["row"]["static_defects"])
        and not printed["row"]["executed"])
    argv_row = argv_arm.get("row") or {}
    argv_met = (bool(argv_row) and argv_row.get("executed") is True
                and argv_row.get("rc") == 2
                and "missing required arguments: work" in argv_row.get(
                    "stderr_tail", ""))
    printed.update({"expected": printed_expect, "met": printed_met,
                    "observed": printed.get("observed")})
    argv_arm.update({"expected": argv_expect, "met": argv_met,
                     "observed": argv_arm.get("observed")})
    arms = [plan, printed, argv_arm]
    ok = all(arm["met"] for arm in arms)
    return {"schema": "kaidoku-r76-plan-command-v1", "rev": rev,
            "plan": PLAN76, "arms": arms, "arms_ok": sum(1 for a in arms
                                                         if a["met"]),
            "arms_total": len(arms), "ok": ok}


CONTROLS = {
    "prose-plan": "the plan block replaced by the round-75 report's printed "
                  "command: PLACEHOLDER_UNBOUND, no execution",
    "missing-required-arg": "a runnable argv with its required --rev removed: "
                            "EXECUTION_FAILED rc 2",
    "ellipsis-rev": "a $REV replaced by an abbreviated hash: "
                    "PLACEHOLDER_UNBOUND",
}


def control(root: str, rev: str, work: str, name: str) -> dict:
    if name not in CONTROLS:
        raise Unevaluable(f"unknown control {name}")
    os.makedirs(work, exist_ok=True)
    if name == "prose-plan":
        command = extract_block(
            read_plan(root, rev, f"{FIXTURES}/r75-printed.md"), "r75")
        row = run_block(root, rev, command, work,
                        os.path.join(work, "out.json"), "survivor_count", "0")
        met = (not row["executed"]
               and any(d.startswith("PLACEHOLDER_UNBOUND")
                       for d in row["static_defects"]))
    elif name == "missing-required-arg":
        command = ("python3 -I -B tools/round-76/record-audit.py --root . "
                   "--rev $REV --json-out $OUT")
        broken = command.replace("--rev $REV ", "")
        row = run_block(root, rev, broken, work,
                        os.path.join(work, "out.json"), "mismatch_count", "0")
        met = (row["executed"] and row["rc"] == 2
               and any(d.startswith("EXECUTION_FAILED")
                       for d in row["defects"]))
    else:  # ellipsis-rev
        command = ("python3 -I -B tools/round-76/record-audit.py --root . "
                   "--rev $REV\u2026 --json-out $OUT")
        row = run_block(root, rev, command, work,
                        os.path.join(work, "out.json"), "mismatch_count", "0")
        met = (not row["executed"]
               and any(d.startswith("PLACEHOLDER_UNBOUND")
                       for d in row["static_defects"]))
    return {"control": name, "expected": CONTROLS[name],
            "met": bool(met), "row": row}


def selftest(root: str, rev: str) -> int:
    work = tempfile.mkdtemp(prefix="plan-command-selftest-")
    try:
        rows = {name: control(root, rev, os.path.join(work, name), name)
                for name in CONTROLS}
    finally:
        subprocess.run(["rm", "-rf", "--", work])
    cases = {name: row["met"] for name, row in rows.items()}
    print(json.dumps({"selftest": "tools/round-76/plan-command.py",
                      "cases": len(cases), "case_names": sorted(cases),
                      "failures": [k for k, v in cases.items() if not v]},
                     indent=1, sort_keys=True))
    return 0 if all(cases.values()) else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--plan", default=PLAN76)
    ap.add_argument("--block")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--battery", action="store_true")
    ap.add_argument("--control")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--work", required=True)
    ap.add_argument("--out")
    ap.add_argument("--counter-field", default="mismatch_count")
    ap.add_argument("--expect-counter", default="0")
    ap.add_argument("--json-out")
    args = ap.parse_args(argv)
    os.makedirs(args.work, exist_ok=True)
    try:
        if args.selftest:
            return selftest(args.root, args.rev)
        if args.control:
            receipt = control(args.root, args.rev, args.work, args.control)
        elif args.battery:
            receipt = battery(args.root, args.rev, args.work)
        elif args.block and args.run:
            command = extract_block(
                read_plan(args.root, args.rev, args.plan), args.block)
            out = args.out or os.path.join(args.work, f"{args.block}.json")
            row = run_block(args.root, args.rev, command, args.work, out,
                            args.counter_field, args.expect_counter)
            receipt = {"schema": "kaidoku-r76-plan-command-v1",
                       "rev": args.rev, "plan": args.plan,
                       "block": args.block, "row": row, "ok": not row["defects"]}
        else:
            raise Unevaluable("one of --run/--battery/--control/--selftest")
    except Unevaluable as exc:
        print(json.dumps({"unevaluable": str(exc)}))
        return 2
    except Refused as exc:
        print(json.dumps({"refused": str(exc)}))
        return 3
    text = json.dumps(receipt, indent=1, sort_keys=True)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(text)
    return 0 if receipt.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
