#!/usr/bin/env python3
"""P1 (m1: drop --diff-merges=first-parent): does the arm change any verdict?

Two merge fixtures, both one-commit-per-side, frozen path = `tools/round-46/`.
  A clean merge: the side branch edits a frozen path, the merge result equals the
    first parent (the merge introduced nothing) -> history arm must read clean.
  B evil merge: the merge resolution itself edits the frozen path -> must read dirty.
"""
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

CLAIMS = ("# claims\n\n## Frozen paths (exact)\n\n- `tools/round-46/`\n\n## After\n\ntail\n")


def fixture(scratch, clean_merge):
    d = tempfile.mkdtemp(dir=scratch, prefix="m1-")
    g = lambda *a: subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    subprocess.run(["git", "-C", d, "config", "user.email", "p1@r46"], check=True)
    subprocess.run(["git", "-C", d, "config", "user.name", "p1"], check=True)
    assert g("rev-parse", "--show-toplevel").stdout.strip() == d, "toplevel mismatch"
    files = {"plans/round-46-claims.md": CLAIMS,
             "tools/round-46/gate.py": "print('v0')\n",
             "tools/round-46/other.txt": "other0\n"}
    for p, t in files.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w").write(t)
    g("add", "-A")
    g("commit", "-q", "-m", "base")
    freeze = g("rev-parse", "HEAD").stdout.strip()
    g("checkout", "-q", "-b", "side")
    open(os.path.join(d, "tools/round-46/gate.py"), "w").write("print('SIDE')\n")
    g("commit", "-q", "-am", "side edits a frozen path")
    g("checkout", "-q", "master")
    open(os.path.join(d, "tools/round-46/other.txt"), "w").write("other-MAIN\n")
    g("commit", "-q", "-am", "mainline edits a non-frozen path")
    if clean_merge:
        # side's change to gate.py is carried by the merge, then the merge is
        # resolved back to the first parent's bytes: the merge introduced nothing.
        g("merge", "--no-ff", "--no-commit", "side")
        # the merge itself is a valid result (both sides changed different files)
        g("commit", "-q", "-m", "clean merge: result equals first parent for gate.py")
    else:
        g("merge", "--no-ff", "--no-commit", "side")
        open(os.path.join(d, "tools/round-46/gate.py"), "w").write("print('EVIL')\n")
        g("add", "tools/round-46/gate.py")
        g("commit", "-q", "-m", "evil merge: resolution edits the frozen path")
    rev = g("rev-parse", "HEAD").stdout.strip()
    return d, freeze, rev


def main():
    scratch = os.environ["HYAKU_SCRATCH"]
    out = {"mutant_dir": WHICH, "gate_sha256": gate.hashlib.sha256(
        open(os.path.join(S, WHICH, "tools/round-46/gate.py"), "rb").read()).hexdigest()
        if hasattr(gate, "hashlib") else None, "cases": []}
    import hashlib
    out["gate_sha256"] = hashlib.sha256(
        open(os.path.join(S, WHICH, "tools/round-46/gate.py"), "rb").read()).hexdigest()
    for label, clean in (("clean-merge", True), ("evil-merge", False)):
        d, freeze, rev = fixture(scratch, clean)
        try:
            code, rec = gate.freeze_state(d, freeze, rev)
            out["cases"].append({"case": label, "exit": code,
                                 "frozen_path_changed": rec.get("frozen_path_changed"),
                                 "touched": rec.get("touched"),
                                 "blob_changed": rec.get("blob_changed"),
                                 "reason": rec.get("reason")})
        finally:
            shutil.rmtree(d, ignore_errors=True)
    print(json.dumps(out, indent=1))


main()
