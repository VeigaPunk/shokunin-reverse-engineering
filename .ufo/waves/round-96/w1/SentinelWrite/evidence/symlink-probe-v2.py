#!/usr/bin/env python3
"""symlink-probe-v2.py - round-96 public-path write-escape probe (R96-C1, calibration).

Round-95 successor of `tools/round-95/symlink-probe.py` with one change: the probe's OWN
receipt is written through the same hardened writer the counters use (mkstemp unique temp
name in the receipt's own directory, flush, fsync, `os.replace`) - closing round-95 M95-i /
named limit 4, where the probe's `open(..., "w")` followed a symlink planted at the probe's
own `--json-out` path. `os.replace` onto a planted link replaces the link, never the victim.

The probe freezes the write-escape difference on the public path of whichever COUNTER writer
it is given (unchanged behaviour):

  1. plant a victim file with a nonce content in the probe's scratch run dir;
  2. plant `<json-out>.tmp` as a symlink to the victim;
  3. run the writer through its PUBLIC CLI (`--root --repair-cmd --work --rev
     --expect --json-out`) as a subprocess, with a repair command that cannot
     repair (the round-93 identity_noop control), so the receipt write itself is
     the exercised surface;
  4. verdict: victim_intact AND receipt_valid. Exit 0 only for a hardened writer.

The probe never writes outside `--work` and never touches the lane tree.

    python3 -I -B tools/round-96/symlink-probe-v2.py --root . \
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
import tempfile

TOOL = "tools/round-96/symlink-probe-v2.py"
VICTIM_TEXT = b"KAIDOKU-R96-PROBE-VICTIM "


def _sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _default(obj):
    if isinstance(obj, (bytes, bytearray)):
        return {"bytes": len(obj), "sha256": hashlib.sha256(bytes(obj)).hexdigest()}
    raise TypeError(f"Cannot serialize object of {type(obj)}")


def write_receipt(path: str, receipt: dict) -> None:
    """Complete JSON or absent, and immune to a planted symlink at the receipt path
    itself or at the predictable `<path>.tmp` name (round-95 M95-i closure)."""
    d = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmp = tempfile.mkstemp(dir=d, prefix=os.path.basename(path) + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=1, sort_keys=True, default=_default)
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise


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
        "class": "R96-C1 symlink write-escape probe (v2 writer)",
        "probe": TOOL,
        "probe_sha256": _sha256_file(os.path.abspath(__file__)),
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
        write_receipt(args.json_out, receipt)
    print(rendered)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
