#!/usr/bin/env python3
"""Offline R52-C1 pre-freeze controls driver.

The v2 counter owns rule semantics: each arm invokes its ``controls`` mode over
committed round-50 after.json envelopes, so this driver never imports or runs REA.
"""
import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
RECEIPTS = "corpus/evidence/round-50/c1"
OLD_RULE = "tools/round-50/gap-rule.json"
NEW_RULE = "tools/round-52/gap-rule.json"
PROVENANCE_BASE = "/fast/scratch/hyaku/kaidoku-r50"
RECEIPT_FRESH_BASE = "646d29c9"
CONTROLS = ("CTL-OLD", "CTL-NEW", "CTL-DN", "CTL-JUNK", "M1", "M2", "M3", "M4")


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--counter", default="tools/round-52/c1-counter.py")
    ap.add_argument("--provenance-base", default=PROVENANCE_BASE)
    ap.add_argument("--receipt-fresh-base", default=RECEIPT_FRESH_BASE)
    ap.add_argument("--json-dir", required=True, help="directory for one JSON receipt per control")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    counter = os.path.abspath(os.path.join(root, a.counter))
    os.makedirs(a.json_dir, exist_ok=True)
    failed = False
    for name in CONTROLS:
        command = [sys.executable, "-I", "-B", counter, "controls", "--root", root,
                   "--receipts", os.path.join(root, RECEIPTS), "--provenance-base",
                   a.provenance_base, "--receipt-fresh-base", a.receipt_fresh_base,
                   "--control", name]
        if name == "CTL-OLD":
            command += ["--gap-rule", os.path.join(root, OLD_RULE)]
        elif name == "CTL-NEW":
            command += ["--gap-rule", os.path.join(root, NEW_RULE)]
        elif name == "CTL-DN":
            command += ["--receipts", os.path.join(a.json_dir, "absent-receipts")]
        result = subprocess.run(command, cwd=root, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True, check=False)
        stdout = result.stdout
        try:
            payload = json.loads(stdout)
        except (ValueError, TypeError):
            payload = {"raw_stdout": stdout}
        expected = {"CTL-OLD": (1, 2), "CTL-NEW": (0, 4), "CTL-DN": (1, 2),
                    "CTL-JUNK": (1, 0), "M1": (1, 0), "M2": (0, 1),
                    "M3": (1, 2), "M4": (1, 0)}[name]
        # Exact detail assertions are deliberately evaluated from the counter's
        # machine-readable receipt; absence is a failed control, not a pass.
        count = payload.get("carriers_matched", payload.get("matched"))
        if name == "CTL-DN":
            ok = result.returncode in (1, 2)
        else:
            ok = result.returncode == expected[0] and count == expected[1]
        receipt = {"control": name, "command": command, "exit_code": result.returncode,
                   "stdout_sha256": hashlib.sha256(stdout.encode()).hexdigest(),
                   "utc": utc_now(), "stdout": stdout, "parsed": payload,
                   "expected_exit": expected[0], "expected_count": expected[1],
                   "verdict": "PASS" if ok else "FAIL"}
        path = os.path.join(a.json_dir, name.lower() + ".json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(receipt, f, indent=2, sort_keys=True)
            f.write("\n")
        print(f"{name}: {receipt['verdict']} exit={result.returncode}")
        failed |= not ok
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
