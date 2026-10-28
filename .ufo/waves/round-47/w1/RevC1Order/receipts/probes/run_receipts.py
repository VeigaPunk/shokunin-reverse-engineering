#!/usr/bin/env python3
"""Run each probe once, record exact command, exit code, stdout sha256 and UTC time."""
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

S = sys.argv[1]
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)

PROBES = [
    ("p0a-bare-selftest",
     ["python3", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-47/exact.py",
      "--selftest"]),
    ("p0b-selftest-with-dummy-required",
     ["python3", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-47/exact.py",
      "--root", "/nonexistent", "--freeze", "x", "--rev", "y", "--selftest"]),
    ("p1-clause7-matrix", ["python3", "-B", "drive_clause7.py", S]),
    ("p2-flag-order-semantics", ["python3", "-B", "probe_order_semantics.py", S]),
    ("p3-clause7-forgery", ["python3", "-B", "probe_clause7_forgery.py", S]),
    ("p4-post-freeze-flip", ["python3", "-B", "probe_postfreeze_flip.py", S]),
    ("p5-kwarg-equivalence", ["python3", "-B", "probe_kwarg_equiv.py", S]),
    ("p6-e2e-counter-forgery", ["python3", "-B", "probe_e2e_forgery.py", S]),
    ("p7-formatter-80col", ["python3", "-B", "probe_formatter.py", S]),
]

rows = []
EXPECT = {"p0a-bare-selftest": 2}   # documented defensive invocation is unreachable
for name, cmd in PROBES:
    t0 = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    env = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S)
    r = subprocess.run(cmd, cwd=S, capture_output=True, env=env)
    t1 = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out = os.path.join(OUT, name + ".json")
    with open(out, "wb") as fh:
        fh.write(r.stdout)
    err = os.path.join(OUT, name + ".stderr")
    with open(err, "wb") as fh:
        fh.write(r.stderr)
    rows.append({"probe": name, "command": " ".join(cmd), "cwd": S,
                 "exit": r.returncode, "expected_exit": EXPECT.get(name, 0),
                 "utc_start": t0, "utc_end": t1,
                 "stdout_sha256": hashlib.sha256(r.stdout).hexdigest(),
                 "stdout_bytes": len(r.stdout),
                 "stderr_sha256": hashlib.sha256(r.stderr).hexdigest(),
                 "stderr_bytes": len(r.stderr),
                 "stdout_receipt": out})
    print(json.dumps(rows[-1]))

with open(os.path.join(OUT, "receipts.jsonl"), "w") as fh:
    for row in rows:
        fh.write(json.dumps(row) + "\n")
bad = [r for r in rows if r["exit"] != r["expected_exit"]]
sys.exit(0 if not bad else 1)
