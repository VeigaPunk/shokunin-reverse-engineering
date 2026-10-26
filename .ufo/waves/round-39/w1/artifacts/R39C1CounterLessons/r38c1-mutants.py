#!/usr/bin/env python3
"""R39C1CounterLessons: score hand-built failure-class fixtures against the
FROZEN round-38 C1 counter (tools/round-38/c1-counter.py) to show which
counter-failure classes it survives. Read-only against the lane: the module is
imported, never modified; fixtures are throwaway git repos under $HYAKU_SCRATCH.

Each case builds the counter's own 'green' fixture shape (as its --selftest
does), applies one lesson-class mutation, and records the counter exit.
want_exit is what a round-39 successor MUST return for the class.
"""
import importlib.util, json, os, subprocess, shutil, sys, tempfile

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
PKG = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
S = os.environ['HYAKU_SCRATCH']

spec = importlib.util.spec_from_file_location('r38c1', LANE + '/tools/round-38/c1-counter.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

fxs = LANE + '/tools/round-38/selftest'
after0 = json.load(open(fxs + '/dev-after.json'))
oracle = open(fxs + '/dev-oracle.tsv').read()
xpin = open(LANE + '/tools/round-27/xpin-attribute.mjs', 'rb').read()

HANDLER = m.HANDLER
ENTRY = m.ENTRY
STEM = m.STEM
OPENED = m.OPENED
XPIN = m.XPIN
CARRIERS = m.CARRIERS
ORADIR = m.ORADIR
AFTERDIR = m.AFTERDIR
CORE = m.CORE_HEADING

be = json.loads(json.dumps(after0))
for c in be['normalized_result']['chunks']:
    c['handler'] = HANDLER
p = os.path.join(S, 'mint.wrapped.json')
json.dump({'data': be}, open(p, 'w'))
r = subprocess.run(['node', LANE + '/tools/round-27/xpin-attribute.mjs', '--pkg65', PKG,
                    '--pkg67', PKG, p], capture_output=True, text=True)
assert r.returncode == 0, 'xpin mint failed: ' + r.stderr
be['evidence_id'] = r.stdout.splitlines()[0].split('\t')[2]
AFTER = json.dumps(be)
sha = after0['subject']['digest']['sha256']
spec4 = {'carriers': [{'id': k, 'sha256': sha} for k in ('K1', 'K2', 'K3', 'K4')]}


def province(row=True, heading=CORE, cell=HANDLER, note=True, extra=''):
    r_ = f'| {cell} | x | {ENTRY} |\n' if row else ''
    fn = '- big-endian/AVM stays Frontier; [2026-10-26: superseded for standard BE v4]\n' if note else ''
    return f'# P\n\n{heading}\n\n| Surface | a | Entry |\n|---|---|---|\n{r_}\n## Next\n{fn}{extra}\n'


def entry(sid='S112'):
    return f'# E\n\nsource: {sid} — x\n'


def registry(sid='S112', opened=OPENED, used=ENTRY, status='mined'):
    head = ('# S\n\n## Registry\n\n| id | source | kind | tier | scope | anchor | teaches | status'
            ' | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n')
    return head + f'| {sid} | s | docs | A | s | a | t | {status} | {opened} | 180d | {used} |\n'


def readme(stem=STEM):
    return f'# R\n\n## Coverage map\n\n| a | b |\n|---|---|\n| x | `{stem}` |\n\n## Other\n'


def run_case(name, want_exit, mutate_freeze=None, data_files=None, mutate_data=None, orphan=False):
    d = tempfile.mkdtemp(prefix='mut.', dir=S)
    try:
        subprocess.run(['git', '-C', d, 'init', '-q'], check=True)
        top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'],
                             capture_output=True, text=True).stdout.strip()
        assert os.path.realpath(top) == os.path.realpath(d), 'fixture toplevel mismatch'

        base = {XPIN: xpin, CARRIERS: json.dumps(spec4), 'PROVINCE.md': province(),
                ENTRY: entry(), 'corpus/SOURCES.md': registry(), 'corpus/README.md': readme()}
        for k in ('K1', 'K2', 'K3', 'K4'):
            base[f'{ORADIR}/{k}/oracle.tsv'] = oracle
            base[f'corpus/evidence/round-37/c1/{k}/carrier.sqsh'] = b'ORIGINAL-BYTES'
        if mutate_freeze:
            base = mutate_freeze(dict(base))

        def put(files):
            for path, content in files.items():
                if content is None:
                    continue
                fp = os.path.join(d, path)
                os.makedirs(os.path.dirname(fp) or d, exist_ok=True)
                open(fp, 'wb').write(content if isinstance(content, bytes) else content.encode())
            subprocess.run(['git', '-C', d, 'add', '-A'], check=True)

        put(base)
        subprocess.run(['git', '-C', d, '-c', 'user.name=fx', '-c', 'user.email=fx@fx',
                        'commit', '-qm', 'freeze'], check=True)
        fz = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'],
                            capture_output=True, text=True).stdout.strip()

        data = dict(base)
        for k in ('K1', 'K2', 'K3', 'K4'):
            data[f'{AFTERDIR}/{k}/after.json'] = AFTER
        if data_files:
            data.update(data_files)
        if mutate_data:
            data = mutate_data(data)
        if orphan:
            subprocess.run(['git', '-C', d, 'checkout', '-q', '--orphan', 'databranch'], check=True)
        put(data)
        subprocess.run(['git', '-C', d, '-c', 'user.name=fx', '-c', 'user.email=fx@fx',
                        'commit', '-qm', 'data', '--allow-empty'], check=True)
        rv = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'],
                            capture_output=True, text=True).stdout.strip()
        try:
            res = m.measure(d, rv, fz, PKG)
            got = 0 if res['met_target'] else 1
            detail = {'carriers_matched': res.get('carriers_matched'),
                      'carriers_unchanged': res.get('carriers_unchanged'),
                      'bindings': res.get('bindings')}
        except m.Unevaluable as e:
            got, detail = 2, {'unevaluable': str(e)}
        verdict = 'SURVIVES (blind)' if got == 0 and want_exit != 0 else (
            'caught' if got == want_exit else 'other')
        return {'mutant': name, 'want_exit': want_exit, 'got_exit': got, 'verdict': verdict,
                'detail': detail}
    finally:
        shutil.rmtree(d, ignore_errors=True)


