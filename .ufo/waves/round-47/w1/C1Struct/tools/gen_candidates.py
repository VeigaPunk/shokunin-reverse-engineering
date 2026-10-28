#!/usr/bin/env python3
"""C1Struct: materialise the candidate block texts and the F1 fixture input."""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("HYAKU_SCRATCH", HERE)
src = open(os.path.join(HERE, "drive.py")).read().split('base = show("SKILL.md")')[0]
exec(compile(src, "drive.py:prefix", "exec"))  # noqa: S102 — scratch-only reuse

OUT = os.path.join(os.path.dirname(HERE), "candidates")
os.makedirs(OUT, exist_ok=True)
base = show("SKILL.md")


def emit(name, text):
    p = os.path.join(OUT, name)
    with open(p, "w") as fh:
        fh.write(text)
    print(f"{name} sha256={hashlib.sha256(text.encode()).hexdigest()} lines={len(text.splitlines())}")


emit("block24-candidate-a.md", BLOCK_A)
emit("block24-candidate-b.md", BLOCK_B)

head, sep, tail = base.partition("## Queue-drain craft ")
body, sep2, rest = tail.partition("\n## ")
emit("SKILL-craft-stripped-to-block24.md",
     head + sep + "\n\n" + BLOCK_B.rstrip("\n") + "\n\n## " + rest)

landed = insert_block(base, BLOCK_B)
emit("SKILL-with-block24-candidate-b.md", landed)
print("anchor: SKILL.md at freeze, insertion point = immediately before the "
      "'## Config custody for live-probe rounds (SOP)' heading (line 632 at the freeze); "
      "craft body ends at line 631.")
