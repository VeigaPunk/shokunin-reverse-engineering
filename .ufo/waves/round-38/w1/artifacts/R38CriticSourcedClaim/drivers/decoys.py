#!/usr/bin/env python3
"""Decoy battery for R38-C1's sourced-claim binding.

Imports the FROZEN counter (tools/round-38/c1-counter.py at the lane, unmodified) and
drives measure() over fixture git repos that differ only in corpus/SOURCES.md and the
entry's source: lines. Fixture construction mirrors the counter's own selftest.
"""
import importlib.util, json, os, shutil, subprocess, sys, tempfile

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
PKG65 = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
OUT = os.path.dirname(os.path.abspath(__file__))

COUNTER = os.environ.get('C1_COUNTER') or os.path.join(LANE, 'tools/round-38/c1-counter.py')
spec = importlib.util.spec_from_file_location('c1counter', COUNTER)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

ENTRY = m.ENTRY
STEM = m.STEM
CARRIERS = m.CARRIERS
ORADIR = m.ORADIR
AFTERDIR = m.AFTERDIR
XPIN = m.XPIN
CORE_HEADING = m.CORE_HEADING
OPENED = m.OPENED

HDR = ('| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n'
       '|---|---|---|---|---|---|---|---|---|---|---|\n')


def row(sid, opened=OPENED, used=ENTRY, status='mined', ncell=11, indent=''):
    cells = [sid, 'fixture source', 'docs', 'A', 'scope', 'anchor', 'teaches', status, opened, '180d', used]
    if ncell == 12:
        cells.append('extra')
    if ncell == 10:
        cells = cells[:-1]
    return indent + '| ' + ' | '.join(cells) + ' |\n'


def registry(*rows):
    return '# S\n\n## Registry\n\n' + HDR + ''.join(rows) + '\n## Paths\n\n- S001 → S002\n'


def readme():
    return f'# R\n\n## Coverage map\n\n| a | b |\n|---|---|\n| x | `{STEM}` |\n\n## Other\n'


def province():
    return (f'# P\n\n{CORE_HEADING}\n\n| Surface | a | Entry |\n|---|---|---|\n'
            f'| squashfs_v4_be | x | {ENTRY} |\n\n## Next\n'
            '- big-endian/AVM stays Frontier; [2026-10-26: superseded for standard BE v4]\n')


def entry(*sids):
    if not sids:
        sids = ('S112',)
    return '# E\n\n' + ''.join(f'source: {s} — x\n' for s in sids)


