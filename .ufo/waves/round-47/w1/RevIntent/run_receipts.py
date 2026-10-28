#!/usr/bin/env python3
"""Run each command once, capture exact stdout bytes, exit code, sha256 and UTC."""
import hashlib
import json
import os
import shlex
import subprocess
import sys
import time

S = os.environ["S"]
OUT = os.path.join(S, "receipts")
os.makedirs(OUT, exist_ok=True)
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"

CMDS = [
    ("01-git-version", "git --version", S),
    ("02-gate-hashes", "cd %s && for r in 13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5 5017e1f7299c3a812e87e7950148f54313dd279e; do echo -n \"$r \"; git show $r:tools/round-46/gate.py | sha256sum; done; echo -n 'worktree '; sha256sum tools/round-46/gate.py" % LANE, LANE),
    ("03-doc-m-sentence", "zcat /usr/share/man/man1/git-log.1.gz | col -b | sed -n '/^\\fB\\\\-m\\\\fR$/,/^\\fB\\\\-c\\\\fR$/p'", S),
    ("04-doc-diffmerges", "zcat /usr/share/man/man1/git-log.1.gz | col -b | sed -n '/diff.merges=.format/,/combined.all.paths/p' | head -80", S),
    ("05-raw-arm-table", """
D=$S/fx-evil-ftez; M=$(git -C "$D" rev-parse HEAD); B=$(git -C "$D" rev-parse HEAD^1)
for a in "-m --diff-merges=first-parent" "--diff-merges=first-parent -m" "--diff-merges=first-parent" "-m" "--diff-merges=separate"; do
  echo "### $a"
  git -C "$D" log $a --name-status -z --format= "$B..$M" -- | od -An -c | head -4
  echo "exit=$?"
done""".replace("$S", S), S),
    ("06-probe1", "cd %s && S=%s TMPDIR=%s HYAKU_SCRATCH=%s python3 -B probe.py" % (S, S, S, S), S),
    ("07-probe2", "cd %s && S=%s TMPDIR=%s HYAKU_SCRATCH=%s python3 -B probe2.py" % (S, S, S, S), S),
    ("08-exact-selftest", "cd %s && S=%s TMPDIR=%s HYAKU_SCRATCH=%s python3 -I -B tools/round-47/exact.py --root . --freeze 5017e1f7299c3a812e87e7950148f54313dd279e --rev 13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5 --selftest" % (LANE, S, S, S), LANE),
    ("09-frozen-set", "cd %s && python3 -I -B -c \"import sys;sys.path.insert(0,'tools/round-46');import gate;print(gate.frozen_set('.', '5017e1f7299c3a812e87e7950148f54313dd279e','plans/round-47-claims.md'))\"" % LANE, LANE),
]

receipts = []
for name, cmd, cwd in CMDS:
    t = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    r = subprocess.run(["bash", "-c", cmd], cwd=cwd, capture_output=True,
                       env=dict(os.environ, S=S))
    path = os.path.join(OUT, name + ".out")
    open(path, "wb").write(r.stdout + b"\n--stderr--\n" + r.stderr)
    receipts.append({"receipt": name, "utc": t, "cwd": cwd, "command": cmd,
                     "exit": r.returncode,
                     "stdout_sha256": hashlib.sha256(r.stdout).hexdigest(),
                     "stdout_bytes": len(r.stdout),
                     "stdout_file": path})
    print("%-20s exit=%s bytes=%d sha=%s" % (name, r.returncode, len(r.stdout),
                                             hashlib.sha256(r.stdout).hexdigest()))

json.dump(receipts, open(os.path.join(OUT, "receipts.json"), "w"), indent=1)
