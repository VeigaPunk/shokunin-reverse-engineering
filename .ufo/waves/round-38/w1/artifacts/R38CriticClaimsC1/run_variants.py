#!/usr/bin/env python3
"""R38-C1 critic: shortcut variants scored by the frozen c1 counter in a scratch fixture repo."""
import copy, json, os, shutil, subprocess, sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
FREEZE = 'e059ca9391642d5b71b6662cabcbdce0d9308719'
PKG = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
S = os.environ['S']
F = os.path.join(S, 'fx')
RES = os.path.join(S, 'results')
ART = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-38/w1/artifacts/R38CriticClaimsC1'
COUNTER = os.path.join(S, 'c1-counter-frozen.py')  # frozen bytes from e059ca93 (sha a7a62b09...)
os.makedirs(RES, exist_ok=True)
os.makedirs(ART, exist_ok=True)

SLIM = [
    'tools/round-27/xpin-attribute.mjs',
    'tools/round-38/selftest/dev-after.json',
    '.ufo/waves/round-38/c1/carriers.json',
    'corpus/evidence/round-37/c1/K1/oracle.tsv', 'corpus/evidence/round-37/c1/K1/carrier.sqsh',
    'corpus/evidence/round-37/c1/K2/oracle.tsv', 'corpus/evidence/round-37/c1/K2/carrier.sqsh',
    'corpus/evidence/round-37/c1/K3/oracle.tsv', 'corpus/evidence/round-37/c1/K3/carrier.bin',
    'corpus/evidence/round-37/c1/K4/oracle.tsv', 'corpus/evidence/round-37/c1/K4/carrier.bin',
    'PROVINCE.md', 'corpus/SOURCES.md', 'corpus/README.md',
]
CARRIERS = json.load(open(os.path.join(LANE, '.ufo/waves/round-38/c1/carriers.json')))
ENTRY = 'corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md'
STEM = '2026-10-26-r38-sasquatch-be-squashfs-recursion'
XENV = dict(os.environ, GIT_AUTHOR_NAME='fixture', GIT_AUTHOR_EMAIL='f@invalid',
            GIT_COMMITTER_NAME='fixture', GIT_COMMITTER_EMAIL='f@invalid')


def sh(*a, **kw):
    return subprocess.run(a, capture_output=True, text=True, **kw)


def git(*a):
    r = sh('git', '-C', F, *a)
    if r.returncode != 0:
        raise SystemExit('git %s: %s' % (' '.join(a), r.stderr))
    return r.stdout


def setup():
    shutil.rmtree(F, ignore_errors=True)
    os.makedirs(F)
    p = sh('git', '-C', LANE, 'archive', '--format=tar', '-o', os.path.join(S, 'freeze.tar'), FREEZE, *SLIM)
    if p.returncode != 0:
        raise SystemExit('archive: ' + p.stderr)
    p = sh('tar', '-xf', os.path.join(S, 'freeze.tar'), '-C', F)
    if p.returncode != 0:
        raise SystemExit('tar: ' + p.stderr)
    git('init', '-q')
    top = git('rev-parse', '--show-toplevel').strip()
    if os.path.realpath(top) != os.path.realpath(F):
        raise SystemExit('fixture toplevel mismatch: %r vs %r' % (top, F))
    git('add', '-A')
    r = sh('git', '-C', F, 'commit', '-qm', 'freeze', env=XENV)
    if r.returncode != 0:
        raise SystemExit('commit freeze: ' + r.stderr)
    return git('rev-parse', 'HEAD').strip()


def mint(env):
    p = os.path.join(S, 'mint.wrapped.json')
    json.dump({'data': env}, open(p, 'w'))
    r = sh('node', os.path.join(F, 'tools/round-27/xpin-attribute.mjs'),
           '--pkg65', PKG, '--pkg67', PKG, p)
    if r.returncode != 0:
        raise SystemExit('xpin mint: ' + r.stderr)
    env['evidence_id'] = r.stdout.splitlines()[0].split('\t')[2]
    return env