def main():
    here = os.path.join(LANE, 'tools/round-38')
    fx = os.path.join(here, 'selftest')
    sroot = m.scratch_root()
    after = json.load(open(os.path.join(fx, 'dev-after.json')))
    oracle = open(os.path.join(fx, 'dev-oracle.tsv')).read()
    sha = after['subject']['digest']['sha256']
    be_after = json.loads(json.dumps(after))
    for c_ in be_after['normalized_result']['chunks']:
        c_['handler'] = m.HANDLER

    mp = os.path.join(sroot, 'mint.wrapped.json')
    json.dump({'data': be_after}, open(mp, 'w'))
    r = subprocess.run(['node', os.path.join(here, '..', 'round-27', 'xpin-attribute.mjs'),
                        '--pkg65', PKG65, '--pkg67', PKG65, mp], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit('xpin mint failed: ' + r.stderr)
    be_after['evidence_id'] = r.stdout.splitlines()[0].split('\t')[2]

    xpin = open(os.path.join(here, '..', 'round-27', 'xpin-attribute.mjs'), 'rb').read()
    cs = {'carriers': [{'id': k, 'sha256': sha} for k in ('K1', 'K2', 'K3', 'K4')]}
    base_files = {XPIN: xpin, CARRIERS: json.dumps(cs)}
    for k in ('K1', 'K2', 'K3', 'K4'):
        base_files[f'{ORADIR}/{k}/oracle.tsv'] = oracle
    good = dict(base_files)
    for k in ('K1', 'K2', 'K3', 'K4'):
        good[f'{AFTERDIR}/{k}/after.json'] = json.dumps(be_after)

    def V(**kw):
        v = dict(good)
        v.update({'PROVINCE.md': province(), ENTRY: entry(), 'corpus/SOURCES.md': registry(row('S112')),
                  'corpus/README.md': readme()})
        v.update(kw)
        return v

    leads_table = ('# S\n\n## Registry\n\n' + HDR + '\n## Leads (unopened)\n\n'
                   + HDR + row('S112') + '\n## Paths\n\n- S001\n')
    searchlog_table = ('# S\n\n## Registry\n\n' + HDR + '\n## Search log\n\n'
                       '- 2026-10-26 — x\n\n' + HDR + row('S112') + '\n## Paths\n\n- S001\n')
    dup_registry = registry(row('S112', opened='2026-10-25', used='corpus/lessons/round-38.md'),
                            row('S112', opened=OPENED, used=ENTRY))
    fenced = ('# E\n\nProvenance format:\n\n```\nsource: S112 — example only\n```\n')

    cases = [
        # name, files, expected exit under the frozen counter (0 = green)
        ('C0 green baseline (Registry row, opened 2026-10-26, used-by=entry)', V(), 0),
        ('C1 source row opened 2026-10-25', V(**{'corpus/SOURCES.md': registry(row('S112', opened='2026-10-25'))}), 1),
        ('C2 used-by lacks the entry', V(**{'corpus/SOURCES.md': registry(row('S112', used='corpus/lessons/round-38.md'))}), 1),
        ('C3 entry cites S1120, Registry holds only S112', V(**{ENTRY: entry('S1120')}), 1),
        ('C4 Registry holds S1120 only, entry cites S112', V(**{'corpus/SOURCES.md': registry(row('S1120'))}), 1),
        ('C5 Registry holds S112 and S1120, entry cites S112', V(**{'corpus/SOURCES.md': registry(row('S112'), row('S1120'))}), 0),
        ('C6 row outside Registry table (## Leads table)', V(**{'corpus/SOURCES.md': leads_table}), 1),
        ('C7 row outside Registry table (## Search log table)', V(**{'corpus/SOURCES.md': searchlog_table}), 1),
        ('C8 used-by lists a different entry path', V(**{'corpus/SOURCES.md': registry(row('S112', used='corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion-other.md'))}), 1),
        ('C9 used-by lists entry as a suffix of a longer path', V(**{'corpus/SOURCES.md': registry(row('S112', used=ENTRY + '.orig'))}), 1),
        ('C10 used-by lists backticked entry path', V(**{'corpus/SOURCES.md': registry(row('S112', used='`' + ENTRY + '`'))}), 1),
        ('C11 status=rejected row, opened 2026-10-26, used-by=entry', V(**{'corpus/SOURCES.md': registry(row('S112', status='rejected'))}), 1),
        ('C12 Registry row indented 4 spaces', V(**{'corpus/SOURCES.md': registry(row('S112', indent='    '))}), 1),
        ('C13 duplicate S112: one 10-25/other-entry, one 10-26/entry', V(**{'corpus/SOURCES.md': dup_registry}), 1),
        ('C14 entry writes "Source:" capitalised', V(**{ENTRY: '# E\n\nSource: S112 — x\n'}), 1),
        ('C15 Registry row with 12 cells', V(**{'corpus/SOURCES.md': registry(row('S112', ncell=12))}), 1),
        ('C16 used-by lists entry with a trailing period', V(**{'corpus/SOURCES.md': registry(row('S112', used=ENTRY + '.'))}), 1),
        ('C17 source: line only inside a fenced code block', V(**{ENTRY: fenced}), 1),
        ('C19 used-by lists entry with a ./ prefix', V(**{'corpus/SOURCES.md': registry(row('S112', used='./' + ENTRY))}), 1),
        ('C20 used-by lists the entry stem without prefix', V(**{'corpus/SOURCES.md': registry(row('S112', used=STEM))}), 1),
        ('C18 entry cites S110 whose used-by lists the entry (2026-10-26)',
         V(**{ENTRY: entry('S110'), 'corpus/SOURCES.md': registry(row('S110'))}), 0),
    ]

    results = []
    for name, files, want in cases:
        d = tempfile.mkdtemp(prefix='decoy.', dir=sroot)
        try:
            subprocess.run(['git', '-C', d, 'init', '-q'], check=True)
            top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'],
                                 capture_output=True, text=True).stdout.strip()
            if os.path.realpath(top) != os.path.realpath(d):
                raise SystemExit('fixture toplevel mismatch')
            env = dict(os.environ, GIT_AUTHOR_NAME='fixture', GIT_AUTHOR_EMAIL='fixture@invalid',
                       GIT_COMMITTER_NAME='fixture', GIT_COMMITTER_EMAIL='fixture@invalid')
            for p, c in base_files.items():
                os.makedirs(os.path.dirname(os.path.join(d, p)) or d, exist_ok=True)
                open(os.path.join(d, p), 'wb').write(c if isinstance(c, bytes) else c.encode())
            subprocess.run(['git', '-C', d, 'add', '-A'], check=True)
            subprocess.run(['git', '-C', d, 'commit', '-qm', 'freeze'], check=True, env=env)
            fz = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
            for p in list(base_files):
                if p not in files:
                    os.remove(os.path.join(d, p))
            for p, c in files.items():
                if c is None:
                    continue
                os.makedirs(os.path.dirname(os.path.join(d, p)) or d, exist_ok=True)
                open(os.path.join(d, p), 'wb').write(c if isinstance(c, bytes) else c.encode())
            subprocess.run(['git', '-C', d, 'add', '-A'], check=True)
            subprocess.run(['git', '-C', d, 'commit', '-qm', 'data', '--allow-empty'], check=True, env=env)
            rv = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
            try:
                res = m.measure(d, rv, fz, PKG65)
                got = 0 if res['met_target'] else 1
                b = res['bindings']
                rec = {'name': name, 'want': want, 'got': got,
                       'sourced': b['sourced'], 'opened_source_rows': b['opened_source_rows'],
                       'entry_source_ids': b['entry_source_ids'],
                       'carriers_matched': res['carriers_matched'],
                       'fail': 'PASS' if got == want else 'MISMATCH'}
            except m.Unevaluable as e:
                got = 2
                rec = {'name': name, 'want': want, 'got': got, 'fail': 'UNE valuable', 'err': str(e)}
            results.append(rec)
            print(json.dumps(rec, sort_keys=True), flush=True)
        finally:
            shutil.rmtree(d, ignore_errors=True)
    json.dump(results, open(os.path.join(OUT, 'decoy-results.json'), 'w'), indent=1)
    kills = [r for r in results if r['fail'] != 'PASS']
    print(json.dumps({'cases': len(results), 'mismatches': len(kills),
                      'kills': [r['name'] for r in kills]}, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
