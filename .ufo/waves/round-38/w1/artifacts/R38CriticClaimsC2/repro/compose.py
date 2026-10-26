#!/usr/bin/env python3
"""Composed kill variants + independent re-derivation of the frozen c2-2/c2-3 control fixtures."""
import json, os, shutil, subprocess, sys, tempfile

S = os.environ['S']
FX = os.path.join(S, 'fx')
BASE = '77091b492cc53f8743bd0701b1e7d5e66123dd84'
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
COUNTER = os.path.join(LANE, 'tools/round-38/c2-counter.py')
ENV = dict(os.environ, GIT_AUTHOR_NAME='critic', GIT_AUTHOR_EMAIL='c@i',
           GIT_COMMITTER_NAME='critic', GIT_COMMITTER_EMAIL='c@i')
DECOY = ('| REA MCP server | x | round-19 re-grepped pin record '
         '`.ufo/waves/round-19/evidence/province-pins-integrated.json`; doctor outputs in '
         '`.ufo/waves/round-19/evidence/doctor/`; historical readiness probe 2026-10-13 |')


def git(*a):
    return subprocess.run(['git', '-C', FX] + list(a), capture_output=True, text=True, check=True)


def read(p):
    return open(os.path.join(FX, p)).read()


def wri(p, t):
    full = os.path.join(FX, p)
    os.makedirs(os.path.dirname(full) or FX, exist_ok=True)
    open(full, 'w').write(t)


def fresh(branch):
    git('checkout', '-q', '-B', branch, BASE)
    git('clean', '-qfd')


def bump_adjacent():
    s = read('SHONEN.md')
    assert '`PROVINCE.md:97-125`' in s
    wri('SHONEN.md', s.replace('`PROVINCE.md:97-125`', '`PROVINCE.md:98-126`'))


def shadow_row_after():
    p = read('PROVINCE.md').splitlines(True)
    i = next(n for n, l in enumerate(p) if l.startswith('| REA MCP server |'))
    p.insert(i + 1, DECOY + '\n')
    wri('PROVINCE.md', ''.join(p))


def intended_repair():
    lines = read('PROVINCE.md').splitlines(True)
    i = next(n for n, l in enumerate(lines) if l.startswith('| REA MCP server |'))
    lines[i] = lines[i].replace('doctor outputs in `evidence/doctor/`',
                                'doctor outputs in `.ufo/waves/round-19/evidence/doctor/`')
    wri('PROVINCE.md', ''.join(lines))


def shonen_shadow():
    s = read('SHONEN.md')
    s = s.replace('17/17 rule blocks', '3/3 rule blocks')
    box = ('- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources\n'
           '  asserted: `SKILL.md:81-314` (craft section; 17/17 rule blocks have resolvable citations, '
           'not a full semantic audit) at round-14 work commit `3e99fbd6f05dc05341bdfbbd7e3b2b86785abc22`; '
           '`SCORECARD.md`, command A; no promotion verifier.\n')
    wri('SHONEN.md', s.rstrip('\n') + '\n' + box)


def junk_unit():
    wri('corpus/knowledge/2026-10-26-zzz-stub.md', 'stub\n')
    r = read('corpus/README.md')
    head, rest = r.split('| section | entries | state |', 1)
    rest = rest.replace('|---|---|---|\n', '|---|---|---|\n| junk | `2026-10-26-zzz-stub` | held |\n', 1)
    wri('corpus/README.md', head + '| section | entries | state |' + rest)
    s = read('SCORECARD.md')
    wri('SCORECARD.md', s.replace('124/124 knowledge files mapped', '125/125 knowledge files mapped'))


def both(fs):
    def run():
        for f in fs:
            f()
    return run


COMPOSED = [
    ('c-shadow-and-range', both([shadow_row_after, bump_adjacent]),
     '(b) bad pointer kept verbatim + shadow duplicate row + Adjacent range refreshed'),
    ('c-shonen-shadow-and-repair', both([intended_repair, shonen_shadow]),
     '(b) intended repair plus a contradictory SHONEN box shadowed by a duplicate'),
    ('c-junk-unit-and-repair', both([intended_repair, junk_unit]),
     '(a) intended repair plus a 1-line stub counted as a mapped knowledge file'),
    ('c-repair-only', intended_repair, 'intended repair alone (known-good control)'),
]

out = []
for branch, fn, desc in COMPOSED:
    fresh(branch)
    fn()
    git('add', '-A')
    git('commit', '-qm', branch)
    rev = git('rev-parse', 'HEAD').stdout.strip()
    r = subprocess.run(['python3', '-I', '-B', COUNTER, '--root', FX, '--rev', rev, '--base', BASE,
                        '--json-out', os.path.join(S, branch + '.json')], capture_output=True, text=True, env=ENV)
    res = json.loads(r.stdout)
    rec = {'branch': branch, 'desc': desc, 'rev': rev, 'exit': r.returncode, **{k: res.get(k) for k in
           ('mismatches', 'unresolved', 'assertion_mismatches', 'guards_ok', 'met_target')}}
    rec['full'] = json.load(open(os.path.join(S, branch + '.json')))
    out.append(rec)
    print(json.dumps({k: rec[k] for k in ('branch', 'rev', 'exit', 'mismatches', 'unresolved',
                                          'assertion_mismatches', 'guards_ok', 'met_target')}))

# ---- re-derive the frozen c2-2 / c2-3 fixtures from the committed generator, with full receipt
sys.path.insert(0, os.path.join(LANE, 'tools/round-38'))
import importlib.util
spec = importlib.util.spec_from_file_location('gc', os.path.join(LANE, 'tools/round-38/gen-controls.py'))
gc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gc)
ctl = []
for kind, defect in (('c2-1', 'junk'), ('c2-2', 'delete'), ('c2-3', 'substitute')):
    d, b, rv, c = gc.c2_fixture(kind, defect)
    tree = {}
    for root, _, fs in os.walk(d):
        if '/.git' in root:
            continue
        for f in fs:
            p = os.path.relpath(os.path.join(root, f), d)
            tree[p] = open(os.path.join(root, f)).read()
    r = subprocess.run(['python3', '-I', '-B', COUNTER, '--root', d, '--rev', rv, '--base', b],
                       capture_output=True, text=True)
    res = json.loads(r.stdout)
    diff = {}
    for p, t in tree.items():
        base_t = subprocess.run(['git', '-C', d, 'show', f'{b}:{p}'], capture_output=True, text=True).stdout
        if base_t != t:
            diff[p] = {'base': base_t, 'rev': t}
    ctl.append({'kind': kind, 'defect': defect, 'base': b, 'rev': rv, 'exit': r.returncode,
                'output': res, 'changed_files': diff})
    print(json.dumps({'control': kind, 'defect': defect, 'exit': r.returncode,
                      'mismatches': res.get('mismatches'), 'guards_ok': res.get('guards_ok')}))
    shutil.rmtree(d, ignore_errors=True)
json.dump({'composed': out, 'controls': ctl}, open(os.path.join(S, 'composed.json'), 'w'), indent=1)
