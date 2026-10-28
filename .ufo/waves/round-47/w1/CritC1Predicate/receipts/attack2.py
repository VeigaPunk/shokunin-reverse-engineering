#!/usr/bin/env python3
"""Single-variable mutations of the LANDED block 24, built at REV.

vF: block 23's table relabelled `24. ` (the claims file's own kill rule).
vG: only the `v2 hole` column replaced by "n/a" (every other cell byte-identical).
vH: only the two arm cells swapped (symbol <-> digest), every other cell identical.
"""
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = sys.argv[1]
SCRATCH = os.environ["HYAKU_SCRATCH"]
sys.path.insert(0, os.path.join(LANE, "tools", "round-47"))
sys.path.insert(0, os.path.join(LANE, "tools", "round-46"))
import exact  # noqa: E402
import gate  # noqa: E402

FILES = ["SKILL.md", "plans/round-47-claims.md", "tools/round-47/exact.py",
         "tools/round-46/gate.py", "corpus/lessons/round-46.md",
         "corpus/lessons/round-45.md"]

skill = gate.show(LANE, REV, "SKILL.md")
blocks = exact.blocks_of(skill)
genuine = blocks[-1]
header, rows = exact.table(genuine)
print("genuine header", header, "rows", len(rows))
for r in rows:
    print("  row:", [c[:60] for c in r])

variants = {}

# vG: the hole column is the only change
g_rows = [[r[0], "n/a", r[2], r[3]] for r in rows]
variants["vG-hole-column-n-a"] = exact.rewrite_rows(genuine, g_rows)

# vH: the arm column is permuted between the two rows that name different arms
h_rows = [r[:] for r in rows]
a = h_rows[0][2], h_rows[2][2]
h_rows[0][2], h_rows[2][2] = a[1], a[0]
variants["vH-arms-swapped"] = exact.rewrite_rows(genuine, h_rows)

# vF: block 23's table relabelled, marker added, title renumbered
b23 = blocks[-2]
assert "freeze-integrity-table v2" in b23
f = b23.replace("23. ", "24. ", 1).replace("<!-- freeze-integrity-table v2 -->",
                                           exact.MARKER, 1)
variants["vF-block23-relabelled"] = f

base = {p: gate.show(LANE, REV, p) for p in FILES}
out = {}
for name, new in variants.items():
    files = dict(base)
    files["SKILL.md"] = skill.replace(genuine, new, 1)
    assert files["SKILL.md"] != skill or name == "vF-block23-relabelled"
    d = os.path.join(SCRATCH, name)
    subprocess.run(["rm", "-rf", d], check=True)
    os.makedirs(d)
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    for k, v in (("user.email", "fx@round47"), ("user.name", "round47 fixture")):
        subprocess.run(["git", "-C", d, "config", k, v], check=True)
    assert subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                          capture_output=True, text=True).stdout.strip() == d
    for p, text in files.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full) or d, exist_ok=True)
        open(full, "w").write(text)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "commit", "-q", "-m", "fixture"], check=True)
    rev = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    out[name] = {"dir": d, "rev": rev}
    print(json.dumps({"variant": name, **out[name]}))
json.dump(out, open(os.path.join(SCRATCH, "fixtures2.json"), "w"), indent=1)
