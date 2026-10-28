#!/usr/bin/env python3
"""P5c: what does `out_path` refuse, exactly?

It compares against the static GRADED tuple, not against the frozen set the claims
file derives. So a frozen path OUTSIDE GRADED is accepted, and the "frozen bytes"
half of the R45-CL22 guard is only as wide as GRADED. Also probes a symlink escape.
"""
import json
import os
import sys

S = os.environ["HYAKU_SCRATCH"]
WHICH = sys.argv[1]
sys.path.insert(0, os.path.join(S, WHICH, "tools", "round-46"))
import gate  # noqa: E402

LANE = os.path.join(S, "p5c-lane")
os.makedirs(os.path.join(LANE, "notes"), exist_ok=True)
os.makedirs(os.path.join(LANE, "tools", "round-46"), exist_ok=True)
open(os.path.join(LANE, "notes", "frozen.md"), "w").write("frozen by a claims file\n")
open(os.path.join(LANE, "SKILL.md"), "w").write("# skill\n")
try:
    os.symlink("/etc/passwd", os.path.join(LANE, "notes", "escape.json"))
except FileExistsError:
    pass

targets = {
    "SKILL.md (graded)": os.path.join(LANE, "SKILL.md"),
    "tools/round-46/x.py (graded dir)": os.path.join(LANE, "tools", "round-46", "x.py"),
    "notes/frozen.md (frozen, NOT graded)": os.path.join(LANE, "notes", "frozen.md"),
    "notes/escape.json (symlink -> /etc/passwd)": os.path.join(LANE, "notes", "escape.json"),
    "/etc/passwd (outside lane)": "/etc/passwd",
    "notes/../SKILL.md (dot-dot)": os.path.join(LANE, "notes", "..", "SKILL.md"),
}
out = {"dir": WHICH, "GRADED": list(gate.GRADED), "results": {}}
for label, p in targets.items():
    resolved, err = gate.out_path(LANE, p)
    out["results"][label] = {"allowed": resolved is not None, "resolved": resolved, "err": err}
print(json.dumps(out, indent=1))
