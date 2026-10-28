#!/usr/bin/env python3
"""Final UTC-stamped receipt ledger for R45W2CritC1Text, written into the seat report dir."""
import hashlib, os, subprocess, sys, datetime

S = "/fast/scratch/hyaku/kaidoku-r45/R45W2CritC1Text"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
OUT = os.path.join(LANE, ".ufo/waves/round-45/w2/R45W2CritC1Text")
WORK = os.path.join(S, "work")
ENV = dict(os.environ, TMPDIR=WORK, HYAKU_SCRATCH=WORK)
ENV.pop("GIT_DIR", None)
COUNTER = os.path.join(LANE, "tools/round-45/c1-counter.py")
PREFLIGHT = os.path.join(S, "preflight.py")
CLAIMS = "plans/round-45-claims.md"
os.makedirs(OUT, exist_ok=True)

def git(d, *a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)

def stamp():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

rows = []

def run(tag, argv, cwd=S):
    t = stamp()
    p = subprocess.run(argv, capture_output=True, text=True, env=ENV, cwd=cwd)
    shown = [a.replace(S, "$S") for a in argv]
    rows.append((tag, p.returncode, hashlib.sha256(p.stdout.encode()).hexdigest(), t, " ".join(shown)))
    print("%-36s exit=%s %s %s" % (tag, p.returncode, hashlib.sha256(p.stdout.encode()).hexdigest()[:16], t))

def fr(name, back=1):
    d = os.path.join(S, "fix-" + name)
    head = git(d, "rev-parse", "HEAD").stdout.strip()
    if back == 0:
        return d, head, head
    return d, git(d, "rev-parse", f"HEAD~{back}").stdout.strip(), head

for name, back in (("header", 1), ("unlocated", 1), ("extra", 1), ("sources", 1),
                   ("badexit", 1), ("touch", 1), ("nos141", 0), ("drop-restored", 0),
                   ("drop-blob", 0), ("stub", 0), ("restore", 2)):
    d, f0, f1 = fr(name, back)
    run("fixture/" + name, [sys.executable, "-I", "-B", COUNTER, "--root", d,
                            "--freeze", f0, "--rev", f1])

d = os.path.join(S, "fix-merge")
f0 = git(d, "rev-parse", "HEAD~2").stdout.strip()
m = git(d, "rev-parse", "HEAD").stdout.strip()
run("merge-resolution/c1-counter", [sys.executable, "-I", "-B", COUNTER, "--root", d,
                                    "--freeze", f0, "--rev", m])
run("merge-resolution/preflight", [sys.executable, "-I", "-B", PREFLIGHT, "--root", d,
                                   "--freeze", f0, "--rev", m,
                                   "--pathspec", CLAIMS, "--freeze-path", CLAIMS])

d = os.path.join(S, "fix-diroid")
f0 = git(d, "rev-parse", "HEAD~1").stdout.strip()
f1 = git(d, "rev-parse", "HEAD").stdout.strip()
run("dir-oid/blob-arm", [sys.executable, "-I", "-B", PREFLIGHT, "--root", d, "--freeze", f0,
                        "--rev", f1, "--pathspec", "data/", "--freeze-path", "data"])

d = os.path.join(S, "fix-dirty")
f0 = git(d, "rev-parse", "HEAD").stdout.strip()
run("dirty/default", [sys.executable, "-I", "-B", PREFLIGHT, "--root", d, "--freeze", f0,
                      "--rev", f0, "--pathspec", "data/", "--freeze-path", "data", "--check-dirty"])
run("dirty/narrowed", [sys.executable, "-I", "-B", PREFLIGHT, "--root", d, "--freeze", f0,
                       "--rev", f0, "--pathspec", "data/", "--freeze-path", "data",
                       "--check-dirty", "--dirty-pathspec", "other/"])

for tag, freez, rev in (
        ("lane/freeze-do-nothing", "f762b7273e3f6ca3c710bb37d5de92a4a4417aec",
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
run("lane/c1-counter-selftest", [sys.executable, "-I", "-B", COUNTER, "--selftest"], cwd=LANE)
run("lane/preflight-selftest", [sys.executable, "-I", "-B", PREFLIGHT, "--selftest"])

with open(os.path.join(OUT, "receipts.tsv"), "w") as fh:
    fh.write("test\texit\tstdout_sha256\tutc\tcommand\n")
    for r in rows:
        fh.write("%s\t%s\t%s\t%s\t%s\n" % r)
print("wrote", os.path.join(OUT, "receipts.tsv"), len(rows), "rows")
