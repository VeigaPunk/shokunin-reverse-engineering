#!/usr/bin/env python3
"""Second wave: same defect class on SCORECARD, masked/decoy pointers, unverified history counts."""
import json, os, subprocess

S = os.environ['S']
FX = os.path.join(S, 'fx')
BASE = '77091b492cc53f8743bd0701b1e7d5e66123dd84'
COUNTER = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-38/c2-counter.py'
ENV = dict(os.environ, GIT_AUTHOR_NAME='critic', GIT_AUTHOR_EMAIL='c@i',
           GIT_COMMITTER_NAME='critic', GIT_COMMITTER_EMAIL='c@i')


def git(*a):
    return subprocess.run(['git', '-C', FX] + list(a), capture_output=True, text=True, check=True)


def read(p):
    return open(os.path.join(FX, p)).read()


def wri(p, t):
    open(os.path.join(FX, p), 'w').write(t)


def fresh(b):
    git('checkout', '-q', '-B', b, BASE)
    git('clean', '-qfd')


def repair():
    lines = read('PROVINCE.md').splitlines(True)
    i = next(n for n, l in enumerate(lines) if l.startswith('| REA MCP server |'))
    lines[i] = lines[i].replace('doctor outputs in `evidence/doctor/`',
                                'doctor outputs in `.ufo/waves/round-19/evidence/doctor/`')
    wri('PROVINCE.md', ''.join(lines))


def shadow_owned_axis():
    """Duplicate `## Owned axes` coverage row: first row's count left wrong, later row right."""
    s = read('SCORECARD.md').splitlines(True)
    i = next(n for n, l in enumerate(s) if l.startswith('| coverage |'))
    assert '124/124 knowledge files mapped' in s[i]
    s[i] = s[i].replace('124/124 knowledge files mapped', '7/7 knowledge files mapped')
    dup = ('| coverage | 9.72 -> 10.0 | 124/124 knowledge files mapped after the round-36 landing | '
           '`corpus/README.md` `## Coverage map`; command A | round 36 |\n')
    s.insert(i + 1, dup)
    wri('SCORECARD.md', ''.join(s))


def decoy_masked_glob():
    """New Core row whose only pointer is backticked but fails the counter's token grammar."""
    p = read('PROVINCE.md').splitlines(True)
    i = next(n for n, l in enumerate(p) if l.startswith('| REA MCP server |'))
    p.insert(i + 1, '| squashfs probe outputs | x | `corpus/evidence/round-38/c1/*` (unresolvable glob) |\n')
    wri('PROVINCE.md', ''.join(p))


def decoy_plaintext():
    """New Core row whose unresolvable reference is written without backticks."""
    p = read('PROVINCE.md').splitlines(True)
    i = next(n for n, l in enumerate(p) if l.startswith('| REA MCP server |'))
    p.insert(i + 1, '| squashfs probe outputs | x | corpus/evidence/round-38/c1/nonexistent.json (plain text) |\n')
    wri('PROVINCE.md', ''.join(p))


def history_count():
    """The revision-labelled historical recount inside the scored cell left unverified."""
    s = read('SCORECARD.md')
    assert '122/122 at `cab59f221fe19726b5692bfa4d9a9679e96b8a73`' in s
    wri('SCORECARD.md', s.replace('122/122 at `cab59f221fe19726b5692bfa4d9a9679e96b8a73`',
                                  '999/999 at `cab59f221fe19726b5692bfa4d9a9679e96b8a73`'))


def both(a, b):
    def run():
        a()
        b()
    return run


CASES = [
    ('d-shadow-owned-axis', both(repair, shadow_owned_axis),
     '(b) SCORECARD Owned-axes duplicate row shadows a wrong count'),
    ('d-decoy-masked-glob', both(repair, decoy_masked_glob),
     '(f) new Core row with an unresolvable backticked glob pointer'),
    ('d-decoy-plaintext', both(repair, decoy_plaintext),
     '(f) new Core row with an unresolvable plain-text pointer'),
    ('d-history-count', both(repair, history_count),
     'history recount 999/999 inside the scored coverage cell'),
]

out = []
for branch, fn, desc in CASES:
    fresh(branch)
    fn()
    git('add', '-A')
    git('commit', '-qm', branch)
    rev = git('rev-parse', 'HEAD').stdout.strip()
    r = subprocess.run(['python3', '-I', '-B', COUNTER, '--root', FX, '--rev', rev, '--base', BASE,
                        '--json-out', os.path.join(S, branch + '.json')], capture_output=True, text=True, env=ENV)
    res = json.loads(r.stdout)
    full = json.load(open(os.path.join(S, branch + '.json')))
    rec = {'branch': branch, 'desc': desc, 'rev': rev, 'exit': r.returncode,
           **{k: res.get(k) for k in ('mismatches', 'unresolved', 'assertion_mismatches', 'guards_ok', 'met_target')},
           'pointers': full.get('pointers'), 'guards': full.get('guards'), 'observed': full.get('observed')}
    out.append(rec)
    print(json.dumps({k: rec[k] for k in ('branch', 'rev', 'exit', 'mismatches', 'unresolved',
                                          'assertion_mismatches', 'guards_ok', 'met_target', 'pointers')}))
json.dump(out, open(os.path.join(S, 'probes2.json'), 'w'), indent=1)
