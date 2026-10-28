#!/usr/bin/env python3
"""Round 3: scope-file attacks (count vs set, existence never checked)."""
import hashlib
import json
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r45/R45W2C2Rerun"
COUNTER = os.path.join(LANE, "tools/round-45/c2-counter.py")
SCOPE_REL = "tools/round-45/registry-scope.json"
CLAIMS_REL = "plans/round-45-claims.md"
BASE_SCOPE = ["tools/round-44/c1-counter.py", "tools/round-44/c1-run.sh",
              "tools/round-44/c2-counter.py", "tools/round-45/frozen-path-preflight.py",
              "tools/round-45/c1-counter.py", "tools/round-45/c2-counter.py"]


def run(args, cwd=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


def git(d, *a):
    return run(["git", "-C", d, *a])


def fixture(name, scope_paths):
    d = os.path.realpath(os.path.join(S, "fx3-" + name))
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    assert git(d, "init", "-q").returncode == 0
    assert os.path.realpath(git(d, "rev-parse", "--show-toplevel").stdout.strip()) == d
    git(d, "config", "user.email", "w2c2@rerun")
    git(d, "config", "user.name", "w2c2 rerun")
    open(os.path.join(d, "SKILL.md"), "w").write(open(os.path.join(LANE, "SKILL.md")).read())
    os.makedirs(os.path.join(d, "tools/round-45"), exist_ok=True)
    open(os.path.join(d, SCOPE_REL), "w").write(
        json.dumps({"scope": "test", "paths": scope_paths}, indent=1))
    os.makedirs(os.path.join(d, "plans"), exist_ok=True)
    open(os.path.join(d, CLAIMS_REL), "w").write(
        open(os.path.join(LANE, CLAIMS_REL)).read())
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "freeze")
    return d, git(d, "rev-parse", "HEAD").stdout.strip()


def score(d, f1, tag):
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "mutate")
    f2 = git(d, "rev-parse", "HEAD").stdout.strip()
    out = os.path.join(S, "score3-" + tag + ".json")
    r = run([sys.executable, "-I", "-B", COUNTER, "--root", d, "--freeze", f1,
             "--rev", f2, "--json-out", out], cwd=S)
    rec = json.load(open(out)) if os.path.exists(out) else {}
    return {"tag": tag, "exit": r.returncode,
            "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
            "registered": rec.get("registered"), "unregistered": rec.get("unregistered"),
            "thin": rec.get("thin"), "scope_size": rec.get("scope_size"),
            "failing": rec.get("failing"), "reason": rec.get("reason"),
            "verdict": rec.get("verdict"), "stderr": r.stderr.strip()[:200]}


def drop_row(d, path):
    p = os.path.join(d, "SKILL.md")
    lines = open(p).read().splitlines(True)
    keep = [l for l in lines if not l.startswith("| `" + path + "` |")]
    assert len(keep) == len(lines) - 1, "row not found: " + path
    open(p, "w").writelines(keep)


def add_row(d, path):
    p = os.path.join(d, "SKILL.md")
    text = open(p).read()
    row = ("| `" + path + "` | gate \u2014 probe | `0` met; `1` not met; `2` unevaluable | "
           "none | x | y | kaidoku |\n")
    lines = text.splitlines(True)
    anchor = next(i for i, l in enumerate(lines) if l.startswith("| `tools/round-45/c2-counter.py` |"))
    lines.insert(anchor + 1, row)
    open(p, "w").writelines(lines)


results = []

# N: scope has 6 entries but one path is duplicated and one instrument is unlisted.
d, f1 = fixture("N-dup-scope", [BASE_SCOPE[0], BASE_SCOPE[0], BASE_SCOPE[1], BASE_SCOPE[2],
                                BASE_SCOPE[3], BASE_SCOPE[4]])
drop_row(d, "tools/round-45/c2-counter.py")   # not in scope, row removed
results.append(score(d, f1, "N-dup-scope-missing-row"))

# O: scope names a path that does not exist in the tree; a row names it.
d, f1 = fixture("O-ghost-instrument", BASE_SCOPE[:5] + ["tools/round-45/ghost-instrument.py"])
add_row(d, "tools/round-45/ghost-instrument.py")
results.append(score(d, f1, "O-ghost-instrument"))

# P: control - same fixture as O but the row is absent -> unregistered.
d, f1 = fixture("P-ghost-norow", BASE_SCOPE[:5] + ["tools/round-45/ghost-instrument.py"])
results.append(score(d, f1, "P-ghost-no-row"))

print(json.dumps(results, indent=1, sort_keys=True))
