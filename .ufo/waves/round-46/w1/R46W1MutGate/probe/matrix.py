#!/usr/bin/env python3
"""Emit the citable mutation matrix: exact command, exit code, stdout sha256, UTC time.

Every row runs the SAME bounded detector on pristine, mutated and (re-read) bytes:
both counters' `--selftest`. `--root/--freeze/--rev` are dummy values: `--selftest`
returns before they are read (they are only argparse-required), which is why a bare
`--selftest` exits 2 and is not the runnable form.
"""
import datetime
import hashlib
import json
import os
import subprocess
import sys

S = os.environ["HYAKU_SCRATCH"]
OUT = sys.argv[1]
TREES = [("base", "frozen@3182047"), ("m1", "m1 drop --diff-merges=first-parent"),
         ("m1b", "m1b reorder the two flags"), ("m2", "m2 drop the blob arm"),
         ("m3", "m3 hard-coded frozen list"), ("m4", "m4 dirty replaces"),
         ("m5", "m5 out_path passthrough"), ("m6", "m6 /tmp scratch allowed"),
         ("headbase", "HEAD@c0112995 pristine"),
         ("h1", "h1 drop --diff-merges (HEAD)"), ("h2", "h2 drop blob arm (HEAD)"),
         ("h3", "h3 hard-coded frozen list (HEAD)"), ("h4", "h4 dirty replaces (HEAD)"),
         ("h5", "h5 out_path passthrough (HEAD)"), ("h6", "h6 /tmp scratch (HEAD)")]

rows = []
for tree, label in TREES:
    tools = os.path.join(S, tree, "tools", "round-46")
    for tool in ("attest.py", "registry.py"):
        cmd = [sys.executable, "-I", "-B", os.path.join(tools, tool),
               "--root", os.path.join(S, tree), "--freeze", "0" * 40, "--rev", "0" * 40,
               "--selftest"]
        t0 = datetime.datetime.now(datetime.timezone.utc)
        p = subprocess.run(cmd, capture_output=True, text=True,
                           env=dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S))
        t1 = datetime.datetime.now(datetime.timezone.utc)
        banner = next((l for l in p.stdout.splitlines() if "_SELFTEST:" in l), "")
        rows.append({
            "tree": tree, "label": label, "tool": tool,
            "gate_sha256": hashlib.sha256(
                open(os.path.join(tools, "gate.py"), "rb").read()).hexdigest(),
            "cmd": " ".join(cmd),
            "exit": p.returncode,
            "stdout_sha256": hashlib.sha256(p.stdout.encode()).hexdigest(),
            "stderr_len": len(p.stderr),
            "banner": banner,
            "utc_start": t0.isoformat(timespec="seconds"),
            "utc_end": t1.isoformat(timespec="seconds"),
        })

doc = {"harness": "both counters' --selftest, dummy --root/--freeze/--rev",
       "python": sys.version.split()[0], "rows": rows}
with open(OUT, "w") as fh:
    fh.write(json.dumps(doc, indent=1) + "\n")
print(json.dumps({"rows": len(rows), "out": OUT}))
