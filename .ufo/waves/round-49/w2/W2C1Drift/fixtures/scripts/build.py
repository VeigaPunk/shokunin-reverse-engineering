import os, subprocess, json, sys, shutil
S = '/fast/scratch/hyaku/kaidoku-r49/W2C1Drift'
L = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
REV = '29883d4ec35a31a8393c4ffb220888c44c0bb022'
FRZ = 'decc5697bfd4ec1e9de4a762ad199d9bd9c4230d'
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1', TMPDIR=S, HYAKU_SCRATCH='/fast/scratch/hyaku')

def g(d, *a, inp=None, check=True):
    p = subprocess.run(['git', '-C', d, *a], input=inp, capture_output=True, env=ENV)
    if check and p.returncode != 0:
        raise SystemExit('git %s failed: %s' % (' '.join(a), p.stderr.decode()))
    return p

def clone(name):
    d = os.path.join(S, 'fx', name)
    shutil.rmtree(d, ignore_errors=True)
    subprocess.run(['git', 'clone', '-q', '--shared', L, d], check=True, env=ENV)
    top = g(d, 'rev-parse', '--show-toplevel').stdout.decode().strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    g(d, 'config', 'user.name', 'w2c1drift-fixture')
    g(d, 'config', 'user.email', 'w2c1drift-fixture@invalid')
    g(d, 'checkout', '-q', '-B', 'main', REV)
    assert g(d, 'rev-parse', 'HEAD').stdout.decode().strip() == REV
    return d

def write(d, rel, data):
    p = os.path.join(d, rel.encode('utf-8', 'surrogateescape').decode('utf-8', 'surrogateescape'))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'wb') as fh:
        fh.write(data)

def commit(d, msg):
    g(d, 'add', '-A')
    g(d, 'commit', '-q', '--allow-empty', '-m', msg)
    return g(d, 'rev-parse', 'HEAD').stdout.decode().strip()

MAN = 'tools/round-49/control-fixtures/pos/manifest.json'
FX = {}

# FX0 control: no commits
d = clone('fx0-none'); FX['fx0-none'] = {'head': REV, 'desc': 'no commits (control)'}

# FX1 direct edit of a frozen manifest
d = clone('fx1-edit'); write(d, MAN, open(os.path.join(L, MAN), 'rb').read() + b'\n')
FX['fx1-edit'] = {'head': commit(d, 'edit frozen manifest'), 'desc': 'edit tools/round-49 manifest'}

# FX2 edit then restore
d = clone('fx2-restore'); orig = open(os.path.join(L, MAN), 'rb').read()
write(d, MAN, orig + b'\n'); commit(d, 'edit')
write(d, MAN, orig); FX['fx2-restore'] = {'head': commit(d, 'restore'), 'desc': 'edit then restore'}

# FX3 side-branch edit hidden by merge -s ours (merge TREESAME to first parent)
d = clone('fx3-ours')
g(d, 'checkout', '-q', '-b', 'side', REV)
write(d, MAN, orig + b'\n'); commit(d, 'side edits frozen manifest')
g(d, 'checkout', '-q', 'main')
g(d, 'merge', '-q', '-s', 'ours', '--no-edit', '-m', 'merge side (ours)', 'side')
net = g(d, 'diff', '--stat', REV, 'HEAD').stdout.decode().strip()
FX['fx3-ours'] = {'head': g(d, 'rev-parse', 'HEAD').stdout.decode().strip(), 'desc': 'side edit, merged -s ours; net tree == REV; net diff=%r' % net}

# FX4 added files under tools/round-49 with special names
for name, label in [('q"x.json', 'dquote'), ('b\\x.json', 'backslash'), ('t\tx.json', 'tab'),
                    ('\u00e9.json', 'nonascii'), ('plain.json', 'plain')]:
    d = clone('fx4-' + label)
    write(d, 'tools/round-49/' + name, b'{}\n')
    FX['fx4-' + label] = {'head': commit(d, 'add ' + label), 'desc': 'added tools/round-49/%r' % name}

# FX5 rename out / FX6 delete
d = clone('fx5-rename'); g(d, 'mv', MAN, 'w2-moved.json')
FX['fx5-rename'] = {'head': commit(d, 'rename out'), 'desc': 'git mv frozen manifest out'}
d = clone('fx6-delete'); g(d, 'rm', '-q', MAN)
FX['fx6-delete'] = {'head': commit(d, 'delete'), 'desc': 'git rm frozen manifest'}

# FX7 carrier bytes; FX8 oracle file; FX9 prior-pins; FX10 non-carrier round-42 fixture
CAR = 'corpus/evidence/round-42/c2/fixtures/v1-le--squashfs_v1.0_le.bin'
d = clone('fx7-carrier'); write(d, CAR, open(os.path.join(L, CAR), 'rb').read() + b'\x00')
FX['fx7-carrier'] = {'head': commit(d, 'carrier bytes'), 'desc': 'append byte to frozen carrier v1le'}
orc = g(L, 'ls-tree', '-r', '--name-only', REV, '--', 'corpus/evidence/round-44/oracle').stdout.decode().split('\n')
orc = [x for x in orc if x][0]
d = clone('fx8-oracle'); write(d, orc, open(os.path.join(L, orc), 'rb').read() + b'x')
FX['fx8-oracle'] = {'head': commit(d, 'oracle'), 'desc': 'edit oracle file %s' % orc}
d = clone('fx9-pins'); pp = 'tools/round-42/prior-pins.json'
write(d, pp, open(os.path.join(L, pp), 'rb').read() + b'\n')
FX['fx9-pins'] = {'head': commit(d, 'pins'), 'desc': 'edit tools/round-42/prior-pins.json'}
NC = 'corpus/evidence/round-42/c2/fixtures/v2ns-le--squashfs_v2.0_le.bin'
d = clone('fx10-noncarrier'); write(d, NC, open(os.path.join(L, NC), 'rb').read() + b'\x00')
FX['fx10-noncarrier'] = {'head': commit(d, 'noncarrier'), 'desc': 'edit non-carrier v2ns fixture (not frozen)'}

# FX11 merge commit itself edits a frozen path (first-parent -m)
d = clone('fx11-mergeedit')
g(d, 'checkout', '-q', '-b', 'side2', REV)
write(d, 'side2.txt', b'side\n'); commit(d, 'side2')
g(d, 'checkout', '-q', 'main')
p = subprocess.run(['git', '-C', d, 'merge', '--no-commit', '--no-ff', 'side2'], capture_output=True, env=ENV)
write(d, MAN, orig + b'\n')
FX['fx11-mergeedit'] = {'head': commit(d, 'merge with frozen edit in merge commit'), 'desc': 'merge commit edits frozen manifest'}

# FX12 edited counter bytes under tools/round-49 (C1 counter edited, run edited copy)
d = clone('fx12-counter'); cp = 'tools/round-49/c1-counter.py'
write(d, cp, open(os.path.join(L, cp), 'rb').read() + b'\n# w2 edit\n')
FX['fx12-counter'] = {'head': commit(d, 'counter edit'), 'desc': 'edit c1-counter.py (run edited copy)'}

json.dump(FX, open(os.path.join(S, 'fx', 'index.json'), 'w'), indent=1, ensure_ascii=False)
for k, v in FX.items(): print(k, v['head'], v['desc'])
