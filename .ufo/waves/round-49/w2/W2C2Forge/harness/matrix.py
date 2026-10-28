import sys, os, json, glob, subprocess
sys.path.insert(0, '/fast/scratch/hyaku/kaidoku-r49/W2C2Forge')
import forge as f
from forge import g, wr, C, R, F, ENV, ctr, commit, OUT, S
src = subprocess.run(['git', '-C', C, 'show', F + ':tools/round-49/c2-mismatch.py'], capture_output=True, env=ENV).stdout.decode()
import mut as mm
ALL = {}
for p in glob.glob(os.path.join(OUT, 'results-*.json')):
    for r in json.load(open(p)):
        ALL[r['label']] = r
POOL = {
 'A1': ['W04', 'N29', 'N45', 'N44'], 'A2': ['W11', 'N16', 'N43'], 'A3': ['W06', 'W12', 'N23'],
 'A4': ['W02', 'W03', 'W10', 'N31', 'N32'], 'A5': ['W05', 'N33'],
 'A6': ['N13', 'N15', 'N17', 'N24', 'N26', 'N27', 'N28', 'N34b', 'N35'],
 'A7': ['W13', 'N25', 'N36'], 'A8': ['N11', 'N12', 'N19', 'N20', 'N21', 'N22', 'N37', 'N39'], 'A9': ['N04', 'N18', 'N40']}
MUT_ATOMS = {'M01': ['A2'], 'M02': ['A2'], 'M03': ['A2'], 'M04': ['A2'], 'M06': ['A3'], 'M08': ['A3'], 'M09': ['A3'],
             'M10': ['A4'], 'M11': ['A4'], 'M13': ['A5'], 'M14': ['A5'], 'M15': ['A6'], 'M16': ['A6'], 'M19': ['A7'],
             'M21': ['A7'], 'M22': ['A8'], 'M23': ['A8'], 'M24': ['A8'], 'M25': ['A8'], 'M28': ['A9'], 'M29': ['A1'],
             'M30': ['A1'], 'M31': ['A1'], 'M32': ['A1'], 'M33': ['A1'], 'M34': ['A1'], 'M35': ['A6'], 'M36': ['A6'],
             'M37': ['A6'], 'M38': ['A6'], 'M39': ['A6'], 'M41': [], 'M42': [], 'M43': []}
genuine = {r['id']: r for r in json.load(open(os.path.join(OUT, 'mutants-genuine.json')))}
survivors = [m for m in MUT_ATOMS if m in genuine and genuine[m]['survives_genuine_REV']]
def chain(mid, text, fc):
    mp = os.path.join(S, 'mut', mid + '.py'); open(mp, 'w').write(text)
    g('checkout', '-q', '-f', '--detach', F); g('clean', '-fdq')
    wr('tools/round-49/c2-mismatch.py', text); X = commit('mutant ' + mid)
    paths = [p for p in g('diff', '--name-only', F, fc).stdout.decode().split('\n') if p and not p.startswith('tools/round-49') and not p.startswith('plans/')]
    if paths: g('checkout', '-q', fc, '--', *paths)
    Y = commit('chain %s on %s' % (mid, fc[:8]))
    return X, Y, mp
out = []
for mid in survivors:
    desc = [d for (i, d, o, n) in mm.M if i == mid][0]
    old, new = [(o, n) for (i, d, o, n) in mm.M if i == mid][0]
    text = src.replace(old, new)
    atoms = MUT_ATOMS[mid]
    labels = [l for a in atoms for l in POOL[a]]
    for lab in labels:
        fc = ALL[lab]['commit'] if lab in ALL else None
        if not fc:
            print('missing', lab); continue
        X, Y, mp = chain(mid, text, fc)
        p = ctr(Y, X, False, ctrpath=mp, tag='%s-%s' % (mid, lab))
        out.append(dict(mutant=mid, desc=desc, forgery=lab, X=X, Y=Y, exit=p['exit'], mismatches=p['mismatches'], red=p['red'], reason=p['reason'], stdout_sha=p['stdout_sha'], passes=p['exit'] == 0))
        print(mid, lab, 'exit', p['exit'], 'red', p['red'], 'reason', p['reason'], '| PASSES' if p['exit'] == 0 else '')
# M40 freeze walk: touch + restore inside FREEZE..REV
mid = 'M40'
old, new = [(o, n) for (i, d, o, n) in mm.M if i == 'M40'][0]
text = src.replace(old, new); mp = os.path.join(S, 'mut', 'M40.py'); open(mp, 'w').write(text)
g('checkout', '-q', '-f', '--detach', F); g('clean', '-fdq'); wr('tools/round-49/c2-mismatch.py', text); X = commit('mutant M40')
paths = [p for p in g('diff', '--name-only', F, R).stdout.decode().split('\n') if p and not p.startswith('tools/round-49') and not p.startswith('plans/')]
g('checkout', '-q', R, '--', *paths); commit('landed on M40')
wr('tools/round-49/c2-mismatch.py', text + '# touched\n'); commit('T1 touch tools/round-49 inside FREEZE..REV')
wr('tools/round-49/c2-mismatch.py', text); Y = commit('T2 restore the blob (touch not un-blocked by restore)')
p = ctr(Y, X, False, ctrpath=mp, tag='M40-T2')
out.append(dict(mutant='M40', desc='touch-and-restore inside FREEZE..REV', forgery='T2', X=X, Y=Y, exit=p['exit'], mismatches=p['mismatches'], red=p['red'], reason=p['reason'], passes=p['exit'] == 0))
print('M40 T2 (mutant)', 'exit', p['exit'], 'reason', p['reason'], '| PASSES' if p['exit'] == 0 else '')
p2 = ctr(Y, F, False, tag='T2-frozen')
print('T2 with the frozen counter and FREEZE', 'exit', p2['exit'], 'reason', p2['reason'])
json.dump(dict(rows=out, T2_frozen=dict(exit=p2['exit'], reason=p2['reason'], stdout_sha=p2['stdout_sha'])), open(os.path.join(OUT, 'matrix.json'), 'w'), indent=1, default=str)
