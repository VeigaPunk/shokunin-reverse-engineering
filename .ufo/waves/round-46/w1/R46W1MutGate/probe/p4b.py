#!/usr/bin/env python3
"""P4b: m4 (dirty replaces instead of unions) against the CURRENT-HEAD gate.py.

At the freeze commit `gate.dirty` had no caller: dropping the union could not change
any verdict, so m4 was an equivalent mutant *of the frozen instrument*. At HEAD
(332f4884, "F5") `freeze_state` calls `dirty(root, paths)` with the WHOLE frozen set,
so the union is load-bearing: with two frozen entries, `pathspecs[-1]` is the only one
scanned and a dirty file under the other is invisible.

Fixture: two frozen entries, only the FIRST is dirty in the worktree.
Correct: dirty = [plans/round-46-claims.md] -> exit 2 frozen_worktree_dirty.
Mutant:  dirty = [] -> exit 0 clean.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

S = os.environ["HYAKU_SCRATCH"]
WHICH = sys.argv[1]                     # a *HEAD-bytes* mutant tree: headm4
sys.path.insert(0, os.path.join(S, WHICH, "tools", "round-46"))
import gate  # noqa: E402

out = {"dir": WHICH,
       "gate_sha256": hashlib.sha256(
           open(os.path.join(S, WHICH, "tools", "round-46", "gate.py"), "rb").read()).hexdigest(),
       "dirty_has_caller": "dirty(root, paths)" in open(
           os.path.join(S, WHICH, "tools", "round-46", "gate.py")).read(),
       "cases": []}

CLAIMS = ("# claims\n\n## Frozen paths (exact)\n\n- `plans/round-46-claims.md`\n"
          "- `tools/round-46/`\n\n## After\n\ntail\n")


def sh(d, *a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)


for label, dirty_target in (("claims-file-dirty", "plans/round-46-claims.md"),
                            ("tool-dir-dirty", "tools/round-46/t.py"),
                            ("none-dirty", None)):
    d = tempfile.mkdtemp(dir=S, prefix="p4b-")
    try:
        subprocess.run(["git", "-C", d, "init", "-q"], check=True)
        for k, v in (("user.email", "p4b@r46"), ("user.name", "p4b")):
            subprocess.run(["git", "-C", d, "config", k, v], check=True)
        assert sh(d, "rev-parse", "--show-toplevel").stdout.strip() == d, "toplevel mismatch"
        for rel, text in (("plans/round-46-claims.md", CLAIMS),
                          ("tools/round-46/t.py", "v0\n"),
                          ("SKILL.md", "# skill\n")):
            full = os.path.join(d, rel)
            os.makedirs(os.path.dirname(full) or d, exist_ok=True)
            open(full, "w").write(text)
        sh(d, "add", "-A")
        sh(d, "commit", "-q", "-m", "base")
        rev = sh(d, "rev-parse", "HEAD").stdout.strip()
        if dirty_target:
            with open(os.path.join(d, dirty_target), "a") as fh:
                fh.write("uncommitted\n")
        code, rec = gate.freeze_state(d, rev, rev)
        out["cases"].append({"case": label, "dirty_target": dirty_target, "exit": code,
                             "dirty": rec.get("dirty"), "reason": rec.get("reason"),
                             "frozen_path_changed": rec.get("frozen_path_changed")})
    finally:
        shutil.rmtree(d, ignore_errors=True)

print(json.dumps(out, indent=1))
