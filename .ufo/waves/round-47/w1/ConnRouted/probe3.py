#!/usr/bin/env python3
"""E7: the v3-arm column binds a multiset, not an assignment — permute the arms."""
import json
import shutil
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r47/ConnRouted"
HEAD = "caafeffa330a15e59412bc037591f6942b51e5aa"
sys.path.insert(0, LANE + "/tools/round-47")
sys.path.insert(0, LANE + "/tools/round-46")
import gate          # noqa: E402
import exact         # noqa: E402

fx = exact._fixture_files(LANE, HEAD)
skill = fx["SKILL.md"]
block = [b for b in exact.blocks_of(skill) if exact.MARKER in b][0]
print("orig arm cells:", [r[2] for r in exact.table(block)[1]])
permuted = (skill.replace("| `symbol` | 1 |", "| `@T@` | 1 |", 1)
                 .replace("| `order` | 1 |", "| `symbol` | 1 |", 1)
                 .replace("| `@T@` | 1 |", "| `order` | 1 |", 1))
assert permuted != skill

for label, text in (("E7-baseline", skill), ("E7-arm-tokens-permuted-across-ids", permuted)):
    f = dict(fx)
    f["SKILL.md"] = text
    fd, frev = exact._repo(f, S)
    try:
        access = lambda p, _d=fd, _r=frev: gate.show(_d, _r, p)  # noqa: E731
        code, rec = exact.score(text, access, "v3", frev, battery=None)
        print(json.dumps({"label": label, "exit": code,
                          "arm_tokens": rec.get("arm_tokens"),
                          "routed_counts": rec.get("routed_counts"),
                          "failing": rec.get("failing")}, sort_keys=True))
    finally:
        shutil.rmtree(fd, ignore_errors=True)
