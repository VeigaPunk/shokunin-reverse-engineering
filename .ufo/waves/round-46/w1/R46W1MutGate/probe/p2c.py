#!/usr/bin/env python3
"""P2c: is the blob arm load-bearing, or only corroborating?

The claim text says the blob arm is INDEPENDENT. If some tamper is invisible to the
history arm and visible only to the blob arm, then dropping the blob arm (m2) turns a
true `frozen_path_changed` into a false clean — a far worse defect than the mislabelled
`restored` P2b measures.

Candidate: a rename INTO the frozen path. `history_touched` parses `--name-status -z`
as (status, ONE path) pairs; a rename emits `R100\\0old\\0new\\0`, so the destination
token is consumed as if it were a status and the frozen path never enters `touched`.
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


def sh(d, *a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)


def try_case(label, claims_paths, mutate):
    d = tempfile.mkdtemp(dir=S, prefix="p2c-")
    try:
        subprocess.run(["git", "-C", d, "init", "-q"], check=True)
        for k, v in (("user.email", "p2c@r46"), ("user.name", "p2c")):
            subprocess.run(["git", "-C", d, "config", k, v], check=True)
        top = sh(d, "rev-parse", "--show-toplevel").stdout.strip()
        assert top == d, "toplevel mismatch"
        body = ("# claims\n\n## Frozen paths (exact)\n\n" +
                "".join("- `%s`\n" % p for p in claims_paths) + "\n## After\n\ntail\n")
        for rel, text in (("plans/round-46-claims.md", body),
                          ("outside/payload.py", "ORIGINAL\n"),
                          ("tools/round-46/keep.py", "keep\n")):
            full = os.path.join(d, rel)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w") as fh:
                fh.write(text)
        sh(d, "add", "-A")
        sh(d, "commit", "-q", "-m", "base")
        freeze = sh(d, "rev-parse", "HEAD").stdout.strip()
        mutate(d)
        rev = sh(d, "rev-parse", "HEAD").stdout.strip()
        code, rec = gate.freeze_state(d, freeze, rev)
        raw = sh(d, "log", "-m", "--diff-merges=first-parent", "--name-status", "-z",
                 "--format=", f"{freeze}..{rev}", "--", *claims_paths).stdout
        return {"case": label, "claims": claims_paths,
                "commits": [x for x in sh(d, "log", "--format=%s", f"{freeze}..{rev}")
                            .stdout.split("\n") if x],
                "raw_name_status": raw, "raw_tokens": raw.split("\0"),
                "frozen_at_rev": sh(d, "ls-tree", "-r", "--name-only", rev,
                                    "--", *claims_paths).stdout.split(),
                "exit": code, "touched": rec.get("touched"),
                "blob_changed": rec.get("blob_changed"), "restored": rec.get("restored"),
                "frozen_path_changed": rec.get("frozen_path_changed"),
                "reason": rec.get("reason")}
    finally:
        shutil.rmtree(d, ignore_errors=True)


def rename_in(d):
    os.makedirs(os.path.join(d, "tools/round-46"), exist_ok=True)
    sh(d, "mv", "outside/payload.py", "tools/round-46/payload.py")
    sh(d, "commit", "-q", "-m", "rename outside/payload.py INTO the frozen directory")


def copy_in(d):
    """A copy (not a rename) into the frozen dir: history arm should see 'A'."""
    os.makedirs(os.path.join(d, "tools/round-46"), exist_ok=True)
    shutil.copyfile(os.path.join(d, "outside/payload.py"),
                    os.path.join(d, "tools/round-46/payload.py"))
    sh(d, "add", "-A")
    sh(d, "commit", "-q", "-m", "add a new file into the frozen directory")


cases = [try_case("rename-into-frozen-dir", ["tools/round-46/"], rename_in),
         try_case("copy-into-frozen-dir", ["tools/round-46/"], copy_in)]
out["cases"] = cases
print(json.dumps(out, indent=1))
