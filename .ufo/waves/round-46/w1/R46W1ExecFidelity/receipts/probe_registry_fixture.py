#!/usr/bin/env python3
"""Build a fixture repo holding the L1's drafted registry section + the frozen census,
then let the caller run the FROZEN registry.py against it.

Usage: probe_registry_fixture.py <scratch-root>
Prints the fixture path and both commits.  Never writes outside scratch.
"""
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
DRAFT = os.path.join(LANE, ".ufo/waves/round-46/l1/registry-section.md")
CENSUS = os.path.join(HERE, "frozen/census.json")

base = sys.argv[1]
d = os.path.join(base, "fixture-reg")
shutil.rmtree(d, ignore_errors=True)
os.makedirs(d)


def git(*args):
    r = subprocess.run(["git", "-C", d, *args], capture_output=True, text=True)
    assert r.returncode == 0, (args, r.stderr)
    return r.stdout


subprocess.run(["git", "-C", d, "init", "-q"], check=True)
top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                     capture_output=True, text=True).stdout.strip()
assert top == d, (top, d)
git("config", "user.email", "fx@round46")
git("config", "user.name", "round46 fixture")

with open(CENSUS) as fh:
    census = json.load(fh)
paths = census["paths"]
with open(DRAFT) as fh:
    section = fh.read()
skill = "# SKILL\n\n## Queue-drain craft (fixture) \n\n- **22. plain.** body\n\n" + section + "\n## Next\n\ntail\n"


def put(rel, text):
    full = os.path.join(d, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as fh:
        fh.write(text)


put("SKILL.md", skill)
put("tools/round-46/census.json", json.dumps(census, indent=1) + "\n")
put("plans/round-46-claims.md",
    "# claims\n\n## Frozen paths (exact)\n\n- `plans/round-46-claims.md`\n- `tools/round-46/`\n")
for p in paths:
    put(p, "stub\n")
git("add", "-A")
git("commit", "-q", "-m", "fixture")
rev = git("rev-parse", "HEAD").strip()
print(json.dumps({"fixture": d, "freeze": rev, "rev": rev, "scope": len(paths)}))
