#!/usr/bin/env python3
"""Merge-blindness and -z attacks on the R45-C1 freeze-integrity arm (scratch fixtures only)."""
import hashlib, json, os, shutil, subprocess, sys

S = "/fast/scratch/hyaku/kaidoku-r45/R45W2CritC1Text"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
WORK = os.path.join(S, "work")
ENV = dict(os.environ, TMPDIR=WORK, HYAKU_SCRATCH=WORK)
ENV.pop("GIT_DIR", None)
COUNTER = os.path.join(LANE, "tools/round-45/c1-counter.py")
PREFLIGHT = os.path.join(S, "preflight.py")
CLAIMS = "plans/round-45-claims.md"

def git(d, *a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)

def sha(t):
    return hashlib.sha256(t.encode()).hexdigest()

d = os.path.join(S, "fix-merge")
if os.path.isdir(d):
    shutil.rmtree(d)
shutil.copytree(os.path.join(S, "tree"), d, symlinks=True)
git(d, "init", "-q", "-b", "main")
git(d, "config", "user.email", "w2@crit")
git(d, "config", "user.name", "w2 crit")
git(d, "add", "-A")
git(d, "commit", "-q", "-m", "freeze")
assert os.path.realpath(git(d, "rev-parse", "--show-toplevel").stdout.strip()) == os.path.realpath(d)
F0 = git(d, "rev-parse", "HEAD").stdout.strip()

git(d, "checkout", "-q", "-b", "side")
open(os.path.join(d, "side.txt"), "w").write("side\n")
git(d, "add", "-A"); git(d, "commit", "-q", "-m", "side work")
git(d, "checkout", "-q", "main")
open(os.path.join(d, "main.txt"), "w").write("main\n")
git(d, "add", "-A"); git(d, "commit", "-q", "-m", "main work")

m = git(d, "merge", "--no-ff", "--no-commit", "side")
# the frozen path is edited in the merge RESOLUTION, not in either parent's own commit
with open(os.path.join(d, CLAIMS), "a") as fh:
    fh.write("merge-resolution edit of a frozen path\n")
git(d, "add", "-A")
c = git(d, "commit", "-q", "-m", "merge side: resolution touches the frozen claims file")
M = git(d, "rev-parse", "HEAD").stdout.strip()
parents = git(d, "rev-list", "--parents", "-n1", M).stdout.split()

out = os.path.join(S, "c1-T9-merge.json")
p = subprocess.run([sys.executable, "-I", "-B", COUNTER, "--root", d, "--freeze", F0,
                    "--rev", M, "--json-out", out], capture_output=True, text=True, env=ENV)
rec = json.load(open(out))
plain = git(d, "log", "--name-only", "--format=", f"{F0}..{M}", "--", CLAIMS)
names = git(d, "log", "-m", "--diff-merges=first-parent", "--name-status", "--format=%x00%H",
            f"{F0}..{M}", "--", CLAIMS)
pf = subprocess.run([sys.executable, "-I", "-B", PREFLIGHT, "--root", d, "--freeze", F0,
                     "--rev", M, "--pathspec", CLAIMS, "--freeze-path", CLAIMS],
                    capture_output=True, text=True, env=ENV)
print(json.dumps({
    "T9-merge-resolution-touch": {
        "merge_commit": M, "parents": parents,
        "frozen_path_changed_by_plain_git_log": bool(plain.stdout.strip()),
        "frozen_path_changed_by_first_parent_log": CLAIMS in names.stdout,
        "c1_counter": {"exit": p.returncode, "met_target": rec.get("met_target"),
                       "frozen_path_changed": rec.get("frozen_path_changed"),
                       "failing": rec.get("failing"), "sha256": sha(p.stdout)},
        "preflight": {"exit": pf.returncode, "stdout_sha256": sha(pf.stdout),
                      "receipt": json.loads(pf.stdout) if pf.stdout.strip() else {}},
    }
}, sort_keys=True))

# The interpreter's own commit-arm invocation, grepped for -z.
src = open(PREFLIGHT).read()
line = [l.strip() for l in src.splitlines() if "--name-status" in l]
print(json.dumps({"commit_arm_invocation": line,
                  "uses_z": any(" -z" in l or "-z\"" in l for l in line)}))
