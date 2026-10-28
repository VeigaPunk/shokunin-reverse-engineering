#!/usr/bin/env python3
"""Order-asymmetry fixture: parents diverge, resolution keeps the FIRST parent's bytes.

Any path whose divergence predates the range's base is named by the merge-relative
second-parent diff and not by the first-parent diff; the reverse never happens.
"""
import json
import os
import subprocess
import sys

S = os.environ["HYAKU_SCRATCH"]
sys.path.insert(0, os.path.join(S, "copy", "tools", "round-46"))
import gate  # noqa: E402

D = os.path.join(S, "probe", "narrow")
subprocess.run(["rm", "-rf", D], check=True)
os.makedirs(D)


def g(*a):
    return subprocess.run(["git", "-C", D, *a], capture_output=True, text=True)


g("init", "-q")
assert g("rev-parse", "--show-toplevel").stdout.strip() == D
g("config", "user.email", "fx@r47")
g("config", "user.name", "fx")


def w(p, s):
    os.makedirs(os.path.dirname(os.path.join(D, p)) or D, exist_ok=True)
    with open(os.path.join(D, p), "w") as fh:
        fh.write(s)


w("h.txt", "base\n")
w("z.txt", "base\n")
g("add", "-A")
g("commit", "-qm", "c0")
g("branch", "-M", "main")
# an OLD commit (before the range base) changes h on the second-parent side only
g("checkout", "-qb", "A")
w("h.txt", "A-side\n")
g("commit", "-qam", "c1 h=A")
cA = g("rev-parse", "A").stdout.strip()
g("checkout", "-q", "main")
# the range base is after A's change: the merge's second parent differs on h, and no
# commit INSIDE the range names h
c1 = cA
g("checkout", "-qb", "B")
w("z.txt", "B-side\n")
g("commit", "-qam", "c2 z=B")
g("merge", "--no-commit", "A")
w("h.txt", "base\n")    # FIRST parent's bytes: the resolution keeps parent 1
w("z.txt", "B-side\n")
g("add", "-A")
g("commit", "-qm", "merge A")
tip = g("rev-parse", "HEAD").stdout.strip()
par = g("rev-list", "--parents", "-n1", tip).stdout.split()[1:]


def parse(order):
    r = subprocess.run(["git", "-C", D, "log", *order, "--name-status", "-z",
                        "--format=", f"{c1}..{tip}", "--", "h.txt", "z.txt"],
                       capture_output=True)
    toks = r.stdout.decode("utf-8", "surrogateescape").split("\0")
    out, i = set(), 0
    while i < len(toks):
        if gate.STATUS.match(toks[i].strip()) and i + 1 < len(toks):
            out.add(toks[i + 1])
            i += 2
        else:
            i += 1
    return sorted(out)


c = parse(["-m", "--diff-merges=first-parent"])
r = parse(["--diff-merges=first-parent", "-m"])
print(json.dumps({"fixture": "resolution-keeps-second-parent",
                  "parents": par, "range": f"{c1}..{tip}",
                  "correct_order": c, "reversed_order": r,
                  "reversed_adds": sorted(set(r) - set(c)),
                  "reversed_loses": sorted(set(c) - set(r)),
                  "read": "reversed adds a merge-relative path; it never loses one"},
                 indent=1))
