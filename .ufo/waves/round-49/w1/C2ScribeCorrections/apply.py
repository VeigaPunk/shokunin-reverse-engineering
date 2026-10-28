#!/usr/bin/env python3
"""Apply the C2 landing text to a scratch clone (never the lane). usage: apply.py <clone>
Commits "dev after (w1 C2)" in the clone only; prints DEV_AFTER=<hash>."""
import os, re, shutil, subprocess, sys

D = sys.argv[1]
T = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/w1/C2ScribeCorrections'
SNAP = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/draft/snapshots'
git = lambda *a: subprocess.run(['git', '-C', D] + list(a), capture_output=True, text=True, check=True).stdout
assert git('rev-parse', '--show-toplevel').strip() == D, 'not the clone'
rd = lambda p: open(os.path.join(D, p), encoding='utf8').read()
def wr(p, s):
    os.makedirs(os.path.dirname(os.path.join(D, p)), exist_ok=True)
    open(os.path.join(D, p), 'w', encoding='utf8').write(s)
txt = lambda f: open(os.path.join(T, f), encoding='utf8').read()

# 1. evidence snapshots (sha256-pinned in the S147/S148 rows)
os.makedirs(os.path.join(D, 'corpus/evidence/round-49/c2'), exist_ok=True)
for f in ('popper.html', 'sysexits.html'):
    shutil.copy(os.path.join(SNAP, f), os.path.join(D, 'corpus/evidence/round-49/c2', f))

# 2. lesson: the counter's LESSON path; the corrections section is the only content here
wr('corpus/lessons/round-49.md', '# Round 49 — lessons\n\nLane `kaidoku`, round 49. Base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`.\n\n' + txt('lesson-corrections.md'))

# 3. SOURCES: two supersession rows after the last S-row; search-log entries before Leads
lines = rd('corpus/SOURCES.md').split('\n')
row = re.compile(r'^ {0,3}\|\s*S\d{3,}\s*\|')
last = max(k for k, l in enumerate(lines) if row.match(l))
lines[last + 1:last + 1] = [l for l in txt('sources-rows.md').split('\n') if l.strip()]
k = lines.index('## Leads (unopened)')
lines[k:k] = [l for l in txt('search-log.md').split('\n') if l.strip()] + ['']
wr('corpus/SOURCES.md', '\n'.join(lines))

# 4. SCORECARD: append the correction section
wr('SCORECARD.md', rd('SCORECARD.md').rstrip('\n') + '\n\n' + txt('scorecard-section.md').rstrip('\n') + '\n')

git('add', '-A')
git('commit', '-q', '-m', 'dev after (w1 C2)')
print('DEV_AFTER=' + git('rev-parse', 'HEAD').strip())
