#!/usr/bin/env python3
"""Arm-deletion and dirty-false-clean attacks on R45-C1's interpreter, scratch fixtures only."""
import hashlib, json, os, shutil, subprocess, sys

S = "/fast/scratch/hyaku/kaidoku-r45/R45W2CritC1Text"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
COUNTER = os.path.join(LANE, "tools/round-45/c1-counter.py")
PREFLIGHT_SRC = subprocess.run(["git", "-C", LANE, "show", "HEAD:tools/round-45/frozen-path-preflight.py"],
                               capture_output=True, text=True).stdout
WORK = os.path.join(S, "work")
os.makedirs(WORK, exist_ok=True)
ENV = dict(os.environ, TMPDIR=WORK, HYAKU_SCRATCH=WORK)
ENV.pop("GIT_DIR", None)

def git(d, *a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)

def sha(t):
    return hashlib.sha256(t.encode()).hexdigest()

def mkfix(name, mutate_preflight=None, extra=None):
    d = os.path.join(S, "fix-" + name)
    if os.path.isdir(d):
        shutil.rmtree(d)
    shutil.copytree(os.path.join(S, "tree"), d, symlinks=True)
    body = PREFLIGHT_SRC
    if mutate_preflight:
        body = mutate_preflight(body)
        assert body != PREFLIGHT_SRC, "mutation did not apply"
    open(os.path.join(d, "tools/round-45/frozen-path-preflight.py"), "w").write(body)
    if extra:
        extra(d)
    git(d, "init", "-q")
    git(d, "config", "user.email", "w2@crit")
    git(d, "config", "user.name", "w2 crit")
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "freeze")
    top = os.path.realpath(git(d, "rev-parse", "--show-toplevel").stdout.strip())
    assert top == os.path.realpath(d), (top, d)
    return d, git(d, "rev-parse", "HEAD").stdout.strip()

def run_preflight(d, tag, args):
    out = os.path.join(S, "pre-%s.json" % tag)
    p = subprocess.run([sys.executable, "-I", "-B",
                        os.path.join(d, "tools/round-45/frozen-path-preflight.py")] + args +
                       ["--json-out", out], capture_output=True, text=True, env=ENV, cwd=S)
    rec = json.load(open(out)) if os.path.exists(out) else {}
    return p.returncode, rec, sha(p.stdout), p.stdout.strip().splitlines()[-1:] if p.stdout.strip() else []

def run_counter(d, f, tag):
    out = os.path.join(S, "c1-%s.json" % tag)
    p = subprocess.run([sys.executable, "-I", "-B", COUNTER, "--root", d, "--freeze", f,
                        "--rev", f, "--json-out", out], capture_output=True, text=True, env=ENV, cwd=S)
    rec = json.load(open(out)) if os.path.exists(out) else {}
    return p.returncode, rec, sha(p.stdout)

def drop_restored(b):
    return b.replace("        elif any(t[\"path\"] == path for t in touched):\n"
                     "            restored.append(path)",
                     "        elif any(t[\"path\"] == path for t in touched):\n"
                     "            pass  # ARM DELETED: restored classification removed")

def drop_blob(b):
    return b.replace("    ok = not touched and not blob_changed and not restored and not dirty",
                     "    blob_changed = []  # ARM DELETED\n"
                     "    ok = not touched and not blob_changed and not restored and not dirty")

res = {}

for name, fn in (("drop-restored", drop_restored), ("drop-blob", drop_blob)):
    d, f0 = mkfix(name, fn)
    pc, prec, psha, tail = run_preflight(d, name, ["--selftest"])
    cc, crec, csha = run_counter(d, f0, name)
    res[name] = {"preflight_selftest": {"exit": pc, "tail": tail, "sha256": psha},
                 "c1_counter": {"exit": cc, "sha256": csha,
                                "met_target": crec.get("met_target"),
                                "preflight_selftest_field": crec.get("preflight_selftest"),
                                "failing": crec.get("failing")}}
    print(json.dumps({name: res[name]}, sort_keys=True))

# dirty false-clean: the A3-disclosed --dirty-pathspec scope replacement.
d = os.path.join(S, "fix-dirty")
if os.path.isdir(d):
    shutil.rmtree(d)
os.makedirs(d)
git(d, "init", "-q")
git(d, "config", "user.email", "w2@crit"); git(d, "config", "user.name", "w2 crit")
for rel, text in (("data/frozen.txt", "A\n"), ("other/keep.txt", "k\n")):
    os.makedirs(os.path.join(d, os.path.dirname(rel)), exist_ok=True)
    open(os.path.join(d, rel), "w").write(text)
git(d, "add", "-A"); git(d, "commit", "-q", "-m", "freeze")
f0 = git(d, "rev-parse", "HEAD").stdout.strip()
open(os.path.join(d, "data/frozen.txt"), "w").write("B dirty\n")  # worktree dirty, frozen path
base = ["--root", d, "--freeze", f0, "--rev", f0, "--pathspec", "data/", "--freeze-path", "data"]
c1, r1, s1, t1 = run_preflight(d, "dirty-default", base + ["--check-dirty"])
c2, r2, s2, t2 = run_preflight(d, "dirty-narrow", base + ["--check-dirty", "--dirty-pathspec", "other/"])
print(json.dumps({"dirty-default": {"exit": c1, "verdict": r1.get("verdict"), "dirty": r1.get("dirty"), "sha256": s1},
                  "dirty-narrow": {"exit": c2, "verdict": r2.get("verdict"), "dirty": r2.get("dirty"), "sha256": s2}},
                 sort_keys=True))
res["dirty"] = {"default": {"exit": c1, "dirty": r1.get("dirty"), "sha256": s1},
                "narrow": {"exit": c2, "dirty": r2.get("dirty"), "sha256": s2}}
json.dump(res, open(os.path.join(S, "attack2-receipts.json"), "w"), indent=1, sort_keys=True)
