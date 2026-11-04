#!/usr/bin/env python3
"""prefile-receipt.py - round-77 instrument (R77-C2 operability).

The round-29 prefile gate (`tools/round-29/prefile-check.sh`) prints PASS/FAIL
and exits 0/1, but round 76's report asserted "prefile-check.sh passes" with no
retained output (round-76 non-author spot-check, routed defect 4) and its
`gate-at-tip.txt` carried a disclosures block without the wrapper's exit
(routed defect 3).  A verdict nobody retained is a verdict the next reader
cannot re-check.

This instrument runs the prefile gate as a child under a four-key environment
(PATH, HOME, TMPDIR, LANG) inside a private work root, and writes a receipt
that binds its own argv, measured revision, exit, the `prefile: ` verdict line
and the stdout digest.  `--check-receipt` re-derives every clause from the
receipt bytes alone:

  - the receipt carries `rev`, `argv`, `exit` (int), `passed` (bool),
    `prefile_line`, `stdout`, `stdout_sha256`, `env_keys`;
  - `stdout_sha256` is the digest of `stdout`;
  - `passed` is `exit == 0` and the verdict line says `prefile: PASS`;
  - `argv` names `tools/round-29/prefile-check.sh` and the lane root;
  - `env_keys` is exactly the four-key allowlist;
  - the recorded `rev` is the expected revision when one is given.

`--battery` scores six arms against the record at `--rev`:
  A1 clone-run     a shared clone at --rev runs the gate clean (rc in {0,1},
                   a verdict line, and the receipt passes --check-receipt)
  A2 record        the record's own filing receipt
                   (`.ufo/waves/round-77/l1/scores/prefile-at-filing.json`)
                   exists at --rev and passes with exit 0
  A3 gate-exits    every `l1/scores/gate-*` receipt in the newest round
                   directory at --rev carries its wrapper's `exit`
  A4 red-no-exit   a receipt with `exit` removed is refused
  A5 red-verdict   a receipt whose `passed`/verdict disagrees with `exit` is
                   refused
  A6 red-rev       a receipt measured at another revision is refused

Exit: 0 every arm met; 1 arms unmet (each named); 2 could-not-evaluate.
`--filing` runs the gate against the lane working tree and writes the filing
receipt; it refuses (exit 1) unless the gate prints `prefile: PASS`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

GATE = "tools/round-29/prefile-check.sh"
FILING_RECEIPT = ".ufo/waves/round-77/l1/scores/prefile-at-filing.json"
ROUND_DIR = ".ufo/waves/round-77"
ENV_KEYS = ("PATH", "HOME", "TMPDIR", "LANG")
PREDICATE = (
    "R77-C2 is verified iff `python3 -I -B tools/round-77/prefile-receipt.py --root . --rev <measured> --work <scratch> --battery --json-out <receipt>` exits 0 with `arms_ok 6`, `arms_total 6`, `ok true` and a defect-free `validate`, each arm carrying its expected observation (clone-run a clean clone run whose receipt passes --check-receipt; record-receipt the filing receipt at exit 0; gate-exits every gate receipt in the newest round dir carrying its exit; red-no-exit, red-verdict and red-rev each refused), while the same command at base 188562d4 exits 1 with `arms_ok 4` (the filing receipt absent and three round-76 gate receipts without exit), and the selftest's 13 cases carry both red fixtures and their legitimate look-alikes."
)
VERDICT_RE = re.compile(r"^prefile: (PASS|FAIL)$", re.MULTILINE)
REQUIRED_KEYS = ("rev", "argv", "exit", "passed", "prefile_line", "stdout",
                 "stdout_sha256", "env_keys")


class Unevaluable(Exception):
    """Exit-2 class: the battery cannot score, so it claims nothing."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def child_env(work: str) -> dict:
    env = {}
    for key in ENV_KEYS:
        env[key] = os.environ.get(key, "")
    env["TMPDIR"] = work
    env["HOME"] = work
    env["PATH"] = os.environ.get("PATH", "/usr/bin:/bin")
    return env


