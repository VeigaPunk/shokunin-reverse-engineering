#!/usr/bin/env python3
"""E9 rerun: duplicated oracle row present in BOTH freeze and data commits.
If the frozen counter goes green, one published file satisfied two oracle rows
(duplicate rows not kept as separate units)."""
import importlib.util, json, os, shutil, subprocess, tempfile

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
S = '/fast/scratch/hyaku/kaidoku-r38/R38ReviewerPredicateIdentity'
ART = LANE + '/.ufo/waves/round-38/w1/artifacts/R38ReviewerPredicateIdentity'
FROZEN_DIR = S + '/frozen'
XPIN = FROZEN_DIR + '/tools/round-27/xpin-attribute.mjs'
PKG65 = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'

spec = importlib.util.spec_from_file_location('c1f', FROZEN_DIR + '/tools/round-38/c1-counter.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)

after0 = json.load(open(FROZEN_DIR + '/tools/round-38/selftest/dev-after.json'))
oracle0 = open(FROZEN_DIR + '/tools/round-38/selftest/dev-oracle.tsv').read()
print('oracle rows original:', len([l for l in oracle0.splitlines() if l]))
SHA = after0['subject']['digest']['sha256']

work = tempfile.mkdtemp(prefix='c1-e9.', dir=S)
env = dict(os.environ, GIT_AUTHOR_NAME='fixture', GIT_AUTHOR_EMAIL='fixture@invalid',
           GIT_COMMITTER_NAME='fixture', GIT_COMMITTER_EMAIL='fixture@invalid')
be = json.loads(json.dumps(after0))
for ch in be['normalized_result']['chunks']:
    ch['handler'] = c.HANDLER
p = os.path.join(work, 'mint.wrapped.json')
json.dump({'data': be}, open(p, 'w'))
r = subprocess.run(['node', XPIN, '--pkg65', PKG65, '--pkg67', PKG65, p], capture_output=True, text=True)
assert r.returncode == 0, r.stderr
be['evidence_id'] = r.stdout.splitlines()[0].split('\t')[2]

dup_oracle = oracle0 + oracle0
print('oracle rows duplicated:', len([l for l in dup_oracle.splitlines() if l]))
base_files = {c.XPIN: open(XPIN, 'rb').read(),
              c.CARRIERS: json.dumps({'carriers': [{'id': k, 'sha256': SHA} for k in ('K1', 'K2', 'K3', 'K4')]}),
              'PROVINCE.md': f'# P\n\n{c.CORE_HEADING}\n\n| Surface | a | Entry |\n|---|---|---|\n| squashfs_v4_be | x | {c.ENTRY} |\n\n## Next\n- big-endian/AVM stays Frontier; [2026-10-26: superseded for standard BE v4]\n',
              c.ENTRY: '# E\n\nsource: S112 — x\n',
              'corpus/SOURCES.md': '# S\n\n## Registry\n\n| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n| S112 | s | docs | A | s | a | t | mined | ' + c.OPENED + ' | 180d | ' + c.ENTRY + ' |\n',
              'corpus/README.md': f'# R\n\n## Coverage map\n\n| a | b |\n|---|---|\n| x | `{c.STEM}` |\n\n## Other\n'}
for k in ('K1', 'K2', 'K3', 'K4'):
    base_files[f'{c.ORADIR}/{k}/oracle.tsv'] = dup_oracle          # duplicated oracle IS the frozen oracle
    base_files[f'{c.AFTERDIR}/{k}/after.json'] = json.dumps(be)
subprocess.run(['git', '-C', work, 'init', '-q'], check=True)
top = subprocess.run(['git', '-C', work, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
assert os.path.realpath(top) == os.path.realpath(work)
for p2, cc in base_files.items():
    os.makedirs(os.path.dirname(os.path.join(work, p2)) or work, exist_ok=True)
    open(os.path.join(work, p2), 'wb').write(cc if isinstance(cc, bytes) else cc.encode())
subprocess.run(['git', '-C', work, 'add', '-A'], check=True)
subprocess.run(['git', '-C', work, 'commit', '-qm', 'freeze'], check=True, env=env)
fz = subprocess.run(['git', '-C', work, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
subprocess.run(['git', '-C', work, 'commit', '-qm', 'data', '--allow-empty'], check=True, env=env)
rv = subprocess.run(['git', '-C', work, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
res = c.measure(work, rv, fz, PKG65)
out = {'decoy': 'E9b-oracle-duplicate-frozen', 'met_target': res['met_target'],
       'carriers_matched': res['carriers_matched'],
       'per_carrier': {k: {'oracle_files': d['oracle_files'], 'after_oracle_hits': d.get('after_oracle_hits'),
                           'matched': d['matched']} for k, d in res['carriers'].items()}}
print(json.dumps(out, sort_keys=True))
json.dump(out, open(ART + '/c1-decoy-E9b.json', 'w'), indent=1, sort_keys=True)
shutil.rmtree(work, ignore_errors=True)
