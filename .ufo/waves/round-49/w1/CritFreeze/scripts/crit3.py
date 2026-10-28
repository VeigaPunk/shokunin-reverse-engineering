import json, os, sys, subprocess, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crit as C
from crit import g, mkrepo, commit, write, FREEZE, BASE
res = {}
def head(d): return g(d, 'rev-parse', 'HEAD').stdout.decode().strip()
# (a) run the full C1 CLI (gate + measure) on the accepted-by-walk and on a control revision
for name in ['S0_benign_nonfrozen', 'S1a_touch_restore_c1counter', 'S2a_new_file_tools', 'S14_plain_copy_add']:
    d = os.path.join(C.S, 'sc', name); rev = head(d)
    C.FREEZE = FREEZE
    r = C.c1_cli(d, rev); res['cli:' + name] = {'rev': rev, 'c1_cli': r}
    print(json.dumps({'cli:' + name: r}, sort_keys=True), flush=True)
# (b) replace-ref attack: hide the touching commit X (edits c1-counter.py) and its restore R
d = mkrepo('S15_replace_ref')
with open(os.path.join(d, 'tools/round-49/c1-counter.py'), 'a') as fh: fh.write('\n# probe\n')
g(d, 'add', '-A'); X = commit(d, 'touch c1-counter')
g(d, 'checkout', FREEZE, '--', 'tools/round-49/c1-counter.py'); g(d, 'add', '-A'); R = commit(d, 'restore')
# fake X': same parent as X (FREEZE), tree = FREEZE tree (no visible change)
tree = g(d, 'rev-parse', FREEZE + '^{tree}').stdout.decode().strip()
fake = g(d, 'commit-tree', tree, '-p', FREEZE, '-m', 'fake X').stdout.decode().strip()
g(d, 'replace', X, fake)
# re-link R onto fake X so the chain reads F -> fake -> R
g(d, 'checkout', '-q', '--detach', R)
R2 = g(d, 'commit-tree', tree, '-p', fake, '-m', 'restore on fake').stdout.decode().strip()
g(d, 'replace', R, R2); rev = R2
C.FREEZE = FREEZE
print('replace list:', g(d, 'replace', '-l').stdout.decode().split())
print('log F..rev (replace on):', g(d, 'log', '-m', '--diff-merges=first-parent', '--name-status', '--pretty=format:', FREEZE + '..' + rev).stdout.decode().strip() or '<empty>')
print('log F..rev (GIT_NO_REPLACE_OBJECTS=1):', subprocess.run(['git','-C',d,'-c','core.useReplaceRefs=false','log','-m','--diff-merges=first-parent','--name-status','--pretty=format:',FREEZE+'..'+rev],capture_output=True).stdout.decode().strip() or '<empty>')
res['S15_replace_ref'] = {'rev': rev, 'X': X, 'R': R, 'c1_walk': C.c1_walk(d, rev), 'c2_walk': C.c2_walk(d, rev)}
print(json.dumps({'S15': res['S15_replace_ref']}, sort_keys=True))
# same clone with replace disabled for the counters (c2 uses git subprocess; c1 uses git()): env-level check
os.environ['GIT_NO_REPLACE_OBJECTS'] = '1'
res['S15_replace_ref_noreplace_env'] = {'c1_walk': C.c1_walk(d, rev), 'c2_walk': C.c2_walk(d, rev)}
del os.environ['GIT_NO_REPLACE_OBJECTS']
print(json.dumps({'S15_env': res['S15_replace_ref_noreplace_env']}, sort_keys=True))
# (c) grafts attack: .git/info/grafts cuts X's parent so X's change is never walked
d = mkrepo('S16_grafts')
with open(os.path.join(d, 'tools/round-49/c2-mismatch.py'), 'a') as fh: fh.write('\n# probe\n')
g(d, 'add', '-A'); X = commit(d, 'touch c2-mismatch')
g(d, 'checkout', FREEZE, '--', 'tools/round-49/c2-mismatch.py'); g(d, 'add', '-A'); R = commit(d, 'restore')
gp = os.path.join(d, '.git', 'info', 'grafts')
os.makedirs(os.path.dirname(gp), exist_ok=True)
open(gp, 'w').write(R + ' ' + FREEZE + '\n')   # R's parent becomes FREEZE; X is cut out of the walk
print('grafts log:', g(d, 'log', '-m', '--diff-merges=first-parent', '--name-status', '--pretty=format:', FREEZE + '..' + R).stdout.decode().strip() or '<empty>')
res['S16_grafts'] = {'rev': R, 'X': X, 'c1_walk': C.c1_walk(d, R), 'c2_walk': C.c2_walk(d, R)}
print(json.dumps({'S16': res['S16_grafts']}, sort_keys=True))
json.dump(res, open(os.path.join(C.S, 'results-walk3.json'), 'w'), indent=1, sort_keys=True)
