#!/usr/bin/env python3
"""PIN-FREE discipline checker (cross seat CN-2, arc3-loop1-round2).

Strict reading: the appended records text must carry ZERO census-locus tokens
anywhere, so no unit (present or future, after any merge) can turn into an
UNDECLARED locus past SCORECARD.md:855. Token families mirror the census v10
detectors at .ufo/gates/c1-census-v10.py:163-167, plus the census's own gate
vocabulary for context reporting.
Usage: pin-free.py <file.md> [more files...]
Exit 0 = clean; 1 = violations.
"""
import re, sys

PIN   = re.compile(r"rea-agents@(\d+\.\d+\.\d+)", re.I)
VER   = re.compile(r"(?<![\d.])6\.\d+\.\d+")
PTR   = re.compile(r"((?:~|/)[\w./+-]+\.(?:json|toml|ya?ml)):(\d+)")
CACHE = re.compile(r"_npx/([0-9a-f]{6,})")
GATE  = re.compile(r"rea-agents|\brea\b|config\.toml|mcp_config\.json|mcp\.json|mcp_servers|devin|\bomp\b|kimi|npx", re.I)

def scan(path):
    txt = open(path, encoding="utf-8", errors="replace").read()
    lines = txt.splitlines()
    hard, soft = [], []
    for i, ln in enumerate(lines, 1):
        for m in PIN.finditer(ln):   hard.append((i, "PIN", m.group(0)))
        for m in VER.finditer(ln):   hard.append((i, "VER", m.group(0)))
        for m in PTR.finditer(ln):   hard.append((i, "PTR", m.group(0)))
        for m in CACHE.finditer(ln): soft.append((i, "CACHE", m.group(0)))
    return hard, soft

rc = 0
for path in sys.argv[1:]:
    hard, soft = scan(path)
    gates = len(GATE.findall(open(path, encoding="utf-8", errors="replace").read()))
    print("== %s  (gate-token contexts: %d)" % (path, gates))
    if hard:
        rc = 1
        print("   PIN-FREE: FAIL  (%d locus token(s))" % len(hard))
        for i, k, v in hard:
            print("     line %d: %s %r" % (i, k, v))
    else:
        print("   PIN-FREE: CLEAN (0 pin/version/pointer tokens)")
    for i, k, v in soft:
        print("   note line %d: cache-hash-like %r (not a locus; prefer removal)" % (i, v))
print("PIN_FREE_VERDICT: %s" % ("FAIL" if rc else "CLEAN"))
sys.exit(rc)
