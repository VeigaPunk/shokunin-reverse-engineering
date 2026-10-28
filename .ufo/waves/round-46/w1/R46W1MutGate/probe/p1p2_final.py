#!/usr/bin/env python3
"""Decisive discriminators for m1 (drop --diff-merges=first-parent) and m2 (drop blob arm).

Fixture facts learned the hard way, recorded because they bound the mutants:
  * the claims file must exist in the fixture (frozen_set reads it at `rev`);
  * the default branch here is `main`, not `master`; a `git checkout master` fails
    silently under `capture_output` and the merge then reports "Already up to date",
    so freeze == rev and every arm reads clean for the wrong reason;
  * the two sides must not edit the same file or the merge conflicts and HEAD
    never moves;
  * `git log A..B` walks every commit reachable from B and not from A, so the side
    commit must not touch the frozen path, else the side commit alone puts it into
    `touched` and the merge arm is not what is measured;
  * a frozen DIRECTORY entry hashes the whole tree, so the blob arm fires on any
    edit and masks the history arm. The m1 fixture therefore freezes the FILE.

P1b (m1): side edits only a non-frozen file; mainline edits the frozen file BEFORE
  freeze.  freeze..rev is then exactly one merge commit whose first-parent diff for
  the frozen file is EMPTY and whose second-parent diff is `M`.  The merge result
  equals the first parent, the blob arm is clean, so `clean` (exit 0) is correct.
  Plain `-m` diffs the merge against BOTH parents, so the mutant reports a touch and
  exits 2: a false could-not-evaluate on a clean history.

P2b (m2): frozen FILE, a tamper that is never reverted.  Correct: touched=[f],
  changed=[f], restored=[].  The mutant derives `restored` from `touched` alone, so
  it reports the tamper as restored.  The verdict is unchanged, which is exactly
  why the exit-code harness cannot see it.
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

FP = "tools/round-46/gate.py"
CLAIMS_FILE = ("# claims\n\n## Frozen paths (exact)\n\n- `" + FP + "`\n\n## After\n\ntail\n")
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
    top = sh(d, "rev-parse", "--show-toplevel").stdout.strip()
    assert top == d, "toplevel mismatch: %r != %r" % (top, d)
    return d


def write(d, rel, text):
    full = os.path.join(d, rel)
    os.makedirs(os.path.dirname(full) or d, exist_ok=True)
    with open(full, "w") as fh:
        fh.write(text)


# ---- P1b: m1 must produce a false exit 2 on a clean merge -----------------------
d = newrepo("p1b-")
write(d, "plans/round-46-claims.md", CLAIMS_FILE)
write(d, FP, "X\n")
write(d, "side.txt", "s0\n")
write(d, "main.txt", "m0\n")
sh(d, "add", "-A")
sh(d, "commit", "-q", "-m", "base")
branch = sh(d, "symbolic-ref", "--short", "HEAD").stdout.strip()
sh(d, "checkout", "-q", "-b", "side")
write(d, "side.txt", "s1\n")
sh(d, "commit", "-q", "-am", "side: non-frozen file only")
sh(d, "checkout", "-q", branch)
write(d, FP, "Y\n")
write(d, "main.txt", "m1\n")
sh(d, "add", "-A")
sh(d, "commit", "-q", "-m", "mainline: frozen file X -> Y; this commit IS the freeze")
freeze = sh(d, "rev-parse", "HEAD").stdout.strip()
mres = sh(d, "merge", "--no-ff", "side", "-m", "clean merge")
rev = sh(d, "rev-parse", "HEAD").stdout.strip()
if freeze == rev:
    raise SystemExit("P1b fixture did not advance rc=%s %s%s"
                     % (mres.returncode, mres.stdout, mres.stderr))
code, rec = gate.freeze_state(d, freeze, rev)
out["p1b"] = {
    "branch": branch,
    "commits_in_range": [x for x in sh(d, "log", "--format=%s", f"{freeze}..{rev}")
                         .stdout.split("\n") if x],
    "frozen_at_freeze": sh(d, "show", f"{freeze}:{FP}").stdout.strip(),
    "frozen_at_rev": sh(d, "show", f"{rev}:{FP}").stdout.strip(),
    "expected": "exit 0, touched [], changed [] (merge introduced nothing)",
    "firstparent_diff": sh(d, "log", "-m", "--diff-merges=first-parent", "--name-status",
                           "--format=", f"{freeze}..{rev}", "--", FP).stdout.split(),
    "plain_m_diff": sh(d, "log", "-m", "--name-status", "--format=",
                       f"{freeze}..{rev}", "--", FP).stdout.split(),
    "exit": code, "touched": rec.get("touched"), "blob_changed": rec.get("blob_changed"),
    "frozen_path_changed": rec.get("frozen_path_changed"), "restored": rec.get("restored"),
    "reason": rec.get("reason"),
}
shutil.rmtree(d, ignore_errors=True)

# ---- P2b: m2 mislabels a persisted tamper as `restored` -------------------------
d = newrepo("p2b-")
write(d, "plans/round-46-claims.md", CLAIMS_FILE)
write(d, FP, "v0\n")
sh(d, "add", "-A")
sh(d, "commit", "-q", "-m", "base")
freeze = sh(d, "rev-parse", "HEAD").stdout.strip()
write(d, FP, "TAMPER\n")
sh(d, "commit", "-q", "-am", "tamper, never reverted")
rev = sh(d, "rev-parse", "HEAD").stdout.strip()
code, rec = gate.freeze_state(d, freeze, rev)
out["p2b"] = {
    "setup": "frozen file tampered and kept; freeze..rev = one edit commit",
    "frozen_at_rev": sh(d, "show", f"{rev}:{FP}").stdout.strip(),
    "expected": "exit 2, touched [f], changed [f], restored [] (nothing was restored)",
    "exit": code, "touched": rec.get("touched"), "blob_changed": rec.get("blob_changed"),
    "restored": rec.get("restored"), "frozen_path_changed": rec.get("frozen_path_changed"),
    "reason": rec.get("reason"),
}
shutil.rmtree(d, ignore_errors=True)

print(json.dumps(out, indent=1))
