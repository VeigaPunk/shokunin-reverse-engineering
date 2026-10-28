#!/usr/bin/env python3
"""P3: the scope-shrink attack — does a measured revision get to shrink its own frozen set?

`frozen_set` reads the claims file at ONE revision (`rev`) in the freeze bytes and at
BOTH ends in the current HEAD bytes (F5, `332f4884`). If a commit inside freeze..rev
rewrites `## Frozen paths` to drop an entry, the arm never looks at the dropped entry.

Freeze bytes (3182047): `frozen_set(root, tip, ...)` only -> the tampered tool is clean.
HEAD bytes:            base ∪ tip -> the dropped entry is still in scope -> exit 2.

This is a SOUNDNESS probe of the instrument the plan froze, not of a mutant.
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
           open(os.path.join(S, WHICH, "tools", "round-46", "gate.py"), "rb").read()).hexdigest()}
CLAIMS_FULL = ("# claims\n\n## Frozen paths (exact)\n\n- `plans/round-46-claims.md`\n"
               "- `tools/round-46/`\n\n## After\n\ntail\n")
# The survivable shrink: keep a DECOY entry that exists and is never touched, and
# drop the entry that names the tampered tool. The claims file itself must also be
# dropped (or the edit to it is itself a frozen-path touch), so the decoy must be
# the ONLY entry left.
CLAIMS_SHRUNK = ("# claims\n\n## Frozen paths (exact)\n\n- `corpus/SOURCES.md`\n"
                 "\n## After\n\ntail\n")


def sh(d, *a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)


d = tempfile.mkdtemp(dir=S, prefix="p3-")
try:
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    for k, v in (("user.email", "p3@r46"), ("user.name", "p3")):
        subprocess.run(["git", "-C", d, "config", k, v], check=True)
    assert sh(d, "rev-parse", "--show-toplevel").stdout.strip() == d
    for rel, text in (("plans/round-46-claims.md", CLAIMS_FULL),
                      ("tools/round-46/counter.py", "HONEST\n"),
                      ("corpus/SOURCES.md", "decoy\n"),
                      ("SKILL.md", "# s\n")):
        full = os.path.join(d, rel)
        os.makedirs(os.path.dirname(full) or d, exist_ok=True)
        open(full, "w").write(text)
    sh(d, "add", "-A")
    sh(d, "commit", "-q", "-m", "base")
    freeze = sh(d, "rev-parse", "HEAD").stdout.strip()
    # ONE commit: tamper the tool AND shrink the frozen section that names it.
    open(os.path.join(d, "tools/round-46/counter.py"), "w").write("TAMPERED\n")
    open(os.path.join(d, "plans/round-46-claims.md"), "w").write(CLAIMS_SHRUNK)
    sh(d, "add", "-A")
    sh(d, "commit", "-q", "-m", "tamper the counter and delete its frozen entry")
    rev = sh(d, "rev-parse", "HEAD").stdout.strip()

    code, rec = gate.freeze_state(d, freeze, rev)
    out.update({
        "attack": "one commit tampers tools/round-46/counter.py AND rewrites `## Frozen paths` "
                  "to a single untouched decoy entry (`corpus/SOURCES.md`), dropping both "
                  "`plans/round-46-claims.md` and `tools/round-46/`",
        "frozen_derived": rec.get("frozen_derived"),
        "frozen_from": rec.get("frozen_from"),
        "touched": rec.get("touched"), "blob_changed": rec.get("blob_changed"),
        "frozen_path_changed": rec.get("frozen_path_changed"),
        "exit": code, "reason": rec.get("reason"),
        "counter_at_rev": sh(d, "show", f"{rev}:tools/round-46/counter.py").stdout.strip(),
        "claims_at_rev_frozen_section": sh(d, "show",
                                           f"{rev}:plans/round-46-claims.md").stdout.strip(),
    })
finally:
    shutil.rmtree(d, ignore_errors=True)

print(json.dumps(out, indent=1))
