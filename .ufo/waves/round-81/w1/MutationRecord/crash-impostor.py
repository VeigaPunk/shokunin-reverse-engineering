#!/usr/bin/env python3
"""strictness-battery.py - round-80 counter (R80-C1 calibration).

Scores TWO pointer binders on one frozen fixture set: the candidate
(`--impl`, normally `tools/round-80/pointer-bind.py`) and the round-79 control
(`--control-impl`, `tools/round-79/pointer-bind.py`).  Four red fixtures are
inputs the round-79 binder accepts and a strict binder must refuse; two green
controls are inputs both must bind, so an implementation that refuses
everything cannot pass.

Red fixtures (from `.ufo/waves/round-80/l1/fixtures/strictness.json`, frozen
before data):
  rb01/rb02  the declared pin `rea-agents@6.7.0` occurs only as a prefix of a
             longer live token (`@6.7.05`, `@6.7.00`): a bare substring test
             binds it, an exact-token rule must not.
  rb03/rb04  the record declares the same client cell twice: round 79's dict
             comprehension keeps the last cell and reports 5 cells with no
             duplicate signal; a strict parser counts both and reports the
             duplicate.

Green controls: an exact quoted pin line and a two-line range whose second line
carries the export as a whole token.

A red case is REFUSED by an implementation when
  * bind:   `bind(...)["matched"]` is false, or
  * record: the receipt carries the duplicate id in `duplicates`, or reports
            more cells than the five declared (`checks_total > 5`) and is not ok.

Modes
  (no mode)          score both implementations
  --selftest         the scorer's contract as cases
  --validate FILE    re-derive a saved receipt's counts
Exit: 0 candidate_false_greens == 0, candidate_green_refusals == 0,
      control_false_greens == 4, control_green_refusals == 0; 1 otherwise;
      2 could-not-evaluate.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

ROUND = 80
SCHEMA = "kaidoku-r80-strictness-battery-v1"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
FIXTURES = ".ufo/waves/round-80/l1/fixtures/strictness.json"
BASE = "16dfa009bf143080dfcdfc5f9ec34bd359536d90"


class Unevaluable(Exception):
    """Exit-2 class: an input cannot be loaded."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: str, data) -> None:
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n")


