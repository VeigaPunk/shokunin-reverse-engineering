#!/usr/bin/env python3
"""Seat-local assembler: splices fragment files over line ranges of the pristine
round-41 counter (original numbering) and applies the mechanical token transforms
to every residual (non-fragment) line. Output = the round-50 counter draft."""
import glob, os, re, sys
SRC = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-41/c1-counter.py'
OUT = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-50/w1/C1CounterPort/tools/round-50/c1-counter.py'
FR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frag')
lines = open(SRC).read().split('\n')
if lines[-1] == '':
    lines.pop()
hunks = []
for p in glob.glob(FR + '/f*_*.txt'):
    m = re.match(r'f(\d+)_(\d+)', os.path.basename(p))
    hunks.append((int(m.group(1)), int(m.group(2)), p))
hunks.sort()
for (a, b, _), (c, d, _) in zip(hunks, hunks[1:]):
    assert b < c, ('overlap', a, b, c, d)

SELFTEST_FROM = 1800
MECH = [
    (r'R41-C1', 'R50-C1'), (r'kaidoku-r41', 'kaidoku-r50'),
    (r"plans/round-41-claims\.md", 'plans/round-50-claims.md'),
    (r'\.ufo/waves/round-41/c1/', 'tools/round-50/'),
    (r'corpus/evidence/round-41/c1', 'corpus/evidence/round-50/c1'),
    (r'tools/round-41/c1-counter\.py', 'tools/round-50/c1-counter.py'),
    (r'squashfs_v4_be_extract', 'squashfs_v4_le_extract'),
    (r'squashfs_v4 derivation', 'squashfs_v4_le derivation'),
    (r"'handler': 'squashfs_v4'", "'handler': HANDLER"),
    (r'sb_carrier\(GZIP_ID', 'sb_carrier(XZ_ID'),
]
IDMAP = {'V3': 'a7530', 'V4': 'a7590', 'L3': 'c6490', 'L4': 'c6430'}

def mech(line, lineno):
    for pat, rep in MECH:
        line = re.sub(pat, rep, line)
    if lineno >= SELFTEST_FROM:
        for k, v in IDMAP.items():
            line = re.sub(r'(?<![A-Za-z0-9_])' + k + r'(?![A-Za-z0-9_])', v, line)
    return line

out = []
i = 1
hi = 0
while i <= len(lines):
    if hi < len(hunks) and i == hunks[hi][0]:
        a, b, p = hunks[hi]
        body = open(p).read()
        out.append(body.rstrip('\n') if body.strip() else '')
        i = b + 1
        hi += 1
        continue
    out.append(mech(lines[i - 1], i))
    i += 1
open(OUT, 'w').write('\n'.join(out) + '\n')
print('wrote', OUT, len(out), 'lines; hunks', len(hunks))
