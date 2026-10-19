#!/usr/bin/env python3
"""RV-4 real-target mutation runner: rebuild variants from the LIVE census bytes,
run the matrix, and stamp every receipt with the tested sha256.

Floor revert (the only mutation):
    line 518  `    g2_ok = n_current_ok > 0`
  ->          `    g2_ok = n_current_ok > 0 or (not stale and not unatt and not undecl and not unres)`
"""
import hashlib
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
SRC = REPO + "/.ufo/gates/c1-census-v10.py"
W = "/var/tmp/rv4-mutation/work/"
R = "/var/tmp/rv4-mutation/receipts/"
TAG = sys.argv[1] if len(sys.argv) > 1 else "landed"

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


def neuter(text, needles=True, gate=False):
    for old, new in NEEDLES if needles else []:
        assert text.count(old) == 1, old
        text = text.replace(old, new)
    if gate:
        assert text.count(GATE_HEAD) == 1
        text = text.replace(GATE_HEAD, GATE_NEUT)
    return text


landed = open(SRC, encoding="utf-8").read()
src_sha = sha(SRC)
assert landed.count(LANDED_FLOOR) == 1, "floor line not uniquely found"
mutant = landed.replace(LANDED_FLOOR, MUTANT_FLOOR)

variants = {
    TAG: landed,
    TAG + "-nog2": mutant,
    TAG + "-neut": neuter(landed),
    TAG + "-nog2-neut": neuter(mutant),
    TAG + "-gate": neuter(landed, needles=False, gate=True),
    TAG + "-nog2-gate": neuter(mutant, needles=False, gate=True),
}
for name, text in variants.items():
    with open(W + name + ".py", "w", encoding="utf-8") as f:
        f.write(text)

print("tested source sha256: %s (%s)" % (src_sha, SRC))
for name in variants:
    out = R + name + ".out"
    with open(out, "w") as f:
        rc = subprocess.call([sys.executable, W + name + ".py", "--root", REPO],
                             stdout=f, stderr=subprocess.STDOUT)
    text = open(out).read()
    g2 = [l.strip() for l in text.splitlines() if "G2 positive" in l]
    dec = [l.strip() for l in text.splitlines() if "DECLARED FAIL CLASSES" in l]
    ver = [l.strip() for l in text.splitlines() if l.startswith("VERDICT") or "VERDICT:" in l]
    loci = [(l.split()[0], l.split("loci=")[1]) for l in text.splitlines() if "loci=" in l]
    print("%-20s sha=%s exit=%s %s | %s | %s | %s"
          % (name, sha(W + name + ".py")[:12], rc, g2, dec, ver, loci))
