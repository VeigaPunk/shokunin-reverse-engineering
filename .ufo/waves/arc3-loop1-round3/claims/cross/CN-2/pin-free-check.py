#!/usr/bin/env python3
"""PIN-FREE discipline checker (cross seat CN-2, arc3-loop1-round3).

Strict reading (round-2 precedent, `.ufo/waves/arc3-loop1-round2/claims/cross/
CN-2/pin-free-check.py`): the appended records text must carry ZERO
census-locus tokens anywhere, so no unit (present or future, after any merge)
can turn into an UNDECLARED locus past the census scope bound. Token families
mirror the census detectors in the landed instrument
`.ufo/gates/c1-census-v10.py`:
  PIN   :239  rea-agents@x.y.z
  VER   :240  bare 6.x.y (digit-boundary guarded)
  PTR   :241  ~/ or / absolute .json/.toml/.yaml path:line
  CACHE :242  _npx/<hex> (soft: not a locus, prefer removal)
Unit-level mode additionally replays the census `units()`/`REA_GATE` reach
(.ufo/gates/c1-census-v10.py:243,266-281) and reports which appended units the
census gate would even look at.

Usage: pin-free-check.py [--units] <file.md> [more files...]
Exit 0 = clean; 1 = violations.
"""
import re, sys

PIN   = re.compile(r"rea-agents@(\d+\.\d+\.\d+)", re.I)
VER   = re.compile(r"(?<![\d.])6\.\d+\.\d+")
PTR   = re.compile(r"((?:~|/)[\w./+-]+\.(?:json|toml|ya?ml)):(\d+)")
CACHE = re.compile(r"_npx/([0-9a-f]{6,})")
GATE  = re.compile(r"rea-agents|\brea\b|config\.toml|mcp_config\.json|mcp\.json|mcp_servers|devin|\bomp\b|kimi|npx", re.I)
SECTION = re.compile(r"^#{1,4} ")
BULLET  = re.compile(r"^\s*[-*] ")


def units(lines):
    i, n = 0, len(lines)
    while i < n:
        if not lines[i].strip():
            i += 1
            continue
        if SECTION.match(lines[i]) or lines[i].lstrip().startswith("|"):
            yield (i, i, lines[i].strip())
            i += 1
            continue
        j = i + 1
        while j < n and lines[j].strip() and not SECTION.match(lines[j]) \
                and not lines[j].lstrip().startswith("|") and not BULLET.match(lines[j]):
            j += 1
        yield (i, j - 1, " ".join(lines[k].strip() for k in range(i, j)))
        i = j


def scan(path):
    txt = open(path, encoding="utf-8", errors="replace").read()
    lines = txt.splitlines()
    hard, soft = [], []
    for i, ln in enumerate(lines, 1):
        for m in PIN.finditer(ln):   hard.append((i, "PIN", m.group(0)))
        for m in VER.finditer(ln):   hard.append((i, "VER", m.group(0)))
        for m in PTR.finditer(ln):   hard.append((i, "PTR", m.group(0)))
        for m in CACHE.finditer(ln): soft.append((i, "CACHE", m.group(0)))
    return txt, lines, hard, soft


show_units = False
argv = [a for a in sys.argv[1:] if a != "--units"]
show_units = "--units" in sys.argv[1:]

rc = 0
for path in argv:
    txt, lines, hard, soft = scan(path)
    gates = len(GATE.findall(txt))
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
    if show_units:
        reach = [(a + 1, b + 1) for (a, b, t) in units(lines) if GATE.search(t)]
        print("   census-reachable units (would be classified): %s"
              % (reach if reach else "none"))
print("PIN_FREE_VERDICT: %s" % ("FAIL" if rc else "CLEAN"))
sys.exit(rc)