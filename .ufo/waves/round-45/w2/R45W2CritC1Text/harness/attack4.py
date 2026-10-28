#!/usr/bin/env python3
"""T10 restore-after-touch, then a UTC-stamped receipt ledger for every attack."""
import hashlib, json, os, shutil, subprocess, sys, datetime

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

def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

ROWS = []

def run(tag, argv, cwd=S):
    t = utc()
    p = subprocess.run(argv, capture_output=True, text=True, env=ENV, cwd=cwd)
    ROWS.append({"test": tag, "command": " ".join(argv), "exit": p.returncode,
                 "stdout_sha256": hashlib.sha256(p.stdout.encode()).hexdigest(),
                 "stdout_head": p.stdout.strip().splitlines()[:1], "utc": t})
    return p, t

# ---- T10: touch a frozen path, then restore it to the freeze bytes ----
d = os.path.join(S, "fix-restore")
if os.path.isdir(d):
    shutil.rmtree(d)
shutil.copytree(os.path.join(S, "tree"), d, symlinks=True)
git(d, "init", "-q", "-b", "main")
git(d, "config", "user.email", "w2@crit"); git(d, "config", "user.name", "w2 crit")
git(d, "add", "-A"); git(d, "commit", "-q", "-m", "freeze")
assert os.path.realpath(git(d, "rev-parse", "--show-toplevel").stdout.strip()) == os.path.realpath(d)
F0 = git(d, "rev-parse", "HEAD").stdout.strip()
orig = subprocess.run(["git", "-C", d, "show", f"{F0}:{CLAIMS}"], capture_output=True, text=True).stdout
open(os.path.join(d, CLAIMS), "a").write("post-freeze edit\n")
git(d, "add", "-A"); git(d, "commit", "-q", "-m", "touch frozen claims")
open(os.path.join(d, CLAIMS), "w").write(orig)
git(d, "add", "-A"); git(d, "commit", "-q", "-m", "restore frozen claims to freeze bytes")
R = git(d, "rev-parse", "HEAD").stdout.strip()
same = subprocess.run(["git", "-C", d, "show", f"{R}:{CLAIMS}"], capture_output=True, text=True).stdout == orig
p10, t10 = run("T10-restore-after-touch/c1-counter",
               [sys.executable, "-I", "-B", COUNTER, "--root", d, "--freeze", F0, "--rev", R])
p10b, _ = run("T10-restore-after-touch/preflight",
              [sys.executable, "-I", "-B", PREFLIGHT, "--root", d, "--freeze", F0, "--rev", R,
               "--pathspec", CLAIMS, "--freeze-path", CLAIMS])
print(json.dumps({"T10": {"tip_blob_equals_freeze_blob": same,
                          "c1_counter": {"exit": p10.returncode, "stdout": p10.stdout.strip()},
                          "preflight": {"exit": p10b.returncode, "stdout": p10b.stdout.strip()}},
                  "utc": t10}, sort_keys=True))

# ---- ledger: exact re-runs of each fixture attack ----
def revs(d):
    head = git(d, "rev-parse", "HEAD").stdout.strip()
    parent = git(d, "rev-parse", "HEAD~1").stdout.strip()
    return (parent, head) if head != parent else (head, head)

for name in ("header", "unlocated", "extra", "sources", "badexit", "touch", "nos141",
             "drop-restored", "drop-blob", "stub"):
    d = os.path.join(S, "fix-" + name)
    f0, f1 = revs(d)
    run("T-fixture/" + name,
        [sys.executable, "-I", "-B", COUNTER, "--root", d, "--freeze", f0, "--rev", f1])

d = os.path.join(S, "fix-dirty")
f0 = git(d, "rev-parse", "HEAD").stdout.strip()
run("dirty/default",
    [sys.executable, "-I", "-B", PREFLIGHT, "--root", d, "--freeze", f0, "--rev", f0,
     "--pathspec", "data/", "--freeze-path", "data", "--check-dirty"])
run("dirty/narrowed-dirty-pathspec",
    [sys.executable, "-I", "-B", PREFLIGHT, "--root", d, "--freeze", f0, "--rev", f0,
     "--pathspec", "data/", "--freeze-path", "data", "--check-dirty", "--dirty-pathspec", "other/"])

d = os.path.join(S, "fix-merge")
f0 = git(d, "rev-parse", "HEAD~2").stdout.strip()
m = git(d, "rev-parse", "HEAD").stdout.strip()
run("merge-resolution/c1-counter",
    [sys.executable, "-I", "-B", COUNTER, "--root", d, "--freeze", f0, "--rev", m])
run("merge-resolution/preflight",
    [sys.executable, "-I", "-B", PREFLIGHT, "--root", d, "--freeze", f0, "--rev", m,
     "--pathspec", CLAIMS, "--freeze-path", CLAIMS])

# ---- lane-level reruns at the three cited revisions ----
for tag, freez, rev in (("lane/freeze-do-nothing", "f762b7273e3f6ca3c710bb37d5de92a4a4417aec",
                         "f762b7273e3f6ca3c710bb37d5de92a4a4417aec"),
                        ("lane/base-do-nothing", "149133d47aa7e90796f96047afe6d251a3e65b2c",
                         "149133d47aa7e90796f96047afe6d251a3e65b2c"),
                        ("lane/A1", "f762b7273e3f6ca3c710bb37d5de92a4a4417aec",
                         "1f4b27f82353d6544dc0c8048b3cfdadd8525d12"),
                        ("lane/A3", "f762b7273e3f6ca3c710bb37d5de92a4a4417aec",
                         "f59565b782c18b0eb691bec12f52d2f80d9f5032"),
                        ("lane/HEAD", "f762b7273e3f6ca3c710bb37d5de92a4a4417aec",
                         "0ee50aaff516571aa607769bbbdf19a3db90dfa5")):
    run(tag, [sys.executable, "-I", "-B", COUNTER, "--root", LANE, "--freeze", freez, "--rev", rev],
        cwd=LANE)
run("lane/c1-selftest", [sys.executable, "-I", "-B", COUNTER, "--selftest"], cwd=LANE)
run("lane/preflight-selftest", [sys.executable, "-I", "-B", PREFLIGHT, "--selftest"])

with open(os.path.join(S, "receipts.tsv"), "w") as fh:
    fh.write("test\texit\tstdout_sha256\tutc\tcommand\n")
    for r in ROWS:
        fh.write("%s\t%s\t%s\t%s\t%s\n" % (r["test"], r["exit"], r["stdout_sha256"], r["utc"], r["command"]))
for r in ROWS:
    print("%-34s exit=%s %s %s" % (r["test"], r["exit"], r["stdout_sha256"][:16], r["utc"]))
