#!/usr/bin/env python3
"""Validate the sibling scribe's five-row append block against the FROZEN C1 counter,
inside vs outside the ## Registry section. Carriers/receipts are the counter's own
selftest fixtures; only the SOURCES.md surface and the entry are under test here.
"""
import importlib.util, json, os, shutil, subprocess, sys, tempfile

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
PKG65 = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
OUT = os.path.dirname(os.path.abspath(__file__))
REV = '9c9d496b73cf066b02639dc54647934a0ba4297a'
BLOCK = os.path.join(LANE, '.ufo/waves/round-38/w1/artifacts/R38ScribeSOURCES/append-block.md')

COUNTER = os.environ.get('C1_COUNTER') or os.path.join(LANE, 'tools/round-38/c1-counter.py')
spec = importlib.util.spec_from_file_location('c1counter', COUNTER)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
ENTRY, CARRIERS, ORADIR, AFTERDIR, XPIN, CORE_HEADING, STEM = (
    m.ENTRY, m.CARRIERS, m.ORADIR, m.AFTERDIR, m.XPIN, m.CORE_HEADING, m.STEM)

real_sources = subprocess.run(['git', '-C', LANE, 'show', f'{REV}:corpus/SOURCES.md'],
                              capture_output=True, check=True).stdout.decode()
block = open(BLOCK).read()


def in_registry(text, blk):
    i = text.index('## Paths')
    return text[:i] + blk + '\n' + text[i:]


def after_leads(text, blk):
    i = text.index('## Leads (unopened)')
    j = text.index('\n', i) + 1
    return text[:j] + '\n' + blk + text[j:]


def entry(sids):
    return '# E\n\n' + ''.join(f'source: {s} — stand-in cited row\n' for s in sids)


def main():
    here = os.path.join(LANE, 'tools/round-38')
    fx = os.path.join(here, 'selftest')
    sroot = m.scratch_root()
    after = json.load(open(os.path.join(fx, 'dev-after.json')))
    oracle = open(os.path.join(fx, 'dev-oracle.tsv')).read()
    sha = after['subject']['digest']['sha256']
    be = json.loads(json.dumps(after))
    for c_ in be['normalized_result']['chunks']:
        c_['handler'] = m.HANDLER
    mp = os.path.join(sroot, 'mint3.wrapped.json')
    json.dump({'data': be}, open(mp, 'w'))
    r = subprocess.run(['node', os.path.join(here, '..', 'round-27', 'xpin-attribute.mjs'),
                        '--pkg65', PKG65, '--pkg67', PKG65, mp], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit('xpin mint failed: ' + r.stderr)
    be['evidence_id'] = r.stdout.splitlines()[0].split('\t')[2]
    xpin = open(os.path.join(here, '..', 'round-27', 'xpin-attribute.mjs'), 'rb').read()

    base = {XPIN: xpin, CARRIERS: json.dumps({'carriers': [{'id': k, 'sha256': sha} for k in ('K1', 'K2', 'K3', 'K4')]})}
    for k in ('K1', 'K2', 'K3', 'K4'):
        base[f'{ORADIR}/{k}/oracle.tsv'] = oracle
    good = dict(base)
    for k in ('K1', 'K2', 'K3', 'K4'):
        good[f'{AFTERDIR}/{k}/after.json'] = json.dumps(be)
    prov = (f'# P\n\n{CORE_HEADING}\n\n| Surface | a | Entry |\n|---|---|---|\n'
            f'| squashfs_v4_be | x | {ENTRY} |\n\n## Next\n'
            '- big-endian/AVM stays Frontier; [2026-10-26: superseded for standard BE v4]\n')
    readme = f'# R\n\n## Coverage map\n\n| a | b |\n|---|---|\n| x | `{STEM}` |\n\n## Other\n'

    def V(sources, sids):
        v = dict(good)
        v.update({'PROVINCE.md': prov, ENTRY: entry(sids), 'corpus/SOURCES.md': sources,
                  'corpus/README.md': readme})
        return v

    all5 = ['S112', 'S113', 'S114', 'S115', 'S116']
    cases = [
        ('S0 scribe block inside ## Registry, entry cites S112..S116', V(in_registry(real_sources, block), all5), 0),
        ('S1 scribe block after ## Leads (outside Registry)', V(after_leads(real_sources, block), all5), 1),
        ('S2 scribe block inside Registry, entry cites only S115 (rejected row)', V(in_registry(real_sources, block), ['S115']), 1),
        ('S3 scribe block inside Registry, entry cites only S116 (mined own-work row)', V(in_registry(real_sources, block), ['S116']), 0),
    ]
    res = []
    for name, files, want in cases:
        d = tempfile.mkdtemp(prefix='decoy3.', dir=sroot)
        try:
            subprocess.run(['git', '-C', d, 'init', '-q'], check=True)
            top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'],
                                 capture_output=True, text=True).stdout.strip()
            if os.path.realpath(top) != os.path.realpath(d):
                raise SystemExit('fixture toplevel mismatch')
            env = dict(os.environ, GIT_AUTHOR_NAME='fixture', GIT_AUTHOR_EMAIL='fixture@invalid',
                       GIT_COMMITTER_NAME='fixture', GIT_COMMITTER_EMAIL='fixture@invalid')
            for p, c in base.items():
                os.makedirs(os.path.dirname(os.path.join(d, p)) or d, exist_ok=True)
                open(os.path.join(d, p), 'wb').write(c if isinstance(c, bytes) else c.encode())
            subprocess.run(['git', '-C', d, 'add', '-A'], check=True)
            subprocess.run(['git', '-C', d, 'commit', '-qm', 'freeze'], check=True, env=env)
            fz = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
            for p in list(base):
                if p not in files:
                    os.remove(os.path.join(d, p))
            for p, c in files.items():
                os.makedirs(os.path.dirname(os.path.join(d, p)) or d, exist_ok=True)
                open(os.path.join(d, p), 'wb').write(c if isinstance(c, bytes) else c.encode())
            subprocess.run(['git', '-C', d, 'add', '-A'], check=True)
            subprocess.run(['git', '-C', d, 'commit', '-qm', 'data'], check=True, env=env)
            rv = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
            r = m.measure(d, rv, fz, PKG65)
            got = 0 if r['met_target'] else 1
            b = r['bindings']
            rec = {'name': name, 'want': want, 'got': got, 'sourced': b['sourced'],
                   'opened_source_rows': b['opened_source_rows'],
                   'entry_source_ids': b['entry_source_ids'],
                   'fail': 'PASS' if got == want else 'MISMATCH'}
        finally:
            shutil.rmtree(d, ignore_errors=True)
        res.append(rec)
        print(json.dumps(rec, sort_keys=True), flush=True)
    json.dump(res, open(os.path.join(OUT, 'decoy3-results.json'), 'w'), indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
