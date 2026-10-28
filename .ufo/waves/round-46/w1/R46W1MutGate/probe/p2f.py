#!/usr/bin/env python3
"""P2f: can the blob arm be the ONLY arm that sees a tamper? (m2 soundness test)

`frozen_set` returns a DIRECTORY entry as (path, True) and a FILE entry as
(path, False). `blob_changed` for a directory compares `rev-parse base:dir` with
`rev-parse tip:dir` (the tree oid); for a file it compares the blob oids.

`history_touched` parses `--name-status -z` as (status, ONE path) token pairs. A
rename prints `R100\\0old\\0new\\0`. With the pathspec limited to the frozen entry,
git only reports the rename when BOTH sides match the pathspec... which is exactly
the case where old is ALSO in scope. So the interesting shape is a file entry that
did not exist at freeze and is created by renaming a file in from outside: only the
destination is in scope, git prints `A` (add), and `touched` sees it.

The remaining shape is a file entry whose MODe changes with no content change:
`blob_changed` compares blob oids, so a mode-only change is invisible to it too.
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


def sh(d, *a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)


def run(entry, files, mutate, label):
    d = tempfile.mkdtemp(dir=S, prefix="p2f-")
    try:
        subprocess.run(["git", "-C", d, "init", "-q"], check=True)
        for k, v in (("user.email", "p2f@r46"), ("user.name", "p2f")):
            subprocess.run(["git", "-C", d, "config", k, v], check=True)
        assert sh(d, "rev-parse", "--show-toplevel").stdout.strip() == d
        allf = dict(files)
        allf["plans/round-46-claims.md"] = (
            "# claims\n\n## Frozen paths (exact)\n\n- `%s`\n\n## After\n\ntail\n" % entry)
        for rel, text in allf.items():
            full = os.path.join(d, rel)
            os.makedirs(os.path.dirname(full) or d, exist_ok=True)
            open(full, "w").write(text)
        sh(d, "add", "-A")
        sh(d, "commit", "-q", "-m", "base")
        freeze = sh(d, "rev-parse", "HEAD").stdout.strip()
        mutate(d)
        rev = sh(d, "rev-parse", "HEAD").stdout.strip()
        code, rec = gate.freeze_state(d, freeze, rev)
        raw = sh(d, "log", "-m", "--diff-merges=first-parent", "--name-status", "-z",
                 "--format=", f"{freeze}..{rev}", "--", entry).stdout
        return {"shape": label, "entry": entry, "exit": code,
                "name_status_tokens": raw.split("\0"),
                "touched": rec.get("touched"), "blob_changed": rec.get("blob_changed"),
                "restored": rec.get("restored"),
                "frozen_path_changed": rec.get("frozen_path_changed"),
                "reason": rec.get("reason"),
                "blob_at_freeze": sh(d, "rev-parse", "--verify", "--quiet",
                                     f"{freeze}:{entry}").stdout.strip() or None,
                "blob_at_rev": sh(d, "rev-parse", "--verify", "--quiet",
                                  f"{rev}:{entry}").stdout.strip() or None}
    finally:
        shutil.rmtree(d, ignore_errors=True)


TARGET = "tools/round-46/payload.py"
cases = []


def rename_in(d):
    """Create the frozen file name by renaming a file in from OUTSIDE the pathspec."""
    os.makedirs(os.path.join(d, "tools/round-46"), exist_ok=True)
    sh(d, "mv", "outside/src.py", TARGET)
    sh(d, "commit", "-q", "-m", "rename outside/src.py -> frozen file name")


def stage_from_elsewhere(d):
    """Content from outside, written direct: a plain add at the frozen name."""
    os.makedirs(os.path.join(d, "tools/round-46"), exist_ok=True)
    shutil.copyfile(os.path.join(d, "outside/src.py"), os.path.join(d, TARGET))
    sh(d, "add", "-A")
    sh(d, "commit", "-q", "-m", "add at the frozen file name")


for label, fn in (("rename-into-frozen-file", rename_in),
                  ("add-at-frozen-file", stage_from_elsewhere)):
    cases.append(run(TARGET, {"outside/src.py": "PAYLOAD\n",
                              "tools/round-46/keep.py": "k\n"}, fn, label))

print(json.dumps({"mutant_dir": WHICH,
                  "gate_sha256": hashlib.sha256(
                      open(os.path.join(S, WHICH, "tools/round-46", "gate.py"), "rb")
                      .read()).hexdigest(), "cases": cases}, indent=1))
