#!/usr/bin/env python3
"""ScribeSources round-47 receipt pass 2: repairs R19/R20 (env was not applied) and
re-measures the frozen path with timestamps."""
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone

S = os.path.dirname(os.path.abspath(__file__))
ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FREEZE = "5017e1f7299c3a812e87e7950148f54313dd279e"
rows = []


def run(label, argv, cwd=S, extra=None, env=None):
    envcopy = dict(os.environ)
    if env:
        envcopy.update(env)
    p = subprocess.run(argv, capture_output=True, text=True, cwd=cwd, env=envcopy)
    out = p.stdout + p.stderr
    row = {"label": label, "argv": argv, "exit": p.returncode,
           "stdout_sha256": hashlib.sha256(out.encode()).hexdigest(),
           "stdout_bytes": len(out.encode()),
           "utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    if extra:
        row.update(extra)
    rows.append(row)
    print(f"{label:26s} exit={p.returncode} {out.strip()[:120]!r}")
    return out


print(datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "pass-2 start")
run("S01-PYTHONPATH-with-I", ["python3", "-I", "-B", "-c",
                              "import sys;print('/evil' in ' '.join(sys.path))"],
    env={"PYTHONPATH": "/evil"})
run("S02-PYTHONPATH-without-I", ["python3", "-B", "-c",
                                 "import sys;print('/evil' in ' '.join(sys.path))"],
    env={"PYTHONPATH": "/evil"})
run("S03-no-flag-path0", ["python3", "-B", "-c", "import sys;print(repr(sys.path[0]))"])
run("S04-I-path0", ["python3", "-I", "-B", "-c", "import sys;print(repr(sys.path[0]))"])
# frozen path, re-measured now
run("S05-hash-object", ["git", "hash-object", "tools/round-47/record.py",
                        "tools/round-47/exact.py"], cwd=ROOT)
run("S06-freeze-blobs", ["git", "rev-parse", f"{FREEZE}:tools/round-47/record.py",
                         f"{FREEZE}:tools/round-47/exact.py"], cwd=ROOT)
run("S07-diff-stat-freeze", ["git", "diff", "--stat", FREEZE, "--", "tools/round-47/"], cwd=ROOT)
run("S08-status-round47", ["git", "status", "--porcelain", "tools/round-47/"], cwd=ROOT)
run("S09-pycache-files", ["find", "tools/round-47", "-name", "*.pyc"], cwd=ROOT)
run("S10-check-ignore", ["git", "check-ignore", "-v",
                         "tools/round-47/__pycache__/exact.cpython-314.pyc"], cwd=ROOT)
run("S11-registry-rows-S14", ["grep", "-c", "^[|] S14", "corpus/SOURCES.md"], cwd=ROOT)
run("S12-S143-present-worktree", ["grep", "-c", "^[|] S143", "corpus/SOURCES.md"], cwd=ROOT)
run("S13-S143-at-freeze", ["git", "show", f"{FREEZE}:corpus/SOURCES.md"], cwd=ROOT,
    extra={"note": "full text; the S143 count is S14"})
run("S14-ls-worktree-round47", ["ls", "-1", "tools/round-47"], cwd=ROOT)
with open(os.path.join(S, "receipts2.jsonl"), "w", encoding="utf-8") as fh:
    for r in rows:
        fh.write(json.dumps(r, sort_keys=True) + "\n")
print("wrote receipts2.jsonl", len(rows))
