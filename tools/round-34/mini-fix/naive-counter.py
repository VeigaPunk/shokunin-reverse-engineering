#!/usr/bin/env python3
"""Naive counter for the replay gate's red case.

Scores a reader on the mini fixture set with NO transformation: the fixture keeps
its own name and its own bytes, so any answer memorized by label, size or digest
is reachable. This is the shape-only counter the gate must refuse; it is never
domain evidence.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

TARGET = 8


def canonical(value):
    if not isinstance(value, dict) or set(value) != {"schema", "records"} or value["schema"] != 1:
        return None
    if not isinstance(value["records"], list):
        return None
    rows = []
    for record in value["records"]:
        if not isinstance(record, dict) or set(record) != {"name", "flags", "value"}:
            return None
        if not isinstance(record["name"], str) or not isinstance(record["flags"], int) or not isinstance(record["value"], int):
            return None
        rows.append({"name": record["name"], "flags": record["flags"], "value": record["value"]})
    return sorted(rows, key=lambda row: (row["name"], row["flags"], row["value"]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--control-reader", required=True)
    args = parser.parse_args()
    base = Path(args.root)
    reader = Path(args.control_reader)
    if not reader.is_file():
        print(json.dumps({"predicate": "naive-control-fixture", "met_target": False,
                          "finding": "reader_absent"}, sort_keys=True))
        return 3
    expected = json.loads((base / "tools/round-34/mini-fix/expected.json").read_text())["fixtures"]
    rows = []
    for name in sorted(expected):
        path = base / "tools/round-34/mini-fix/fixtures" / name
        run = subprocess.run([sys.executable, "-I", "-B", str(reader), str(path)],
                             capture_output=True, text=True, timeout=60,
                             env={"PATH": "/usr/bin:/bin", "HOME": "/tmp", "LANG": "C"})
        observed = None
        if run.returncode == 0:
            try:
                observed = canonical(json.loads(run.stdout))
            except (ValueError, TypeError):
                observed = None
        rows.append({"fixture": name, "ok": observed == expected[name], "exit": run.returncode})
    matched = sum(1 for row in rows if row["ok"])
    print(json.dumps({"predicate": "naive-control-fixture; shape-only, never domain evidence",
                      "target": TARGET, "matched": matched, "met_target": matched == TARGET,
                      "rows": rows, "finding": "records_match" if matched == TARGET else "records_mismatch"},
                     sort_keys=True))
    return 0 if matched == TARGET else 1


if __name__ == "__main__":
    sys.exit(main())
