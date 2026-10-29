#!/usr/bin/env python3
# Fixture: a frozen oracle edited INSIDE a merge commit, scored against the round-41
# and round-49 freeze walks (read-only on the lane; every git write is in a scratch fixture).
# Run: python3 merge_drift_fixture.py   -> $S/merge-drift.json
import os, subprocess, json, hashlib, importlib.util, shutil
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
S = '/fast/scratch/hyaku/kaidoku-r50/C1ShortcutCritic'
os.makedirs(S, exist_ok=True)
os.environ.update(TMPDIR=S, HYAKU_SCRATCH='/fast/scratch/hyaku', GIT_NO_REPLACE_OBJECTS='1')
D = subprocess.check_output(['mktemp', '-d', '-p', S]).decode().strip()

def G(*a, check=True):
    r = subprocess.run(['git', '-C', D, *a], capture_output=True)
    if check and r.returncode != 0:
        raise SystemExit(f'git {a} failed: {r.stderr.decode()}')
    return r

G('init', '-q')
assert subprocess.check_output(['git', '-C', D, 'rev-parse', '--show-toplevel']).decode().strip() == D
G('config', 'user.name', 'c1shortcut'); G('config', 'user.email', 'c1shortcut@fixture.invalid')
ORC = 'corpus/evidence/round-50/c1/a7530/oracle.tsv'

def w(p, s):
    fp = os.path.join(D, p); os.makedirs(os.path.dirname(fp), exist_ok=True); open(fp, 'w').write(s)

rows = ''.join(f'file{i}.bin\t{hashlib.sha256(bytes([i])).hexdigest()}\t{i+1}\n' for i in range(4))
w(ORC, rows)
w('tools/round-41/c1-counter.py', open(os.path.join(LANE, 'tools/round-41/c1-counter.py')).read())
w('x.txt', 'x0\n'); w('y.txt', 'y0\n')
G('add', '-A'); G('commit', '-q', '-m', 'freeze F')
F = G('rev-parse', 'HEAD').stdout.decode().strip()
G('checkout', '-q', '-b', 'side-a', F); w('x.txt', 'x1\n'); G('commit', '-qam', 'side a')
G('checkout', '-q', '-b', 'side-b', F); w('y.txt', 'y1\n'); G('commit', '-qam', 'side b')
G('checkout', '-q', '-b', 'main-m', 'side-a')
assert G('merge', '--no-ff', '--no-commit', 'side-b', check=False).returncode == 0
shrunk = ''.join(rows.splitlines(True)[:-1])          # drop one oracle row inside the merge
w(ORC, shrunk); G('add', '-A'); G('commit', '-q', '-m', 'merge side-b with oracle edit')
M = G('rev-parse', 'HEAD').stdout.decode().strip()
G('checkout', '-q', '-b', 'plain', F); w(ORC, shrunk); G('commit', '-qam', 'plain oracle edit')
P = G('rev-parse', 'HEAD').stdout.decode().strip()

out = {'freeze': F, 'merge': M, 'plain': P}
out['git_log_name_only_F_M'] = G('log', '--pretty=format:', '--name-only', '--no-renames', f'{F}..{M}').stdout.decode()
out['git_log_m_name_status_F_M'] = G('log', '-m', '--diff-merges=first-parent', '--name-status', '--pretty=format:', f'{F}..{M}').stdout.decode()
out['git_diff_name_status_F_M'] = G('diff', '--name-status', F, M).stdout.decode()

def load(name, src):
    dst = os.path.join(S, name + '.py'); shutil.copy(src, dst)
    spec = importlib.util.spec_from_file_location(name, dst); mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod); return mod

r41 = load('r41counter', os.path.join(LANE, 'tools/round-41/c1-counter.py'))
r49 = load('r49counter', os.path.join(LANE, 'tools/round-49/c1-counter.py'))
spec = {'carriers': [{'id': 'a7530', 'oracle': ORC}]}
out['r41_frozen_drift_F_M'] = r41.frozen_drift(D, F, M, spec)     # expected [] (hole)
out['r49_frozen_drift_F_M'] = r49.frozen_drift(D, F, M, spec)
out['r41_frozen_drift_F_P'] = r41.frozen_drift(D, F, P, spec)     # control: plain commit caught
out['r49_frozen_drift_F_P'] = r49.frozen_drift(D, F, P, spec)     # control: round-49 walk lacks the 'oracle' key
out['oracle_sha256_frozen'] = hashlib.sha256(rows.encode()).hexdigest()
out['oracle_sha256_merge'] = hashlib.sha256(shrunk.encode()).hexdigest()
json.dump(out, open(os.path.join(S, 'merge-drift.json'), 'w'), indent=1)
print(json.dumps(out, indent=1))
