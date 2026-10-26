#!/usr/bin/env python3
"""R38ReviewerPredicateIdentity — C1 falsifiers against the FROZEN c1-counter blob.

Mirrors the frozen selftest's green fixture, then applies one claim-violating
mutation at a time. A variant with counter-verdict exit 0 (met_target true)
meets the frozen target while violating a P38-C1 sentence.
"""
import importlib.util, json, os, shutil, subprocess, sys, tempfile

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
S = '/fast/scratch/hyaku/kaidoku-r38/R38ReviewerPredicateIdentity'
ART = LANE + '/.ufo/waves/round-38/w1/artifacts/R38ReviewerPredicateIdentity'
FROZEN_DIR = S + '/frozen'
FROZEN = FROZEN_DIR + '/tools/round-38/c1-counter.py'
XPIN = FROZEN_DIR + '/tools/round-27/xpin-attribute.mjs'
PKG65 = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'

spec = importlib.util.spec_from_file_location('c1f', FROZEN)
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)

after0 = json.load(open(FROZEN_DIR + '/tools/round-38/selftest/dev-after.json'))
oracle0 = open(FROZEN_DIR + '/tools/round-38/selftest/dev-oracle.tsv').read()
SHA = after0['subject']['digest']['sha256']


def mint(env, workdir):
    p = os.path.join(workdir, 'mint.wrapped.json')
    json.dump({'data': env}, open(p, 'w'))
    r = subprocess.run(['node', XPIN, '--pkg65', PKG65, '--pkg67', PKG65, p],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit('mint failed: ' + r.stderr)
    env['evidence_id'] = r.stdout.splitlines()[0].split('\t')[2]
    return env


def province(row=True, heading=None, cell='squashfs_v4_be', note_text=None, extra=''):
    heading = heading or c.CORE_HEADING
    r = f'| {cell} | x | {c.ENTRY} |\n' if row else ''
    nt = note_text if note_text is not None else \
        '- big-endian/AVM stays Frontier; [2026-10-26: superseded for standard BE v4]\n'
    return f'# P\n\n{heading}\n\n| Surface | a | Entry |\n|---|---|---|\n{r}{extra}\n## Next\n{nt}\n'


def entry(sid='S112'):
    return f'# E\n\nsource: {sid} — x\n'


def registry(rows):
    head = ('# S\n\n## Registry\n\n| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n'
            '|---|---|---|---|---|---|---|---|---|---|---|\n')
    return head + ''.join(rows)


def srow(sid='S112', opened=None, used=None):
    opened = opened or c.OPENED
    used = used if used is not None else c.ENTRY
    return f'| {sid} | s | docs | A | s | a | t | mined | {opened} | 180d | {used} |\n'


def readme(stem=None):
    stem = stem or c.STEM
    return f'# R\n\n## Coverage map\n\n| a | b |\n|---|---|\n| x | `{stem}` |\n\n## Other\n'


def build(name, mutate=None, files_fn=None):
    work = tempfile.mkdtemp(prefix='c1-decoy.', dir=S)
    env = dict(os.environ, GIT_AUTHOR_NAME='fixture', GIT_AUTHOR_EMAIL='fixture@invalid',
               GIT_COMMITTER_NAME='fixture', GIT_COMMITTER_EMAIL='fixture@invalid')
    be = json.loads(json.dumps(after0))
    for ch in be['normalized_result']['chunks']:
        ch['handler'] = c.HANDLER
    if mutate:
        mutate(be)
    be = mint(be, work)
    base_files = {c.XPIN: open(XPIN, 'rb').read(),
                  c.CARRIERS: json.dumps({'carriers': [{'id': k, 'sha256': SHA} for k in ('K1', 'K2', 'K3', 'K4')]})}
    for k in ('K1', 'K2', 'K3', 'K4'):
        base_files[f'{c.ORADIR}/{k}/oracle.tsv'] = oracle0
    files = files_fn(dict(base_files), be) if files_fn else dict(base_files)
    for k in ('K1', 'K2', 'K3', 'K4'):
        files.setdefault(f'{c.AFTERDIR}/{k}/after.json', json.dumps(be))
    files.setdefault('PROVINCE.md', province())
    files.setdefault(c.ENTRY, entry())
    files.setdefault('corpus/SOURCES.md', registry([srow()]))
    files.setdefault('corpus/README.md', readme())
    subprocess.run(['git', '-C', work, 'init', '-q'], check=True)
    top = subprocess.run(['git', '-C', work, 'rev-parse', '--show-toplevel'],
                         capture_output=True, text=True).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(work), 'fixture toplevel mismatch'
    for p, cc in base_files.items():
        os.makedirs(os.path.dirname(os.path.join(work, p)) or work, exist_ok=True)
        open(os.path.join(work, p), 'wb').write(cc if isinstance(cc, bytes) else cc.encode())
    subprocess.run(['git', '-C', work, 'add', '-A'], check=True)
    subprocess.run(['git', '-C', work, 'commit', '-qm', 'freeze'], check=True, env=env)
    fz = subprocess.run(['git', '-C', work, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    for p in list(base_files):
        if p not in files:
            os.remove(os.path.join(work, p))
    for p, cc in files.items():
        if cc is None:
            continue
        os.makedirs(os.path.dirname(os.path.join(work, p)) or work, exist_ok=True)
        open(os.path.join(work, p), 'wb').write(cc if isinstance(cc, bytes) else cc.encode())
    subprocess.run(['git', '-C', work, 'add', '-A'], check=True)
    subprocess.run(['git', '-C', work, 'commit', '-qm', 'data', '--allow-empty'], check=True, env=env)
    rv = subprocess.run(['git', '-C', work, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    try:
        res = c.measure(work, rv, fz, PKG65)
        got = 0 if res['met_target'] else 1
    except c.Unevaluable as e:
        got, res = 2, {'unevaluable': str(e)}
    summary = {'decoy': name, 'counter_verdict_exit': got, 'met_target': res.get('met_target'),
               'carriers_matched': res.get('carriers_matched'), 'bindings': res.get('bindings'),
               'unevaluable': res.get('unevaluable')}
    print(json.dumps(summary, sort_keys=True))
    json.dump(summary, open(ART + f'/c1-decoy-{name}.json', 'w'), indent=1, sort_keys=True)
    shutil.rmtree(work, ignore_errors=True)
    return got


results = {}

# sanity: unmutated green fixture must pass (exit 0)
results['green-sanity'] = build('green-sanity')

# E1: the only 'big-endian'+'superseded' line DENIES the supersession
results['E1-note-denial'] = build(
    'E1-note-denial',
    files_fn=lambda f, be: {**f, 'PROVINCE.md': province(
        note_text='- the big-endian Frontier bullet is not superseded; big-endian ground stays Frontier.\n')})

# E2: extraction_gaps key absent entirely (receipt does not state its gaps)
def e2(be):
    be['normalized_result'].pop('extraction_gaps', None)
results['E2-gaps-field-absent'] = build('E2-gaps-field-absent', mutate=e2)

# E3: provider version forged (unblob version never checked)
def e3(be):
    be['provider']['version'] = '9.9.9'
results['E3-provider-version-forged'] = build('E3-provider-version-forged', mutate=e3)

# E4: duplicate S-id rows — the entry's cited row opened 2026-10-25, a shadow
# duplicate opened 2026-10-26 satisfies the counter
results['E4-duplicate-sid'] = build(
    'E4-duplicate-sid',
    files_fn=lambda f, be: {**f, 'corpus/SOURCES.md': registry([
        srow(opened='2026-10-25', used='corpus/lessons/round-38.md'),
        srow(opened=c.OPENED, used=c.ENTRY)])})

# E5: row only under a SECOND '## Round-38 additions to Core' heading
# (section() first-match blind spot -> false negative expected)
dup_heading = ('# P\n\n## Round-38 additions to Core\n\n| Surface | a | Entry |\n|---|---|---|\n'
               '\n## Round-38 additions to Core\n\n| Surface | a | Entry |\n|---|---|---|\n'
               f'| squashfs_v4_be | x | {c.ENTRY} |\n\n## Next\n'
               '- big-endian/AVM stays Frontier; [2026-10-26: superseded for standard BE v4]\n')
results['E5-duplicate-heading'] = build(
    'E5-duplicate-heading',
    files_fn=lambda f, be: {**f, 'PROVINCE.md': dup_heading})

# E8: carrier bytes replaced with junk at the pinned paths (counter never
# hashes carrier bytes; pins are checked only against the receipt's subject digest)
def e8files(f, be):
    for k, rel in (('K1', 'carrier.sqsh'), ('K2', 'carrier.sqsh'), ('K3', 'carrier.bin'), ('K4', 'carrier.bin')):
        f[f'corpus/evidence/round-37/c1/{k}/{rel}'] = b'NOT-A-SQUASHFS-IMAGE' * 8
    return f
results['E8-carrier-bytes-junk'] = build('E8-carrier-bytes-junk', files_fn=e8files)

# E9: oracle.tsv with a duplicated row (same rel+sha twice); one published file
# satisfies both rows -> hits == oracle_files
results['E9-oracle-duplicate-row'] = build(
    'E9-oracle-duplicate-row',
    files_fn=lambda f, be: {**{k: v for k, v in f.items() if not k.endswith('/oracle.tsv')},
                            **{f'{c.ORADIR}/{k}/oracle.tsv': oracle0 + oracle0 for k in ('K1', 'K2', 'K3', 'K4')}})

# E10: registry row with 12 cells (len!=11 -> skipped -> false negative expected)
results['E10-registry-12-cells'] = build(
    'E10-registry-12-cells',
    files_fn=lambda f, be: {**f, 'corpus/SOURCES.md': registry(
        [srow()[:-1] + ' extra |\n'])})

print(json.dumps(results, sort_keys=True))
json.dump(results, open(ART + '/c1-decoy-summary.json', 'w'), indent=1, sort_keys=True)
