#!/usr/bin/env python3
"""R34-C2 counter: the pre-freeze shortcut-replay capability, one command.

Runs, at one revision, in this order:
 1. the gate's isolated self-test (outer CLI, exit and stable findings; mutants
    of its refusal, positive-control and shortcut-floor branches must die);
 2. the red case: a shape-only counter whose label-keyed memorization meets the
    target must be REFUSED;
 3. the green case: the identity-defeating counter on the same eight fixtures
    must be CLEAN, with the structural positive control meeting the target.

Emits one JSON receipt and a stable verdict line. Exit 0 only when all three
hold; 1 on a claim miss with the failing clause named; 2 when a pinned
instrument is absent or unreadable.
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

PREDICATE = ("P34-shortcut-replay: the committed replay gate refuses the shape-only counter whose "
             "label-keyed memorization meets its target, clears the identity-defeating counter on the "
             "same eight fixtures where every registered shortcut class stays below target, and its "
             "selftest kills every mutant of its own refusal, positive-control and shortcut-floor "
             "branches.")
TARGET = {"selftest_failures": 0, "mutants_killed": 3, "red_verdict": "REPLAY_GATE_REFUSED",
          "green_verdict": "REPLAY_GATE_CLEAN"}
GATE = "tools/round-34/replay-gate.py"
CONFIGS = {"red": "tools/round-34/gate-config-naive.json",
           "green": "tools/round-34/gate-config-mini.json"}


def run(argv, cwd):
    run_result = subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True, timeout=900,
                                env={"PATH": "/usr/bin:/bin", "HOME": "/tmp", "LANG": "C"})
    return run_result


def gate(root, args):
    with tempfile.NamedTemporaryFile("r", suffix=".json", delete=False) as handle:
        out = handle.name
    try:
        run_result = run([sys.executable, "-I", "-B", str(root / GATE), "--root", str(root),
                          "--json-out", out] + args, root)
        line = run_result.stdout.strip().splitlines()[-1] if run_result.stdout.strip() else ""
        try:
            payload = json.loads(Path(out).read_text())
        except (OSError, ValueError):
            payload = None
        if payload is None:
            try:
                payload = json.loads(line)
            except ValueError:
                payload = None
    finally:
        Path(out).unlink(missing_ok=True)
    return {"exit": run_result.returncode, "line": line, "payload": payload,
            "stderr": run_result.stderr[-2000:]}


def main():
    global GATE
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--rev", required=True)
    parser.add_argument("--json-out")
    parser.add_argument("--gate", default=GATE,
                        help="Control only: score an alternative gate. Production runs use the pinned default.")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    receipt = {"predicate": PREDICATE, "target": TARGET, "measured_revision": args.rev,
               "gate_path": args.gate, "gate_present": (root / args.gate).is_file()}
    GATE = args.gate
    if not receipt["gate_present"]:
        receipt.update({"finding": "gate_absent", "met_target": False, "exit": 2})
        if args.json_out:
            Path(args.json_out).write_text(json.dumps(receipt, indent=1, sort_keys=True) + "\n")
        print(f"GATE_COUNTER_UNEVALUABLE finding=gate_absent measured_revision={args.rev} "
              f"gate_path={args.gate}")
        return 2
    missing = [path for path in CONFIGS.values() if not (root / path).is_file()]
    if missing:
        receipt.update({"finding": "pinned_input_absent", "missing": missing, "met_target": False, "exit": 2})
        if args.json_out:
            Path(args.json_out).write_text(json.dumps(receipt, indent=1, sort_keys=True) + "\n")
        print(f"GATE_COUNTER_UNEVALUABLE finding=pinned_input_absent paths={','.join(missing)}")
        return 2

    selftest = gate(root, ["--selftest"])
    summary = selftest["payload"] or {}
    red = gate(root, ["--config", CONFIGS["red"]])
    green = gate(root, ["--config", CONFIGS["green"]])

    red_classes = (red["payload"] or {}).get("classes_over_target") or []
    green_rows = (green["payload"] or {}).get("rows") or []
    positive = next((row for row in green_rows if row.get("class") == "structural"), {})
    receipt.update({
        "selftest_exit": selftest["exit"],
        "selftest_line": selftest["line"],
        "selftest_failures": int(summary.get("failures", -1)) if summary else None,
        "mutants_killed": int(summary.get("mutants_killed", -1)) if summary else None,
        "red": {"exit": red["exit"], "line": red["line"], "verdict": (red["payload"] or {}).get("verdict"),
                "classes_over_target": red_classes},
        "green": {"exit": green["exit"], "line": green["line"],
                  "verdict": (green["payload"] or {}).get("verdict"),
                  "positive_matched": positive.get("matched"),
                  "shortcuts_below_target": sum(1 for row in green_rows
                                                if row.get("class") != "structural" and not row.get("met_target"))},
    })
    clauses = {
        "selftest_clean": receipt["selftest_exit"] == 0 and receipt["selftest_failures"] == TARGET["selftest_failures"],
        "mutants_killed": receipt["mutants_killed"] == TARGET["mutants_killed"],
        "red_refused": receipt["red"]["exit"] == 2 and receipt["red"]["verdict"] == TARGET["red_verdict"]
                       and "label-memorization" in red_classes,
        "green_clean": receipt["green"]["exit"] == 0 and receipt["green"]["verdict"] == TARGET["green_verdict"],
        "green_positive_meets_target": receipt["green"]["positive_matched"] == 8,
        "gate_present": True,
    }
    receipt["clauses"] = clauses
    receipt["met_target"] = all(clauses.values())
    receipt["finding"] = "shortcut_gate_discriminates" if receipt["met_target"] else "shortcut_gate_miss"
    receipt["exit"] = 0 if receipt["met_target"] else 1
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(receipt, indent=1, sort_keys=True) + "\n")
    print(f"{'GATE_COUNTER_OK' if receipt['met_target'] else 'GATE_COUNTER_MISS'} "
          f"finding={receipt['finding']} selftest_failures={receipt['selftest_failures']} "
          f"mutants_killed={receipt['mutants_killed']} red={receipt['red']['verdict']} "
          f"green={receipt['green']['verdict']} "
          f"green_positive_matched={receipt['green']['positive_matched']} "
          f"clauses_failed={','.join(sorted(k for k, v in clauses.items() if not v)) or '-'}")
    return receipt["exit"]


if __name__ == "__main__":
    sys.exit(main())
