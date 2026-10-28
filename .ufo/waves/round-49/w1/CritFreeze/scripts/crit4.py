import json, os, sys, subprocess, shutil, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crit as C
from crit import g, mkrepo, commit, FREEZE, BASE
res = {}
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
# S15b: replace-ref: X (touch) kept as real object; replacement X' has tree == FREEZE tree
d = mkrepo('S15b_replace_touch')
with open(os.path.join(d, 'tools/round-49/c2-mismatch.py'), 'a') as fh: fh.write('\n# probe\n')
g(d, 'add', '-A'); X = commit(d, 'touch c2-mismatch')
g(d, 'checkout', FREEZE, '--', 'tools/round-49/c2-mismatch.py'); g(d, 'add', '-A'); R = commit(d, 'restore')
tree = g(d, 'rev-parse', FREEZE + '^{tree}').stdout.decode().strip()
Xp = g(d, 'commit-tree', tree, '-p', FREEZE, '-m', 'X replaced').stdout.decode().strip()
g(d, 'replace', X, Xp)
C.FREEZE = FREEZE
res['S15b_replace_touch'] = {'X': X, 'X_replacement': Xp, 'rev': R,
    'walk_replace_on': {'log': g(d, 'log', '-m', '--diff-merges=first-parent', '--name-status', '--pretty=format:', FREEZE + '..' + R).stdout.decode().strip(),
                        'c1': C.c1_walk(d, R), 'c2': C.c2_walk(d, R)},
    'walk_replace_off': {'log': subprocess.run(['git', '-C', d, '-c', 'core.useReplaceRefs=false', 'log', '-m', '--diff-merges=first-parent', '--name-status', '--pretty=format:', FREEZE + '..' + R], capture_output=True).stdout.decode().strip()}}
print(json.dumps({'S15b': res['S15b_replace_touch']}, sort_keys=True))

# S17: altered counter run from OUTSIDE the lane against a clean REV (do-nothing tree = FREEZE).
os.makedirs(os.path.join(C.S, 'alt'), exist_ok=True)
src = open(os.path.join(C.S, 'frozen', 'c2-mismatch.py')).read()
alt = src.replace("ATOMS = {'A1': a1,", "ATOMS = {'A1': (lambda r, rev, L: []), 'A1x': a1,", 1)
# force every atom green: replace the score() body's result with empty results
alt2 = src.replace('def score(r, rev):\n    L = lesson_lines(r, rev)\n    res = {}',
                   'def score(r, rev):\n    L = lesson_lines(r, rev)\n    return {k: [] for k in ATOM_IDS}\n    res = {}', 1)
assert alt2 != src
open(os.path.join(C.S, 'alt', 'c2-mismatch-altered.py'), 'w').write(alt2)
rev = g(d, 'rev-parse', FREEZE).stdout.decode().strip()
clean = mkrepo('S17_clean_at_freeze')
out = {}
for label, path in [('frozen_bytes', os.path.join(C.S, 'frozen', 'c2-mismatch.py')),
                    ('altered_bytes', os.path.join(C.S, 'alt', 'c2-mismatch-altered.py'))]:
    p = subprocess.run([sys.executable, '-I', '-B', path, '--root', clean, '--rev', FREEZE, '--freeze', FREEZE],
                       capture_output=True, cwd=C.S, env=C.ENV)
    j = json.loads(p.stdout.decode())
    out[label] = {'path': path, 'sha256': sha(path), 'exit': p.returncode, 'mismatches': j.get('mismatches'),
                  'counter_sha256_in_output': j.get('counter_sha256')}
res['S17_altered_counter_outside_lane'] = out
print(json.dumps({'S17': out}, sort_keys=True))

# S19: receipt identity self-check: a receipt stamped by an altered C1 copy verifies with --verify-receipt
alt1 = os.path.join(C.S, 'alt', 'c1-counter-altered.py')
shutil.copy(os.path.join(C.S, 'frozen', 'c1-counter.py'), alt1)
rec = os.path.join(C.S, 'alt', 'receipt-altered.json')
json.dump({'counter': alt1, 'counter_sha256': sha(alt1), 'exit_code': 0, 'carriers_matched': 4}, open(rec, 'w'))
p = subprocess.run([sys.executable, '-I', '-B', os.path.join(C.S, 'frozen', 'c1-counter.py'), '--verify-receipt', rec],
                   capture_output=True, cwd=C.S, env=C.ENV)
res['S19_verify_receipt_altered_counter'] = {'exit': p.returncode, 'stdout': p.stdout.decode().strip(), 'freeze_c1_sha256': sha(os.path.join(C.S, 'frozen', 'c1-counter.py')), 'altered_sha256': sha(alt1)}
print(json.dumps({'S19': res['S19_verify_receipt_altered_counter']}, sort_keys=True))
json.dump(res, open(os.path.join(C.S, 'results-walk4.json'), 'w'), indent=1, sort_keys=True)
