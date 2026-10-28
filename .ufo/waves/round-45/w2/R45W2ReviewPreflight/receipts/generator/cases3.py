#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys
sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r45/R45W2ReviewPreflight")
from driver import fixture, write, commit, gate, git, raw, S, run, sha, OUT
import json
import datetime

# ---- B1: a path added AFTER the freeze and deleted before REV ----
d = fixture("b1-added-then-deleted")
write(d, "frozen/a.txt", "alpha\n")
write(d, "other.txt", "o\n")
f = commit(d, "freeze")
write(d, "frozen/new.txt", "new\n")
commit(d, "add frozen/new.txt")
os.remove(os.path.join(d, "frozen/new.txt"))
r = commit(d, "delete frozen/new.txt")
raw("b1-raw-log", d, "log", "-m", "--diff-merges=first-parent", "--name-status",
    "--format=%x00%H", "%s..%s" % (f, r), "--", "frozen/")
gate(d, f, r)

# ---- B2: copy (C records need --find-copies; the gate does not pass -C) ----
d = fixture("b2-copy")
write(d, "frozen/a.txt", "alpha\n")
f = commit(d, "freeze")
shutil.copyfile(os.path.join(d, "frozen/a.txt"), os.path.join(d, "frozen/c.txt"))
r = commit(d, "copy a->c")
raw("b2-raw-log", d, "log", "--name-status", "--format=%H", "%s..%s" % (f, r), "--", "frozen/")
raw("b2-raw-log-with-C", d, "log", "-C", "--find-copies-harder", "--name-status",
    "--format=%H", "%s..%s" % (f, r), "--", "frozen/")
gate(d, f, r)

# ---- B3: --freeze-path omitted, directory pathspec present ----
d = fixture("b3-no-freeze-path")
write(d, "frozen/a.txt", "alpha\n")
f = commit(d, "freeze")
gate(d, f, f, pathspecs=(), freeze_paths=())

# ---- B4: glob pathspec accepted by covers() ----
d = fixture("b4-glob-pathspec")
write(d, "frozen/sub/a.txt", "alpha\n")
f = commit(d, "freeze")
gate(d, f, f, pathspecs=("frozen/*",), freeze_paths=("frozen",))

# ---- B5: skip-worktree variant of the dirty-arm blindness ----
d = fixture("b5-skip-worktree")
write(d, "frozen/a.txt", "alpha\n")
f = commit(d, "freeze")
git(d, "update-index", "--skip-worktree", "frozen/a.txt", check=True)
write(d, "frozen/a.txt", "modified-under-skip-worktree\n")
raw("b5-raw-status-z", d, "status", "--porcelain", "-z", "--", "frozen/")
raw("b5-raw-ls-files-v", d, "ls-files", "-v", "--", "frozen/")
gate(d, f, f, check_dirty=True)

# ---- B6: mutation probe on a COPY: drop the -m from the commit arm ----
src = os.path.join(S, "preflight.py")
mutsrc = os.path.join(S, "preflight-nom.py")
text = open(src).read()
assert '"log", "-m", "--diff-merges=first-parent"' in text
mut = text.replace('"log", "-m", "--diff-merges=first-parent"',
                   '"log", "--diff-merges=first-parent"')
open(mutsrc, "w").write(mut)
print("mutation sha", sha(mut))
a5 = os.path.join(S, "fx", "a5-merge-ours")
import driver
driver.GATE = mutsrc
rec = gate(a5, json.load(open(os.path.join(OUT, "a5-merge-ours.json")))["receipt"]["freeze"],
           json.load(open(os.path.join(OUT, "a5-merge-ours.json")))["receipt"]["rev"])
print("mutation exit", rec["exit"], rec["receipt"].get("touched"), rec["receipt"].get("verdict"))
os.rename(os.path.join(OUT, "a5-merge-ours.json"), os.path.join(OUT, "b6-nom-a5.json"))
driver.GATE = src

# ---- B7: the lane's own frozen dir, live (read-only on the lane) ----
lane = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
freeze = "f762b7273e3f6ca3c710bb37d5de92a4a4417aec"
tip = git(lane, "rev-parse", "HEAD")[1].strip()
argv = [sys.executable, "-I", "-B", src, "--root", lane, "--freeze", freeze,
        "--rev", tip, "--pathspec", "tools/round-45/", "--pathspec",
        "plans/round-45-claims.md", "--freeze-path", "tools/round-45",
        "--freeze-path", "plans/round-45-claims.md", "--check-dirty",
        "--require-pathspec"]
code, out, err = run(argv, S)
rec = {"case": "b7-lane-live",
       "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "argv": argv, "exit": code, "stdout_sha256": sha(out),
       "stderr": err[:2000], "stdout_head": out[:4000]}
json.dump(rec, open(os.path.join(OUT, "b7-lane-live.json"), "w"), indent=1, sort_keys=True)
print(json.dumps({"case": "b7-lane-live", "exit": code, "sha": sha(out),
                  "receipt": json.loads(out.strip().splitlines()[-1]) if out.strip() else None},
                 sort_keys=True))
raw("b7-lane-status", lane, "status", "--porcelain", "-z", "--", "tools/round-45/",
    "plans/round-45-claims.md")
raw("b7-lane-untracked-present", lane, "ls-files", "--others", "--exclude-standard",
    "--", "tools/round-45/")
raw("b7-lane-selftest-receipt", lane, "log", "-1", "--format=%H", "--",
    ".ufo/waves/round-45/controls/preflight-selftest.txt")
