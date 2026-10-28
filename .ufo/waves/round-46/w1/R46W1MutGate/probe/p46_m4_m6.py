#!/usr/bin/env python3
"""P4 (m4: `dirty` replaces rather than unions) and P6 (m6: /tmp scratch allowed).

Both call the gate functions directly: neither has a caller in the frozen counters
(`grep -n 'gate.dirty' tools/round-46/*.py` -> no hits), so the selftests cannot
reach either arm even in principle.
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

# --- P4: dirty() over two pathspecs, one file dirty under each -------------------
d = tempfile.mkdtemp(dir=S, prefix="p4-")
g = lambda *a: subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)
subprocess.run(["git", "-C", d, "init", "-q"], check=True)
subprocess.run(["git", "-C", d, "config", "user.email", "p4@r46"], check=True)
subprocess.run(["git", "-C", d, "config", "user.name", "p4"], check=True)
assert g("rev-parse", "--show-toplevel").stdout.strip() == d
for p in ("tools/round-46/a.py", "tools/round-46/b.py"):
    full = os.path.join(d, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write("v0\n")
g("add", "-A")
g("commit", "-q", "-m", "base")
# dirty under BOTH pathspecs
open(os.path.join(d, "tools/round-46/a.py"), "w").write("dirty-a\n")
open(os.path.join(d, "tools/round-46/b.py"), "w").write("dirty-b\n")
out["p4_dirty"] = {
    "union_two_pathspecs": gate.dirty(d, ["tools/round-46/a.py", "tools/round-46/b.py"]),
    "single_pathspec_a": gate.dirty(d, ["tools/round-46/a.py"]),
    "single_pathspec_b": gate.dirty(d, ["tools/round-46/b.py"]),
    "no_pathspec": gate.dirty(d, []),
}
shutil.rmtree(d, ignore_errors=True)

# --- P6: scratch() under a /tmp root ---------------------------------------------
saved = {k: os.environ.get(k) for k in ("HYAKU_SCRATCH", "TMPDIR")}
try:
    os.environ.pop("HYAKU_SCRATCH", None)
    os.environ["TMPDIR"] = "/tmp"
    made, err = gate.scratch("p6-")
    out["p6_tmp_scratch"] = {"dir": made, "err": err,
                            "under_tmp": bool(made) and str(made).startswith("/tmp")}
    if made:
        shutil.rmtree(made, ignore_errors=True)
    os.environ["TMPDIR"] = "/var/tmp"
    made, err = gate.scratch("p6v-")
    out["p6_vartmp_scratch"] = {"dir": made, "err": err}
    if made:
        shutil.rmtree(made, ignore_errors=True)
    os.environ.pop("TMPDIR", None)
    made, err = gate.scratch("p6n-")
    out["p6_no_root_scratch"] = {"dir": made, "err": err}
    if made:
        shutil.rmtree(made, ignore_errors=True)
finally:
    for k, v in saved.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v
    os.environ.setdefault("TMPDIR", S)

print(json.dumps(out, indent=1))
