import json, hashlib, subprocess, os, stat, sys
L = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
REV = '29883d4ec35a31a8393c4ffb220888c44c0bb022'
FRZ = 'decc5697bfd4ec1e9de4a762ad199d9bd9c4230d'
C1 = 'corpus/evidence/round-49/c1'
ids = ['v1le', 'v1be', 'v2le', 'v2be']
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def git(*a, check=True):
    p = subprocess.run(['git', '-C', L, *a], capture_output=True, env=env)
    if check and p.returncode: raise SystemExit('git %s rc=%d %s' % (a, p.returncode, p.stderr[:300]))
    return p.stdout
def blob(path, rev=REV):
    p = subprocess.run(['git', '-C', L, 'show', f'{rev}:{path}'], capture_output=True, env=env)
    return p.stdout if p.returncode == 0 else None
def sha(b): return hashlib.sha256(b).hexdigest()
out = {}
# 1. tree listing at REV
lines = git('ls-tree', '-r', '-l', REV, '--', C1).decode().splitlines()
tree = {}
for ln in lines:
    meta, path = ln.split('\t', 1)
    mode, typ, oid, size = meta.split()
    tree[path] = dict(mode=mode, type=typ, oid=oid, size=int(size))
print('committed entries', len(tree), 'modes', sorted({v['mode'] for v in tree.values()}), 'types', sorted({v['type'] for v in tree.values()}))
# 2. disk walk
disk = {}
for dp, dn, fn in os.walk(os.path.join(L, C1)):
    for f in dn + fn:
        full = os.path.join(dp, f)
        rel = os.path.relpath(full, L)
        disk[rel] = dict(islink=os.path.islink(full), isdir=os.path.isdir(full) and not os.path.islink(full))
files_disk = {k for k, v in disk.items() if not v['isdir']}
print('disk files', len(files_disk), 'disk symlinks', [k for k, v in disk.items() if v['islink']], 'disk dirs', sorted(k for k,v in disk.items() if v['isdir']))
print('committed-not-on-disk', sorted(set(tree) - files_disk)[:20])
print('on-disk-not-committed', sorted(files_disk - set(tree))[:20])
# 3. per-file content equality committed vs disk
mism = []
for p in sorted(tree):
    cb = blob(p)
    if cb is None: mism.append((p, 'no-blob')); continue
    if sha(cb) != sha(open(os.path.join(L, p), 'rb').read()) if os.path.exists(os.path.join(L,p)) and not os.path.islink(os.path.join(L,p)) else True:
        mism.append((p, 'disk-differs-or-missing'))
    if len(cb) != tree[p]['size']: mism.append((p, 'size-vs-ls-tree'))
print('committed vs disk mismatches:', mism)
# 4. symlink / mode / type checks for the four trees
for i in ids:
    for p in tree:
        if p.startswith(f'{C1}/{i}/firmware.bin_extract/') and tree[p]['mode'] != '100644':
            print('NONREG-MODE', p, tree[p])
print('any 120000 in c1 tree:', [p for p,v in tree.items() if v['mode']=='120000'])
# 5. blob sizes > 1MiB
print('max blob size', max(v['size'] for v in tree.values()))
json.dump({'tree': tree}, open('tree.json', 'w'), indent=1)
