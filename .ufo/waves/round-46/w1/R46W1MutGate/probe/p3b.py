#!/usr/bin/env python3
"""P3b (m3: hard-coded frozen list): two fixtures that separate it from the claims file.

Case A — the claims file names a THIRD frozen path; one commit touches only that path.
         Pristine derives three entries and exits 2; the mutant never reads the file, so the
         third entry is out of scope and it reads clean.
Case B — the claims file is DELETED in freeze..rev (so it cannot be derived at all).
         Pristine exits 2 `claims file absent at rev`; the mutant scores the artefact anyway.
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

out = {"dir": WHICH,
       "gate_sha256": hashlib.sha256(
           open(os.path.join(S, WHICH, "tools", "round-46", "gate.py"), "rb").read()).hexdigest(),
       "cases": []}


def sh(d, *a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)


def repo(claims, files):
    d = tempfile.mkdtemp(dir=S, prefix="p3b-")
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    for k, v in (("user.email", "p3b@r46"), ("user.name", "p3b")):
        subprocess.run(["git", "-C", d, "config", k, v], check=True)
    assert sh(d, "rev-parse", "--show-toplevel").stdout.strip() == d, "toplevel mismatch"
    payload = dict(files)
    if claims is not None:
        payload["plans/round-46-claims.md"] = claims
    for rel, text in payload.items():
        full = os.path.join(d, rel)
        os.makedirs(os.path.dirname(full) or d, exist_ok=True)
        open(full, "w").write(text)
    sh(d, "add", "-A")
    sh(d, "commit", "-q", "-m", "base")
    return d, sh(d, "rev-parse", "HEAD").stdout.strip()


# ---- Case A ---------------------------------------------------------------------
CLAIMS3 = ("# claims\n\n## Frozen paths (exact)\n\n- `plans/round-46-claims.md`\n"
           "- `tools/round-46/`\n- `evidence/C1.json`\n\n## After\n\ntail\n")
d, freeze = repo(CLAIMS3, {"tools/round-46/counter.py": "HONEST\n",
                           "evidence/C1.json": "C1-HONEST\n"})
try:
    open(os.path.join(d, "evidence/C1.json"), "w").write("C1-TAMPERED\n")
    sh(d, "commit", "-q", "-am", "touch ONLY the third frozen entry")
    rev = sh(d, "rev-parse", "HEAD").stdout.strip()
    code, rec = gate.freeze_state(d, freeze, rev)
    out["cases"].append({"case": "third-frozen-entry-touched", "exit": code,
                         "frozen_derived": rec.get("frozen_derived"),
                         "touched": rec.get("touched"),
                         "blob_changed": rec.get("blob_changed"),
                         "frozen_path_changed": rec.get("frozen_path_changed"),
                         "reason": rec.get("reason"),
                         "evidence_at_rev": sh(d, "show", f"{rev}:evidence/C1.json")
                         .stdout.strip()})
finally:
    shutil.rmtree(d, ignore_errors=True)

# ---- Case B ---------------------------------------------------------------------
d, freeze = repo("# claims\n\n## Frozen paths (exact)\n\n- `plans/round-46-claims.md`\n"
                 "- `tools/round-46/`\n\n## After\n\ntail\n",
                 {"tools/round-46/counter.py": "HONEST\n", "SKILL.md": "# s\n"})
try:
    open(os.path.join(d, "tools/round-46/counter.py"), "w").write("TAMPERED\n")
    sh(d, "rm", "-q", "plans/round-46-claims.md")
    sh(d, "commit", "-q", "-am", "tamper the tool and delete the claims file")
    rev = sh(d, "rev-parse", "HEAD").stdout.strip()
    code, rec = gate.freeze_state(d, freeze, rev)
    out["cases"].append({"case": "claims-file-deleted-at-rev", "exit": code,
                         "frozen_derived": rec.get("frozen_derived"),
                         "touched": rec.get("touched"),
                         "blob_changed": rec.get("blob_changed"),
                         "frozen_path_changed": rec.get("frozen_path_changed"),
                         "reason": rec.get("reason"),
                         "counter_at_rev": sh(d, "show", f"{rev}:tools/round-46/counter.py")
                         .stdout.strip()})
finally:
    shutil.rmtree(d, ignore_errors=True)

print(json.dumps(out, indent=1))
