#!/usr/bin/env python3
import os
import subprocess
import sys
sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r45/R45W2ReviewPreflight")
from driver import fixture, write, commit, gate, git, raw, S

# ---- A5: merge that keeps the first parent's frozen bytes (TREESAME) ----
d = fixture("a5-merge-ours")
write(d, "frozen/a.txt", "alpha\n")
write(d, "frozen/b.txt", "beta\n")
write(d, "other.txt", "o\n")
f = commit(d, "freeze")
br = git(d, "symbolic-ref", "--short", "HEAD")[1].strip()
git(d, "checkout", "-q", "-b", "side", f, check=True)
write(d, "frozen/a.txt", "tampered\n")
s1 = commit(d, "side tampers frozen/a.txt")
git(d, "checkout", "-q", br, check=True)
write(d, "other.txt", "o2\n")
commit(d, "unrelated")
code, out, err = git(d, "merge", "-s", "ours", "--no-edit", "side")
print("merge rc", code, out, err)
m = git(d, "rev-parse", "HEAD")[1].strip()
raw("a5-raw-log-gateform", d, "log", "-m", "--diff-merges=first-parent",
    "--name-status", "--format=%x00%H", "%s..%s" % (f, m), "--", "frozen/")
raw("a5-raw-log-nom", d, "log", "--name-status", "--format=%H", "%s..%s" % (f, m), "--", "frozen/")
raw("a5-raw-log-fullhistory", d, "log", "--full-history", "--name-status",
    "--format=%H", "%s..%s" % (f, m), "--", "frozen/")
raw("a5-raw-log-whole-tree", d, "log", "--name-status", "--format=%H", "%s..%s" % (f, m))
raw("a5-raw-show-merge", d, "show", "--name-status", "--format=%H", "-m", m)
raw("a5-raw-blob-eq", d, "rev-parse", "%s:frozen/a.txt" % f, "%s:frozen/a.txt" % m)
gate(d, f, m)

# ---- A5b: two-sided conflict resolved to a third value (record duplication) ----
d = fixture("a5b-merge-conflict")
write(d, "frozen/a.txt", "alpha\n")
write(d, "other.txt", "o\n")
f = commit(d, "freeze")
br = git(d, "symbolic-ref", "--short", "HEAD")[1].strip()
git(d, "checkout", "-q", "-b", "side", f, check=True)
write(d, "frozen/a.txt", "side\n")
commit(d, "side value")
git(d, "checkout", "-q", br, check=True)
write(d, "frozen/a.txt", "main\n")
commit(d, "main value")
git(d, "merge", "side")
write(d, "frozen/a.txt", "merged\n")
commit(d, "merge resolved to merged")
m = git(d, "rev-parse", "HEAD")[1].strip()
raw("a5b-raw-gateform", d, "log", "-m", "--diff-merges=first-parent",
    "--name-status", "--format=%x00%H", "%s..%s" % (f, m), "--", "frozen/")
rec = gate(d, f, m)
print("a5b touched:", rec["receipt"].get("touched"))

# ---- A6: covers() with a parent pathspec git does accept ----
d = fixture("a6-covers-parent")
write(d, "frozen/sub/a.txt", "alpha\n")
write(d, "frozen/top.txt", "top\n")
f = commit(d, "freeze")
gate(d, f, f, pathspecs=("frozen/",), freeze_paths=("frozen/sub",))

# ---- A6b: covers() accepts a single descendant file as covering the dir ----
d = fixture("a6b-covers-file")
write(d, "frozen/a.txt", "alpha\n")
write(d, "frozen/b.txt", "beta\n")
f = commit(d, "freeze")
write(d, "frozen/b.txt", "tampered\n")
commit(d, "tamper frozen/b.txt")
write(d, "frozen/b.txt", "beta\n")
r = commit(d, "restore frozen/b.txt")
raw("a6b-raw-log-scoped", d, "log", "--name-status", "--format=%H", "%s..%s" % (f, r), "--", "frozen/a.txt")
rec = gate(d, f, r, pathspecs=("frozen/a.txt",), freeze_paths=("frozen",))
print("a6b exit", rec["exit"], rec["receipt"].get("touched"), rec["receipt"].get("blob_changed"))

# ---- A7: a frozen path with a non-ASCII name (git quotes it) ----
d = fixture("a7-nonascii")
write(d, "frozen/a.txt", "alpha\n")
write(d, "frozen/\u00e4.txt", "alpha-umlaut\n")
f = commit(d, "freeze")
raw("a7-raw-ls-tree", d, "ls-tree", "-r", "--name-only", f, "--", "frozen/")
write(d, "frozen/\u00e4.txt", "changed-umlaut\n")
r = commit(d, "touch non-ascii frozen path")
raw("a7-raw-log", d, "log", "--name-status", "--format=%H", "%s..%s" % (f, r), "--", "frozen/")
raw("a7-raw-revparse-a", d, "rev-parse", "%s:frozen/\u00e4.txt" % f)
raw("a7-raw-revparse-b", d, "rev-parse", "%s:frozen/\u00e4.txt" % r)
gate(d, f, r)

# ---- A8: dirty arm vs an ignored untracked file under the frozen dir ----
d = fixture("a8-ignored-untracked")
write(d, ".gitignore", "__pycache__/\n")
write(d, "frozen/a.txt", "alpha\n")
f = commit(d, "freeze")
write(d, "frozen/__pycache__/x.cpython-313.pyc", "bytecode\n")
raw("a8-raw-status-z", d, "status", "--porcelain", "-z", "--", "frozen/")
raw("a8-raw-check-ignore", d, "check-ignore", "-v", "frozen/__pycache__/x.cpython-313.pyc")
gate(d, f, f, check_dirty=True)

# ---- A9: assume-unchanged frozen file modified in the worktree ----
d = fixture("a9-assume-unchanged")
write(d, "frozen/a.txt", "alpha\n")
f = commit(d, "freeze")
git(d, "update-index", "--assume-unchanged", "frozen/a.txt", check=True)
write(d, "frozen/a.txt", "modified-in-worktree\n")
raw("a9-raw-status-z", d, "status", "--porcelain", "-z", "--", "frozen/")
gate(d, f, f, check_dirty=True)

# ---- A10: pathspec that is a child directory (sibling shielded) ----
d = fixture("a10-child-pathspec")
write(d, "frozen/sub/a.txt", "alpha\n")
write(d, "frozen/b.txt", "beta\n")
f = commit(d, "freeze")
write(d, "frozen/b.txt", "tampered\n")
r = commit(d, "tamper frozen/b.txt")
raw("a10-raw-log-child", d, "log", "--name-status", "--format=%H", "%s..%s" % (f, r), "--", "frozen/sub")
gate(d, f, r, pathspecs=("frozen/sub",), freeze_paths=("frozen",))
