#!/usr/bin/env python3
"""Real-registry decoys: what the frozen C1 sourced binding accepts on the lane's own
corpus/SOURCES.md bytes (HEAD 9c9d496b), with only the candidate edits.

Reuses the frozen counter module unchanged.
"""
import importlib.util, json, os, shutil, subprocess, sys, tempfile

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
PKG65 = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
OUT = os.path.dirname(os.path.abspath(__file__))
REV = '9c9d496b73cf066b02639dc54647934a0ba4297a'

COUNTER = os.environ.get('C1_COUNTER') or os.path.join(LANE, 'tools/round-38/c1-counter.py')
spec = importlib.util.spec_from_file_location('c1counter', COUNTER)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
ENTRY, CARRIERS, ORADIR, AFTERDIR, XPIN, CORE_HEADING = m.ENTRY, m.CARRIERS, m.ORADIR, m.AFTERDIR, m.XPIN, m.CORE_HEADING
STEM = m.STEM

real_sources = subprocess.run(['git', '-C', LANE, 'show', f'{REV}:corpus/SOURCES.md'],
                              capture_output=True, check=True).stdout.decode()


def s108_with_usedby(extra):
    out = []
    for l in real_sources.splitlines(keepends=True):
        if l.startswith('| S108 |'):
            cells = [c.strip() for c in l.strip().strip('|').split('|')]
            assert len(cells) == 11, len(cells)
            cells[10] = cells[10] + ', ' + extra
            l = '| ' + ' | '.join(cells) + ' |\n'
        out.append(l)
    return ''.join(out)


NEW_ROW = ('| S112 | fixture source — https://example.invalid/x | docs | A | scope | anchor | teaches '
           '| mined | 2026-10-26 | 180d | ' + ENTRY + ' |\n')


def append_after_heading(text, heading, block):
    lines = text.splitlines(keepends=True)
    i = [n for n, l in enumerate(lines) if l.startswith(heading)][0]
    return ''.join(lines[:i + 1]) + '\n' + block + ''.join(lines[i + 1:])


def registry_append(text, block):
    lines = text.splitlines(keepends=True)
    i = [n for n, l in enumerate(lines) if l.startswith('## Paths')][0]
    return ''.join(lines[:i]) + block + '\n' + ''.join(lines[i:])


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
    mp = os.path.join(sroot, 'mint2.wrapped.json')
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

    def V(sources, entry='# E\n\nsource: S108 — x\n'):
        v = dict(good)
        v.update({'PROVINCE.md': prov, ENTRY: entry, 'corpus/SOURCES.md': sources, 'corpus/README.md': readme})
        return v

    cases = [
        ('R0 real registry unedited, entry cites S108 (opened 2026-10-26, used-by=r36 entry)',
         V(real_sources), 1),
        ('R1 real registry, S108 used-by += r38 entry, entry cites S108',
         V(s108_with_usedby(ENTRY)), 0),
        ('R2 real registry + new S112 row at end of Registry table, entry cites S112',
         V(registry_append(real_sources, NEW_ROW), entry='# E\n\nsource: S112 — x\n'), 0),
        ('R3 real registry + same S112 row appended after ## Leads (outside Registry)',
         V(append_after_heading(real_sources, '## Leads (unopened)', NEW_ROW), entry='# E\n\nsource: S112 — x\n'), 1),
        ('R5 real registry + S112 row under a ### sub-heading inside Registry',
         V(registry_append(real_sources, '### Round-38 sources\n\n' + NEW_ROW), entry='# E\n\nsource: S112 — x\n'), 0),
        ('R4 real registry + new S112 row with status rejected, opened 2026-10-26, used-by=entry',
         V(registry_append(real_sources, NEW_ROW.replace('| mined |', '| rejected |')), entry='# E\n\nsource: S112 — x\n'), 1),
    ]
    results = []
    for name, files, want in cases:
        d = tempfile.mkdtemp(prefix='decoy2.', dir=sroot)
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
            try:
                res = m.measure(d, rv, fz, PKG65)
                got = 0 if res['met_target'] else 1
                b = res['bindings']
                rec = {'name': name, 'want': want, 'got': got,
                       'sourced': b['sourced'], 'opened_source_rows': b['opened_source_rows'],
                       'entry_source_ids': b['entry_source_ids'], 'carriers_matched': res['carriers_matched'],
                       'fail': 'PASS' if got == want else 'MISMATCH'}
            except m.Unevaluable as e:
                rec = {'name': name, 'want': want, 'got': 2, 'fail': 'UNEVALUABLE', 'err': str(e)}
            results.append(rec)
            print(json.dumps(rec, sort_keys=True), flush=True)
        finally:
            shutil.rmtree(d, ignore_errors=True)
    json.dump(results, open(os.path.join(OUT, 'decoy2-results.json'), 'w'), indent=1)
    print(json.dumps({'mismatches': [r['name'] for r in results if r['fail'] != 'PASS']}, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
