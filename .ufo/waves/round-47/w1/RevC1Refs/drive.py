#!/usr/bin/env python3
"""Clause-8 attack driver: build a one-commit fixture repo, swap block 24's Refs line,
run the frozen counter against it, record exit code + stdout sha256."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r47/RevC1Refs"
FILES = ["SKILL.md", "plans/round-47-claims.md", "tools/round-47/exact.py",
         "tools/round-46/gate.py", "corpus/lessons/round-46.md",
         "corpus/lessons/round-45.md", "corpus/lessons/.gitkeep"]
MARKER = "<!-- exactness-table v3 -->"


def blob(path, rev="HEAD"):
    return subprocess.run(["git", "-C", LANE, "show", f"{rev}:{path}"],
                          capture_output=True, text=True).stdout


def base_files(rev="HEAD"):
    return {p: blob(p, rev) for p in FILES}


def split_block(skill):
    i = skill.index(MARKER)
    start = skill.rindex("- **", 0, i)
    end = skill.index("\n## ", i)
    return start, end


def swap_refs(skill, refs, extra=None):
    """Replace the Refs line of the marked block with `refs`; optionally inject text."""
    if refs is None:
        return skill
    start, end = split_block(skill)
    block = skill[start:end]
    lines = block.splitlines()
    out = []
    for line in lines:
        if line.strip().startswith("Refs:"):
            out.append("  Refs: " + refs)
        else:
            out.append(line)
    block = "\n".join(out)
    if extra is not None:
        block = extra(block)
    return skill[:start] + block + skill[end:]


def make_repo(name, skill, extra=None):
    d = os.path.join(S, "fx-" + name)
    shutil.rmtree(d, ignore_errors=True)
    files = base_files()
    files["SKILL.md"] = skill
    files.update(extra or {})
    for p, text in files.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full) or d, exist_ok=True)
        with open(full, "w") as fh:
            fh.write(text)
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    for k, v in (("user.email", "fx@round47"), ("user.name", "round47 fixture")):
        subprocess.run(["git", "-C", d, "config", k, v], check=True)
    top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "commit", "-q", "-m", "fixture"], check=True)
    rev = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    return d, rev


def run(name, skill, interpreter=None, top=None, extra=None):
    d, rev = make_repo(name, skill, extra)
    interp = interpreter or os.path.join(d, "tools/round-47/exact.py")
    cmd = ["python3", "-I", "-B", interp, "--root", d, "--freeze", rev, "--rev", rev]
    env = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S)
    r = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=S)
    rec = {"variant": name, "fixture": d, "rev": rev,
           "cmd": " ".join(cmd), "exit": r.returncode,
           "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
           "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "interpreter": interp,
           "interpreter_sha256": hashlib.sha256(open(interp, "rb").read()).hexdigest()}
    try:
        body = json.loads(r.stdout)
        rec["failing"] = body.get("failing")
        rec["met_target"] = body.get("met_target")
        rec["refs"] = body.get("refs")
        rec["cited"] = body.get("cited")
        rec["unresolved"] = body.get("unresolved_citations")
        rec["battery"] = {k: v for k, v in (body.get("battery") or {}).items()
                          if k != "fixtures"}
        rec["reason"] = body.get("reason")
        rec["interpreter_sha256_expected"] = body.get("interpreter_sha256_expected")
    except Exception:
        rec["stdout_head"] = r.stdout[:600]
        rec["stderr_head"] = r.stderr[:600]
    path = os.path.join(S, "receipts", name + ".json")
    with open(path, "w") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps({k: rec.get(k) for k in
                      ("variant", "exit", "met_target", "failing", "refs", "battery",
                       "reason", "interpreter_sha256")}, indent=1))
    return rec


if __name__ == "__main__":
    which = sys.argv[1]
    skill = base_files()["SKILL.md"]
    print("baseline file ready", which)
