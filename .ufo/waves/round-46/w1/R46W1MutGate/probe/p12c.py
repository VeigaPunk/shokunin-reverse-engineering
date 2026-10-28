#!/usr/bin/env python3
"""Decisive discriminators for m1 (drop --diff-merges=first-parent) and m2 (drop blob arm).

Fixture construction notes that earlier drafts got wrong:
  * the claims file must exist in the fixture (frozen_set reads it at rev);
  * the two branches must not edit the same file, or the merge conflicts and HEAD
    never moves (freeze..rev then empty, and every arm reads clean for the wrong
    reason);
  * `git log A..B` walks every commit reachable from B and not from A, so the side
    commit must not touch the frozen path — otherwise the side commit itself puts
    the path into `touched` and the merge arm is not what is being measured.

P1b (m1): side edits only a non-frozen file; mainline edits the frozen path BEFORE
  freeze.  Then freeze..rev is the single merge commit, merge result == first parent
  for the frozen path, merge result != second parent.  Correct verdict: clean.
  Under plain `-m` the merge is diffed against BOTH parents, so the second-parent
  view shows the frozen path as M and the mutant reports a spurious exit 2.

P2b (m2): a rename INTO the frozen path.  `history_touched` consumes `--name-status`
  as (status, one path) token pairs; a rename line prints `R100<TAB>old<TAB>new` in
  plain output (and `R100\0old\0new\0` in -z), so the DESTINATION token is consumed
  as if it were a status and the frozen path never reaches `touched`.  The blob arm
  is the only arm that sees it, so dropping it (m2) reads clean.
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

# File-level frozen entry (not the directory): the directory entry's tree hash
# changes on any edit, so the blob arm would catch P1b before the history arm is
# ever decisive.
CLAIMS_FILE = ("# claims\n\n## Frozen paths (exact)\n\n- `tools/round-46/gate.py`\n\n"
               "## After\n\ntail\n")
# Directory-level frozen entry for P2b: the rename lands INSIDE the directory, so
# the tree hash moves and only the blob arm sees it.
CLAIMS_DIR = ("# claims\n\n## Frozen paths (exact)\n\n- `tools/round-46/`\n\n## After\n\ntail\n")
out = {"mutant_dir": WHICH,
       "gate_sha256": hashlib.sha256(
           open(os.path.join(S, WHICH, "tools", "round-46", "gate.py"), "rb").read()).hexdigest()}


def sh(d, *a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)


def newrepo(prefix):
    d = tempfile.mkdtemp(dir=S, prefix=prefix)
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    for k, v in (("user.email", "px@r46"), ("user.name", "px")):
        subprocess.run(["git", "-C", d, "config", k, v], check=True)
    assert sh(d, "rev-parse", "--show-toplevel").stdout.strip() == d, "toplevel mismatch"
    return d


def write(d, rel, text):
    full = os.path.join(d, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as fh:
        fh.write(text)


# ---- P1b ------------------------------------------------------------------------
d = newrepo("p1b-")
write(d, "plans/round-46-claims.md", CLAIMS)
write(d, "tools/round-46/gate.py", "X\n")
write(d, "side.txt", "s0\n")
write(d, "main.txt", "m0\n")
sh(d, "add", "-A")
sh(d, "commit", "-q", "-m", "base")
sh(d, "checkout", "-q", "-b", "side")
write(d, "side.txt", "s1\n")                     # side touches ONLY a non-frozen file
sh(d, "commit", "-q", "-am", "side: non-frozen file only")
sh(d, "checkout", "-q", "master")
write(d, "tools/round-46/gate.py", "Y\n")        # frozen path edited on the FIRST parent
write(d, "main.txt", "m1\n")
sh(d, "add", "-A")
sh(d, "commit", "-q", "-m", "mainline: frozen path X -> Y (this is FREEZE)")
freeze = sh(d, "rev-parse", "HEAD").stdout.strip()
mres = sh(d, "merge", "--no-ff", "side", "-m", "clean merge")
rev = sh(d, "rev-parse", "HEAD").stdout.strip()
fp = "tools/round-46/gate.py"
log_range = sh(d, "log", "--format=%s", f"{freeze}..{rev}").stdout.split("\n")
if freeze == rev:
    raise SystemExit("P1b fixture did not advance: " + mres.stdout + mres.stderr)
out["p1b"] = {
    "commits_in_range": [x for x in log_range if x],
    "frozen_at_freeze": sh(d, "show", f"{freeze}:{fp}").stdout.strip(),
    "frozen_at_rev": sh(d, "show", f"{rev}:{fp}").stdout.strip(),
    "merge_rc": mres.returncode,
    "firstparent_diff": sh(d, "log", "-m", "--diff-merges=first-parent", "--name-status",
                           "--format=", f"{freeze}..{rev}", "--", fp).stdout.split(),
    "plain_m_diff": sh(d, "log", "-m", "--name-status", "--format=",
                       f"{freeze}..{rev}", "--", fp).stdout.split(),
}
code, rec = gate.freeze_state(d, freeze, rev)
out["p1b"].update({"exit": code, "touched": rec.get("touched"),
                   "blob_changed": rec.get("blob_changed"),
                   "frozen_path_changed": rec.get("frozen_path_changed")})
shutil.rmtree(d, ignore_errors=True)

# ---- P2b ------------------------------------------------------------------------
d = newrepo("p2b-")
write(d, "plans/round-46-claims.md", CLAIMS)
write(d, "outside/gate.py", "ORIGINAL\n")
write(d, "outside/gate2.py", "ORIGINAL2\n")
sh(d, "add", "-A")
sh(d, "commit", "-q", "-m", "base")
freeze = sh(d, "rev-parse", "HEAD").stdout.strip()
os.makedirs(os.path.join(d, "tools/round-46"), exist_ok=True)
sh(d, "mv", "outside/gate.py", "tools/round-46/gate.py")
sh(d, "commit", "-q", "-m", "rename a file INTO the frozen path")
rev = sh(d, "rev-parse", "HEAD").stdout.strip()
fp = "tools/round-46/gate.py"
raw = sh(d, "log", "-m", "--diff-merges=first-parent", "--name-status", "-z",
         "--format=", f"{freeze}..{rev}", "--", fp).stdout
out["p2b"] = {
    "commits_in_range": [x for x in sh(d, "log", "--format=%s",
                                       f"{freeze}..{rev}").stdout.split("\n") if x],
    "frozen_present_at_freeze": sh(d, "cat-file", "-e", f"{freeze}:{fp}").returncode == 0,
    "frozen_at_rev": sh(d, "show", f"{rev}:{fp}").stdout.strip(),
    "raw_name_status_nul": raw,
    "raw_tokens": raw.split("\0"),
    "nul_split_plain": sh(d, "log", "-m", "--diff-merges=first-parent", "--name-status",
                          "-z", "--no-renames", "--format=",
                          f"{freeze}..{rev}", "--", fp).stdout.split("\0"),
}
code, rec = gate.freeze_state(d, freeze, rev)
out["p2b"].update({"exit": code, "touched": rec.get("touched"),
                   "blob_changed": rec.get("blob_changed"),
                   "frozen_path_changed": rec.get("frozen_path_changed")})
shutil.rmtree(d, ignore_errors=True)

print(json.dumps(out, indent=1))
