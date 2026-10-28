import os, subprocess, json, sys
S = '/fast/scratch/hyaku/kaidoku-r49/W2C1Drift'
L = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
REV = '29883d4ec35a31a8393c4ffb220888c44c0bb022'
BASE = 'e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9'
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1', TMPDIR=S, HYAKU_SCRATCH='/fast/scratch/hyaku')
def g(d, *a, env=None, check=True):
    p = subprocess.run(['git', '-C', d, *a], capture_output=True, env=env or ENV)
    if check and p.returncode != 0: raise SystemExit('git %s: %s' % (a, p.stderr.decode()))
    return p
paths = ['corpus/evidence/round-49/c1/%s/after.json' % i for i in ('v1le', 'v1be', 'v2le', 'v2be')]
idx = json.load(open(os.path.join(S, 'fx', 'index.json')))
for name, pdate in [('fx14a-datesort-later', '2026-10-28T23:00:00Z'), ('fx14b-datesort-earlier', '2026-10-28T20:00:00Z')]:
    d = os.path.join(S, 'fx', name)
    subprocess.run(['rm', '-rf', d]); subprocess.run(['git', 'clone', '-q', '--shared', L, d], check=True, env=ENV)
    assert os.path.realpath(g(d, 'rev-parse', '--show-toplevel').stdout.decode().strip()) == os.path.realpath(d)
    g(d, 'config', 'user.name', 'w2c1drift-fixture'); g(d, 'config', 'user.email', 'w2c1drift-fixture@invalid')
    g(d, 'checkout', '-q', '-B', 'main', REV)
    g(d, 'rm', '-q', *paths); g(d, 'commit', '-q', '-m', 'delete receipts (main)')
    g(d, 'checkout', '-q', '-b', 'pre', BASE)
    for p in paths:
        fp = os.path.join(d, p); os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, 'wb').write(g(L, 'show', REV + ':' + p).stdout)
    e2 = dict(ENV, GIT_AUTHOR_DATE=pdate, GIT_COMMITTER_DATE=pdate)
    g(d, 'add', '-A'); g(d, 'commit', '-q', '-m', 'pre-freeze-branch add (date %s)' % pdate, env=e2)
    g(d, 'checkout', '-q', 'main')
    g(d, 'merge', '-q', '--no-ff', '--no-edit', '-m', 'merge pre branch', 'pre')
    head = g(d, 'rev-parse', 'HEAD').stdout.decode().strip()
    idx[name] = {'head': head, 'desc': 'receipts deleted on main then re-added via a branch from BASE with committer date %s; merged' % pdate}
    print(name, head)
    print(g(d, 'log', '--diff-filter=A', '--format=%h %cI %s', head, '--', paths[0]).stdout.decode())
json.dump(idx, open(os.path.join(S, 'fx', 'index.json'), 'w'), indent=1, ensure_ascii=False)
