#!/usr/bin/env python3
"""Receipt harness: run one command and record seat, argv, exit, stdout sha256, wall time."""
import argparse
import datetime as dt
import hashlib
import json
import os
import shlex
import subprocess
import sys
import time


def now():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seat", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--note", default="")
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    a = ap.parse_args()
    cmd = a.cmd[1:] if a.cmd and a.cmd[0] == "--" else a.cmd
    os.makedirs(a.out, exist_ok=True)
    started = now()
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True)
    wall = round(time.time() - t0, 3)
    out = p.stdout
    err = p.stderr
    op = os.path.join(a.out, f"{a.name}.stdout.txt")
    ep = os.path.join(a.out, f"{a.name}.stderr.txt")
    with open(op, "wb") as f:
        f.write(out)
    with open(ep, "wb") as f:
        f.write(err)
    rec = {
        "seat": a.seat,
        "name": a.name,
        "argv": cmd,
        "argv_shell": " ".join(shlex.quote(x) for x in cmd),
        "cwd": os.getcwd(),
        "started_at": started,
        "finished_at": now(),
        "wall_s": wall,
        "exit": p.returncode,
        "stdout_bytes": len(out),
        "stdout_sha256": hashlib.sha256(out).hexdigest(),
        "stderr_bytes": len(err),
        "stderr_sha256": hashlib.sha256(err).hexdigest(),
        "stdout_path": os.path.relpath(op, os.getcwd()),
        "stderr_path": os.path.relpath(ep, os.getcwd()),
        "note": a.note,
        "exit_semantics": {0: "met/clean", 1: "failed", 2: "could-not-evaluate"}.get(
            p.returncode, "other"
        ),
    }
    rp = os.path.join(a.out, f"{a.name}.json")
    with open(rp, "w") as f:
        json.dump(rec, f, indent=1)
        f.write("\n")
    sys.stdout.write(out.decode("utf-8", "replace"))
    sys.stderr.write(err.decode("utf-8", "replace"))
    print(f"[receipt] {rp} exit={p.returncode} stdout_sha256={rec['stdout_sha256']} wall={wall}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
