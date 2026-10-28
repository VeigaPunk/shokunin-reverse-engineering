#!/usr/bin/env python3
"""R44Assim receipt runner (round-44 wave 1).

Runs one read-only shell command inside the kaidoku lane and records the receipt fields the
round contract requires: seat, exact command, exit code, sha256 of captured stdout, wall time.

Usage: receipt.py <outdir> <receipt-id> <command>
Writes <outdir>/<receipt-id>.json and prints a one-line summary.
No VCS mutation, no network, no writes outside <outdir>.
"""
import hashlib
import json
import subprocess
import sys
import time

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
SEAT = "R44Assim"

outdir, rid, cmd = sys.argv[1], sys.argv[2], sys.argv[3]
t0 = time.monotonic()
p = subprocess.run(["bash", "-c", cmd], cwd=LANE, capture_output=True)
wall_ms = int((time.monotonic() - t0) * 1000)

rec = {
    "seat": SEAT,
    "id": rid,
    "command": cmd,
    "cwd": LANE,
    "exit": p.returncode,
    "stdout_sha256": hashlib.sha256(p.stdout).hexdigest(),
    "stdout_bytes": len(p.stdout),
    "stderr_sha256": hashlib.sha256(p.stderr).hexdigest(),
    "stderr_bytes": len(p.stderr),
    "wall_ms": wall_ms,
    "stdout": p.stdout.decode("utf-8", "replace")[:8000],
    "stderr": p.stderr.decode("utf-8", "replace")[:4000],
}
with open(f"{outdir}/{rid}.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(rec, indent=1) + "\n")
print(f"{rid} exit={p.returncode} stdout_sha256={rec['stdout_sha256'][:16]} wall={wall_ms}ms")
