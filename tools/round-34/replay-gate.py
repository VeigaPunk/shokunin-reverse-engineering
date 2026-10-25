#!/usr/bin/env python3
"""P34-shortcut-replay: pre-freeze structure-blind replay gate.

Obligation (QUALITY 67): before a finite ELF structural-decoding counter is
frozen, exercise readers that memorize the fixture set by an invariant key --
input size, input label, whole-file digest, fixed byte slices, the record order
itself -- under the counter's own predicate. If any shortcut meets the frozen
target, the counter measures shape, not structure, and the freeze is refused.

The gate is generic: it runs whatever counter argv the config names, with the
counter's own reader flag, and reads the counter's own receipt fields.

Verdicts (stable, greppable):
  REPLAY_GATE_CLEAN        exit 0  finding=no_shortcut_meets_target
  REPLAY_GATE_REFUSED      exit 2  finding=shortcut_meets_target
  REPLAY_GATE_UNEVALUABLE  exit 3  finding=<reason>

A clean verdict also requires the registered positive control (a real
structural reader) to meet the target, so a gate that cannot run anything --
or a counter no reader can satisfy -- can never report CLEAN.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SCHEMA = 1
MIN_SHORTCUTS = 3
TIMEOUT = 300


class Unevaluable(Exception):
    pass


def load_config(path):
    value = json.loads(Path(path).read_text())
    if not isinstance(value, dict) or value.get("schema") != SCHEMA:
        raise Unevaluable("config_schema")
    for key in ("predicate", "counter", "positive_control", "shortcuts"):
        if key not in value:
            raise Unevaluable("config_missing:" + key)
    counter = value["counter"]
    if not isinstance(counter, dict) or not isinstance(counter.get("argv"), list) or not counter["argv"]:
        raise Unevaluable("config_counter_argv")
    if sum(1 for part in counter["argv"] if isinstance(part, str) and "{reader}" in part) != 1:
        raise Unevaluable("config_counter_reader_placeholder")
    target = value.get("target")
    if type(target) is not int or target < 1:
        raise Unevaluable("config_target")
    positive = value["positive_control"]
    if not isinstance(positive, dict) or not positive.get("path") or not positive.get("class"):
        raise Unevaluable("config_positive_control")
    shortcuts = value["shortcuts"]
    if not isinstance(shortcuts, list) or len(shortcuts) < MIN_SHORTCUTS:  # MUT-A
        raise Unevaluable("config_shortcut_count")
    classes = []
    for item in shortcuts:
        if not isinstance(item, dict) or not item.get("path") or not item.get("class"):
            raise Unevaluable("config_shortcut_entry")
        classes.append(item["class"])
    if len(set(classes)) != len(classes):
        raise Unevaluable("config_shortcut_duplicate_class")
    # MUT-B
    return value


def resolve(root, path):
    candidate = Path(path)
    return candidate if candidate.is_absolute() else Path(root) / candidate


def run_counter(config, root, reader_path):
    argv = [part.replace("{reader}", str(reader_path)) for part in config["counter"]["argv"]]
    try:
        run = subprocess.run(argv, capture_output=True, text=True, timeout=TIMEOUT,
                             cwd=str(root), env={"PATH": "/usr/bin:/bin", "HOME": "/tmp",
                                                 "LANG": "C"})
    except (OSError, subprocess.TimeoutExpired) as error:
        raise Unevaluable("counter_spawn:" + type(error).__name__)
    payload = None
    for line in reversed([text for text in run.stdout.splitlines() if text.strip()]):
        try:
            payload = json.loads(line)
            break
        except ValueError:
            continue
    if not isinstance(payload, dict):
        raise Unevaluable("counter_receipt_unreadable")
    matched = payload.get(config["counter"].get("matched_field", "matched"))
    target = payload.get(config["counter"].get("target_field", "target"))
    met = payload.get(config["counter"].get("met_field", "met_target"))
    if type(matched) is not int or type(target) is not int or type(met) is not bool:
        raise Unevaluable("counter_receipt_fields")
    if target != config["target"]:
        raise Unevaluable("counter_target_mismatch")
    return {"matched": matched, "target": target, "met_target": met,
            "finding": payload.get("finding"), "exit": run.returncode}


def evaluate(config, root):
    positive_spec = config["positive_control"]
    positive_path = resolve(root, positive_spec["path"])
    if not positive_path.is_file():
        raise Unevaluable("positive_control_absent")
    positive = run_counter(config, root, positive_path)
    positive["class"] = positive_spec["class"]
    findings = [positive]
    for item in config["shortcuts"]:
        reader = resolve(root, item["path"])
        if not reader.is_file():
            raise Unevaluable("shortcut_absent:" + item["class"])
        result = run_counter(config, root, reader)
        result["class"] = item["class"]
        findings.append(result)
    if not positive["met_target"]:  # MUT-C
        return {"verdict": "REPLAY_GATE_UNEVALUABLE", "exit": 3,
                "finding": "positive_control_below_target",
                "rows": findings, "classes_over_target": []}
    over = sorted(row["class"] for row in findings if row["met_target"] and row["class"] != positive_spec["class"])
    if over:  # MUT-D
        return {"verdict": "REPLAY_GATE_REFUSED", "exit": 2,
                "finding": "shortcut_meets_target",
                "rows": findings, "classes_over_target": over}
    return {"verdict": "REPLAY_GATE_CLEAN", "exit": 0,
            "finding": "no_shortcut_meets_target",
            "rows": findings, "classes_over_target": []}


def summarise(result):
    over = ",".join(result["classes_over_target"]) or "-"
    below = sum(1 for row in result["rows"]
                if row["class"] != result["rows"][0]["class"] and not row["met_target"])
    return (f"{result['verdict']} finding={result['finding']} "
            f"shortcuts_below_target={below} shortcuts_over_target={over}")


# ---------------------------------------------------------------- self-test
SELFTEST_COUNTER = '''#!/usr/bin/env python3
import json, os, sys
scenario = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenario.json")))
parser_reader = sys.argv[sys.argv.index("--control-reader") + 1]
key = os.path.basename(parser_reader)
if scenario.get("garbage"):
    print("not json")
    sys.exit(0)
print(json.dumps({"predicate": "selftest", "target": scenario["target"],
                  "matched": scenario["matched"].get(key, 0),
                  "met_target": scenario["matched"].get(key, 0) == scenario["target"],
                  "finding": "selftest"}), flush=True)
'''

SELFTEST_CASES = [
    ("clean", {"target": 4, "matched": {"pos.py": 4, "s1.py": 1, "s2.py": 2, "s3.py": 0}}, (0, "REPLAY_GATE_CLEAN", "")),
    ("red-one", {"target": 4, "matched": {"pos.py": 4, "s1.py": 4, "s2.py": 1, "s3.py": 0}}, (2, "REPLAY_GATE_REFUSED", "shortcuts_over_target=s1")),
    ("red-two", {"target": 4, "matched": {"pos.py": 4, "s1.py": 4, "s2.py": 4, "s3.py": 3}}, (2, "REPLAY_GATE_REFUSED", "shortcuts_over_target=s1,s2")),
    ("boundary-below", {"target": 4, "matched": {"pos.py": 4, "s1.py": 3, "s2.py": 3, "s3.py": 3}}, (0, "REPLAY_GATE_CLEAN", "")),
    ("positive-below", {"target": 4, "matched": {"pos.py": 3, "s1.py": 0, "s2.py": 0, "s3.py": 0}}, (3, "REPLAY_GATE_UNEVALUABLE", "positive_control_below_target")),
    ("counter-garbage", {"target": 4, "matched": {}, "garbage": True}, (3, "REPLAY_GATE_UNEVALUABLE", "counter_receipt_unreadable")),
]

MUTANTS = [
    ("always-clean", "if over:", "if False:", "red-mut", 2),
    ("no-positive-check", "if not positive[\"met_target\"]:", "if False:", "positive-below", 3),
    ("vacuous-no-shortcut-floor",
     "if not isinstance(shortcuts, list) or len(shortcuts) < MIN_SHORTCUTS:",
     "if not isinstance(shortcuts, list):", "two-shortcuts-unevaluable", 3),
]


def selftest():
    source = Path(__file__).read_text()
    failures = []
    cases = 0
    with tempfile.TemporaryDirectory(prefix="kaidoku-r34-gate-") as work:
        root = Path(work)
        (root / "counter.py").write_text(SELFTEST_COUNTER)
        for name in ("pos.py", "s1.py", "s2.py", "s3.py"):
            (root / name).write_text("# selftest reader\n")
        (root / "counter.py").chmod(0o755)

        def config_for(case_name, scenario, shortcuts=None, positive="pos.py"):
            spec = {
                "schema": 1,
                "predicate": "selftest",
                "counter": {"argv": [sys.executable, "-I", "-B", str(root / "counter.py"),
                                     "--control-reader", "{reader}"],
                            "matched_field": "matched", "target_field": "target",
                            "met_field": "met_target"},
                "target": scenario["target"],
                "positive_control": {"class": "structural", "path": positive},
                "shortcuts": shortcuts if shortcuts is not None else [
                    {"class": "s1", "path": "s1.py"},
                    {"class": "s2", "path": "s2.py"},
                    {"class": "s3", "path": "s3.py"}],
            }
            path = root / ("config-" + case_name + ".json")
            (root / "scenario.json").write_text(json.dumps(scenario))
            path.write_text(json.dumps(spec))
            return path

        for case_name, scenario, (want_exit, want_verdict, want_token) in SELFTEST_CASES:
            cases += 1
            config = config_for(case_name, scenario)
            try:
                result = evaluate(load_config(config), root)
            except Unevaluable as error:
                result = {"verdict": "REPLAY_GATE_UNEVALUABLE", "exit": 3,
                          "finding": str(error), "rows": [{"class": "structural"}],
                          "classes_over_target": []}
            line = summarise(result)
            ok = result["exit"] == want_exit and want_verdict in line and want_token in line
            print(json.dumps({"case": case_name, "ok": ok, "observed": line,
                              "expected": f"{want_verdict} {want_token}"}, sort_keys=True))
            if not ok:
                failures.append(case_name)

        # schema / vacuous-gate refusals
        for case_name, shortcuts in (
            ("two-shortcuts-unevaluable", [{"class": "s1", "path": "s1.py"},
                                           {"class": "s2", "path": "s2.py"}]),
            ("duplicate-class-unevaluable", [{"class": "s1", "path": "s1.py"},
                                             {"class": "s1", "path": "s2.py"},
                                             {"class": "s3", "path": "s3.py"}]),
        ):
            cases += 1
            config = config_for(case_name, {"target": 4, "matched": {"pos.py": 4}}, shortcuts=shortcuts)
            try:
                result = evaluate(load_config(config), root)
                line = summarise(result)
                ok = False
            except Unevaluable as error:
                line = "REPLAY_GATE_UNEVALUABLE finding=" + str(error)
                ok = str(error) in ("config_shortcut_count", "config_shortcut_duplicate_class")
            print(json.dumps({"case": case_name, "ok": ok, "observed": line}, sort_keys=True))
            if not ok:
                failures.append(case_name)

        cases += 1
        config = config_for("positive-absent", {"target": 4, "matched": {"pos.py": 4}}, positive="missing.py")
        try:
            evaluate(load_config(config), root)
            ok = False
            line = "no refusal"
        except Unevaluable as error:
            ok = str(error) == "positive_control_absent"
            line = "REPLAY_GATE_UNEVALUABLE finding=" + str(error)
        print(json.dumps({"case": "positive-absent", "ok": ok, "observed": line}, sort_keys=True))
        if not ok:
            failures.append("positive-absent")

        # mutants of this file must be killed by the red and vacuous cases
        red = json.loads(config_for("red-mut", {"target": 4, "matched": {"pos.py": 4, "s1.py": 4,
                                                                       "s2.py": 1, "s3.py": 0}}).read_text())
        killed = 0
        for mutant_name, needle, replacement, case_name, expected_exit in MUTANTS:
            cases += 1
            if needle not in source:
                failures.append(mutant_name + "-anchor-missing")
                continue
            mutant_path = root / ("mutant-" + mutant_name + ".py")
            mutant_path.write_text(source.replace(needle, replacement, 1))
            run = subprocess.run([sys.executable, "-I", "-B", str(mutant_path), "--root", str(root),
                                  "--config", str(root / ("config-" + case_name + ".json"))],
                                 capture_output=True, text=True, timeout=TIMEOUT)
            killed_here = run.returncode != expected_exit
            print(json.dumps({"case": "mutant-kill:" + mutant_name, "killed": killed_here,
                              "mutant_exit": run.returncode,
                              "observed": run.stdout.strip().splitlines()[-1:]}, sort_keys=True))
            if killed_here:
                killed += 1
            else:
                failures.append(mutant_name)
    print(json.dumps({"selftest": "replay-gate", "cases": cases, "failures": len(failures),
                      "failed": failures, "mutants_killed": killed, "mutants": len(MUTANTS)},
                     sort_keys=True))
    return 0 if not failures else 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--config")
    parser.add_argument("--json-out")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if not args.config:
        parser.error("--config is required unless --selftest")
    try:
        config = load_config(args.config)
        result = evaluate(config, Path(args.root))
    except Unevaluable as error:
        result = {"verdict": "REPLAY_GATE_UNEVALUABLE", "exit": 3, "finding": str(error),
                  "rows": [], "classes_over_target": []}
    except (OSError, ValueError) as error:
        result = {"verdict": "REPLAY_GATE_UNEVALUABLE", "exit": 3,
                  "finding": type(error).__name__ + ":" + str(error),
                  "rows": [], "classes_over_target": []}
    result["config"] = os.path.abspath(args.config) if args.config else None
    result["root"] = os.path.abspath(args.root)
    print(summarise(result))
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")
    return result["exit"]


if __name__ == "__main__":
    sys.exit(main())
