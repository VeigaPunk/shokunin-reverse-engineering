#!/usr/bin/env python3
"""Attribution control: floor intact, H3 diagnostic print reverted, needles neutered."""
import sys

sys.path.insert(0, "/var/tmp/rv4-mutation")
W = "/var/tmp/rv4-mutation/work/"

src = open(W + "instr-h3.py", encoding="utf-8").read()

PRINT_NEW = (
    '    print("G2 positive-assertion guard: %s (current-ok loci=%d, total loci=%d)" %\n'
    '          ("ok" if g2_ok else "SUSPECT", len(out.get("current-ok", [])),\n'
    '           sum(c["loci"] for c in counts.values())))\n'
)
PRINT_OLD = '    print("G2 positive-assertion guard: %s" % ("ok" if g2_ok else "SUSPECT"))\n'
assert src.count(PRINT_NEW) == 1
t = src.replace(PRINT_NEW, PRINT_OLD)

NEEDLES = [
    ('PIN = re.compile(r"rea-agents@(\\d+\\.\\d+\\.\\d+)", re.I)',
     'PIN = re.compile(r"rea-agents@(ZZZ\\d+)", re.I)'),
    ('VER = re.compile(r"(?<![\\d.])6\\.\\d+\\.\\d+")',
     'VER = re.compile(r"(?<![\\d.])9\\.\\d+\\.\\d+")'),
    ('PTR = re.compile(r"((?:~|/)[\\w./+-]+\\.(?:json|toml|ya?ml)):(\\d+)")',
     'PTR = re.compile(r"((?:~|/)ZZZ\\.(?:json|toml|ya?ml)):(\\d+)")'),
]
for old, new in NEEDLES:
    assert t.count(old) == 1, old
    t = t.replace(old, new)

open(W + "instr-h3-noprint-neut.py", "w", encoding="utf-8").write(t)
print("built instr-h3-noprint-neut.py (floor intact, print reverted, needles neutered)")
