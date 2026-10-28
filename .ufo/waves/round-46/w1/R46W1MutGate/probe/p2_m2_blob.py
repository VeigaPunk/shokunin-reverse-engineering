#!/usr/bin/env python3
"""P2 (m2: blob arm dropped): what does the receipt lose?

Case A touch-and-keep: a commit edits the frozen path and it stays edited.  Base
  must report restored == [] (nothing was restored); the mutant derives restored
  from `touched` alone, so it reports the path as restored.
Case B touch-and-restore: edit then revert.  Both should report restored == [path].
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

CLAIMS = "# claims\n\n## Frozen paths (exact)\n\n- `tools/round-46/`\n\n## After\n\ntail\n"
P = "tools/round-46/gate.py"


def fixture(scratch, restore):
    d = tempfile.mkdtemp(dir=scratch, prefix="m2-")
    g = lambda *a: subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    subprocess.run(["git", "-C", d, "config", "user.email", "p2@r46"], check=True)
    subprocess.run(["git", "-C", d, "config", "user.name", "p2"], check=True)
    assert g("rev-parse", "--show-toplevel").stdout.strip() == d
    for path, text in (("plans/round-46-claims.md", CLAIMS), (P, "v0\n")):
        full = os.path.join(d, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w").write(text)
    g("add", "-A")
    g("commit", "-q", "-m", "base")
    freeze = g("rev-parse", "HEAD").stdout.strip()
    open(os.path.join(d, P), "w").write("TAMPER\n")
    g("commit", "-q", "-am", "tamper")
    if restore:
        open(os.path.join(d, P), "w").write("v0\n")
        g("commit", "-q", "-am", "restore")
    return d, freeze, g("rev-parse", "HEAD").stdout.strip()


def main():
    import hashlib
    out = {"mutant_dir": WHICH,
           "gate_sha256": hashlib.sha256(
               open(os.path.join(S, WHICH, "tools/round-46/gate.py"), "rb").read()).hexdigest(),
           "cases": []}
    for label, restore in (("tamper-kept", False), ("tamper-restored", True)):
        d, freeze, rev = fixture(os.environ["HYAKU_SCRATCH"], restore)
        try:
            code, rec = gate.freeze_state(d, freeze, rev)
            out["cases"].append({"case": label, "exit": code,
                                 "touched": rec.get("touched"),
                                 "blob_changed": rec.get("blob_changed"),
                                 "restored": rec.get("restored"),
                                 "frozen_path_changed": rec.get("frozen_path_changed"),
                                 "reason": rec.get("reason")})
        finally:
            shutil.rmtree(d, ignore_errors=True)
    print(json.dumps(out, indent=1))


main()
