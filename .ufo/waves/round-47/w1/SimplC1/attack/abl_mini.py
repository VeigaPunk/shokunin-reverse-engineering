#!/usr/bin/env python3
"""Small ablations quoted in SimplC1's report (dead fixture entry, decorative battery
field, redundant marker-block-count clause, and the load-bearing A6 citation loop).

Each cut is applied to a COPY of tools/round-47/exact.py in scratch; the lane tree is
never touched. Run:  python3 -I -B abl_mini.py <scratch-root> <lane-root> <rev>
"""
import json
import os
import shutil
import subprocess
import sys

S, LANE, REV = sys.argv[1], sys.argv[2], sys.argv[3]
SRC = os.path.join(LANE, "tools", "round-47", "exact.py")
GATE = os.path.join(LANE, "tools", "round-46", "gate.py")
src = open(SRC).read()

CUTS = {
    "dead-round45-fixture": (', MUST_CITE, "corpus/lessons/round-45.md"', ", MUST_CITE"),
    "battery-digest-field": ('           "genuine_green": 0, "crash": 0, "mutations_sha256": MUT_DIGEST}',
                             '           "genuine_green": 0, "crash": 0}'),
    "c1-marker-block-count": ('        if len(marked) != 1:\n'
                              '            failing.append(f"marker_block_count {len(marked)} != 1")',
                              "        pass"),
    "a6-fixture-citation-loop": ('''    try:
        marked = [b for b in blocks_of(skill or "") if MARKER in b]
    except Malformed:
        marked = []
    if marked:
        for name, _, _ in HARD_REF.findall(marked[0]):
            if name not in out:
                body = gate.show(root, rev, name)
                if body is not None:
                    out[name] = body''', "    pass"),
}


def run(mod, extra):
    p = subprocess.run([sys.executable, "-I", "-B", mod, "--root", LANE, "--freeze",
                        "f54b3b6d", "--rev", REV, *extra], capture_output=True, text=True,
                       env=dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S))
    return p.returncode, p.stdout


out = {}
for name, (old, new) in CUTS.items():
    if old not in src:
        out[name] = {"error": "anchor not found"}
        continue
    d = os.path.join(S, "ablmin", name, "tools")
    os.makedirs(os.path.join(d, "round-47"), exist_ok=True)
    os.makedirs(os.path.join(d, "round-46"), exist_ok=True)
    mod = os.path.join(d, "round-47", "exact.py")
    open(mod, "w").write(src.replace(old, new, 1))
    shutil.copy(GATE, os.path.join(d, "round-46", "gate.py"))
    ec, body = run(mod, [])
    sec, sbody = run(mod, ["--selftest"])
    try:
        rec = json.loads(body)
        bat = rec.get("battery") or {}
    except Exception:
        rec, bat = {"raw": body[:200]}, {}
    out[name] = {"counter_exit": ec, "met": rec.get("met_target"), "failing": rec.get("failing"),
                 "genuine_green": bat.get("genuine_green"), "v2_green": bat.get("v2_green"),
                 "v3_green": bat.get("v3_green"), "selftest_exit": sec,
                 "selftest_head": (sbody.splitlines() or [""])[0]}
print(json.dumps(out, indent=1))
