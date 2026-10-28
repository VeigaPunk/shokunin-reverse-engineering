#!/usr/bin/env python3
"""P2d: is the blob arm the ONLY arm that sees a rename INSIDE a frozen directory?

`history_touched` parses `--name-status -z` as (status, ONE path) token pairs. A
rename inside the frozen pathspec prints `R100\\0old\\0new\\0`; the parser consumes
`R100`+`old`, then meets `new` (not a status) and discards it. So the history arm
can report NEITHER name, while the frozen directory's tree hash has changed.

If that holds, dropping the blob arm (m2) is a SOUNDNESS defect: a tamper committed
inside the frozen directory scores clean, exit 0.
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
CLAIMS = "# claims\n\n## Frozen paths (exact)\n\n- `tools/round-46/`\n\n## After\n\ntail\n"


def sh(d, *a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)


def case(label, mutate, frozen_dir="tools/round-46/"):
    d = tempfile.mkdtemp(dir=S, prefix="p2d-")
    try:
        subprocess.run(["git", "-C", d, "init", "-q"], check=True)
        for k, v in (("user.email", "p2d@r46"), ("user.name", "p2d")):
            subprocess.run(["git", "-C", d, "config", k, v], check=True)
        assert sh(d, "rev-parse", "--show-toplevel").stdout.strip() == d, "toplevel mismatch"
        for rel, text in (("plans/round-46-claims.md", CLAIMS),
                          ("tools/round-46/alpha.py", "ALPHA\n"),
                          ("tools/round-46/beta.py", "BETA\n")):
            full = os.path.join(d, rel)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            open(full, "w").write(text)
        sh(d, "add", "-A")
        sh(d, "commit", "-q", "-m", "base")
        freeze = sh(d, "rev-parse", "HEAD").stdout.strip()
        mutate(d)
        rev = sh(d, "rev-parse", "HEAD").stdout.strip()
        code, rec = gate.freeze_state(d, freeze, rev)
        raw = sh(d, "log", "-m", "--diff-merges=first-parent", "--name-status", "-z",
                 "--format=", f"{freeze}..{rev}", "--", frozen_dir).stdout
        return {"case": label,
                "commits": [x for x in sh(d, "log", "--format=%s", f"{freeze}..{rev}")
                            .stdout.split("\n") if x],
                "config_renames": sh(d, "config", "--get", "diff.renames").stdout.strip() or "(unset)",
                "name_status_plain": sh(d, "log", "-m", "--diff-merges=first-parent",
                                        "--name-status", "--format=", f"{freeze}..{rev}",
                                        "--", frozen_dir).stdout,
                "name_status_tokens": raw.split("\0"),
                "dir_hash_freeze": sh(d, "rev-parse", f"{freeze}:tools/round-46").stdout.strip(),
                "dir_hash_rev": sh(d, "rev-parse", f"{rev}:tools/round-46").stdout.strip(),
                "exit": code, "touched": rec.get("touched"),
                "blob_changed": rec.get("blob_changed"), "restored": rec.get("restored"),
                "frozen_path_changed": rec.get("frozen_path_changed"),
                "reason": rec.get("reason")}
    finally:
        shutil.rmtree(d, ignore_errors=True)


def rename_within(d):
    sh(d, "mv", "tools/round-46/alpha.py", "tools/round-46/alpha-renamed.py")
    sh(d, "commit", "-q", "-m", "rename INSIDE the frozen directory")


def edit_and_rename(d):
    sh(d, "mv", "tools/round-46/beta.py", "tools/round-46/gamma.py")
    with open(os.path.join(d, "tools/round-46/gamma.py"), "a") as fh:
        fh.write("TAMPERED\n")
    sh(d, "commit", "-q", "-m", "rename inside the frozen dir and edit the destination")


out["cases"] = [case("rename-within-frozen-dir", rename_within),
                case("rename-and-edit-within", edit_and_rename)]
print(json.dumps(out, indent=1))
