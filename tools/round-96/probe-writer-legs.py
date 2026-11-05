#!/usr/bin/env python3
"""probe-writer-legs.py - R96-C1 before/after legs for the probe's own receipt write.

Round-95 M95-i / SentinelWrite finding (f): `tools/round-95/symlink-probe.py` writes its
own `--json-out` with `open(..., "w")`, so a symlink planted AT the probe's receipt path
is followed and the victim file is consumed. The v2 probe writes through the hardened
mkstemp + `os.replace` writer, so `os.replace` swaps the link itself and the victim
survives. Both legs run the probe with a writer path that does not exist, so the writer
subprocess fails fast (identity_noop rejects the battery arguments) and the exercised
surface is exactly the probe's own receipt write.

  before leg  `--probe tools/round-95/symlink-probe.py`   victim_intact must be false
  after leg   `--probe tools/round-96/symlink-probe-v2.py` victim_intact must be true

Exit 0 iff both expected behaviours are observed; anything else is exit 1.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import shutil
import subprocess
import sys

TOOL = "tools/round-96/probe-writer-legs.py"


def sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def run_leg(root: str, probe: str, work: str, rev: str, expect: str) -> dict:
    run_dir = os.path.join(work, "run")
    shutil.rmtree(run_dir, ignore_errors=True)
    os.makedirs(run_dir, exist_ok=True)
    victim = os.path.join(run_dir, "victim.txt")
    planted = b"KAIDOKU-R96-PROBE-WRITER-VICTIM " + secrets.token_hex(8).encode() + b"\n"
    with open(victim, "wb") as fh:
        fh.write(planted)
    out = os.path.join(run_dir, "probe-receipt.json")
    os.symlink(victim, out)  # planted AT the probe's own receipt path
    cmd = [sys.executable, "-I", "-B", os.path.join(root, probe), "--root", root,
           "--writer", ".ufo/waves/round-93/controls/identity_noop.py",
           "--repair-cmd", "tools/round-93/controls/identity_noop.py",
           "--work", os.path.join(run_dir, "battery-work"), "--rev", rev,
           "--expect", expect, "--json-out", out]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    with open(victim, "rb") as fh:
        victim_after = fh.read()
    rec = None
    try:
        with open(out, encoding="utf-8") as fh:
            rec = json.load(fh)
    except (OSError, ValueError):
        rec = None
    victim_intact = victim_after == planted
    return {"probe": probe, "probe_rc": p.returncode,
            "victim_intact": victim_intact,
            "receipt readable through the path": rec is not None,
            "receipt_verdict": rec.get("verdict") if isinstance(rec, dict) else None,
            "receipt_victim_intact": rec.get("victim_intact")
            if isinstance(rec, dict) else None,
            "receipt_written_at": out}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--work", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--expect", default=("repaired 12 of 12; wrong 0; unsafe 0; "
                                         "intact 6 of 6; far-refused 12 of 12; "
                                         "fresh-roundtrip 2 of 2"))
    ap.add_argument("--json-out")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    os.makedirs(os.path.abspath(args.work), exist_ok=True)
    before = run_leg(root, "tools/round-95/symlink-probe.py",
                     os.path.join(args.work, "before"), args.rev, args.expect)
    after = run_leg(root, "tools/round-96/symlink-probe-v2.py",
                    os.path.join(args.work, "after"), args.rev, args.expect)
    ok = (before["victim_intact"] is False and after["victim_intact"] is True)
    receipt = {
        "class": "R96-C1 probe receipt write path: planted link at --json-out",
        "counter": TOOL,
        "counter_sha256": sha256_file(os.path.abspath(__file__)),
        "world_revision": args.rev,
        "before": before,
        "after": after,
        "expected": "before victim consumed (open(w) follows), after victim intact "
                    "(mkstemp + os.replace swaps the link)",
        "label": "before victim_intact %s; after victim_intact %s"
                 % (before["victim_intact"], after["victim_intact"]),
        "met_target": ok,
        "exit": 0 if ok else 1,
    }
    rendered = json.dumps(receipt, indent=1, sort_keys=True)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(rendered + "\n")
    print(rendered)
    print(receipt["label"], "met", ok, "exit", 0 if ok else 1)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
