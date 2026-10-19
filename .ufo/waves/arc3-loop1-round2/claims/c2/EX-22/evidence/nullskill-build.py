#!/usr/bin/env python3
"""EX-22 nullskill fixture builder (arc3-loop1-round2).

EX-14's `nullskill` fixture rebuilt from scratch: SKILL.md keeps 371 lines but
rows 10-20 are stripped of every needle (pins and bare versions), so the file
stays readable and gate-clean yet contributes zero loci. PROVINCE.md and
SCORECARD.md are copied verbatim from the pre-edit tree.

usage: nullskill-build.py <tree-pre-dir> <tree-nullskill-dir>
"""
import os
import re
import sys

src, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)
for f in ('PROVINCE.md', 'SCORECARD.md'):
    open(os.path.join(dst, f), 'w', encoding='utf-8').write(
        open(os.path.join(src, f), encoding='utf-8').read())
lines = open(os.path.join(src, 'SKILL.md'), encoding='utf-8').read().split('\n')
for i in range(9, 20):
    if i < len(lines):
        lines[i] = re.sub(r'rea-agents@\d+\.\d+\.\d+', 'rea-agents@X.Y.Z', lines[i])
        lines[i] = re.sub(r'(?<![\d.])6\.\d+\.\d+', 'X.Y.Z', lines[i])
open(os.path.join(dst, 'SKILL.md'), 'w', encoding='utf-8').write('\n'.join(lines))
print('nullskill written to %s' % dst)