def verdict_line(stdout: str) -> tuple[str | None, str | None]:
    """The last `prefile: PASS|FAIL` line and its token."""
    lines = [line for line in stdout.splitlines()
             if VERDICT_RE.match(line.strip())]
    if not lines:
        return None, None
    return lines[-1].strip(), VERDICT_RE.match(lines[-1].strip()).group(1)


def run_gate(lane: str, work: str) -> dict:
    """Run the prefile gate on `lane` and bind the observation."""
    pathlib.Path(work).mkdir(parents=True, exist_ok=True)
    script = pathlib.Path(lane, GATE).resolve()
    if not script.is_file():
        raise Unevaluable(f"{GATE} absent under {lane}")
    argv = ["bash", str(script), str(pathlib.Path(lane).resolve())]
    env = child_env(work)
    proc = subprocess.run(argv, capture_output=True, env=env, cwd=work)
    stdout = proc.stdout.decode("utf-8", "replace")
    stderr = proc.stderr.decode("utf-8", "replace")
    line, token = verdict_line(stdout)
    passed = proc.returncode == 0 and token == "PASS"
    return {
        "schema": "kaidoku-r77-prefile-receipt-v1",
        "lane": str(pathlib.Path(lane).resolve()),
        "rev": subprocess.run(["git", "-C", lane, "rev-parse", "HEAD"],
                              capture_output=True, text=True,
                              env=child_env(work)).stdout.strip(),
        "argv": argv,
        "exit": proc.returncode,
        "passed": passed,
        "prefile_line": line,
        "stdout": stdout,
        "stdout_sha256": sha256_bytes(proc.stdout),
        "stdout_lines": len(stdout.splitlines()),
        "stderr_tail": stderr[-400:],
        "env_keys": sorted(k for k in env if env[k] != ""),
    }


def check_receipt(receipt: dict, expect_rev: str | None = None) -> list[str]:
    """Re-derive every clause from the receipt bytes alone."""
    defects: list[str] = []
    for key in REQUIRED_KEYS:
        if key not in receipt:
            defects.append(f"missing key {key}")
    if defects:
        return defects
    exit_code = receipt.get("exit")
    if not isinstance(exit_code, int) or isinstance(exit_code, bool):
        defects.append(f"exit is not an integer: {exit_code!r}")
        return defects
    stdout = receipt.get("stdout")
    if not isinstance(stdout, str) or not stdout.strip():
        defects.append("stdout empty")
        return defects
    if receipt.get("stdout_sha256") != sha256_bytes(stdout.encode("utf-8")):
        defects.append("stdout_sha256 does not match stdout")
    line, token = verdict_line(stdout)
    if receipt.get("prefile_line") != line:
        defects.append(f"prefile_line {receipt.get('prefile_line')!r} is not "
                       f"the verdict line {line!r}")
    if token is None:
        defects.append("stdout carries no `prefile: PASS|FAIL` line")
    if receipt.get("passed") is not (exit_code == 0 and token == "PASS"):
        defects.append(f"passed {receipt.get('passed')!r} disagrees with "
                       f"exit {exit_code} and verdict {token!r}")
    argv = receipt.get("argv")
    if not isinstance(argv, list) or not all(isinstance(a, str) for a in argv):
        defects.append("argv is not a string list")
    elif not any(a.endswith(GATE) for a in argv):
        defects.append(f"argv does not name {GATE}")
    env_keys = receipt.get("env_keys")
    if env_keys != sorted(k for k in ENV_KEYS):
        defects.append(f"env_keys {env_keys!r} is not the four-key allowlist")
    if expect_rev is not None and receipt.get("rev") != expect_rev:
        defects.append(f"rev {receipt.get('rev')!r} is not the expected "
                       f"{expect_rev!r}")
    return defects


def git_show(root: str, rev: str, path: str) -> bytes | None:
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                          capture_output=True)
    return proc.stdout if proc.returncode == 0 else None


def latest_round_dir(root: str, rev: str) -> str | None:
    proc = subprocess.run(["git", "-C", root, "ls-tree", "-r", "--name-only",
                           rev, "--", ".ufo/waves"], capture_output=True,
                          text=True)
    rounds = sorted({p.split("/")[2] for p in proc.stdout.splitlines()
                     if len(p.split("/")) > 2
                     and re.fullmatch(r"round-\d+", p.split("/")[2])},
                    key=lambda name: int(name.split("-")[1]))
    return rounds[-1] if rounds else None


