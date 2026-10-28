#!/usr/bin/env python3
import sys
sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r45/R45W2ReviewPreflight")
from driver import fixture, write, commit, gate, git, raw, S
import os

# ---- A1: rename inside the frozen dir (record format R100 <old> <new>) ----
d = fixture("a1-rename-within")
write(d, "frozen/a.txt", "alpha\n")
write(d, "frozen/b.txt", "beta\n")
write(d, "other.txt", "other\n")
f = commit(d, "freeze")
git(d, "mv", "frozen/a.txt", "frozen/c.txt", check=True)
r = commit(d, "rename a->c")
raw("a1-raw-log", d, "log", "--name-status", "--format=%H", "%s..%s" % (f, r))
raw("a1-raw-log-pathlimited", d, "log", "--name-status", "--format=%H",
    "%s..%s" % (f, r), "--", "frozen/")
gate(d, f, r)

# ---- A1b: rename from outside INTO the frozen dir (source cell) ----
d = fixture("a1b-rename-into")
write(d, "frozen/a.txt", "alpha\n")
write(d, "other/x.txt", "x\n")
f = commit(d, "freeze")
git(d, "mv", "other/x.txt", "frozen/x.txt", check=True)
r = commit(d, "move x into frozen")
raw("a1b-raw-log-pathlimited", d, "log", "--name-status", "--format=%H",
    "%s..%s" % (f, r), "--", "frozen/")
gate(d, f, r)

# ---- A2: untracked directory collapse in the dirty arm ----
d = fixture("a2-untracked-dir")
write(d, "frozen/a.txt", "alpha\n")
f = commit(d, "freeze")
for i in range(8):
    write(d, "frozen/pack/f%d.json" % i, "%d\n" % i)
raw("a2-raw-status-z", d, "status", "--porcelain", "-z")
gate(d, f, f, check_dirty=True)
# A2b: same eight files, spelled as one untracked file each under the tracked dir
d = fixture("a2b-untracked-files")
write(d, "frozen/a.txt", "alpha\n")
f = commit(d, "freeze")
for i in range(8):
    write(d, "frozen/n%d.json" % i, "%d\n" % i)
raw("a2b-raw-status-z", d, "status", "--porcelain", "-z")
gate(d, f, f, check_dirty=True)
# A2c: dirty-pathspec narrower than the untracked dir
d = fixture("a2c-untracked-dir-narrow")
write(d, "frozen/sub/a.txt", "alpha\n")
f = commit(d, "freeze")
for i in range(3):
    write(d, "frozen/sub/pack/f%d.json" % i, "%d\n" % i)
raw("a2c-raw-status-z-narrow", d, "status", "--porcelain", "-z", "--", "frozen/sub/")
gate(d, f, f, check_dirty=True, dirty_pathspecs=("frozen/sub/",))

# ---- A3: deleted then recreated with identical bytes ----
d = fixture("a3-deleted-recreated")
write(d, "frozen/a.txt", "alpha\n")
write(d, "other.txt", "o\n")
f = commit(d, "freeze")
os.remove(os.path.join(d, "frozen/a.txt"))
commit(d, "delete frozen/a.txt")
write(d, "frozen/a.txt", "alpha\n")
r = commit(d, "recreate identical")
gate(d, f, r)
# A3b: deleted only
d = fixture("a3b-deleted-only")
write(d, "frozen/a.txt", "alpha\n")
write(d, "frozen/b.txt", "beta\n")
f = commit(d, "freeze")
os.remove(os.path.join(d, "frozen/a.txt"))
r = commit(d, "delete frozen/a.txt")
gate(d, f, r)

# ---- A4a: symlink retarget ----
d = fixture("a4a-symlink-retarget")
write(d, "frozen/a.txt", "alpha\n")
write(d, "frozen/b.txt", "beta\n")
os.symlink("a.txt", os.path.join(d, "frozen/link"))
f = commit(d, "freeze")
os.remove(os.path.join(d, "frozen/link"))
os.symlink("b.txt", os.path.join(d, "frozen/link"))
r = commit(d, "retarget symlink")
raw("a4a-raw-log", d, "log", "--name-status", "--format=%H", "%s..%s" % (f, r))
gate(d, f, r)
# A4a2: symlink replaced by a regular file with the same text
d = fixture("a4a2-symlink-to-file")
write(d, "frozen/a.txt", "alpha\n")
os.symlink("a.txt", os.path.join(d, "frozen/link"))
f = commit(d, "freeze")
os.remove(os.path.join(d, "frozen/link"))
write(d, "frozen/link", "a.txt")
r = commit(d, "symlink to file")
raw("a4a2-raw-log", d, "log", "--name-status", "--format=%H", "%s..%s" % (f, r))
gate(d, f, r)

# ---- A4b: submodule pointer bump ----
sub = os.path.join(S, "fx", "a4b-subsrepo")
if os.path.isdir(sub):
    import shutil
    shutil.rmtree(sub)
os.makedirs(sub)
git(sub, "init", "-q", check=True)
git(sub, "config", "user.email", "rev@r45", check=True)
git(sub, "config", "user.name", "rev r45", check=True)
git(sub, "config", "commit.gpgsign", "false", check=True)
write(sub, "s.txt", "one\n")
c1 = commit(sub, "s1")
write(sub, "s.txt", "two\n")
c2 = commit(sub, "s2")
d = fixture("a4b-submodule-bump")
write(d, "frozen/a.txt", "alpha\n")
git(d, "-c", "protocol.file.allow=always", "submodule", "add", "-q", sub, "frozen/sub", check=True)
git(d, "checkout", c1, "--", check=True) if False else None
# pin submodule to c1 inside the parent commit
git(d, "-C", "frozen/sub", "checkout", "-q", c1, check=True) if False else None
import subprocess
subprocess.run(["git", "-C", os.path.join(d, "frozen/sub"), "checkout", "-q", c1], check=True)
f = commit(d, "freeze with submodule at s1")
subprocess.run(["git", "-C", os.path.join(d, "frozen/sub"), "checkout", "-q", c2], check=True)
r = commit(d, "bump submodule to s2")
raw("a4b-raw-log", d, "log", "--name-status", "--format=%H", "%s..%s" % (f, r))
gate(d, f, r)
