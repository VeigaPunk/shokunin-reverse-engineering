#!/usr/bin/env python3
"""Does the decoy path in a self-shrunk frozen section have to exist?"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

S = "/fast/scratch/hyaku/kaidoku-r46/R46W1RevRestoredUnion"
sys.path.insert(0, os.path.join(S, "lib"))
import gate  # noqa: E402

d = tempfile.mkdtemp(dir=S, prefix="decoy-")
subprocess.run(["git", "-C", d, "init", "-q"], check=True)
for k, v in (("user.email", "r46@fixture"), ("user.name", "r46 fixture")):
    subprocess.run(["git", "-C", d, "config", k, v], check=True)
top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                     capture_output=True, text=True).stdout.strip()
assert os.path.realpath(top) == os.path.realpath(d), (top, d)


def put(rel, text):
    full = os.path.join(d, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as fh:
        fh.write(text)


def commit(msg):
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "commit", "-q", "-m", msg], check=True)
    return subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()


CLAIMS = "plans/round-46-claims.md"
put(CLAIMS, "# c\n\n## Frozen paths (exact)\n\n- `plans/round-46-claims.md`\n"
            "- `tools/round-46/`\n\n## After\n\nx\n")
put("tools/round-46/gate.py", "print('gate')\n")
fz = commit("freeze")
put(CLAIMS, "# c\n\n## Frozen paths (exact)\n\n- `does/not/exist/`\n\n## After\n\nx\n")
put("tools/round-46/gate.py", "print('gate')\n# tampered\n")
rev = commit("decoy that exists nowhere + tampered tool")
code, rec = gate.freeze_state(d, fz, rev, CLAIMS)
print(json.dumps({"case": "decoy path that exists nowhere",
                  "exit": code, "derived": rec.get("frozen_derived"),
                  "touched": rec.get("touched"), "blob_changed": rec.get("blob_changed"),
                  "restored": rec.get("restored"),
                  "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                  "stdout_sha256": hashlib.sha256(
                      json.dumps(rec, sort_keys=True).encode()).hexdigest()}, indent=1))
shutil.rmtree(d, ignore_errors=True)
