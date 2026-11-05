#!/usr/bin/env python3
"""symlink-probe.py - round-95 public-path write-escape probe (R95-C1, calibration).

Round 94's SentinelWrite finding F1 (recorded, remediation routed): a local attacker
who pre-plants a symlink at `<json-out>.tmp` makes the round-94 writer follow it —
the receipt bytes are written through the link into the victim file, and the victim
is then renamed over the receipt path. The probe freezes that difference on the
public path of whichever writer it is given:

  1. plant a victim file with a nonce content in the probe's scratch run dir;
  2. plant `<json-out>.tmp` as a symlink to the victim;
  3. run the writer through its PUBLIC CLI (`--root --repair-cmd --work --rev
     --expect --json-out`) as a subprocess, with a repair command that cannot
     repair (the round-93 identity_noop control), so the receipt write itself is
     the exercised surface;
  4. verdict: victim_intact AND receipt_valid. Exit 0 only for a hardened writer.

The probe never writes outside `--work` and never touches the lane tree.

    python3 -I -B tools/round-95/symlink-probe.py --root . \
      --writer tools/round-94/stop-boundary-repair-battery-v4.py \
      --repair-cmd .ufo/waves/round-93/controls/identity_noop.py \
      --work <scratch> --rev <rev> --expect '<FROZEN_LABEL>' --json-out <receipt>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import subprocess
import sys

TOOL = "tools/round-95/symlink-probe.py"
VICTIM_TEXT = b"KAIDOKU-R95-PROBE-VICTIM "


def _sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--writer", required=True)
    ap.add_argument("--repair-cmd", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--expect", required=True)
    ap.add_argument("--json-out")
    args = ap.parse_args(argv)
    root = os.path.abspath(args.root)
    run = os.path.join(os.path.abspath(args.work), "symlink-run")
    os.makedirs(run, exist_ok=True)
    victim = os.path.join(run, "victim.txt")
    planted = VICTIM_TEXT + secrets.token_hex(8).encode() + b"\n"
    with open(victim, "wb") as fh:
        fh.write(planted)
    target = os.path.join(run, "receipt.json")
    if os.path.lexists(target + ".tmp"):
        os.remove(target + ".tmp")
    os.symlink(victim, target + ".tmp")

    workdir = os.path.join(run, "battery-work")
    cmd = [sys.executable, "-I", "-B", os.path.join(root, args.writer),
           "--root", root, "--repair-cmd", args.repair_cmd,
           "--work", workdir, "--rev", args.rev, "--expect", args.expect,
           "--json-out", target]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=1200)
    with open(victim, "rb") as fh:
        victim_after = fh.read()
    victim_intact = victim_after == planted
    receipt_valid = False
    rec = None
    try:
        with open(target, encoding="utf-8") as fh:
            rec = json.load(fh)
        receipt_valid = isinstance(rec, dict)
    except (OSError, ValueError):
        receipt_valid = False
    ok = victim_intact and receipt_valid
    receipt = {
        "class": "R95-C1 symlink write-escape probe",
        "probe": TOOL,
        "writer": args.writer,
        "writer_sha256": _sha256_file(os.path.join(root, args.writer)),
        "repair_cmd": args.repair_cmd,
        "revision": args.rev,
        "writer_rc": p.returncode,
        "writer_stderr_tail": p.stderr[-500:],
        "victim_intact": victim_intact,
        "receipt_valid": receipt_valid,
        "receipt_label": rec.get("label") if isinstance(rec, dict) else None,
        "receipt_met": rec.get("met_target") if isinstance(rec, dict) else None,
        "tmp_left": os.path.lexists(target + ".tmp"),
        "tmp_is_symlink": os.path.islink(target + ".tmp"),
        "verdict": "hardened" if ok else "followed-symlink",
        "met": ok,
    }
    rendered = json.dumps(receipt, indent=1, sort_keys=True)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(rendered + "\n")
    print(rendered)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
