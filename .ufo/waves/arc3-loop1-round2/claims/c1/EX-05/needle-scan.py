#!/usr/bin/env python3
"""EX-05 (c1, round 2): independent gated-token scan over a diff.

Reads a unified diff on stdin (or a file + the added lines are computed from
it) and applies the census v10 needle vocabulary to every ADDED line, plus the
unit-level gate the census uses (a unit is a locus only if it matches REA_GATE
AND holds at least one needle).

Usage: python3 needle-scan.py <diff-file>
Exit 0 if no added line carries a needle; exit 1 if any does (each printed).
"""
import re
import sys

PIN = re.compile(r"rea-agents@(\d+\.\d+\.\d+)", re.I)
VER = re.compile(r"(?<![\d.])6\.\d+\.\d+")
PTR = re.compile(r"((?:~|/)[\w./+-]+\.(?:json|toml|ya?ml)):(\d+)")
CACHE = re.compile(r"_npx/([0-9a-f]{6,})")
REA_GATE = re.compile(
    r"rea-agents|\brea\b|config\.toml|mcp_config\.json|mcp\.json|mcp_servers|"
    r"devin|\bomp\b|kimi|npx", re.I)
NEEDLES = [("pin", PIN), ("bare", VER), ("ptr", PTR), ("cache", CACHE)]


def main(path):
    added = []
    for line in open(path, encoding="utf-8", errors="replace"):
        if line.startswith("+") and not line.startswith("+++"):
            added.append(line[1:].rstrip("\n"))
    hits = 0
    for n, text in enumerate(added, 1):
        for kind, pat in NEEDLES:
            for m in pat.finditer(text):
                hits += 1
                print("ADDED-LINE %d [%s] %r : %r" % (n, kind, m.group(0), text[:120]))
        if REA_GATE.search(text):
            has = any(p.search(text) for _, p in NEEDLES)
            print("ADDED-LINE %d [gate%s] %r" % (n, "+needle" if has else "-only", text[:120]))
    print("added_lines=%d needle_hits=%d" % (len(added), hits))
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