def fake_receipts():
    base = json.load(open(os.path.join(F, 'tools/round-38/selftest/dev-after.json')))
    out = {}
    for c in CARRIERS['carriers']:
        k = c['id']
        rows = []
        for line in open(os.path.join(F, 'corpus/evidence/round-37/c1', k, 'oracle.tsv')):
            rel, sha, size = line.rstrip('\n').split('\t')
            rows.append((rel, sha, int(size)))
        e = copy.deepcopy(base)
        name = os.path.basename(c['path'])
        e['subject'] = {'name': name, 'digest': {'sha256': c['sha256']},
                        'local_path': '/nonexistent/' + name, 'format': 'file', 'architecture': None}
        e['parameters'] = {'path': '/nonexistent/' + name, 'output_directory': '/nonexistent/out',
                           'max_depth': 3, 'max_output_bytes': 268435456, 'max_output_files': 10000}
        nr = e['normalized_result']
        nr['files'] = [{'relative_path': rel, 'path': '/nonexistent/out/' + rel, 'size': sz,
                        'sha256': sha, 'reported_sha256': sha, 'mime_type': 'text/plain',
                        'analysis_depth': 1, 'runtime_address': None} for rel, sha, sz in rows]
        nr['chunks'] = [{'input_path': '$input', 'provider_id': '157887:1',
                         'range': {'offset': 0, 'length': 4096}, 'handler': 'squashfs_v4_be',
                         'encrypted': False, 'root_file_range': {'offset': 0, 'length': 4096},
                         'extraction_failed': False}]
        nr['extraction_gaps'] = []
        nr['coverage'] = 'complete'
        e.pop('evidence_id', None)
        out[k] = mint(e)
    return out


def freeze_text(path):
    r = sh('git', '-C', F, 'show', 'FZ:' + path)
    return None


def base_files():
    return {p: git('show', 'HEAD:' + p) for p in SLIM}


def prov_with(row_section='round38', decoy_top=False):
    prov = git('show', 'HEAD:PROVINCE.md').rstrip('\n') + '\n'
    row = ('| squashfs_v4_be | stock unblob 26.6.4 extract-firmware on the four frozen BE v4 '
           'carriers; no external extractor | ' + ENTRY + ' |\n')
    if row_section == 'round38':
        return prov + '\n## Round-38 additions to Core\n\n| Surface | Route | Entry |\n|---|---|---|\n' + row
    if row_section == 'round36':
        return (prov + '\n## Round-36 additions to Core (decoy)\n\n| Surface | Route | Entry |\n|---|---|---|\n'
                + row + '\n## Round-38 additions to Core\n\n| Surface | Route | Entry |\n|---|---|---|\n')
    if row_section == 'dup':
        lines = prov.splitlines()
        decoy = ['', '## Round-38 additions to Core', '', '| Surface | Route | Entry |',
                 '|---|---|---|', row.rstrip('\n'), '']
        text = '\n'.join(lines[:3] + decoy + lines[3:]) + '\n'
        return text + '\n## Round-38 additions to Core\n\n| Surface | Route | Entry |\n|---|---|---|\n'


def reg_row(sid='S112', opened='2026-10-26', used=ENTRY):
    return ('| %s | stub source — https://example.invalid/x | docs | A | scope | anchor | teaches '
            '| mined | %s | 180d | %s |\n' % (sid, opened, used))


def add_reg(text, row):
    return text.rstrip('\n') + '\n' + row


def append_used_by(text, sid, pointer):
    out = []
    for line in text.splitlines():
        if line.startswith('| %s |' % sid):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            cells[10] = cells[10] + ', ' + pointer
            out.append('| ' + ' | '.join(cells) + ' |')
        else:
            out.append(line)
    return '\n'.join(out) + '\n'


def readme_with(stem):
    text = git('show', 'HEAD:corpus/README.md')
    lines = text.splitlines()
    i = lines.index('## Coverage map')
    j = i + 1
    while not lines[j].lstrip().startswith('|'):
        j += 1
    while lines[j].lstrip().startswith('|'):
        j += 1
    lines.insert(j, '| SquashFS big-endian v4 | `%s` | held — x |' % stem)
    return '\n'.join(lines) + '\n'


def entry_text(sid='S112', body=''):
    return '# stub entry\n\n' + body + 'source: ' + sid + ' — unblob squashfs handler\n'


def run_variant(name, edits):
    git('reset', '-q', '--hard', FZVAR)
    for p, content in edits.items():
        full = os.path.join(F, p)
        if content is None:
            if os.path.exists(full):
                os.remove(full)
            continue
        os.makedirs(os.path.dirname(full), exist_ok=True)
        mode = 'wb' if isinstance(content, bytes) else 'w'
        with open(full, mode) as fh:
            fh.write(content)
    git('add', '-A')
    r = sh('git', '-C', F, 'commit', '-qm', name, '--allow-empty', env=XENV)
    if r.returncode != 0:
        raise SystemExit('commit %s: %s' % (name, r.stderr))
    rv = git('rev-parse', 'HEAD').strip()
    out = os.path.join(RES, name + '.json')
    r = sh('python3', '-I', '-B', COUNTER, '--root', F, '--rev', rv, '--freeze', FZVAR,
           '--pkg65', PKG, '--json-out', out)
    try:
        res = json.loads(r.stdout)
    except Exception:
        res = {'raw': r.stdout, 'stderr': r.stderr}
    return r.returncode, res


