#!/usr/bin/env python3
"""Independent regeneration check: freeze generator blobs, seed=freeze, compare to committed."""
import hashlib, json, os, shutil, subprocess, sys

L = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
REV = '42c10a58cb2cae3a4a0122af35a0cf95ac718043'
FREEZE = '7fce308631a8b457d6b7c5a4b39a923c4e9a49de'
S = os.environ['S']
WORK = os.path.join(S, 'regen')
shutil.rmtree(WORK, ignore_errors=True)
os.makedirs(WORK)
TREE = os.path.join(WORK, 'tree')
OUT = os.path.join(WORK, 'out')


def show(rev, path):
    p = subprocess.run(['git', '-C', L, 'show', '%s:%s' % (rev, path)], capture_output=True)
    if p.returncode:
        raise SystemExit('missing %s at %s' % (path, rev[:8]))
    return p.stdout


def materialise():
    p = subprocess.run(['git', '-C', L, 'ls-tree', '-r', '--name-only', FREEZE,
                        '--', 'tools/round-40', 'tools/round-39'],
                       capture_output=True, text=True)
    n = 0
    for rel in p.stdout.split():
        dest = os.path.join(TREE, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, 'wb') as fh:
            fh.write(show(FREEZE, rel))
        n += 1
    return n


print('materialised', materialise(), 'freeze blobs')
gen = os.path.join(TREE, 'tools/round-40/heldout-gen-v2.py')
writer = os.path.join(TREE, 'tools/round-39/gen-squashfs.py')
env = dict(os.environ)
env['KAIDOKU_GEN_SQUASHFS'] = writer
env['TMPDIR'] = os.path.join(WORK, 'tmp')
os.makedirs(env['TMPDIR'], exist_ok=True)
p = subprocess.run([sys.executable, '-I', '-B', gen, '--seed', FREEZE, '--out', OUT],
                   cwd=TREE, capture_output=True, text=True, env=env)
print('generator exit', p.returncode)
if p.returncode:
    print(p.stderr[-3000:])
    raise SystemExit(1)
rman = json.load(open(os.path.join(OUT, 'manifest.json')))
cman = json.loads(show(REV, 'corpus/evidence/round-40/c2/heldout/manifest.json'))
print('regen seed', rman.get('seed'))
print('regen carriers', len(rman.get('carriers') or []), 'committed', len(cman['carriers']))
bad = []
for rc, cc in zip(rman['carriers'], cman['carriers']):
    fp = os.path.join(OUT, rc['carrier'])
    sha = hashlib.sha256(open(fp, 'rb').read()).hexdigest() if os.path.isfile(fp) else None
    if sha != cc['sha256'] or rc['id'] != cc['id'] or rc.get('label') != cc.get('label') \
            or rc.get('action') != cc.get('action') or rc.get('class') != cc.get('class'):
        bad.append((cc['id'], sha, cc['sha256']))
print('sha/label/action mismatches:', len(bad))
for b in bad[:8]:
    print('  ', b)
committed_env = {}
for cc in cman['carriers']:
    d = cc['carrier'].split('/')[0]
    committed_env[cc['id']] = (d, cc['label'], cc['action'], cc['sha256'])
print('all 26 regenerated identical:',
      not bad and len(rman['carriers']) == 26)
