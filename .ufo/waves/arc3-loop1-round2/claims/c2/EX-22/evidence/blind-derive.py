#!/usr/bin/env python3
"""EX-22 blind-instrument derivation (arc3-loop1-round2).

Rule measured: neuter needle regexes by replacing the lines that start with
`PIN = re.compile(`, `VER = re.compile(`, `PTR = re.compile(` with
never-matching patterns. `--needles` selects which of the three to neuter
(all three = blind-all; PIN only = partial-blindness control).

usage: blind-derive.py <src.py> <dst.py> PIN,VER,PTR
"""
import sys

src, dst, needles = sys.argv[1], sys.argv[2], set(sys.argv[3].split(','))
lines = open(src, encoding='utf-8').read().split('\n')
n = 0
for i, l in enumerate(lines):
    for nd in needles:
        if l.startswith(nd + ' = re.compile('):
            lines[i] = '%s = re.compile(r"(?!)"%s)' % (nd, ', re.I' if nd == 'PIN' else '')
            n += 1
assert n == len(needles), (n, needles)
open(dst, 'w', encoding='utf-8').write('\n'.join(lines))
print('neutered %d needle(s) -> %s' % (n, dst))
