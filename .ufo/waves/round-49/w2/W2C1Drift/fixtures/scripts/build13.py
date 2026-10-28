import os, subprocess, json
S = '/fast/scratch/hyaku/kaidoku-r49/W2C1Drift'
L = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
REV = '29883d4ec35a31a8393c4ffb220888c44c0bb022'
BASE = 'e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9'
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1', TMPDIR=S, HYAKU_SCRATCH='/fast/scratch/hyaku')
def g(d, *a, env=None, check=True):
    p = subprocess.run(['git', '-C', d, *a], capture_output=True, env=env or ENV)
    if check and p.returncode != 0: raise SystemExit('git %s: %s' % (a, p.stderr.decode()))
    return p
d = os.path.join(S, 'fx', 'fx13-datesort')
subprocess.run(['rm', '-rf', d]); subprocess.run(['git', 'clone', '-q', '--shared', L, d], check=True, env=ENV)
top = g(d, 'rev-parse', '--show-toplevel').stdout.decode().strip(); assert os.path.realpath(top) == os.path.realpath(d)
g(d, 'config', 'user.name', 'w2c1drift-fixture'); g(d, 'config', 'user.email', 'w2c1drift-fixture@invalid')
g(d, 'checkout', '-q', '-B', 'main', REV)
g(d, 'checkout', '-q', '-b', 'pre', BASE)  # pre-freeze base: a branch that does NOT descend from the freeze
paths = ['corpus/evidence/round-49/c1/%s/after.json' % i for i in ('v1le', 'v1be', 'v2le', 'v2be')]
for p in paths:
    data = g(L, 'show', REV + ':' + p).stdout
    fp = os.path.join(d, p); os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, 'wb').write(data)
e2 = dict(ENV, GIT_AUTHOR_DATE='2026-10-28T23:00:00Z', GIT_COMMITTER_DATE='2026-10-28T23:00:00Z')
g(d, 'add', '-A'); g(d, 'commit', '-q', '-m', 'pre-freeze-branch add of receipts (committer date later than 4aabb0b)', env=e2)
pre = g(d, 'rev-parse', 'HEAD').stdout.decode().strip()
g(d, 'checkout', '-q', 'main')
g(d, 'merge', '-q', '--no-ff', '--no-edit', '-m', 'merge pre-freeze branch', 'pre')
head = g(d, 'rev-parse', 'HEAD').stdout.decode().strip()
print('fx13 pre=%s head=%s' % (pre, head))
idx = json.load(open(os.path.join(S, 'fx', 'index.json')))
idx['fx13-datesort'] = {'head': head, 'desc': 'receipts also added on a branch from BASE (not descending from FREEZE), committer date later than 4aabb0b; merged'}
json.dump(idx, open(os.path.join(S, 'fx', 'index.json'), 'w'), indent=1, ensure_ascii=False)
print(g(d, 'log', '--format=%H %P %cI %s', '-n', '4', 'HEAD').stdout.decode())
print('first-add order:', g(d, 'log', '--diff-filter=A', '--format=%H %cI', REV, '--', paths[0]).stdout.decode())
print('first-add order at head:', g(d, 'log', '--diff-filter=A', '--format=%H %cI', head, '--', paths[0]).stdout.decode())
