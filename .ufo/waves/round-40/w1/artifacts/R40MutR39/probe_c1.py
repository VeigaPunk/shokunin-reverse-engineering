#!/usr/bin/env python3
"""Differential fixtures for surviving c1-counter mutants: one fixture repo per probe,
pristine measure() vs mutant measure() on the same bytes."""
import hashlib, importlib.util, json, os, shutil, subprocess, sys, tempfile

S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
P65 = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
FXD = os.path.join(S, 'mirror', 'tools', 'round-39', 'selftest')
MIRROR = os.path.join(S, 'mirror', 'tools', 'round-39')
os.makedirs(os.path.join(S, 'hyaku'), exist_ok=True)
os.makedirs(S + '/probe-work', exist_ok=True)

spec = importlib.util.spec_from_file_location('c1p', os.path.join(S, 'c1-counter.py'))
P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)

dev = json.load(open(os.path.join(FXD, 'dev-after.json')))
oracle_tsv = open(os.path.join(FXD, 'dev-oracle.tsv')).read()
symlinks_tsv = open(os.path.join(FXD, 'dev-symlinks.tsv')).read()
xpin = open(os.path.join(S, 'mirror', 'tools', 'round-27', 'xpin-attribute.mjs'), 'rb').read()
IDS, AFTERDIR, ENTRY, STEM = P.IDS, P.AFTERDIR, P.ENTRY, P.STEM
CORE, FRONT, XPIN_PATH, CARRIERS = P.CORE_HEADING, P.FRONTIER_MARK, P.XPIN, P.CARRIERS

blobs = {k: ('fixture carrier %s\n' % k).encode() for k in IDS}
blobs.update({'K1': P.sb_blocks(1, b'K1-gzip'), 'K2': P.sb_blocks(1, b'K2-gzip'),
              'K5': P.sb_blocks(1, b'K5-gzip'), 'K6': P.sb_blocks(2, b'K6-xz')})
pins = {k: hashlib.sha256(blobs[k]).hexdigest() for k in IDS}


def env_for(k, with_links=True):
    e = json.loads(json.dumps(dev))
    e['subject']['name'] = k.lower() + '.sqsh'
    e['subject']['digest']['sha256'] = pins[k]
    e['subject']['local_path'] = '/fixture/' + k.lower() + '.sqsh'
    e['parameters']['output_directory'] = (
        '/fast/scratch/hyaku/kaidoku-r39/R39C1Counter/selftest/%s-after' % k.lower())
    if not with_links:
        e['normalized_result']['extraction_gaps'] = []
        e['normalized_result']['unpublished_entries'] = []
    return e


def mint(envs):
    return P.mint_many(S + '/probe-work', os.path.join(S, 'mirror', 'tools', 'round-27',
                                                       'xpin-attribute.mjs'), P65, envs)


def province():
    r = '| `squashfs_v4_be` | x | `%s` |\n' % ENTRY
    fn = '- %s, 2026-10-26: the Frontier bullet\'s big-endian part is superseded by `%s`.\n' % (FRONT, STEM)
    return '# P\n\n%s\n\n| Surface | a | Entry |\n|---|---|---|\n%s\n## Next\n%s\n' % (CORE, r, fn)


def spec_json():
    cs = [{'id': k, 'path': '%s/%s/carrier.sqsh' % (AFTERDIR, k), 'sha256': pins[k],
           'oracle': '%s/%s/oracle.tsv' % (AFTERDIR, k),
           'symlinks': '%s/%s/symlinks.tsv' % (AFTERDIR, k),
           'receipt': '%s/%s/after.json' % (AFTERDIR, k)} for k in IDS]
    return json.dumps({'claim': 'R39-C1', 'carriers': cs}, indent=1)


def frozen_files():
    f = {XPIN_PATH: xpin, CARRIERS: spec_json(), 'plans/round-39-claims.md': b'# plan\n',
         'tools/round-39/c1-counter.py': open(os.path.join(S, 'c1-counter.py'), 'rb').read(),
         'tools/round-39/c1-run.sh': b'#!/bin/sh\nexit 0\n',
         'PROVINCE.md': province(), ENTRY: '# E\n\nsource: S1121 - x\n',
         'corpus/SOURCES.md':
             '# S\n\n## Registry\n\n| id | source | kind | tier | scope | anchor | teaches '
             '| status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n'
             + '| S1121 | s | docs | A | s | a | t | mined | %s | 180d | %s |\n' % (P.OPENED, ENTRY)
             + '| S112 | s | docs | A | s | a | t | mined | %s | 180d | %s |\n' % (P.OPENED, ENTRY),
         'corpus/README.md': '# R\n\n## Coverage map\n\n| a | b |\n|---|---|\n| x | `%s` |\n\n## Other\n' % STEM}
    for k in IDS:
        f['%s/%s/carrier.sqsh' % (AFTERDIR, k)] = blobs[k]
        f['%s/%s/oracle.tsv' % (AFTERDIR, k)] = oracle_tsv
        f['%s/%s/symlinks.tsv' % (AFTERDIR, k)] = symlinks_tsv if k != 'K1' else ''
    return f


def receipt_path(k):
    return '%s/%s/after.json' % (AFTERDIR, k)


def commit_all(d, files, msg):
    for p, c in files.items():
        fp = os.path.join(d, p)
        os.makedirs(os.path.dirname(fp) or d, exist_ok=True)
        if c is None:
            if os.path.exists(fp):
                os.remove(fp)
            continue
        open(fp, 'wb').write(c if isinstance(c, bytes) else c.encode())
    subprocess.run(['git', '-C', d, 'add', '-A'], check=True)
    subprocess.run(['git', '-C', d, '-c', 'user.name=fx', '-c', 'user.email=fx@fx',
                    'commit', '-qm', msg, '--allow-empty'], check=True)
    return subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'],
                          capture_output=True, text=True).stdout.strip()


