#!/usr/bin/env python3
"""Add the third frozen check-receipt fixture (r68 landing receipt) to every row."""
from __future__ import annotations

import json
import os
import subprocess
import sys

SCRATCH = "/fast/scratch/hyaku/kaidoku-r69/MutBattery"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
R68 = os.path.join(LANE, ".ufo/waves/round-68/l1/scores/c2-at-landing.json")
PY = sys.executable


def probe(path):
    p = subprocess.run([PY, "-I", "-B", path, "--check-receipt", R68],
                       capture_output=True, text=True, timeout=120)
    payload = None
    for text in (p.stdout, p.stderr):
        try:
            cand = json.loads(text)
        except json.JSONDecodeError:
            continue
        if isinstance(cand, dict) and "check" in cand:
            payload = cand
            break
    return {"rc": p.returncode, "failing": (payload or {}).get("failing"),
            "met": (payload or {}).get("met")}


def main():
    results = json.load(open(os.path.join(SCRATCH, "results.json"), encoding="utf-8"))
    base = probe(os.path.join(SCRATCH, "pristine-packed-elf.py"))
    results["baseline"]["receipts"]["r68"] = {
        "rc": base["rc"], "failing": base["failing"], "met": base["met"]}
    for m in results["mutants"]:
        path = os.path.join(SCRATCH, m["id"] + "-packed-elf.py")
        rec = probe(path)
        m["check_receipt"]["r68"] = rec
        dev = {n: {"pristine_rc": results["baseline"]["receipts"][n]["rc"],
                   "mutant_rc": m["check_receipt"][n]["rc"]}
               for n in m["check_receipt"]
               if m["check_receipt"][n]["rc"] != results["baseline"]["receipts"][n]["rc"]}
        m["receipt_rc_deviations"] = dev
    with open(os.path.join(SCRATCH, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps({"r68_pristine": base}, indent=1))


if __name__ == "__main__":
    main()