def load_module(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise Unevaluable(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def bind_ok(module, case: dict) -> bool:
    result = module.bind(case["pointer"], list(case["tokens"]),
                         list(case["lines"]))
    return bool(result.get("matched"))


def duplicate_refused(receipt: dict, cell_id: str) -> bool:
    """The Rule's conjunction: every declared cell counted AND the id reported."""
    duplicates = receipt.get("duplicates") or []
    total = receipt.get("checks_total")
    return bool(isinstance(duplicates, list) and cell_id in duplicates
                and isinstance(total, int) and total > 5
                and receipt.get("ok") is not True)


def make_fixture_repo(template: str, append_cell: str, work: str) -> str:
    root = pathlib.Path(work) / "fixture-repo"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    (root / "PROVINCE.md").write_text(template + append_cell + "\n")
    subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
    proc = subprocess.run(["git", "-C", str(root), "rev-parse",
                           "--show-toplevel"], capture_output=True, text=True)
    if proc.returncode != 0 or proc.stdout.strip() != str(root):
        raise Unevaluable("fixture repo is not rooted where it was created")
    subprocess.run(["git", "-C", str(root), "-c", "user.name=fixture",
                    "-c", "user.email=fixture@invalid",
                    "add", "PROVINCE.md"], check=True)
    subprocess.run(["git", "-C", str(root), "-c", "user.name=fixture",
                    "-c", "user.email=fixture@invalid",
                    "commit", "-q", "-m", "fixture record"], check=True)
    return str(root)


def score(module, fixtures: dict, work: str) -> dict:
    rows: list[dict] = []
    for case in fixtures["red_cases"]:
        row = {"case": case["id"], "kind": case["kind"], "refused": False,
               "detail": ""}
        if case["kind"] == "bind":
            row["refused"] = not bind_ok(module, case)
            row["detail"] = "matched" if not row["refused"] else "refused"
        else:
            repo = make_fixture_repo(fixtures["record_template"],
                                     case["append_cell"], work)
            receipt = module.battery(repo, "HEAD", None)
            row["refused"] = duplicate_refused(receipt, case["cell_id"])
            row["detail"] = json.dumps(
                {k: receipt.get(k) for k in ("checks_total", "matched",
                                             "duplicates")}, sort_keys=True)
        rows.append(row)
    greens: list[dict] = []
    for case in fixtures["green_cases"]:
        bound = bind_ok(module, case)
        greens.append({"case": case["id"], "bound": bound,
                       "refused": not bound})
    return {"false_greens": sum(1 for r in rows if not r["refused"]),
            "green_refusals": sum(1 for g in greens if g["refused"]),
            "red": rows, "green": greens}


def validate_receipt(receipt: dict) -> dict:
    defects: list[str] = []
    for arm in ("candidate", "control"):
        block = receipt.get(arm) or {}
        red = block.get("red") or []
        green = block.get("green") or []
        if block.get("false_greens") != sum(1 for r in red if not r.get("refused")):
            defects.append(f"{arm}.false_greens does not re-derive from red rows")
        if block.get("green_refusals") != sum(1 for g in green if g.get("refused")):
            defects.append(f"{arm}.green_refusals does not re-derive from green rows")
        if not HEX64.match(block.get("sha256") or ""):
            defects.append(f"{arm}.sha256 is not a 64-hex digest")
    fixture = receipt.get("fixtures") or {}
    if receipt.get("cases") != len(fixture.get("red_ids") or []):
        defects.append("cases does not re-derive from the fixture red ids")
    if receipt.get("green_cases") != len(fixture.get("green_ids") or []):
        defects.append("green_cases does not re-derive from the fixture green ids")
    cand = receipt.get("candidate") or {}
    ctrl = receipt.get("control") or {}
    if receipt.get("ok"):
        if cand.get("false_greens") != 0:
            defects.append("ok true with candidate false greens")
        if cand.get("green_refusals") != 0:
            defects.append("ok true with candidate green refusals")
        if ctrl.get("false_greens") != receipt.get("cases"):
            defects.append("ok true while the control does not reproduce "
                           "every red case")
        if ctrl.get("green_refusals") != 0:
            defects.append("ok true while the control refuses a green control")
    if not receipt.get("checked_at"):
        defects.append("checked_at is absent")
    inst = receipt.get("instrument") or {}
    if inst.get("sha256") != sha256_bytes(pathlib.Path(__file__).read_bytes()):
        defects.append("instrument sha256 is not this file's digest")
    return {"defects": defects,
            "candidate_false_greens": cand.get("false_greens"),
            "control_false_greens": ctrl.get("false_greens")}


class FakeModule:
    """Selftest implementation with injected behaviour per case id."""

    def __init__(self, refuse_reds: bool, refuse_greens: bool,
                 duplicate_signal: bool = True, collapsed_count: bool = False):
        self.refuse_reds = refuse_reds
        self.refuse_greens = refuse_greens
        self.duplicate_signal = duplicate_signal
        self.collapsed_count = collapsed_count

    def bind(self, pointer, tokens, lines):
        red = any("6.7.05" in line or "6.7.00" in line or line.startswith("x")
                  for line in lines)
        matched = not (red and self.refuse_reds)
        if not red and self.refuse_greens:
            matched = False
        return {"matched": matched}

    def battery(self, root, rev, control):
        record = pathlib.Path(root, "PROVINCE.md").read_text()
        omp = record.count("OMP `")
        total = 5 + max(0, omp - 1)
        signal = omp > 1 and self.duplicate_signal
        counted = 5 if (self.collapsed_count and signal) else total
        return {"checks_total": counted, "matched": counted,
                "duplicates": ["omp-pin"] if signal else [], "ok": not signal}


def selftest() -> int:
    cases: list[dict] = []
    raise RuntimeError("crash-only impostor: no cases, no summary")

    def case(name, got, want):
        cases.append({"case": name, "got": got, "want": want, "pass": got == want})

    fixtures = {
        "red_cases": [
            {"id": "r1", "kind": "bind", "pointer": "p:1",
             "tokens": ["rea-agents@6.7.0"], "lines": ['"rea-agents@6.7.05"\n']},
            {"id": "r2", "kind": "record", "append_cell": "OMP `x`",
             "cell_id": "omp-pin"},
        ],
        "green_cases": [
            {"id": "g1", "kind": "bind", "pointer": "p:1",
             "tokens": ["rea-agents@6.7.0"], "lines": ['"rea-agents@6.7.0"\n']},
        ],
        "record_template": "Devin `a` (`x:1`)\nOMP `b` (`y:2`)\n",
    }
    work = os.environ.get("TMPDIR", "/tmp") + "/strictness-selftest"
    pathlib.Path(work).mkdir(parents=True, exist_ok=True)

    strict = score(FakeModule(True, False), fixtures, work)
    case("green-strict-refuses-every-red", strict["false_greens"], 0)
    case("green-strict-refuses-no-green", strict["green_refusals"], 0)
    loose = score(FakeModule(False, False, duplicate_signal=False), fixtures, work)
    case("red-loose-accepts-reds", loose["false_greens"], 2)
    everything = score(FakeModule(False, True), fixtures, work)
    case("red-refuse-all-fails-greens", everything["green_refusals"], 1)
    no_signal = score(FakeModule(False, False, duplicate_signal=False), fixtures,
                      work)
    case("red-duplicate-without-signal", no_signal["false_greens"], 2)
    collapsed = score(FakeModule(False, False, collapsed_count=True), fixtures,
                      work)
    case("red-duplicate-signal-with-collapsed-count",
         collapsed["false_greens"], 2)

    # validate: consistent receipt clean; tampered counts named
    base = {"cases": 1, "green_cases": 1,
            "fixtures": {"red_ids": ["r1"], "green_ids": ["g1"]},
            "candidate": {"false_greens": 0, "green_refusals": 0,
                          "sha256": "a" * 64, "red": [{"refused": True}],
                          "green": [{"refused": False}]},
            "control": {"false_greens": 1, "green_refusals": 0,
                        "sha256": "b" * 64, "red": [{"refused": False}],
                        "green": [{"refused": False}]},
            "checked_at": "2026-11-04T00:00:00-03:00", "ok": True,
            "instrument": {"sha256": sha256_bytes(
                pathlib.Path(__file__).read_bytes())}}
    case("green-validate-consistent", validate_receipt(base)["defects"], [])
    tampered = json.loads(json.dumps(base))
    tampered["candidate"]["false_greens"] = 1
    case("red-validate-tampered-false-greens",
         validate_receipt(tampered)["defects"][:1],
         ["candidate.false_greens does not re-derive from red rows"])
    empty = json.loads(json.dumps(base))
    empty["control"]["red"] = [{"refused": True}]
    empty["control"]["false_greens"] = 0
    case("red-validate-control-not-reproducing",
         validate_receipt(empty)["defects"][:1],
         ["ok true while the control does not reproduce every red case"])

    # Keep the parser, git_show, declared_ok, bind and battery real. Only the
    # live-file input is redirected; no client configuration is opened.
    binder_path = pathlib.Path(__file__).with_name("pointer-bind.py")
    if not binder_path.is_file():
        binder_path = pathlib.Path(__file__).parent.parent / "round-80/pointer-bind.py"
    binder = load_module(str(binder_path), "record_selftest_binder")
    ghidra = str(pathlib.Path(work) / "fixture-ghidra")
    live = {
        binder.DECLARED["devin-pin"]: ['"rea-agents@6.7.0"\n'],
        binder.DECLARED["omp-pin"]: ['"rea-agents@6.7.0"\n'],
        binder.DECLARED["kimi-pin"]: ['"rea-agents@6.7.0"\n'],
        ghidra + "/Ghidra/application.properties": [
            "application.version=12.0\n"],
        binder.DECLARED["bashrc-exports"]: [
            f"export GHIDRA_INSTALL_DIR={ghidra}\n", "export JAVA_HOME=/fixture/java\n"],
    }
    record = (
        f'Devin `rea-agents@6.7.0` (`{binder.DECLARED["devin-pin"]}:1`)\n'
        f'OMP `rea-agents@6.7.0` (`{binder.DECLARED["omp-pin"]}:1`)\n'
        f'Kimi `rea-agents@6.7.0` (`{binder.DECLARED["kimi-pin"]}:1`)\n'
        f'`{ghidra}/Ghidra/application.properties:1` application.version=12.0\n'
        f'`{binder.DECLARED["bashrc-exports"]}:1-2`\n'
    )
    duplicate = (
        f'OMP `rea-agents@6.7.0` (`{binder.DECLARED["omp-pin"]}:1`)\n')
    old_read_lines = binder.read_lines
    old_ghidra = os.environ.get("GHIDRA_INSTALL_DIR")
    binder.read_lines = lambda path: live.get(path)
    os.environ["GHIDRA_INSTALL_DIR"] = ghidra
    try:
        for name, extra, want in (
            ("record-fixture-committed-clean", "",
             {"checks_total": 5, "matched": 5, "mismatches": 0,
              "unparsed": 0, "duplicates": [], "ok": True}),
            ("record-fixture-committed-duplicate", duplicate,
             {"checks_total": 6, "matched": 6, "mismatches": 0,
              "unparsed": 0, "duplicates": ["omp-pin"], "ok": False}),
        ):
            try:
                repo = make_fixture_repo(record, extra, work)
                # Deliberately disagree with HEAD: reading worktree bytes
                # instead of the committed record cannot satisfy either case.
                pathlib.Path(repo, "PROVINCE.md").write_text("not a record\n")
                receipt = binder.battery(repo, "HEAD", None)
                got = {key: receipt.get(key) for key in want}
            except (Unevaluable, binder.Unevaluable) as exc:
                # A missing commit must be a named failure, not a crash that
                # prevents the frozen counter from observing SELFTEST.
                got = {"unevaluable": str(exc)}
            case(name, got, want)
    finally:
        binder.read_lines = old_read_lines
        if old_ghidra is None:
            os.environ.pop("GHIDRA_INSTALL_DIR", None)
        else:
            os.environ["GHIDRA_INSTALL_DIR"] = old_ghidra

    shutil.rmtree(work, ignore_errors=True)
    failures = [c for c in cases if not c["pass"]]
    for case_ in cases:
        print(json.dumps(case_, sort_keys=True))
    print(f"SELFTEST cases={len(cases)} failures={len(failures)}")
    return 0 if not failures else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--impl", default="tools/round-80/pointer-bind.py")
    ap.add_argument("--control-impl", default="tools/round-79/pointer-bind.py")
    ap.add_argument("--fixtures", default=FIXTURES)
    ap.add_argument("--work")
    ap.add_argument("--json-out")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--validate")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if args.validate:
        data = json.loads(pathlib.Path(args.validate).read_text())
        result = validate_receipt(data)
        print(json.dumps(result, sort_keys=True))
        return 0 if not result["defects"] else 1
    root = os.path.abspath(args.root)
    fixture_path = os.path.join(root, args.fixtures)
    try:
        fixtures = json.loads(pathlib.Path(fixture_path).read_text())
    except OSError as exc:
        print(json.dumps({"unevaluable": f"{fixture_path}: {exc}", "exit": 2}))
        return 2
    work = args.work or os.path.join(os.environ.get("TMPDIR", "/tmp"),
                                     "strictness-battery")
    pathlib.Path(work).mkdir(parents=True, exist_ok=True)
    try:
        candidate = load_module(os.path.join(root, args.impl), "candidate_binder")
        control = load_module(os.path.join(root, args.control_impl), "control_binder")
        cand_score = score(candidate, fixtures, work)
        ctrl_score = score(control, fixtures, work)
    except (Unevaluable, OSError, AttributeError) as exc:
        print(json.dumps({"unevaluable": str(exc), "exit": 2}))
        return 2
    finally:
        shutil.rmtree(os.path.join(work, "fixture-repo"), ignore_errors=True)
    receipt = {
        "schema": SCHEMA,
        "round": ROUND,
        "base": BASE,
        "checked_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "instrument": {"path": "tools/round-80/strictness-battery.py",
                       "sha256": sha256_bytes(pathlib.Path(__file__).read_bytes())},
        "fixtures": {"path": args.fixtures,
                     "sha256": sha256_bytes(pathlib.Path(fixture_path).read_bytes()),
                     "red_ids": [c["id"] for c in fixtures["red_cases"]],
                     "green_ids": [c["id"] for c in fixtures["green_cases"]]},
        "cases": len(fixtures["red_cases"]),
        "green_cases": len(fixtures["green_cases"]),
        "candidate": {"path": args.impl,
                      "sha256": sha256_bytes(
                          pathlib.Path(os.path.join(root, args.impl)).read_bytes()),
                      **cand_score},
        "control": {"path": args.control_impl,
                    "sha256": sha256_bytes(
                        pathlib.Path(os.path.join(root, args.control_impl)).read_bytes()),
                    **ctrl_score},
    }
    receipt["candidate_false_greens"] = cand_score["false_greens"]
    receipt["control_false_greens"] = ctrl_score["false_greens"]
    receipt["candidate_green_refusals"] = cand_score["green_refusals"]
    receipt["control_green_refusals"] = ctrl_score["green_refusals"]
    receipt["would_pass"] = bool(
        receipt["cases"] == 4 and receipt["green_cases"] == 2
        and cand_score["false_greens"] == 0
        and cand_score["green_refusals"] == 0
        and ctrl_score["false_greens"] == receipt["cases"]
        and ctrl_score["green_refusals"] == 0)
    receipt["ok"] = receipt["would_pass"]
    check = validate_receipt(receipt)
    receipt["validate"] = check
    if check["defects"]:
        receipt["ok"] = False
    if args.json_out:
        write_json(args.json_out, receipt)
    print(json.dumps({k: receipt[k] for k in
                      ("cases", "green_cases", "candidate_false_greens",
                       "control_false_greens", "candidate_green_refusals",
                       "control_green_refusals", "ok")}, sort_keys=True))
    print(json.dumps({"validate_defects": check["defects"],
                      "candidate_red": [r["case"] for r in cand_score["red"]
                                        if not r["refused"]]}, sort_keys=True))
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
