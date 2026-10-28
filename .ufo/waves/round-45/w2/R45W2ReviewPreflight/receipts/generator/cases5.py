import json, os, sys
sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r45/R45W2ReviewPreflight")
import driver
from driver import gate, raw, S, OUT, sha, run

# regenerate the narrow-pathspec false-clean receipt (it was overwritten by the control)
a6b = os.path.join(S, "fx", "a6b-covers-file")
b8 = json.load(open(os.path.join(OUT, "b8-a6b-control-full-pathspec.json")))["receipt"]
gate(a6b, b8["freeze"], b8["rev"], pathspecs=("frozen/a.txt",), freeze_paths=("frozen",))

# B9: drop both merge flags on the a5 fixture
src = os.path.join(S, "preflight.py")
noMerge = os.path.join(S, "preflight-plainlog.py")
a5rec = json.load(open(os.path.join(OUT, "b6-nom-a5.json")))["receipt"]
driver.GATE = noMerge
gate(os.path.join(S, "fx", "a5-merge-ours"), a5rec["freeze"], a5rec["rev"])
os.rename(os.path.join(OUT, "a5-merge-ours.json"), os.path.join(OUT, "b9-plainlog-a5.json"))
driver.GATE = src

# B10
a7 = os.path.join(S, "fx", "a7-nonascii")
freeze = json.load(open(os.path.join(OUT, "a7-nonascii.json")))["receipt"]["freeze"]
quoted = '"frozen/\\303\\244.txt"'
code, out, err = run(["git", "-C", a7, "rev-parse", "%s:%s" % (freeze, quoted)], S)
json.dump({"case": "b10-quoted-revparse", "argv": ["git", "-C", a7, "rev-parse", "%s:%s" % (freeze, quoted)],
           "exit": code, "stdout_sha256": sha(out), "stdout": out, "stderr": err},
          open(os.path.join(OUT, "b10-quoted-revparse.json"), "w"), indent=1, sort_keys=True)
print(json.dumps({"case": "b10", "exit": code, "stderr": err.strip()[:200]}, sort_keys=True))
raw("b10-ls-tree-z", a7, "ls-tree", "-r", "-z", "--name-only", freeze, "--", "frozen/")

# B11
lane = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
raw("b11-lane-ls-files-others", lane, "ls-files", "--others", "--", "tools/round-45/")
