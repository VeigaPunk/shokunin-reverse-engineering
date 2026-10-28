#!/usr/bin/env python3
"""Executed-vs-graded split: a dirty worktree gate.py changes the freeze arm the counter
runs while clause 7 still grades the committed literal."""
import hashlib, json, os, shutil, subprocess, sys, time

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r47/CritC1Sizing"
D = os.path.join(S, "fx-gatesplit")
shutil.rmtree(D, ignore_errors=True)
os.makedirs(D)


def git(*a):
    return subprocess.run(["git", "-C", D, *a], capture_output=True, text=True)


git("init", "-q")
git("config", "user.email", "fx@round47")
git("config", "user.name", "round47 fixture")
assert git("rev-parse", "--show-toplevel").stdout.strip() == os.path.realpath(D)

FILES = ["SKILL.md", "plans/round-47-claims.md", "tools/round-47/exact.py",
         "tools/round-46/gate.py", "corpus/lessons/round-46.md",
         "corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md"]
for p in FILES:
    full = os.path.join(D, p)
    os.makedirs(os.path.dirname(full) or D, exist_ok=True)
    shutil.copyfile(os.path.join(LANE, p), full)
git("add", "-A")
git("commit", "-q", "-m", "base")
c1 = git("rev-parse", "HEAD").stdout.strip()

with open(os.path.join(D, "plans/round-47-claims.md"), "a") as fh:
    fh.write("\ntamper line\n")
git("commit", "-qam", "tamper")
c2 = git("rev-parse", "HEAD").stdout.strip()
git("checkout", c1, "--", "plans/round-47-claims.md")
git("commit", "-qam", "restore")
c3 = git("rev-parse", "HEAD").stdout.strip()
print("c1", c1[:8], "c2", c2[:8], "c3", c3[:8])

NEUTER = ("def history_touched(root, base, tip, paths):\n"
          "    return [], None\n")
gpath = os.path.join(D, "tools/round-46/gate.py")
REAL_GATE = open(gpath).read()
start = REAL_GATE.index("def history_touched")
end = REAL_GATE.index("def blob_changed")
NEUTERED = REAL_GATE[:start] + NEUTER + "\n\n" + REAL_GATE[end:]

RUNS = []


def run(label, counter, rev):
    cmd = [sys.executable, "-I", "-B", counter, "--root", D, "--freeze", c1, "--rev", rev]
    t0 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    r = subprocess.run(cmd, capture_output=True, text=True,
                       env=dict(os.environ, HYAKU_SCRATCH=S, TMPDIR=S))
    rec = {"run": label, "cmd": " ".join(cmd), "exit": r.returncode,
           "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(), "t0": t0}
    try:
        j = json.loads(r.stdout)
        rec.update(reason=j.get("reason"), touched=j.get("touched"),
                   restored=j.get("restored"), blob_changed=j.get("blob_changed"),
                   frozen_path_changed=j.get("frozen_path_changed"),
                   dirty=j.get("dirty"), met_target=j.get("met_target"),
                   failing=j.get("failing"))
    except Exception:
        rec["tail"] = (r.stdout + r.stderr)[-1500:]
    RUNS.append(rec)
    print(label, "exit", r.returncode, "reason", rec.get("reason"),
          "touched", rec.get("touched"), "restored", rec.get("restored"),
          "dirty", rec.get("dirty"))
    return rec


# A: lane counter, clean worktree -> the tamper+restore is seen
run("clean-lane", os.path.join(LANE, "tools/round-47/exact.py"), c3)

# B: worktree gate.py neutered (uncommitted), counter executed from the fixture
open(gpath, "w").write(NEUTERED)
r = run("dirty-gate", os.path.join(D, "tools/round-47/exact.py"), c3)
print("   committed gate has ORDER once:",
      git("show", f"{c3}:tools/round-46/gate.py").stdout.count('"-m", "--diff-merges=first-parent"'))

# C: control, worktree gate.py restored
open(gpath, "w").write(REAL_GATE)
run("restored-gate", os.path.join(D, "tools/round-47/exact.py"), c3)

open(os.path.join(S, "gatesplit.json"), "w").write(json.dumps(RUNS, indent=1))