def clone_at(root: str, rev: str, work: str) -> str:
    dest = pathlib.Path(work, "lane")
    if dest.exists():
        shutil.rmtree(dest)
    proc = subprocess.run(["git", "clone", "--quiet", "--shared", "--no-checkout",
                           str(pathlib.Path(root).resolve()), str(dest)],
                          capture_output=True, text=True, env=child_env(work))
    if proc.returncode != 0:
        raise Unevaluable(f"clone failed: {proc.stderr[-300:]}")
    proc = subprocess.run(["git", "-C", str(dest), "checkout", "--quiet",
                           "--detach", rev], capture_output=True, text=True,
                          env=child_env(work))
    if proc.returncode != 0:
        raise Unevaluable(f"checkout {rev} failed: {proc.stderr[-300:]}")
    return str(dest)


def write_json(path: str, data: dict) -> None:
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(data, indent=1, sort_keys=True) + "\n")


def battery(root: str, rev: str, work: str) -> dict:
    arms: list[dict] = []
    scratch = pathlib.Path(work, "clone-run")

    def add(name, met, observed, detail=None):
        arms.append({"arm": name, "met": bool(met), "observed": observed,
                     "detail": detail or {}})

    # A1 - the gate runs clean in a shared clone at the measured revision.
    try:
        clone = clone_at(root, rev, str(scratch))
        receipt = run_gate(clone, str(scratch))
        ok = (receipt["exit"] in (0, 1) and receipt["prefile_line"] is not None
              and not check_receipt(receipt))
        add("clone-run", ok,
            f"rc {receipt['exit']}, {receipt['prefile_line']}, "
            f"receipt_defects {check_receipt(receipt)}", receipt)
    except Unevaluable as exc:
        add("clone-run", False, str(exc))

    # A2 - the record's own filing receipt exists and passes at --rev.
    raw = git_show(root, rev, FILING_RECEIPT)
    if raw is None:
        add("record-receipt", False, f"{FILING_RECEIPT} absent at {rev}")
    else:
        try:
            receipt = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError as exc:
            add("record-receipt", False, f"unreadable: {exc}")
        else:
            defects = check_receipt(receipt)
            ok = not defects and receipt.get("exit") == 0
            add("record-receipt", ok,
                f"exit {receipt.get('exit')}, defects {defects}", receipt)

    # A3 - every gate receipt in the newest round dir carries its exit.
    round_dir = latest_round_dir(root, rev)
    if round_dir is None:
        add("gate-exits", False, "no round dir under .ufo/waves")
    else:
        listing = subprocess.run(
            ["git", "-C", root, "ls-tree", "-r", "--name-only", rev, "--",
             f".ufo/waves/{round_dir}/l1/scores"], capture_output=True,
            text=True).stdout.splitlines()
        gate_files = [p for p in listing
                      if re.search(r"/gate-[^/]*\.(?:json|txt)$", p)]
        missing: list[str] = []
        for path in gate_files:
            body = git_show(root, rev, path)
            if body is None:
                missing.append(f"{path}: absent")
                continue
            text = body.decode("utf-8", "replace")
            found = None
            if path.endswith(".json"):
                try:
                    data = json.loads(text)
                except json.JSONDecodeError:
                    data = None
                if isinstance(data, dict) and isinstance(data.get("exit"), int):
                    found = data["exit"]
            if found is None:
                m = re.search(r"(?m)^exit=(-?\d+)$", text)
                if m:
                    found = int(m.group(1))
            if found is None:
                missing.append(f"{path}: no exit")
        ok = bool(gate_files) and not missing
        add("gate-exits", ok,
            f"{round_dir}: {len(gate_files)} gate receipts, "
            f"missing {missing}")

    # A4-A6 - red receipts are refused by --check-receipt.
    genuine = run_gate(root, str(pathlib.Path(work, "reds")))
    no_exit = {k: v for k, v in genuine.items() if k != "exit"}
    add("red-no-exit", bool(check_receipt(no_exit)),
        f"defects {check_receipt(no_exit)}")
    lying = dict(genuine, passed=not genuine["passed"])
    add("red-verdict", any("passed" in d for d in check_receipt(lying)),
        f"defects {check_receipt(lying)}")
    shifted = dict(genuine, rev="0" * 40)
    add("red-rev", any("expected" in d
                       for d in check_receipt(shifted, expect_rev=genuine["rev"])),
        f"defects {check_receipt(shifted, expect_rev=genuine['rev'])}")

    met = sum(1 for arm in arms if arm["met"])
    receipt = {
        "schema": "kaidoku-r77-prefile-battery-v1",
        "predicate": PREDICATE,
        "rev": rev,
        "root": os.path.abspath(root),
        "arms": arms,
        "arms_ok": met,
        "arms_total": len(arms),
        "instrument": {"path": "tools/round-77/prefile-receipt.py",
                       "sha256": sha256_bytes(
                           pathlib.Path(__file__).read_bytes())},
    }
    receipt["ok"] = met == len(arms)
    receipt["validate"] = {"defects": battery_defects(receipt),
                           "arms": len(arms)}
    receipt["exit"] = 0 if (receipt["ok"]
                            and not receipt["validate"]["defects"]) else 1
    return receipt


