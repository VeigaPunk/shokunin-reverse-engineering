#!/usr/bin/env python3
"""Decisive discriminators for m1 (drop --diff-merges=first-parent) and m2 (drop blob arm).

P1b (m1): a merge whose FIRST-PARENT diff is empty for the frozen path, whose
  SECOND-PARENT diff is not, and whose side commit does not touch the frozen path
  inside freeze..rev.  The frozen path is byte-identical at freeze and rev, so the
  blob arm is clean: `clean` is the correct verdict.  Plain `-m` (the mutant) shows
  both parents' diffs, so it reports the frozen path as touched -> spurious exit 2.

P2b (m2): a rename INTO the frozen file from outside it.  `--name-status` pairs
  "R100" with the OLD name, and `history_touched` consumes exactly two tokens, so
  the destination (the frozen path) never enters `touched`.  The blob arm is the
  only arm that sees it.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

S = os.environ["HYAKU_SCRATCH"]
WHICH = sys.argv[1]
sys.path.insert(0, os.path.join(S, WHICH, "tools", "round-46"))
import gate  # noqa: E402

out = {"mutant_dir": WHICH,
       "gate_sha256": hashlib.sha256(
           open(os.path.join(S, WHICH, "tools", "round-46", "gate.py"), "rb").read()).hexdigest()}


def git_in(d, *a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)


def newrepo(prefix):
    d = tempfile.mkdtemp(dir=S, prefix=prefix)
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    for k, v in (("user.email", "px@r46"), ("user.name", "px")):
        subprocess.run(["git", "-C", d, "config", k, v], check=True)
    assert git_in(d, "rev-parse", "--show-toplevel").stdout.strip() == d, "toplevel mismatch"
    return d


def write(d, rel, text):
    full = os.path.join(d, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as fh:
        fh.write(text)


# ---- P1b ------------------------------------------------------------------------
d = newrepo("p1b-")
write(d, "tools/round-46/gate.py", "X\n")
write(d, "u.txt", "u0\n")
git_in(d, "add", "-A")
git_in(d, "commit", "-q", "-m", "base")
git_in(d, "checkout", "-q", "-b", "side")
write(d, "u.txt", "u-side\n")
git_in(d, "commit", "-q", "-am", "side: touches only a non-frozen file")
git_in(d, "checkout", "-q", "master")
write(d, "tools/round-46/gate.py", "Y\n")   # the only change to the frozen path
write(d, "u.txt", "u-main\n")
git_in(d, "add", "-A")
git_in(d, "commit", "-q", "-m", "mainline: frozen path X -> Y, this is FREEZE")
freeze = git_in(d, "rev-parse", "HEAD").stdout.strip()
git_in(d, "merge", "--no-ff", "side", "-m", "clean merge")
rev = git_in(d, "rev-parse", "HEAD").stdout.strip()
fp = "tools/round-46/gate.py"
out["p1b"] = {
    "setup": "side commit touches only u.txt; frozen path changed before FREEZE by mainline",
    "frozen_path_at_freeze": git_in(d, "show", f"{freeze}:{fp}").stdout.strip(),
    "frozen_path_at_rev": git_in(d, "show", f"{rev}:{fp}").stdout.strip(),
    "side_commits_in_range": git_in(d, "log", "--format=%s", f"{freeze}..{rev}").stdout.split("\n"),
    "first_parent_diff_of_merge": git_in(d, "log", "-m", "--diff-merges=first-parent",
                                         "--name-status", "--format=", f"{freeze}..{rev}",
                                         "--", fp).stdout.split(),
    "plain_m_diff_of_merge": git_in(d, "log", "-m", "--name-status", "--format=",
                                    f"{freeze}..{rev}", "--", fp).stdout.split(),
}
code, rec = gate.freeze_state(d, freeze, rev)
out["p1b"].update({"exit": code, "touched": rec.get("touched"),
                   "blob_changed": rec.get("blob_changed"),
                   "frozen_path_changed": rec.get("frozen_path_changed"),
                   "reason": rec.get("reason")})
shutil.rmtree(d, ignore_errors=True)

# ---- P2b ------------------------------------------------------------------------
d = newrepo("p2b-")
write(d, "other/gate.py", "ORIGINAL\n")
write(d, "tools/round-46/stub.py", "s\n")
git_in(d, "add", "-A")
git_in(d, "commit", "-q", "-m", "base")
freeze = git_in(d, "rev-parse", "HEAD").stdout.strip()
os.makedirs(os.path.join(d, "tools/round-46"), exist_ok=True)
git_in(d, "mv", "other/gate.py", "tools/round-46/gate.py")
git_in(d, "commit", "-q", "-m", "rename a file INTO the frozen path")
rev = git_in(d, "rev-parse", "HEAD").stdout.strip()
fp = "tools/round-46/gate.py"
out["p2b"] = {
    "setup": "git mv other/gate.py -> tools/round-46/gate.py inside freeze..rev",
    "frozen_path_at_freeze": git_in(d, "cat-file", "-e", f"{freeze}:{fp}").returncode,
    "frozen_path_at_rev": git_in(d, "show", f"{rev}:{fp}").stdout.strip(),
    "raw_name_status": git_in(d, "log", "-m", "--diff-merges=first-parent", "--name-status",
                              "--format=", f"{freeze}..{rev}", "--", fp).stdout.split("\n"),
}
code, rec = gate.freeze_state(d, freeze, rev)
out["p2b"].update({"exit": code, "touched": rec.get("touched"),
                   "blob_changed": rec.get("blob_changed"),
                   "frozen_path_changed": rec.get("frozen_path_changed"),
                   "reason": rec.get("reason")})
shutil.rmtree(d, ignore_errors=True)

print(json.dumps(out, indent=1))