def main():
    global FZVAR
    FZVAR = setup()
    FZ = FZVAR
    # store FZ in a file for later subprocess-free reuse
    open(os.path.join(S, 'fz.txt'), 'w').write(FZ)
    receipts = fake_receipts()
    after = {('corpus/evidence/round-38/c1/%s/after.json' % k): json.dumps(v, indent=1) for k, v in receipts.items()}
    prov_ok = prov_with('round38')
    reg_ok = add_reg(git('show', 'HEAD:corpus/SOURCES.md'), reg_row())
    readme_ok = readme_with(STEM)
    entry_ok = entry_text('S112')

    variants = [
        ('a-do-nothing', {}),
        ('b-receipts-only', dict(after)),
        ('c-full-shortcut', dict(after, **{
            ENTRY: entry_ok, 'PROVINCE.md': prov_ok,
            'corpus/SOURCES.md': reg_ok, 'corpus/README.md': readme_ok})),
        ('d-row-wrong-section', dict(after, **{
            ENTRY: entry_ok, 'PROVINCE.md': prov_with('round36'),
            'corpus/SOURCES.md': reg_ok, 'corpus/README.md': readme_ok})),
        ('e-row-decoy-duplicate-heading', dict(after, **{
            ENTRY: entry_ok, 'PROVINCE.md': prov_with('dup'),
            'corpus/SOURCES.md': reg_ok, 'corpus/README.md': readme_ok})),
        ('f-entry-same-basename-other-dir', dict(after, **{
            'corpus/knowledge/archive/' + STEM + '.md': entry_ok,
            'PROVINCE.md': prov_ok.replace(ENTRY, 'corpus/knowledge/archive/' + STEM + '.md'),
            'corpus/SOURCES.md': reg_ok.replace(ENTRY, 'corpus/knowledge/archive/' + STEM + '.md'),
            'corpus/README.md': readme_ok})),
        ('g-source-opened-earlier', dict(after, **{
            ENTRY: entry_ok, 'PROVINCE.md': prov_ok,
            'corpus/SOURCES.md': add_reg(git('show', 'HEAD:corpus/SOURCES.md'), reg_row(opened='2026-10-25')),
            'corpus/README.md': readme_ok})),
        ('h-reuse-existing-today-row', dict(after, **{
            ENTRY: entry_text('S110'), 'PROVINCE.md': prov_ok,
            'corpus/SOURCES.md': append_used_by(git('show', 'HEAD:corpus/SOURCES.md'), 'S110', ENTRY),
            'corpus/README.md': readme_ok})),
        ('i-entry-cites-S1120', dict(after, **{
            ENTRY: entry_text('S1120'), 'PROVINCE.md': prov_ok,
            'corpus/SOURCES.md': reg_ok, 'corpus/README.md': readme_ok})),
        ('j-readme-stem-prefix', dict(after, **{
            ENTRY: entry_ok, 'PROVINCE.md': prov_ok, 'corpus/SOURCES.md': reg_ok,
            'corpus/README.md': readme_with(STEM + '-draft')})),
        ('k-readme-other-stem', dict(after, **{
            ENTRY: entry_ok, 'PROVINCE.md': prov_ok, 'corpus/SOURCES.md': reg_ok,
            'corpus/README.md': readme_with('2026-10-26-r38-other')})),
        ('l-carrier-bytes-swapped', dict(after, **{
            ENTRY: entry_ok, 'PROVINCE.md': prov_ok, 'corpus/SOURCES.md': reg_ok,
            'corpus/README.md': readme_ok,
            'corpus/evidence/round-37/c1/K1/carrier.sqsh': b'not a squashfs image\n',
            'corpus/evidence/round-37/c1/K3/carrier.bin': b''})),
        ('m-entry-stub-no-claim-text', dict(after, **{
            ENTRY: 'source: S112\n', 'PROVINCE.md': prov_ok, 'corpus/SOURCES.md': reg_ok,
            'corpus/README.md': readme_ok})),
    ]
    rows = []
    for name, edits in variants:
        code, res = run_variant(name, edits)
        b = res.get('bindings', {})
        rows.append({'variant': name, 'exit': code, 'met_target': res.get('met_target'),
                     'carriers_matched': res.get('carriers_matched'),
                     'bindings': b,
                     'subject_ok': {k: v.get('after_subject_ok') for k, v in (res.get('carriers') or {}).items()}})
        print(json.dumps(rows[-1], sort_keys=True))
    json.dump(rows, open(os.path.join(ART, 'c1-shortcut-variants.json'), 'w'), indent=1, sort_keys=True)
    for name, _ in variants:
        for f in (name + '.json',):
            src = os.path.join(RES, f)
            if os.path.exists(src):
                shutil.copy(src, os.path.join(ART, f))
    print('DONE')


if __name__ == '__main__':
    main()
