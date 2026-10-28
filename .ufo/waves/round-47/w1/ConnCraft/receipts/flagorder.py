#!/usr/bin/env python3
"""Does the R46-CL6 flag order actually blind gate.history_touched?

Runs the real gate.history_touched on a merge fixture, then the same call with the
two flags reversed, and compares the touched path sets. Read-only: the fixture lives
under HYAKU_SCRATCH.
"""
import json
import os
import subprocess
import sys

S = os.environ["HYAKU_SCRATCH"]
sys.path.insert(0, os.path.join(S, "copy", "tools", "round-46"))
import gate  # noqa: E402

D = os.path.join(S, "probe", "merge2")
subprocess.run(["rm", "-rf", D], check=True)
os.makedirs(D)


def g(*args, binary=False, inp=None):
    return subprocess.run(["git", "-C", D, *args], capture_output=True,
                          text=not binary, check=False)


g("init", "-q")
top = g("rev-parse", "--show-toplevel").stdout.strip()
assert top == D, (top, D)
g("config", "user.email", "fx@round47")
g("config", "user.name", "fx")


def write(p, s):
    os.makedirs(os.path.dirname(os.path.join(D, p)) or D, exist_ok=True)
    with open(os.path.join(D, p), "w") as fh:
        fh.write(s)


write("f.txt", "a\n")
write("g.txt", "a\n")
write("frozen/keep.txt", "keep\n")
g("add", "-A")
g("commit", "-qm", "base")
base = g("rev-parse", "HEAD").stdout.strip()

# first parent: right (the branch we are on), second parent: left
g("checkout", "-qb", "right")
write("f.txt", "right\n")
write("g.txt", "right-g\n")
g("commit", "-qam", "right edit")
g("checkout", "-qb", "left", base)
write("f.txt", "left\n")
write("g.txt", "left-g\n")
write("frozen/keep.txt", "tampered on left\n")
g("commit", "-qam", "left edit")
g("checkout", "-q", "right")
m = g("merge", "left")
assert m.returncode != 0, "expected a conflict"
# resolution: f.txt keeps FIRST parent's bytes, g.txt takes SECOND parent's,
# frozen/keep.txt takes the SECOND parent's tampering (the resolution edit that matters)
write("f.txt", "right\n")
write("g.txt", "left-g\n")
write("frozen/keep.txt", "tampered on left\n")
g("add", "-A")
g("commit", "-qm", "merge left")
tip = g("rev-parse", "HEAD").stdout.strip()
parents = g("rev-list", "--parents", "-n1", tip).stdout.split()[1:]
assert len(parents) == 2, parents

touched_correct, err = gate.history_touched(D, base, tip, ["frozen/keep.txt"])
# the reversed call, byte-identical except the flag order the gate hardcodes
r = subprocess.run(["git", "-C", D, "log", "--diff-merges=first-parent", "-m",
                    "--name-status", "-z", "--format=", f"{base}..{tip}", "--",
                    "frozen/keep.txt"], capture_output=True)
tokens = r.stdout.decode("utf-8", "surrogateescape").split("\0")
touched_rev = set()
i = 0
while i < len(tokens):
    if gate.STATUS.match(tokens[i].strip()) and i + 1 < len(tokens):
        touched_rev.add(tokens[i + 1])
        i += 2
        continue
    i += 1
touched_rev = sorted(touched_rev)

bool_correct, _ = gate.history_touched(D, base, tip, ["f.txt", "g.txt"])
# same extraction for the reversed order over the same two paths
r2 = subprocess.run(["git", "-C", D, "log", "--diff-merges=first-parent", "-m",
                     "--name-status", "-z", "--format=", f"{base}..{tip}", "--",
                     "f.txt", "g.txt"], capture_output=True)
toks = r2.stdout.decode("utf-8", "surrogateescape").split("\0")
wide = set()
i = 0
while i < len(toks):
    if gate.STATUS.match(toks[i].strip()) and i + 1 < len(toks):
        wide.add(toks[i + 1])
        i += 2
        continue
    i += 1

print(json.dumps({
    "base": base, "tip": tip, "parents": parents,
    "frozen_arm_correct_order": touched_correct, "frozen_arm_reversed_order": touched_rev,
    "reversed_loses_a_path": sorted(set(touched_correct or []) - set(touched_rev)),
    "reversed_adds_paths": sorted(set(touched_rev) - set(touched_correct or [])),
    "two_path_arm_correct": bool_correct, "two_path_arm_reversed": sorted(wide),
    "reversed_adds_here": sorted(wide - set(bool_correct or [])),
    "reversed_loses_here": sorted(set(bool_correct or []) - wide),
}, indent=1))
