#!/usr/bin/env python3
"""CriticC2 scratch: fg3 = fg2 (pure oracle caller, alias) with the packheader-not-found refusal relabelled."""
import shutil

S = "/fast/scratch/hyaku/kaidoku-r99/CriticC2"
CL = S + "/clone"
SRC = CL + "/tools/round-99/critic/fg2-oracle-only-alias.py"
OUT = CL + "/tools/round-99/critic/fg3-oracle-relabel.py"
s = open(SRC, encoding="utf-8").read()
OLD = '        raise Refuse("packheader-candidates:%d" % len(found))'
assert s.count(OLD) == 1
s = s.replace(OLD, '        raise Refuse("truncated: packheader-candidates:%d" % len(found))', 1)
open(OUT, "w", encoding="utf-8").write(s)
shutil.copyfile(OUT, S + "/cands/fg3-oracle-relabel.py")
print("fg3 written", len(s))
