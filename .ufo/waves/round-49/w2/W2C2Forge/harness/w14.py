import os, subprocess, json, sys
sys.path.insert(0, '/fast/scratch/hyaku/kaidoku-r49/W2C2Forge')
import forge as f
from forge import g, wr, rd, C, R, F, ENV, ctr, commit, reset
src = subprocess.run(['git', '-C', C, 'show', F + ':tools/round-49/c2-mismatch.py'], capture_output=True, env=ENV).stdout.decode()
old = "'A4': a4, "
assert src.count(old) == 1, src.count(old)
spoof = src.replace(old, "'A4': (lambda r, rev, L, dups: []), ")
spath = os.path.join(f.S, 'c2-spoof.py'); open(spath, 'w').write(spoof)
assert g('rev-parse', '--show-toplevel').stdout.decode().strip() == C
g('checkout', '-q', '-f', '--detach', F); g('clean', '-fdq')
wr('tools/round-49/c2-mismatch.py', spoof)
X = commit('spoof: counter with A4 disabled (operator-chosen freeze)')
paths = [p for p in g('diff', '--name-only', F, R).stdout.decode().split('\n') if p and not p.startswith('tools/round-49') and not p.startswith('plans/')]
g('checkout', '-q', R, '--', *paths)
for p in paths:
    pass
f.reset  # noop reference
# W03 record edit: results json drops 3 seats, lesson restates A4 seats=72
import json as j
d = j.loads(subprocess.run(['git', '-C', C, 'show', R + ':.ufo/waves/round-48/r48-w1-results.json'], capture_output=True, env=ENV).stdout)
d['results'] = d['results'][:-3]
wr('.ufo/waves/round-48/r48-w1-results.json', j.dumps(d, indent=1))
f.line_rep('corpus/lessons/round-49.md', r'^- A4 ', lambda l: '- A4 seats=72 reports=72 missing=')
Y = commit('spoofed-freeze record: W03 edit on top of spoofed counter')
print('X', X, 'Y', Y, 'paths restored', len(paths))
print('spoof-freeze', json.dumps({k: v for k, v in ctr('HEAD', X, False, ctrpath=spath, tag='W14-spoof-freeze').items()}, default=str))
print('spoof-battery-n/a')
print('real-freeze', json.dumps(ctr('HEAD', F, False, ctrpath=spath, tag='W14-spoof-realfreeze'), default=str))
print('frozen-counter-realfreeze', json.dumps(ctr('HEAD', F, False, tag='W14-frozen-realfreeze'), default=str))
