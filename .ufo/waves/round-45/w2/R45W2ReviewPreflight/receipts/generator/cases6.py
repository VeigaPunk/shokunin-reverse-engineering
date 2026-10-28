import json, os, sys
sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r45/R45W2ReviewPreflight")
import driver
from driver import fixture, write, commit, gate, git, raw, S, OUT
d = fixture("c1-rename-out")
write(d, "frozen/a.txt", "alpha\n"); write(d, "frozen/b.txt", "beta\n")
f = commit(d, "freeze")
git(d, "mv", "frozen/a.txt", "other-a.txt", check=True)
r = commit(d, "rename frozen/a.txt out of the frozen dir")
raw("c1-raw-log-pathlimited", d, "log", "--name-status", "--format=%H", "%s..%s" % (f, r), "--", "frozen/")
gate(d, f, r)
# pristine a5 receipt with a recorded exit code
a5 = os.path.join(S, "fx", "a5-merge-ours")
b = json.load(open(os.path.join(OUT, "b6-nom-a5.json")))["receipt"]
gate(a5, b["freeze"], b["rev"])
os.rename(os.path.join(OUT, "a5-merge-ours.json"), os.path.join(OUT, "a5-pristine-merge-ours.json"))