results = []

# M-A shadow/duplicate Core heading: first occurrence carries the row, the
# intended (second) section carries none. QUALITY 77 class.
shadow = (f'# P\n\n{CORE}\n\n| Surface | a | Entry |\n|---|---|---|\n| {HANDLER} | x | {ENTRY} |\n'
          '\n## Interlude\n\nsome other round text\n\n'
          f'{CORE}\n\n| Surface | a | Entry |\n|---|---|---|\n'
          '\n## Next\n- big-endian/AVM stays Frontier; [2026-10-26: superseded for standard BE v4]\n')
results.append(run_case('M-A shadow core heading (first wins)', 1,
                        mutate_freeze=lambda b: {**b, 'PROVINCE.md': shadow}))

# M-B frontier decoy: real note gone, decoy line with both keywords in an
# unrelated section; the Frontier bullet itself stays unmoved.
results.append(run_case('M-B frontier decoy line, unscoped check', 1,
                        mutate_freeze=lambda b: {**b, 'PROVINCE.md': province(
                            note=False,
                            extra='## Changelog\n\n- big-endian status: superseded per another lane\n')}))

# M-C pre-seen receipt: after.json committed already at the freeze commit
# (nothing is first-added in a commit descending from the freeze).
results.append(run_case('M-C after.json already present at freeze', 1,
                        mutate_freeze=lambda b: {**b,
                            **{f'{AFTERDIR}/{k}/after.json': AFTER for k in ('K1', 'K2', 'K3', 'K4')}}))

# M-D SOURCES row status unchecked: 'rejected' row still satisfies the binding.
results.append(run_case('M-D sources row status=rejected', 1,
                        data_files={'corpus/SOURCES.md': registry(status='rejected')}))

# M-G stem boundary: coverage-map cell holds STEM plus a suffix; substring hit.
results.append(run_case('M-G coverage stem substring (stem + "-v2")', 1,
                        data_files={'corpus/README.md': readme(stem=STEM + '-v2')}))

# M-L used-by near-miss: used-by names ENTRY with a suffix; substring hit.
results.append(run_case('M-L used-by path suffix (entry + ".bak")', 1,
                        data_files={'corpus/SOURCES.md': registry(used=ENTRY + '.bak')}))

# M-H carrier bytes swapped at the measured revision; pins in carriers.json
# unchanged and never compared against the actual carrier blobs (QUALITY 49).
def swap_carriers(data):
    for k in ('K1', 'K2', 'K3', 'K4'):
        data[f'corpus/evidence/round-37/c1/{k}/carrier.sqsh'] = b'SWAPPED-BYTES'
    return data
results.append(run_case('M-H carrier bytes swapped under frozen pins', 1,
                        mutate_data=swap_carriers))

# M-I measured revision does not descend from the freeze (orphan data commit).
results.append(run_case('M-I rev not a descendant of freeze', 1, orphan=True))

# M-J stub entry at the ENTRY path (green-check: the frozen counter must and
# does catch a stub without a source line — QUALITY 81 stub class).
results.append(run_case('M-J stub entry without source line (control)', 1,
                        data_files={ENTRY: '# E\n'}))

out = {'counter': 'tools/round-38/c1-counter.py (frozen bytes, imported unmodified)',
       'pkg65': PKG, 'cases': results}
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'r38c1-mutant-results.json'), 'w'), indent=1)
bad = [r['mutant'] for r in results if r['got_exit'] != r['want_exit'] and r['want_exit'] == 1 and r['got_exit'] == 0]
print('SURVIVING_BLIND:', json.dumps(bad))
sys.exit(0)
