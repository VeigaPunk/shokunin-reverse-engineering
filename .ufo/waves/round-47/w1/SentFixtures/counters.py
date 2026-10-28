#!/usr/bin/env python3
"""Run both counters against every fixture; record exact argv, rc, stdout sha256, UTC."""
import hashlib
import json
import os
import subprocess
import sys
import datetime

S, L, REV = sys.argv[1:4]
REC = os.path.join(S, "receipts")
fx = json.load(open(os.path.join(REC, "fixtures-structural.json")))
rows = []


def run(name, tool, root, extra):
    argv = [sys.executable, "-I", "-B", os.path.join(L, "tools", "round-47", tool),
            "--root", root, *extra]
    env = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S)
    t0 = datetime.datetime.now(datetime.timezone.utc)
    r = subprocess.run(argv, capture_output=True, env=env, timeout=900)
    t1 = datetime.datetime.now(datetime.timezone.utc)
    out = r.stdout.decode("utf-8", "replace")
    try:
        payload = json.loads(out)
    except ValueError:
        payload = {"unparsed": out[:2000]}
    row = {"name": name, "tool": tool, "root": root, "argv": argv[2:],
           "start_utc": t0.isoformat(), "end_utc": t1.isoformat(),
           "rc": r.returncode, "stdout_sha256": hashlib.sha256(r.stdout).hexdigest(),
           "stdout_bytes": len(r.stdout), "stderr": r.stderr.decode()[:800],
           "receipt": payload}
    rows.append(row)
    print(f"{name:28s} {tool:10s} rc={r.returncode} "
          f"reason={payload.get('reason')} failing={payload.get('failing')} "
          f"met={payload.get('met_target')}")
    return row


m1 = open(os.path.join(REC, "f1-merge-oid.txt")).read().strip()
m1b = open(os.path.join(REC, "f1b-merge-oid.txt")).read().strip()
run("F1-merge-conflict", "exact.py", os.path.join(S, "F1"),
    ["--freeze", REV, "--rev", m1, "--no-battery"])
run("F1b-evil-merge", "exact.py", os.path.join(S, "F1b"),
    ["--freeze", REV, "--rev", m1b, "--no-battery"])
run("F2-rename", "exact.py", os.path.join(S, "F2"),
    ["--freeze", REV, "--rev", fx["F2-rename"]["rev"], "--no-battery"])
run("F3-symlink", "exact.py", os.path.join(S, "F3"),
    ["--freeze", REV, "--rev", fx["F3-symlink"]["rev"], "--no-battery"])
run("F3-symlink", "record.py", os.path.join(S, "F3"),
    ["--rev", fx["F3-symlink"]["rev"], "--no-battery"])
run("F3-symlink-claims", "exact.py", os.path.join(S, "F3"),
    ["--freeze", REV, "--rev", fx["F3-symlink-claims"]["rev"], "--no-battery"])
run("F4-submodule", "exact.py", os.path.join(S, "F4"),
    ["--freeze", REV, "--rev", fx["F4-submodule"]["rev"]])
run("F4-submodule", "record.py", os.path.join(S, "F4"),
    ["--rev", fx["F4-submodule"]["rev"], "--no-battery"])
run("F4c-submodule-frozen", "exact.py", os.path.join(S, "F4c"),
    ["--freeze", REV, "--rev", fx["F4c-submodule-frozen"]["rev"], "--no-battery"])
run("F5-bare", "exact.py", os.path.join(S, "F5.git"),
    ["--freeze", REV, "--rev", REV, "--no-battery"])
run("F5-bare", "record.py", os.path.join(S, "F5.git"), ["--rev", REV, "--no-battery"])
json.dump(rows, open(os.path.join(REC, "counter-runs.json"), "w"), indent=1, sort_keys=True)