def load_mutant(mutant_src):
    shutil.copy(mutant_src, os.path.join(MIRROR, 'c1-counter.py'))
    name = 'c1m%d' % load_mutant.n
    load_mutant.n += 1
    sp = importlib.util.spec_from_file_location(name, os.path.join(MIRROR, 'c1-counter.py'))
    mod = importlib.util.module_from_spec(sp); sp.loader.exec_module(mod)
    return mod
load_mutant.n = 0


def run_case(name, steps, freeze_index, mutant_src):
    CUR = load_mutant(mutant_src)
    d = tempfile.mkdtemp(prefix='c1-probe.', dir=os.path.join(S, 'hyaku'))
    try:
        subprocess.run(['git', '-C', d, 'init', '-q'], check=True)
        top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'],
                             capture_output=True, text=True).stdout.strip()
        assert os.path.realpath(top) == os.path.realpath(d), 'fixture toplevel mismatch'
        revs = [commit_all(d, files, 'step%d' % i) for i, files in enumerate(steps)]
        fz, rv = revs[freeze_index], revs[-1]
        out = {}
        for tag, mod in (('pristine', P), ('mutant', CUR)):
            try:
                r = mod.measure(d, rv, fz, P65)
                bad = {k: sorted(x for x in P.CLAUSES if not r['carriers'][k].get(x))
                       for k in r['carriers']
                       if not all(r['carriers'][k].get(x) for x in P.CLAUSES)
                       or r['carriers'][k].get('oracle_hits') != r['carriers'][k].get('oracle_files')}
                out[tag] = {'exit': 0 if r['met_target'] else 1, 'met': r['met_target'],
                            'matched': r['carriers_matched'], 'failing': bad}
            except mod.Unevaluable as e:
                out[tag] = {'exit': 2, 'reason': e.reason}
        print('%s\tpristine=%s\tmutant=%s' % (name, json.dumps(out['pristine']),
                                              json.dumps(out['mutant'])))
        return out
    finally:
        shutil.rmtree(d, ignore_errors=True)


green = {k: env_for(k, k != 'K1') for k in IDS}
for k, i in mint(green).items():
    green[k]['evidence_id'] = i
frozen = frozen_files()
results = {}


def receipts(envs):
    return {receipt_path(k): json.dumps(v) for k, v in envs.items()}


def probe(pid, name, fn):
    envs = json.loads(json.dumps(green))
    fn(envs)
    results[pid] = run_case(name, [frozen, receipts(envs)], 0,
                            os.path.join(S, 'm.py'))


def apply_mid(mid):
    """Install mutant <mid> as S/m.py using mutate.py's registry."""
    import mutate
    for m_id, tool, old, new, clause, prov in mutate.MUTANTS:
        if m_id == mid:
            shutil.copy(os.path.join(S, tool), os.path.join(S, 'm.py'))
            src = open(os.path.join(S, 'm.py'), encoding='utf-8').read()
            assert src.count(old) == (2 if mid == 'T13' else 1), (mid, src.count(old))
            open(os.path.join(S, 'm.py'), 'w', encoding='utf-8').write(src.replace(old, new))
            return True
    raise SystemExit('unknown mutant ' + mid)


def f_c1(envs):
    for f in envs['K2']['normalized_result']['files']:
        if (f.get('relative_path') or '').endswith('/a/run.sh'):
            f['relative_path'] = 'a/run.sh'
    envs['K2']['evidence_id'] = mint({'m': envs['K2']})['m']


def f_c2(envs):
    envs['K2']['normalized_result']['files'][0]['sha256'] = 'f' * 64
    envs['K2']['evidence_id'] = mint({'m': envs['K2']})['m']


def f_c3(envs):
    envs['K6']['normalized_result']['chunks'][0]['handler'] = 'xsquashfs_v4_bey'
    envs['K6']['evidence_id'] = mint({'m': envs['K6']})['m']


def f_c5(envs):
    envs['K2']['evidence_id'] = envs['K2']['evidence_id'].upper()


def f_c7(envs):
    envs['K3']['normalized_result']['extraction_gaps'][0]['kind'] = 'extractor-failure'
    envs['K3']['evidence_id'] = mint({'m': envs['K3']})['m']


def f_c9(envs):
    envs['K2']['normalized_result']['files'] = [
        f for f in envs['K2']['normalized_result']['files']
        if not (f.get('relative_path') or '').endswith('space name.txt')]
    envs['K2']['evidence_id'] = mint({'m': envs['K2']})['m']


for mid, fn in (('N-C1', f_c1), ('N-C2', f_c2), ('N-C3', f_c3), ('N-C5', f_c5),
                ('N-C7', f_c7), ('N-C9', f_c9)):
    apply_mid(mid)
    probe(mid, mid, fn)

# ---- N-C10: receipt added at freeze, deleted, re-added after freeze
apply_mid('N-C10')
r_all = receipts(green)
step0 = dict(frozen); step0[receipt_path('K2')] = r_all[receipt_path('K2')]
step1 = {k: v for k, v in r_all.items() if '/K2/' not in k}
step1[receipt_path('K2')] = None
results['N-C10'] = run_case('N-C10', [step0, step1, r_all], 0, os.path.join(S, 'm.py'))

json.dump(results, open(os.path.join(S, 'probe-c1-results.json'), 'w'), indent=1)
print('wrote probe-c1-results.json')
