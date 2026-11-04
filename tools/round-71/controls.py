#!/usr/bin/env python3
"""controls.py - round-71 instrument (the round's do-nothing and shortcut controls).

Six controls, each scored with the same frozen counters the claims use:

  c1-base-world            the round-71 seam probe at the round-70 landing
                           (7c155617) against the round-70 route: 7 of 10 arms,
                           A8/A9/A10 false (the world a do-nothing control holds)
  c1-constant-probe        a probe receipt asserting ten true arms with no
                           observations is rejected by the probe's --validate
  c2-do-nothing            the round-70 battery's committed landing receipt
                           carries 10 base-world + 2 landing-world rows and no
                           lying-field row (12 forged rows, target 18)
  c2-constant-battery      a battery receipt with six lying rows whose rc pairs
                           are (0, 0) is rejected by the battery's --validate
  c3-base-nonconformant    the registry census at the base revision reports six
                           nonconformant round-70 rows, exit 1
  c3-junk-row              a scratch registry with a five-cell junk row is
                           rejected as nonconformant, exit 1

Exit 0 every control shows what it must; 1 a control misses (named); 2 bad argv
or an unreadable base artifact.  `--validate <receipt>` checks the control
receipt's structural honesty.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

TOOL = "tools/round-71/controls.py"
BASE_REV = "82c8e620c9222fb218aa0260570a3765da2afb44"
R70_REV = "7c155617bb42dadf1725b88a06fe3f235c364f0a"
R70_RECEIPT = ".ufo/waves/round-70/l1/scores/c1-at-landing.json"
R70_LANDING = ".ufo/waves/round-70/l1/scores/c3-at-landing.json"
REA_PKG = "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents"


class Unevaluable(Exception):
    """Exit-2 class: a control cannot be scored, so it claims nothing."""


def run(argv: list[str], timeout: int = 2400, env: dict | None = None) -> dict:
    try:
        proc = subprocess.run(argv, capture_output=True, text=True,
                              timeout=timeout, env=env)
    except OSError as exc:
        raise Unevaluable(f"control child unexecutable: {argv[0]} "
                          f"({exc.__class__.__name__}: {exc})")
    return {"argv": argv, "rc": proc.returncode, "stdout": proc.stdout,
            "stderr_tail": proc.stderr[-3000:]}


def json_out(text: str) -> dict | None:
    for chunk in [text.strip()] + [line.strip() for line in text.splitlines()[::-1]]:
        if not chunk:
            continue
        try:
            payload = json.loads(chunk)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            return payload
    return None


def arm(aid: str, ok: bool, observed: dict) -> dict:
    return {"id": aid, "ok": bool(ok), "observed": observed}


def check(root: str, work: str, probe: str, battery: str, census: str) -> dict:
    if not os.path.isdir(work):
        raise Unevaluable(f"--work is not a directory: {work}")
    scratch = tempfile.mkdtemp(prefix="controls-", dir=work)
    arms = []
    try:
        # c1-base-world: the round-70 route at its own landing, 7 of 10 arms.
        try:
            with open(os.path.join(root, R70_LANDING), encoding="utf-8") as fh:
                r70_landing = json.load(fh)
            expect_upx = r70_landing["carriers"][0]["runs"]["pack"]["argv"][0]
        except (OSError, json.JSONDecodeError, KeyError, IndexError) as exc:
            raise Unevaluable(f"round-70 landing receipt unusable: {exc}")
        os.makedirs(os.path.dirname(expect_upx), exist_ok=True)
        shutil.copy2("/usr/bin/upx", expect_upx)
        os.chmod(expect_upx, 0o755)
        base = run([sys.executable, "-I", "-B", probe, "--root", root,
                    "--rev", R70_REV, "--tool", "tools/round-70/packed-elf.py",
                    "--battery", "tools/round-70/mutation-check.py",
                    "--pkg", REA_PKG, "--work", scratch,
                    "--receipt", R70_LANDING,
                    "--expect-upx", expect_upx])
        bjson = json_out(base["stdout"]) or {}
        passed = bjson.get("arms_passed")
        failed = bjson.get("failed") or []
        arms.append(arm("c1-base-world",
                        base["rc"] == 1 and passed == 7
                        and set(failed) == {"A8_child_env_observed",
                                            "A9_concurrent_collision",
                                            "A10_run_binding"},
                        {"rc": base["rc"], "arms_passed": passed,
                         "failed": failed}))

        # c1-constant-probe: a ten-arm receipt with no observations is rejected.
        const = {"instrument": "tools/round-71/packed-elf.py",
                 "rev": "a" * 40, "arms": [
                     {"id": "A%d" % i, "ok": True, "observed": {}}
                     for i in range(1, 11)],
                 "arms_passed": 10, "target": 10, "failed": [], "ok": True}
        const_path = os.path.join(scratch, "constant-probe.json")
        with open(const_path, "w", encoding="utf-8") as fh:
            json.dump(const, fh)
        val = run([sys.executable, "-I", "-B", probe, "--validate", const_path])
        arms.append(arm("c1-constant-probe", val["rc"] == 1,
                        {"validate_rc": val["rc"],
                         "defects": (json_out(val["stdout"]) or {}).get("defects")}))

        # c2-do-nothing: the round-70 battery receipt carries 12 forged rows, 0
        # lying-field rows (target 18).
        try:
            with open(os.path.join(root, R70_RECEIPT), encoding="utf-8") as fh:
                base_receipt = json.load(fh)
        except (OSError, json.JSONDecodeError) as exc:
            raise Unevaluable(f"round-70 battery receipt unreadable: {exc}")
        shapes = len(base_receipt.get("shapes") or [])
        landing = len(base_receipt.get("landing_probe_shapes") or [])
        lying = len(base_receipt.get("lying_shapes") or [])
        arms.append(arm("c2-do-nothing",
                        shapes == 10 and landing == 2 and lying == 0,
                        {"base_world_shapes": shapes,
                         "landing_world_shapes": landing,
                         "lying_shapes": lying, "forged_total": shapes + lying,
                         "target": 16}))

        # c2-constant-battery: six lying rows whose rc pair is (0, 0).
        const_bat = {"schema": "kaidoku-r71-forged-receipts-v1",
                     "shapes": [{"shape": "F1", "declared_clause": "rev",
                                 "base_rc": 0, "landing_rc": 1}],
                     "lying_shapes": [{"shape": "L%d" % i, "declared_clause": "x",
                                      "first_cut_rc": 0, "superseded_rc": 0,
                                      "clause_found": True} for i in range(6)],
                     "genuine": {"checker_rc": 0}}
        const_bat_path = os.path.join(scratch, "constant-battery.json")
        with open(const_bat_path, "w", encoding="utf-8") as fh:
            json.dump(const_bat, fh)
        valb = run([sys.executable, "-I", "-B", battery, "--validate",
                    const_bat_path])
        arms.append(arm("c2-constant-battery", valb["rc"] == 1,
                        {"validate_rc": valb["rc"],
                         "defects": (json_out(valb["stdout"]) or {}).get("defects")}))

        # c3-base-nonconformant: the base registry has six nonconformant rows.
        cb = run([sys.executable, "-I", "-B", census, "--root", root,
                  "--rev", BASE_REV, "--generate",
                  "--out", os.path.join(scratch, "census-base.json")])
        cbjson = json_out(cb["stdout"]) or {}
        defects = [r.get("defects") for r in cbjson.get("nonconformant") or []]
        arms.append(arm("c3-base-nonconformant",
                        cb["rc"] == 1 and len(defects) == 6
                        and all(d == ["pinned-empty"] for d in defects),
                        {"rc": cb["rc"], "rows": cbjson.get("rows"),
                         "nonconformant": len(defects),
                         "defects": defects[:2]}))

        # c3-junk-row: a scratch registry with a five-cell junk row fails.
        fixture = os.path.join(scratch, "fixture-root")
        os.makedirs(os.path.join(fixture, "tools"))
        with open(os.path.join(fixture, "tools", "junk.py"), "w") as fh:
            fh.write("# fixture\n")
        table = ("<!-- instrument-registry v2 -->\n"
                 "| tool | gate or probe - purpose | verdict map (exit codes) | "
                 "self-test command | pinned-value path | write scope | owner |\n"
                 "|---|---|---|---|---|---|---|\n"
                 "| `tools/junk.py` | gate - junk | 0/1 | --selftest | pin | "
                 "none | kaidoku |\n"
                 "| `tools/junk2.py` | gate - junk | 0/1 | --selftest |\n"
                 "<!-- /instrument-registry -->\n")
        with open(os.path.join(fixture, "SKILL.md"), "w") as fh:
            fh.write(table)
        cj = run([sys.executable, "-I", "-B", census, "--root", fixture,
                  "--rev", "WORKTREE"])
        cjjson = json_out(cj["stdout"]) or {}
        arms.append(arm("c3-junk-row", cj["rc"] == 1
                        and [r.get("defects") for r in
                             cjjson.get("nonconformant") or []]
                        == [["cells<6", "pinned-empty", "path-absent"]],
                        {"rc": cj["rc"],
                         "nonconformant": cjjson.get("nonconformant")}))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    failed = [a["id"] for a in arms if not a["ok"]]
    return {"tool": TOOL, "base_rev": BASE_REV, "r70_rev": R70_REV,
            "arms": arms, "arms_passed": len(arms) - len(failed),
            "target": len(arms), "failed": failed, "ok": not failed,
            "scratch": scratch}


def validate(path: str) -> int:
    try:
        with open(path, encoding="utf-8") as fh:
            receipt = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"validate": "controls-receipt", "unevaluable": str(exc)}))
        return 2
    defects = []
    arms = receipt.get("arms")
    if not isinstance(arms, list) or not arms:
        defects.append("arms absent or empty")
        arms = []
    for a in arms:
        if not isinstance(a.get("id"), str):
            defects.append("an arm has no id")
        if not isinstance(a.get("ok"), bool):
            defects.append(f"{a.get('id')}: ok not a bool")
        if not isinstance(a.get("observed"), dict) or not a.get("observed"):
            defects.append(f"{a.get('id')}: no observation")
    derived = [a.get("id") for a in arms if a.get("ok") is True]
    if receipt.get("arms_passed") != len(derived):
        defects.append("arms_passed disagrees with the arm rows")
    if receipt.get("target") != len(arms):
        defects.append("target != arm rows")
    if sorted(receipt.get("failed") or []) != sorted(
            a.get("id") for a in arms if a.get("ok") is not True):
        defects.append("failed disagrees with the arm rows")
    out = {"validate": "controls-receipt", "path": path, "ok": not defects,
           "defects": defects, "arms": len(arms)}
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0 if not defects else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root")
    ap.add_argument("--work")
    ap.add_argument("--probe")
    ap.add_argument("--battery")
    ap.add_argument("--census")
    ap.add_argument("--json-out")
    ap.add_argument("--validate")
    args = ap.parse_args(argv)
    if args.validate:
        return validate(args.validate)
    if not (args.root and args.work and args.probe and args.battery and args.census):
        print("controls: --root, --work, --probe, --battery and --census are "
              "required", file=sys.stderr)
        return 2
    try:
        receipt = check(args.root, args.work, args.probe, args.battery,
                        args.census)
    except Unevaluable as exc:
        print(json.dumps({"schema": "kaidoku-r71-controls-v1",
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
