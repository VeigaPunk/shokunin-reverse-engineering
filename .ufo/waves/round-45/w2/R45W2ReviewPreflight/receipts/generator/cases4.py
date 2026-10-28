#!/usr/bin/env python3
import json
import os
import sys
sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r45/R45W2ReviewPreflight")
import driver
from driver import fixture, write, commit, gate, git, raw, S, OUT, sha, run

# ---- B8: control for A6b — same history, the full directory pathspec ----
a6b = os.path.join(S, "fx", "a6b-covers-file")
rec = json.load(open(os.path.join(OUT, "a6b-covers-file.json")))["receipt"]
gate(a6b, rec["freeze"], rec["rev"], pathspecs=("frozen/",), freeze_paths=("frozen",))
os.rename(os.path.join(OUT, "a6b-covers-file.json"),
          os.path.join(OUT, "b8-a6b-control-full-pathspec.json"))

# ---- B9: mutation probe: drop BOTH merge flags from the commit arm ----
src = os.path.join(S, "preflight.py")
noMerge = os.path.join(S, "preflight-plainlog.py")
text = open(src).read()
mut = text.replace('"log", "-m", "--diff-merges=first-parent"', '"log"')
assert mut != text
open(noMerge, "w").write(mut)
print("mutation sha", sha(mut))
a5 = os.path.join(S, "fx", "a5-merge-ours")
driver.GATE = noMerge
gate(a5, rec := json.load(open(os.path.join(OUT, "a5-merge-ours.json")))["receipt"]["freeze"],
     json.load(open(os.path.join(OUT, "a5-merge-ours.json")))["receipt"]["rev"])
os.rename(os.path.join(OUT, "a5-merge-ours.json"),
          os.path.join(OUT, "b9-plainlog-a5.json"))
driver.GATE = src

# ---- B10: the quoted ls-tree name does not resolve; -z shows the raw name ----
a7 = os.path.join(S, "fx", "a7-nonascii")
freeze = json.load(open(os.path.join(OUT, "a7-nonascii.json")))["receipt"]["freeze"]
quoted = '"frozen/\\303\\244.txt"'
code, out, err = run(["git", "-C", a7, "rev-parse", "%s:%s" % (freeze, quoted)], S)
rec = {"case": "b10-quoted-revparse", "argv": ["git", "-C", a7, "rev-parse",
       "%s:%s" % (freeze, quoted)], "exit": code, "stdout_sha256": sha(out),
       "stdout": out, "stderr": err}
json.dump(rec, open(os.path.join(OUT, "b10-quoted-revparse.json"), "w"), indent=1, sort_keys=True)
print(json.dumps({"case": "b10", "exit": code, "stderr": err.strip()[:200]}, sort_keys=True))
raw("b10-ls-tree-z", a7, "ls-tree", "-r", "-z", "--name-only", freeze, "--", "frozen/")

# ---- B11: the lane's frozen dir contains an ignored untracked directory ----
lane = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
raw("b11-lane-ls-files-others", lane, "ls-files", "--others", "--", "tools/round-45/")
raw("b11-lane-frozen-dir-worktree", lane, "ls-tree", "-r", "--name-only",
    "f762b7273e3f6ca3c710bb37d5de92a4a4417aec", "--", "tools/round-45/")
