#!/usr/bin/env python3
"""Read-only re-derivation driver for the R45 SCORECARD number table.

Usage: run.py <label> <argv...>
Runs the command with cwd=/ and env TMPDIR pointing at scratch, captures
stdout, exit code, stdout sha256 and UTC, writes <label>.stdout + <label>.json.
Never writes outside scratch.
"""
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

S = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"

label = sys.argv[1]
argv = sys.argv[2:]
env = dict(os.environ)
env["TMPDIR"] = S
env["HYAKU_SCRATCH"] = S
utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
r = subprocess.run(argv, cwd="/", capture_output=True, text=True, env=env)
out = r.stdout
sha = hashlib.sha256(out.encode()).hexdigest()
with open(os.path.join(S, label + ".stdout"), "w") as fh:
    fh.write(out)
rec = {
    "label": label,
    "utc": utc,
    "cwd": "/",
    "cmd": " ".join(argv),
    "exit": r.returncode,
    "stdout_sha256": sha,
    "stderr_head": r.stderr[:400],
}
try:
    rec["json"] = json.loads(out)
except Exception:
    rec["json"] = None
with open(os.path.join(S, label + ".json"), "w") as fh:
    json.dump(rec, fh, indent=1, sort_keys=True)
print(json.dumps(rec, indent=1, sort_keys=True)[:4000])
sys.exit(0)
