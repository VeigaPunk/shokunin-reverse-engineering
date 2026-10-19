#!/usr/bin/env python3
"""RV-4 real-target mutation: EX-16's LANDED census (sha 7b5a0e88...), H3 floor reverted only."""
import hashlib
import os

SRC = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/c1-census-v10.py"
W = "/var/tmp/rv4-mutation/work/"

LANDED_FLOOR = "    g2_ok = n_current_ok > 0\n"
MUTANT_FLOOR = ("    g2_ok = n_current_ok > 0 or "
                "(not stale and not unatt and not undecl and not unres)\n")
NEEDLES = [
    ('PIN = re.compile(r"rea-agents@(\\d+\\.\\d+\\.\\d+)", re.I)',
     'PIN = re.compile(r"rea-agents@(ZZZ\\d+)", re.I)'),
    ('VER = re.compile(r"(?<![\\d.])6\\.\\d+\\.\\d+")',
     'VER = re.compile(r"(?<![\\d.])9\\.\\d+\\.\\d+")'),
    ('PTR = re.compile(r"((?:~|/)[\\w./+-]+\\.(?:json|toml|ya?ml)):(\\d+)")',
     'PTR = re.compile(r"((?:~|/)ZZZ\\.(?:json|toml|ya?ml)):(\\d+)")'),
]
GATE_HEAD = ('REA_GATE = re.compile(r"rea-agents|\\brea\\b|config\\.toml|mcp_config\\.json|'
             'mcp\\.json|mcp_servers|devin|\\bomp\\b|kimi|npx", re.I)')
GATE_NEUT = 'REA_GATE = re.compile(r"ZZZ_never_matches_ZZZ")'


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


landed = open(SRC, encoding="utf-8").read()
print("landed sha256:", sha(SRC))
assert landed.count(LANDED_FLOOR) == 1, landed.count(LANDED_FLOOR)

open(W + "instr-landed.py", "w", encoding="utf-8").write(landed)
mutant = landed.replace(LANDED_FLOOR, MUTANT_FLOOR)
open(W + "instr-landed-nog2.py", "w", encoding="utf-8").write(mutant)


def neuter(text, needles=True, gate=True):
    for old, new in NEEDLES if needles else []:
        assert text.count(old) == 1, old
        text = text.replace(old, new)
    if gate:
        assert text.count(GATE_HEAD) == 1
        text = text.replace(GATE_HEAD, GATE_NEUT)
    return text


open(W + "instr-landed-neut.py", "w", encoding="utf-8").write(neuter(landed))
open(W + "instr-landed-nog2-neut.py", "w", encoding="utf-8").write(neuter(mutant))
open(W + "instr-landed-gate.py", "w", encoding="utf-8").write(neuter(landed, needles=False))
open(W + "instr-landed-nog2-gate.py", "w", encoding="utf-8").write(neuter(mutant, needles=False))

for f in ("instr-landed.py", "instr-landed-nog2.py", "instr-landed-neut.py",
          "instr-landed-nog2-neut.py", "instr-landed-gate.py", "instr-landed-nog2-gate.py"):
    print("%-26s %s" % (f, sha(W + f)))
