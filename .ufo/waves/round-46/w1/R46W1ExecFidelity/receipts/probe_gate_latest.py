#!/usr/bin/env python3
"""Probe: is the claims file self-protecting in gate.freeze_state?

Builds fixture repos (temporary, under HYAKU_SCRATCH) and calls the FROZEN
gate.freeze_state.  No lane write, no /tmp write.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

FROZEN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "headlatest")
sys.path.insert(0, FROZEN)
import gate  # noqa: E402

BASE = os.environ["HYAKU_SCRATCH"]

CLAIMS_FULL = (
    "# claims\n\nfiller\n\n## Frozen paths (exact)\n\n"
    "- `plans/round-46-claims.md`\n- `tools/round-46/`\n\n## After\n\ntail\n")


def git(d, *args):
    r = subprocess.run(["git", "-C", d, *args], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return r.stdout


def repo():
    d = tempfile.mkdtemp(dir=BASE, prefix="probe-")
    assert d.startswith(BASE)
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True).stdout.strip()
    assert top == d, (top, d)
    git(d, "config", "user.email", "probe@round46")
    git(d, "config", "user.name", "round46 probe")
    return d


def put(d, rel, text):
    full = os.path.join(d, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as fh:
        fh.write(text)


def commit(d, msg):
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", msg)
    return git(d, "rev-parse", "HEAD").strip()


def show(tag, code, rec):
    print(json.dumps({"probe": tag, "exit": code,
                      "frozen_derived": rec.get("frozen_derived"),
                      "frozen_path_changed": rec.get("frozen_path_changed"),
                      "reason": rec.get("reason")}, sort_keys=True))


def scenario(name, rev_claims, rev_tool, rev_skill="skill\n"):
    d = repo()
    try:
        put(d, "plans/round-46-claims.md", CLAIMS_FULL)
        put(d, "tools/round-46/attest.py", "tool v1\n")
        put(d, "tools/round-46/gate.py", "gate v1\n")
        put(d, "SKILL.md", "skill\n")
        freeze = commit(d, "freeze")
        put(d, "plans/round-46-claims.md", rev_claims)
        put(d, "tools/round-46/attest.py", rev_tool)
        put(d, "SKILL.md", rev_skill)
        rev = commit(d, "rev")
        code, rec = gate.freeze_state(d, freeze, rev, "plans/round-46-claims.md")
        show(name, code, rec)
        return code
    finally:
        shutil.rmtree(d, ignore_errors=True)


ONLY_TOOLS = "# claims\n\nEDITED CLAUSE TEXT\n\n## Frozen paths (exact)\n\n- `tools/round-46/`\n"
ONLY_CLAIMS = "# claims\n\n## Frozen paths (exact)\n\n- `plans/round-46-claims.md`\n"
FULL_EDITED = CLAIMS_FULL.replace("filler", "filler EDITED")

# 1 control: frozen tool bytes changed, claims unchanged -> must be caught (2)
scenario("tool-changed-claims-intact", CLAIMS_FULL, "tool v2\n")
# 2 control: claims body edited, tool unchanged, both entries kept -> must be caught (2)
scenario("claims-edited-entries-intact", FULL_EDITED, "tool v1\n")
# 3 attack: claims edited (clause text changed) AND its own frozen-path line dropped
scenario("claims-edited-self-line-dropped", ONLY_TOOLS, "tool v1\n")
# 4 attack: claims at rev lists only itself, so a tool edit is outside the derived set
scenario("tool-changed-and-tools-line-dropped", ONLY_CLAIMS, "tool v2\n")
