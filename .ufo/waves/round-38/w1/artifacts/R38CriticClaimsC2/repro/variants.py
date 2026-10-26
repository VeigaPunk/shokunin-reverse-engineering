#!/usr/bin/env python3
"""Attack P38-C2 with shortcut variants on a scratch clone of the lane at base 77091b49."""
import json, os, subprocess, sys

S = os.environ['S']
FX = os.path.join(S, 'fx')
BASE = '77091b492cc53f8743bd0701b1e7d5e66123dd84'
COUNTER = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-38/c2-counter.py'
ENV = dict(os.environ, GIT_AUTHOR_NAME='critic', GIT_AUTHOR_EMAIL='c@i',
           GIT_COMMITTER_NAME='critic', GIT_COMMITTER_EMAIL='c@i')
BAD = 'evidence/doctor/`'
GOOD = '.ufo/waves/round-19/evidence/doctor/`'
DECOY = ('| REA MCP server | x | round-19 re-grepped pin record '
         '`.ufo/waves/round-19/evidence/province-pins-integrated.json`; doctor outputs in '
         '`.ufo/waves/round-19/evidence/doctor/`; historical readiness probe 2026-10-13 |')


def git(*a, **kw):
    return subprocess.run(['git', '-C', FX] + list(a), capture_output=True, text=True, check=kw.get('check', True))


def read(p):
    return open(os.path.join(FX, p)).read()


def wri(p, t):
    full = os.path.join(FX, p)
    os.makedirs(os.path.dirname(full) or FX, exist_ok=True)
    open(full, 'w').write(t)


def fresh(branch):
    git('checkout', '-q', '-B', branch, BASE)
    git('clean', '-qfd')


def row_replace(old, new):
    """Replace inside the single `| REA MCP server |` Core row only."""
    lines = read('PROVINCE.md').splitlines(True)
    i = next(n for n, l in enumerate(lines) if l.startswith('| REA MCP server |'))
    assert lines[i].count(old) == 1, (old, lines[i].count(old))
    lines[i] = lines[i].replace(old, new)
    wri('PROVINCE.md', ''.join(lines))


def v_intended():
    """Control-positive: the intended repair (pointer to the committed doctor tree)."""
    row_replace(BAD, GOOD)


def v_shadow_after():
    """(b) Keep the bad row verbatim; append a duplicate row with the same first cell."""
    p = read('PROVINCE.md').splitlines(True)
    i = next(n for n, l in enumerate(p) if l.startswith('| REA MCP server |'))
    p.insert(i + 1, DECOY + '\n')
    wri('PROVINCE.md', ''.join(p))


def v_shadow_before():
    """Order control: the duplicate placed above the bad row (last wins -> should stay red)."""
    p = read('PROVINCE.md').splitlines(True)
    i = next(n for n, l in enumerate(p) if l.startswith('| REA MCP server |'))
    p.insert(i, DECOY + '\n')
    wri('PROVINCE.md', ''.join(p))


def v_same_basename():
    """(d) Substitute a different document that shares the basename `evidence/doctor`."""
    wri('corpus/evidence/doctor/doctor-6.5.0.txt', 'forged\n')
    wri('corpus/evidence/doctor/doctor-6.7.0.txt', 'forged\n')
    row_replace(BAD, 'corpus/evidence/doctor/`')


def v_delete_padded():
    """(c) Delete the bad pointer, pad the global pointer total elsewhere."""
    row_replace('doctor outputs in `evidence/doctor/`', 'doctor outputs unpublished')
    p = read('PROVINCE.md')
    p = p.replace('| sasquatch squashfs recursion |',
                  '| sasquatch squashfs recursion `plans/` |', 1)
    wri('PROVINCE.md', p)


def v_junk_counts():
    """(a) Junk unit: empty knowledge stub + coverage-map token + count bumped to match."""
    wri('corpus/knowledge/2026-10-26-zzz-stub.md', 'stub\n')
    r = read('corpus/README.md')
    head, rest = r.split('| section | entries | state |', 1)
    rest = rest.replace('|---|---|---|\n', '|---|---|---|\n| junk | `2026-10-26-zzz-stub` | held |\n', 1)
    wri('corpus/README.md', head + '| section | entries | state |' + rest)
    s = read('SCORECARD.md')
    assert '124/124 knowledge files mapped' in s
    wri('SCORECARD.md', s.replace('124/124 knowledge files mapped', '125/125 knowledge files mapped'))


