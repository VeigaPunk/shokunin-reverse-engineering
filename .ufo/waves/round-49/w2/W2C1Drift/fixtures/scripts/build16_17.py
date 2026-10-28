import os, subprocess, json
S = '/fast/scratch/hyaku/kaidoku-r49/W2C1Drift'
L = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
REV = '29883d4ec35a31a8393c4ffb220888c44c0bb022'
FRZ = 'decc5697bfd4ec1e9de4a762ad199d9bd9c4230d'
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1', TMPDIR=S, HYAKU_SCRATCH='/fast/scratch/hyaku')
def g(d, *a, env=None, check=True, inp=None):
    p = subprocess.run(['git', '-C', d, *a], capture_output=True, env=env or ENV, input=inp)
    if check and p.returncode != 0: raise SystemExit('git %s: %s' % (a, p.stderr.decode()))
    return p
def fresh(name):
    d = os.path.join(S, 'fx', name)
    subprocess.run(['rm', '-rf', d]); subprocess.run(['git', 'clone', '-q', '--shared', L, d], check=True, env=ENV)
    assert os.path.realpath(g(d, 'rev-parse', '--show-toplevel').stdout.decode().strip()) == os.path.realpath(d)
    g(d, 'config', 'user.name', 'w2c1drift-fixture'); g(d, 'config', 'user.email', 'w2c1drift-fixture@invalid')
    g(d, 'checkout', '-q', '-B', 'main', REV)
    return d
idx = json.load(open(os.path.join(S, 'fx', 'index.json')))
# FX16: replacement ref hides a post-freeze frozen-file edit (disclosed limit; env defends)
d = fresh('fx16-replace')
man = 'tools/round-49/control-fixtures/pos/manifest.json'
orig = open(os.path.join(L, man), 'rb').read()
open(os.path.join(d, man), 'wb').write(orig + b'\n'); g(d, 'add', '-A'); g(d, 'commit', '-q', '-m', 'edit frozen manifest (to be replaced)')
X = g(d, 'rev-parse', 'HEAD').stdout.decode().strip()
tree = g(d, 'rev-parse', REV + '^{tree}').stdout.decode().strip()
Y = g(d, 'commit-tree', tree, '-p', REV, '-m', 'edit frozen manifest (to be replaced)').stdout.decode().strip()
g(d, 'replace', X, Y)
idx['fx16-replace'] = {'head': X, 'desc': 'frozen edit X replaced by Y (tree == REV); run with and without GIT_NO_REPLACE_OBJECTS'}
print('fx16 X', X, 'Y', Y)
# FX17: copy detection (diff.renames=copies) -> a frozen path ADDED as a copy
d = fresh('fx17-copy')
g(d, 'config', 'diff.renames', 'copies')
readme = open(os.path.join(L, 'corpus/README.md'), 'rb').read()
open(os.path.join(d, 'corpus/README.md'), 'wb').write(readme + b'\nw2 touch\n')
open(os.path.join(d, 'tools/round-49/copied-from-readme.md'), 'wb').write(readme)
g(d, 'add', '-A'); g(d, 'commit', '-q', '-m', 'copy into frozen dir')
H = g(d, 'rev-parse', 'HEAD').stdout.decode().strip()
idx['fx17-copy'] = {'head': H, 'desc': 'commit modifies corpus/README.md and adds tools/round-49/copied-from-readme.md (copy of old README); repo config diff.renames=copies'}
print('fx17 H', H)
print('raw counter-style walk (copies config):')
print(g(d, '-c', 'core.quotePath=false', 'log', '-m', '--diff-merges=first-parent', '--name-status', '--pretty=format:', FRZ + '..HEAD').stdout.decode())
json.dump(idx, open(os.path.join(S, 'fx', 'index.json'), 'w'), indent=1, ensure_ascii=False)
