#!/usr/bin/env python3
"""C1Struct: the exit-2 paths that clause 1 depends on (malformed heading, frozen drift)."""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("HYAKU_SCRATCH", HERE)
src = open(os.path.join(HERE, "drive.py")).read().split('base = show("SKILL.md")')[0]
exec(compile(src, "drive.py:prefix", "exec"))  # noqa: S102 — scratch-only reuse

base = show("SKILL.md")
out = {"cases": []}

# (a) the craft heading loses its trailing space -> Malformed -> exit 2, never a verdict
malformed = insert_block(base, BLOCK_B).replace(
    "## Queue-drain craft (rounds 5-12", "## Queue-drain craft(rounds 5-12", 1)
files = fixture_files(malformed)
d, rev = exact._repo(files, S, prefix="c1struct-")
try:
    f = lambda p: gate.show(d, rev, p)  # noqa: E731
    code, rec = exact.score(files["SKILL.md"], f, "v3", rev, battery=None)
finally:
    shutil.rmtree(d, ignore_errors=True)
row = {"case": "malformed-craft-heading", "exit": code, "reason": rec.get("reason"),
       "failing": rec.get("failing")}
out["cases"].append(row)
print(json.dumps(row))

# (b) a frozen path changed after the freeze commit -> exit 2 frozen_path_changed
files = fixture_files(insert_block(base, BLOCK_B))
d, rev1 = exact._repo(files, S, prefix="c1struct-")
try:
    p = os.path.join(d, "tools/round-47/exact.py")
    with open(p, "a") as fh:
        fh.write("\n# drift\n")
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "commit", "-q", "-m", "drift"], check=True)
    rev2 = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], capture_output=True,
                          text=True).stdout.strip()
    code, rec = exact.evaluate(d, rev1, rev2, "v3", with_battery=False)
    row = {"case": "frozen-path-drift-after-freeze", "exit": code,
           "frozen_path_changed": rec.get("frozen_path_changed"),
           "reason": rec.get("reason"), "failing": rec.get("failing"),
           "freeze": rev1, "rev": rev2}
finally:
    shutil.rmtree(d, ignore_errors=True)
out["cases"].append(row)
print(json.dumps(row))

with open(os.path.join(HERE, "exit2.json"), "w") as fh:
    json.dump(out, fh, indent=1)
