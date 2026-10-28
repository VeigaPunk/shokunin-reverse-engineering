#!/usr/bin/env python3
"""CritC1Predicate: build one-commit fixture repos carrying a VACUOUS craft block 24.

Each variant replaces the landed block 24 with rows that carry the right tokens and pins
but teach nothing (junk hole cells, arms permuted against their routed ids, every exit
cell claiming 0). The fixture repo is committed once, so freeze == rev, the only
configuration in which exact.py can reach its structural clauses.
"""
import hashlib
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = sys.argv[1] if len(sys.argv) > 1 else "e856beb5"
SCRATCH = os.environ.get("HYAKU_SCRATCH") or "/fast/scratch/hyaku/kaidoku-r47/CritC1Predicate"
sys.path.insert(0, os.path.join(LANE, "tools", "round-47"))
sys.path.insert(0, os.path.join(LANE, "tools", "round-46"))
import exact  # noqa: E402
import gate  # noqa: E402

FILES = ["SKILL.md", "plans/round-47-claims.md", "tools/round-47/exact.py",
         "tools/round-46/gate.py", "corpus/lessons/round-46.md",
         "corpus/lessons/round-45.md"]


def git(*args, cwd=None):
    return subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True)


def fixture(name, files, root):
    d = os.path.join(root, name)
    subprocess.run(["rm", "-rf", d], check=True)
    os.makedirs(d)
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    for k, v in (("user.email", "fx@round47"), ("user.name", "round47 fixture")):
        subprocess.run(["git", "-C", d, "config", k, v], check=True)
    top = git("rev-parse", "--show-toplevel", cwd=d).stdout.strip()
    assert top == d, (top, d)
    for p, text in files.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full) or d, exist_ok=True)
        with open(full, "w") as fh:
            fh.write(text)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "commit", "-q", "-m", "fixture: vacuous block 24"],
                   check=True)
    rev = git("rev-parse", "HEAD", cwd=d).stdout.strip()
    return d, rev


PIN = hashlib.sha256(gate.show(LANE, REV, "tools/round-47/exact.py").encode()).hexdigest()
DIGEST = exact.MUT_DIGEST

HEADER = "| trigger | v2 hole | v3 arm | exit |\n|---|---|---|---|\n"


def block(rows, refs, prose="An exactness matrix.", title="24. An exactness matrix."):
    body = (f"{title}** {exact.MARKER} `tools/round-47/exact.py` "
            f"interpreter_sha256:{PIN} mutations_sha256:{DIGEST} names "
            "substring-arm, duplicate-routed-id, stale-mutations-digest, "
            "flag-order-drift.\n\n" + prose + "\n\n" + HEADER)
    for r in rows:
        body += "| " + " | ".join(r) + " |\n"
    return body + f"\n  Refs: {refs}\n"


VARIANTS = {
    # A: minimum that satisfies every structural clause — junk hole cells, arms permuted
    # against their routed ids, every exit cell claiming "met" for a defect that exists.
    "vA-junk-holes-permuted-arms": block(
        [["R46-CL2", "n/a", "order", "0"],
         ["R46-CL3", "n/a", "symbol", "0"],
         ["R46-CL4", "n/a", "once", "0"],
         ["R46-CL6", "n/a", "digest", "0"]],
        "`corpus/lessons/round-46.md:1`, `corpus/lessons/round-46.md:1`, "
        "`corpus/lessons/round-46.md:1`"),
    # B: hole cells empty outright, single-word filler elsewhere.
    "vB-empty-holes": block(
        [["R46-CL2", "", "digest", "2"],
         ["R46-CL3", "", "order", "2"],
         ["R46-CL4", "", "symbol", "2"],
         ["R46-CL6", "", "once", "2"]],
        "`corpus/lessons/round-46.md:57-66`, `plans/round-47-claims.md:1`, "
        "`tools/round-47/exact.py`"),
    # C: the same three citations repeated three times (count, not coverage).
    "vC-repeated-refs": block(
        [["R46-CL2", "x", "symbol", "1"],
         ["R46-CL3", "x", "once", "1"],
         ["R46-CL4", "x", "digest", "1"],
         ["R46-CL6", "x", "order", "2"]],
        "`corpus/lessons/round-46.md:57-66`, `corpus/lessons/round-46.md:57-66`, "
        "`corpus/lessons/round-46.md:57-66`"),
    # D: no distinctness — every arm cell is the same vocabulary token.
    "vD-same-arm-four-times": block(
        [["R46-CL2", "?", "symbol", "0"],
         ["R46-CL3", "?", "symbol", "0"],
         ["R46-CL4", "?", "symbol", "0"],
         ["R46-CL6", "?", "symbol", "0"]],
        "`corpus/lessons/round-46.md:57-66`, `plans/round-47-claims.md:1`, "
        "`corpus/lessons/round-46.md:57-66`"),
    # E: nothing but the pins, a filler table and a title that names no subject.
    "vE-titleless-nonsense": block(
        [["R46-CL2", "", "order", "1"],
         ["R46-CL3", "", "symbol", "1"],
         ["R46-CL4", "", "once", "1"],
         ["R46-CL6", "", "digest", "1"]],
        "`corpus/lessons/round-46.md:1`, `plans/round-47-claims.md:1`, "
        "`tools/round-47/exact.py`",
        prose="", title="24. Shopping list."),
    # CONTROL: the landed block itself, unchanged, for the genuine battery exits.
    "control-genuine": None,
}

results = {}
skill_src = gate.show(LANE, REV, "SKILL.md")
real_block = exact.blocks_of(skill_src)[-1]
print("real block 24 title:", real_block.split("**", 1)[0])
print("PIN", PIN, "DIGEST", DIGEST)

base = {p: gate.show(LANE, REV, p) for p in FILES}
assert all(v is not None for v in base.values()), [k for k, v in base.items() if v is None]

for name, new in VARIANTS.items():
    files = dict(base)
    if new is not None:
        files["SKILL.md"] = skill_src.replace(real_block, new, 1)
        assert files["SKILL.md"] != skill_src
    d, rev = fixture(name, files, SCRATCH)
    results[name] = {"fixture": d, "rev": rev}
    print(json.dumps({"variant": name, "fixture": d, "rev": rev}))

print(json.dumps(results))
