import sys, os, json, subprocess
sys.path.insert(0, '/fast/scratch/hyaku/kaidoku-r49/W2C2Forge')
import forge as f
from forge import rep, line_rep, SRC, L, C, R, F, ENV, g, wr, commit
import mut as mm
def n46(): line_rep(SRC, r'^\| S147 \|', lambda l: l.replace('if a theory is incompatible with possible empirical observations it is scientific', 'if a theory is incompatible with possible empirical observations it is unscientific', 1))
def n47(): rep(L, 'log_c093e798=3440,3441,3445 ', 'log_c093e798=3440,3441,3445 log_12345678=3440 ')
EX = [('N46', 'S147 quote altered by one word, count kept at 21 (quote not in snapshot)', 'red A6 (quote not in snapshot)', n46),
      ('N47', 'A3 line carries an extra log_ key not in the required set', 'red A3', n47)]
res = []
for label, desc, expect, fn in EX:
    f.reset(); fn(); msg = f.commit('forgery ' + label)
    p = f.ctr('HEAD', F, False, tag=label)
    print(label, 'frozen exit', p['exit'], 'red', p['red'], '|', expect, '|', (p['why'].get(p['red'][0]) if p['red'] else ''))
    res.append(dict(label=label, desc=desc, expect=expect, commit=msg, plain=p))
json.dump(res, open(os.path.join(f.OUT, 'results-extra4.json'), 'w'), indent=1, default=str)
src = subprocess.run(['git', '-C', C, 'show', F + ':tools/round-49/c2-mismatch.py'], capture_output=True, env=ENV).stdout.decode()
for mid, lab in [('M06', 'N47'), ('M39', 'N46')]:
    desc, old, new = [(d, o, n) for (i, d, o, n) in mm.M if i == mid][0]
    text = src.replace(old, new); mp = os.path.join(f.S, 'mut', mid + '.py'); open(mp, 'w').write(text)
    fc = [r['commit'] for r in res if r['label'] == lab][0]
    g('checkout', '-q', '-f', '--detach', F); g('clean', '-fdq'); wr('tools/round-49/c2-mismatch.py', text); X = commit('mutant ' + mid)
    paths = [p for p in g('diff', '--name-only', F, fc).stdout.decode().split('\n') if p and not p.startswith('tools/round-49') and not p.startswith('plans/')]
    g('checkout', '-q', fc, '--', *paths); Y = commit('chain')
    p = f.ctr(Y, X, False, ctrpath=mp, tag='%s-%s' % (mid, lab))
    print('MUTANT', mid, 'with', lab, 'exit', p['exit'], 'red', p['red'], '| PASSES' if p['exit'] == 0 else '| caught')
