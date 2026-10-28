#!/usr/bin/env python3
"""P5b: m5 (out_path passes the path through) end-to-end through the real CLI.

The guard's job (R45-CL22) is to refuse a `--json-out` that would overwrite the
graded surface. Here the counter is run against a FIXTURE repo whose root is the
fixture, so the write lands inside scratch, never in the lane, and the graded
surface is a fixture-owned SKILL.md.

base  : --json-out <fixture>/SKILL.md  -> exit 2, SKILL.md bytes unchanged
mutant: --json-out <fixture>/SKILL.md  -> the receipt overwrites SKILL.md
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
TOOLS = os.path.join(S, WHICH, "tools", "round-46")
CLAIMS = ("# claims\n\n## Frozen paths (exact)\n\n- `tools/round-46/`\n\n## After\n\ntail\n")
SKILL = "# SKILL\n\n## Queue-drain craft (fixture) \n\n- **1. Plain rule.** body\n"

out = {"mutant_dir": WHICH,
       "gate_sha256": hashlib.sha256(
           open(os.path.join(TOOLS, "gate.py"), "rb").read()).hexdigest(), "cases": []}


def sh(d, *a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)


d = tempfile.mkdtemp(dir=S, prefix="p5b-")
subprocess.run(["git", "-C", d, "init", "-q"], check=True)
for k, v in (("user.email", "p5b@r46"), ("user.name", "p5b")):
    subprocess.run(["git", "-C", d, "config", k, v], check=True)
assert sh(d, "rev-parse", "--show-toplevel").stdout.strip() == d, "toplevel mismatch"
for rel, text in (("plans/round-46-claims.md", CLAIMS), ("SKILL.md", SKILL),
                  ("tools/round-46/keep.py", "k\n")):
    full = os.path.join(d, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(text)
sh(d, "add", "-A")
sh(d, "commit", "-q", "-m", "base")
rev = sh(d, "rev-parse", "HEAD").stdout.strip()
skill_path = os.path.join(d, "SKILL.md")
before = hashlib.sha256(open(skill_path, "rb").read()).hexdigest()

for label, target in (("inside-graded-surface", skill_path),
                      ("claims-frozen-file", os.path.join(d, "plans/round-46-claims.md"))):
    pre = hashlib.sha256(open(target, "rb").read()).hexdigest()
    r = subprocess.run([sys.executable, "-I", "-B", os.path.join(TOOLS, "attest.py"),
                        "--root", d, "--freeze", rev, "--rev", rev,
                        "--no-battery", "--json-out", target],
                       capture_output=True, text=True,
                       env=dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S))
    post = hashlib.sha256(open(target, "rb").read()).hexdigest()
    out["cases"].append({"case": label, "target_rel": os.path.relpath(target, d),
                         "exit": r.returncode, "stdout": r.stdout.strip()[:200],
                         "stderr_tail": r.stderr.strip().splitlines()[-1:] if r.stderr else [],
                         "target_sha256_before": pre, "target_sha256_after": post,
                         "overwritten": pre != post})
    # restore the fixture target for the next case
    if pre != post:
        open(target, "w").write(SKILL if target == skill_path else CLAIMS)

out["fixture_skill_sha256"] = before
shutil.rmtree(d, ignore_errors=True)
print(json.dumps(out, indent=1))
