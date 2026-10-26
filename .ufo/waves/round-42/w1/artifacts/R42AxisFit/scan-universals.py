#!/usr/bin/env python3
"""Scan the round-42 draft claims for universal-quantifier wording.

Outputs one line per matched line: line number, the quantifier tokens found, and
the line text. The analysis (whether the set a quantifier ranges over is
enumerated by the claim's counting command) is in universals-enumeration.tsv.
"""
import re, sys

CLAIMS = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/plans/round-42-claims.md'
WORDS = re.compile(r'\b(all|complete|every|whole|any|never|always|each|no)\b|\b(at most one)\b', re.I)

def main():
    out = []
    with open(CLAIMS, encoding='utf-8') as fh:
        for ln, line in enumerate(fh, 1):
            toks = sorted({m.group(0).lower() for m in WORDS.finditer(line)})
            if toks:
                out.append((ln, ','.join(toks), line.rstrip()))
    for ln, toks, text in out:
        print(f'{ln}\t{toks}\t{text}')

if __name__ == '__main__':
    main()