def v_shonen_shadow():
    """(b) SHONEN box: leave a contradictory claim, shadow it with a duplicate box text."""
    s = read('SHONEN.md')
    assert s.count('17/17 rule blocks') == 1
    s = s.replace('17/17 rule blocks', '3/3 rule blocks')
    box = ('- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources\n'
           '  asserted: `SKILL.md:81-314` (craft section; 17/17 rule blocks have resolvable citations, '
           'not a full semantic audit) at round-14 work commit `3e99fbd6f05dc05341bdfbbd7e3b2b86785abc22`; '
           '`SCORECARD.md`, command A; no promotion verifier.\n')
    wri('SHONEN.md', s.rstrip('\n') + '\n' + box)


def v_decoy_row():
    """(f) Decoy PROVINCE Core row with a unique first cell; bad row untouched."""
    p = read('PROVINCE.md').splitlines(True)
    i = next(n for n, l in enumerate(p) if l.startswith('| REA MCP server |'))
    p.insert(i + 1, DECOY + '\n')
    wri('PROVINCE.md', ''.join(p).replace('| REA MCP server | x | round-19 re-grepped pin record '
                                         '`.ufo/waves/round-19/evidence/province-pins-integrated.json`; '
                                         'doctor outputs in `.ufo/waves/round-19/evidence/doctor/`; '
                                         'historical readiness probe 2026-10-13 |',
                                         '| doctor recheck | x | `.ufo/waves/round-19/evidence/province-pins-integrated.json` '
                                         '`.ufo/waves/round-19/evidence/doctor/` |', 1))


def v_remove_unit():
    """(e) Remove one Capabilities row (the round-36 squashfs row)."""
    s = read('SCORECARD.md').splitlines(True)
    keep = [l for l in s if not l.startswith('| REA SquashFS recursion through sasquatch (LE v4) |')]
    assert len(keep) == len(s) - 1
    wri('SCORECARD.md', ''.join(keep))


VARIANTS = [
    ('v-intended-repair', v_intended, 'intended: pointer to .ufo/waves/round-19/evidence/doctor/', 'green-want'),
    ('v-shadow-row-after', v_shadow_after, '(b) shadow duplicate Core row after the bad one', 'kill-want'),
    ('v-shadow-row-before', v_shadow_before, 'order control: duplicate above the bad row', 'red-want'),
    ('v-same-basename-doc', v_same_basename, '(d) substituted doc sharing basename evidence/doctor', 'kill-want'),
    ('v-delete-padded', v_delete_padded, '(c) delete bad pointer, pad global total', 'red-want'),
    ('v-junk-counts', v_junk_counts, '(a) stub knowledge unit + bumped matching count', 'measure'),
    ('v-shonen-shadow', v_shonen_shadow, '(b/f) SHONEN contradictory box shadowed by duplicate', 'kill-want'),
    ('v-decoy-row', v_decoy_row, '(f) decoy Core row, unique first cell', 'red-want'),
    ('v-remove-unit', v_remove_unit, '(e) remove a Capabilities row', 'red-want'),
]

out = []
for branch, fn, desc, want in VARIANTS:
    fresh(branch)
    fn()
    git('add', '-A')
    git('commit', '-qm', branch)
    rev = git('rev-parse', 'HEAD').stdout.strip()
    r = subprocess.run(['python3', '-I', '-B', COUNTER, '--root', FX, '--rev', rev, '--base', BASE,
                        '--json-out', os.path.join(S, branch + '.json')],
                       capture_output=True, text=True, env=ENV)
    try:
        res = json.loads(r.stdout)
    except Exception:
        res = {'raw': r.stdout, 'err': r.stderr[-2000:]}
    rec = {'branch': branch, 'desc': desc, 'rev': rev, 'exit': r.returncode,
           'mismatches': res.get('mismatches'), 'unresolved': res.get('unresolved'),
           'assertion_mismatches': res.get('assertion_mismatches'),
           'guards_ok': res.get('guards_ok'), 'met_target': res.get('met_target'),
           'pointers': res.get('pointers'), 'guard_detail': None}
    j = os.path.join(S, branch + '.json')
    if os.path.exists(j):
        full = json.load(open(j))
        rec['pointers'] = full.get('pointers')
        rec['guard_detail'] = full.get('guards')
    out.append(rec)
    print(json.dumps(rec))
json.dump(out, open(os.path.join(S, 'variants.json'), 'w'), indent=1)