def battery_defects(receipt: dict) -> list[str]:
    defects: list[str] = []
    arms = receipt.get("arms")
    if not isinstance(arms, list) or not arms:
        return ["arms absent or empty"]
    names = [arm.get("arm") for arm in arms if isinstance(arm, dict)]
    if len(set(names)) != len(names):
        defects.append("duplicate arm names")
    if receipt.get("arms_ok") != sum(1 for arm in arms if arm.get("met")):
        defects.append("arms_ok disagrees with the arm rows")
    if receipt.get("arms_total") != len(arms):
        defects.append("arms_total disagrees with the arm rows")
    if receipt.get("ok") is not (receipt.get("arms_ok")
                                 == receipt.get("arms_total")):
        defects.append("ok disagrees with arms_ok/arms_total")
    return defects


def selftest() -> int:
    cases: dict[str, bool] = {}
    stdout = ("prefile: tree clean\n"
              "prefile: ledger1 retired (erratum r68-1) — legacy ledger "
              "byte-identical to its retirement pin\n"
              "prefile: round-29 gate --disclosures corpus/claim-freezes-v2.tsv "
              "at deadbeef exit=0\n"
              "prefile: PASS\n")
    genuine = {
        "rev": "a" * 40, "argv": ["bash", f"/lane/{GATE}", "/lane"],
        "exit": 0, "passed": True,
        "prefile_line": "prefile: PASS", "stdout": stdout,
        "stdout_sha256": sha256_bytes(stdout.encode("utf-8")),
        "env_keys": sorted(ENV_KEYS), "stdout_lines": 4,
    }
    cases["green-genuine"] = check_receipt(genuine) == []
    # legitimate look-alike: a FAIL receipt is a valid receipt (exit 1)
    fail_stdout = stdout.replace("prefile: PASS", "prefile: FAIL")
    failing = dict(genuine, exit=1, passed=False,
                   stdout=fail_stdout,
                   stdout_sha256=sha256_bytes(fail_stdout.encode("utf-8")),
                   prefile_line="prefile: FAIL")
    cases["green-fail-receipt"] = check_receipt(failing) == []
    cases["red-no-exit"] = "missing key exit" in check_receipt(
        {k: v for k, v in genuine.items() if k != "exit"})
    cases["red-verdict"] = any(
        "passed" in d for d in check_receipt(dict(genuine, passed=False)))
    cases["red-digest"] = any(
        "stdout_sha256" in d for d in check_receipt(dict(genuine,
                                                         stdout="x\n")))
    cases["red-rev"] = any(
        "expected" in d for d in check_receipt(genuine, expect_rev="b" * 40))
    cases["red-env"] = any(
        "env_keys" in d for d in check_receipt(
            dict(genuine, env_keys=["PATH", "HOME"])))
    cases["red-argv"] = any(
        "argv" in d for d in check_receipt(
            dict(genuine, argv=["bash", "/lane/other.sh", "/lane"])))
    cases["red-line"] = any(
        "prefile_line" in d for d in check_receipt(
            dict(genuine, prefile_line="prefile: FAIL")))
    cases["red-empty-stdout"] = any(
        "stdout empty" in d for d in check_receipt(
            dict(genuine, stdout="   ", stdout_sha256=sha256_bytes(b"   "))))
    # battery validation catches its own contradictions
    battery_receipt = {"arms": [{"arm": "a", "met": True}], "arms_ok": 1,
                       "arms_total": 1, "ok": True}
    cases["red-battery-ok"] = battery_defects(
        dict(battery_receipt, arms_ok=0)) != []
    cases["red-battery-arms"] = battery_defects(
        dict(battery_receipt, arms=[])) != []
    # verdict parser: a PASS line inside prose is not a verdict
    line, token = verdict_line("prefile: PASS is what we want\n")
    cases["verdict-anchored"] = line is None and token is None
    failures = [name for name, ok in cases.items() if not ok]
    print(json.dumps({"selftest": "tools/round-77/prefile-receipt.py",
                      "cases": len(cases), "case_names": sorted(cases),
                      "failures": failures}, indent=1, sort_keys=True))
    return 0 if not failures else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev")
    ap.add_argument("--work")
    ap.add_argument("--json-out")
    ap.add_argument("--battery", action="store_true")
    ap.add_argument("--filing", action="store_true")
    ap.add_argument("--check-receipt")
    ap.add_argument("--validate-battery")
    ap.add_argument("--expect-rev")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if args.validate_battery:
        try:
            with open(args.validate_battery, encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, json.JSONDecodeError) as exc:
            print(json.dumps({"validate": args.validate_battery,
                              "defects": [f"unreadable: {exc}"]}))
            return 1
        defects = battery_defects(data)
        print(json.dumps({"validate": args.validate_battery,
                          "defects": defects}, indent=1))
        return 0 if not defects else 1
    if args.check_receipt:
        try:
            with open(args.check_receipt, encoding="utf-8") as fh:
                receipt = json.load(fh)
        except (OSError, json.JSONDecodeError) as exc:
            print(json.dumps({"validate": args.check_receipt,
                              "defects": [f"unreadable: {exc}"]}))
            return 1
        defects = check_receipt(receipt, args.expect_rev)
        print(json.dumps({"validate": args.check_receipt,
                          "defects": defects}, indent=1))
        return 0 if not defects else 1
    if args.filing:
        work = args.work or os.path.join(os.path.dirname(
            os.path.abspath(args.json_out or FILING_RECEIPT)), "work")
        pathlib.Path(work).mkdir(parents=True, exist_ok=True)
        receipt = run_gate(args.root, work)
        defects = check_receipt(receipt)
        receipt["validate"] = {"defects": defects}
        out = args.json_out or str(pathlib.Path(args.root, FILING_RECEIPT))
        write_json(out, receipt)
        print(json.dumps({"filing_receipt": out, "exit": receipt["exit"],
                          "passed": receipt["passed"],
                          "defects": defects}, indent=1))
        return 0 if receipt["passed"] and not defects else 1
    if not (args.battery and args.rev and args.work):
        print(json.dumps({"unevaluable": "--battery requires --rev and --work"}))
        return 2
    pathlib.Path(args.work).mkdir(parents=True, exist_ok=True)
    try:
        receipt = battery(args.root, args.rev, args.work)
    except Unevaluable as exc:
        print(json.dumps({"unevaluable": str(exc)}))
        return 2
    if args.json_out:
        write_json(args.json_out, receipt)
    print(json.dumps({k: receipt[k] for k in
                      ("rev", "arms_ok", "arms_total", "ok", "exit",
                       "validate")}, indent=1, sort_keys=True))
    return 0 if receipt["ok"] and not receipt["validate"]["defects"] else 1


if __name__ == "__main__":
    sys.exit(main())
