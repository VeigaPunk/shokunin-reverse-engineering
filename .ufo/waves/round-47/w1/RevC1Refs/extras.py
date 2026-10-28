#!/usr/bin/env python3
"""Clause-8 extras: (a) every selectored citation made contentless, (b) the dirty guard.

Reproduce with:  R47_PIN=<lane rev> python3 extras.py
Fixtures are `git archive <PIN>` copies of the lane; only SKILL.md's block 24 is varied.
"""
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import tarfile
import time

S = "/fast/scratch/hyaku/kaidoku-r47/RevC1Refs"
os.makedirs(os.path.join(S, "receipts"), exist_ok=True)
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
MARKER = "<!-- exactness-table v3 -->"
PIN = os.environ.get("R47_PIN") or subprocess.run(
    ["git", "-C", LANE, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()


def blob(p):
    return subprocess.run(["git", "-C", LANE, "show", f"{PIN}:{p}"],
                          capture_output=True, text=True).stdout


SKILL = blob("SKILL.md")


def span(skill):
    i = skill.index(MARKER)
    return skill.rindex("- **", 0, i), skill.index("\n## ", i)


def contentless(skill):
    a, b = span(skill)
    block = re.sub(r"corpus/lessons/round-46\.md:\d+(?:-\d+)?",
                   "corpus/lessons/round-46.md:1-1", skill[a:b])
    block = re.sub(r"plans/round-47-claims\.md:\d+(?:-\d+)?",
                   "plans/round-47-claims.md:1-1", block)
    return skill[:a] + block + skill[b:]


def fixture(name, skill):
    d = os.path.join(S, "fx-" + name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    tar = subprocess.run(["git", "-C", LANE, "archive", PIN], capture_output=True)
    assert tar.returncode == 0
    with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
        tf.extractall(d, filter=lambda m, p: None if (m.issym() or m.islnk()) else m)
    open(os.path.join(d, "SKILL.md"), "w").write(skill)
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    for k, v in (("user.email", "fx@round47"), ("user.name", "round47 fixture")):
        subprocess.run(["git", "-C", d, "config", k, v], check=True)
    top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "commit", "-q", "-m", "fixture"], check=True)
    return d, subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                             capture_output=True, text=True).stdout.strip()


def run(name, fixture_dir, rev, interp, battery, note):
    cmd = ["python3", "-I", "-B", interp, "--root", fixture_dir, "--freeze", rev,
           "--rev", rev] + ([] if battery else ["--no-battery"])
    r = subprocess.run(cmd, capture_output=True, text=True,
                       env=dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S), cwd=S)
    out = {"variant": name, "lane_pin": PIN, "fixture": fixture_dir, "fixture_rev": rev,
           "cmd": " ".join(cmd), "note": note, "exit": r.returncode,
           "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
           "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    try:
        b = json.loads(r.stdout)
        out.update({k: b.get(k) for k in
                    ("failing", "met_target", "refs", "unresolved_citations", "reason")})
        out["battery"] = {k: v for k, v in (b.get("battery") or {}).items()
                          if k != "fixtures"}
    except Exception:
        out["stdout_head"] = r.stdout[:300]
        out["stderr_head"] = r.stderr[:300]
    open(os.path.join(S, "receipts", name + ".json"), "w").write(
        json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(f"{name:24s} exit={out['exit']} refs={out.get('refs')} "
          f"battery={out.get('battery')} failing={out.get('failing')} "
          f"reason={out.get('reason')}")
    return out


d, rev = fixture("x1_contentless", contentless(SKILL))
run("x1_all_contentless", d, rev, os.path.join(d, "tools/round-47/exact.py"), True,
    "every selectored citation in block 24 rewritten to <file>:1-1")

d, rev = fixture("x2_dirty", SKILL)
interp = os.path.join(d, "tools/round-47/exact.py")
run("x2_clean", d, rev, interp, False, "control")
open(interp, "a").write("\n# worktree edit after the commit\n")
run("x2_dirty_worktree", d, rev, interp, False,
    "worktree copy of the counter edited after the commit")
