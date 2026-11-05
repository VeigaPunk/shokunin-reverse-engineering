#!/usr/bin/env python3
"""CriticC2 scratch: pure oracle-caller forgery fg2 (arithmetic disabled, static screen evaded by alias)."""
import shutil

S = "/fast/scratch/hyaku/kaidoku-r99/CriticC2"
CL = S + "/clone"
OUT = CL + "/tools/round-99/critic/fg2-oracle-only-alias.py"
base = open(CL + "/tools/round-99/upx-pe-repair.py", encoding="utf-8").read()
TRUNC = "    if len(b) < end:"
REPLACE = "        os.replace(tmp, a.out)"
assert base.count(TRUNC) == 1 and base.count(REPLACE) == 1
s = base.replace(TRUNC, "    if 0:", 1)
oracle = ('        import os as o\n'
          '        if o.system("/usr/bin/upx -t -q \'%s\' >/dev/null 2>&1" % tmp) != 0:\n'
          '            return refuse("truncated (oracle said no)", a.json)\n')
s = s.replace(REPLACE, oracle + REPLACE, 1)
open(OUT, "w", encoding="utf-8").write(s)
shutil.copyfile(OUT, S + "/cands/fg2-oracle-only-alias.py")
print("fg2 written", len(s))
