#!/usr/bin/env python3
"""Forgery arms against the counter (scratch clones only). Each arm clones the green REV from
the apply.py fixture, applies ONE edit, commits in the scratch clone, and runs the draft counter
twice (plain, and --battery). usage: forge.py <scratch-dir> <freeze> <after-clone>"""
import hashlib, json, os, re, subprocess, sys

S, FREEZE, AFTER = sys.argv[1], sys.argv[2], sys.argv[3]
CTR = os.environ.get('CTR', '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/draft/tools/round-49/c2-mismatch.py')
LESSON = 'corpus/lessons/round-49.md'
sha = lambda b: hashlib.sha256(b).hexdigest()


def sh(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True)


def clone(name):
    d = os.path.join(S, name)
    sh(['rm', '-rf', d])
    sh(['git', 'clone', '-q', '--shared', AFTER, d])
    sh(['git', '-C', d, 'config', 'user.name', 'r49-forge'])
    sh(['git', '-C', d, 'config', 'user.email', 'r49-forge@dev.invalid'])
    top = sh(['git', '-C', d, 'rev-parse', '--show-toplevel']).stdout.decode().strip()
    assert top == d, (top, d)
    return d


def edit(d, path, fn):
    p = os.path.join(d, path)
    b = open(p, 'rb').read()
    nb = fn(b)
    assert nb != b, 'no-op edit: %s' % path
    open(p, 'wb').write(nb)


def commit(d):
    sh(['git', '-C', d, 'add', '-A'])
    sh(['git', '-C', d, 'commit', '-q', '-m', 'forgery'])
    return sh(['git', '-C', d, 'rev-parse', 'HEAD']).stdout.decode().strip()


def rep1(a, b):
    return lambda x: x.replace(a.encode(), b.encode(), 1)


def row_edit(a, b, rid):
    def f(x):
        out, hit = [], False
        for l in x.decode().split('\n'):
            if l.startswith('| %s ' % rid) and a in l:
                l, hit = l.replace(a, b, 1), True
            out.append(l)
        assert hit, 'row %s / %r not found' % (rid, a)
        return '\n'.join(out).encode()
    return f


def f5(x):
    # forged snapshot: the quote and the heading, nothing else; S147 pin rewritten to match
    return (b'<html><body><h2>2. Backdrop to Popper\xe2\x80\x99s Thought</h2><p>falsifiability as his '
            b'criterion for demarcating science from non-science: if a theory is incompatible with '
            b'possible empirical observations it is scientific.</p></body></html>\n')


def f7(x):
    j = json.loads(x)
    j['results'] = [r for r in j['results'] if r['name'] != 'C1Meaning']
    return (json.dumps(j, indent=2) + '\n').encode()


def f8(x):
    return x[:-1] + b' \n'  # one extra space before the final newline: raw and stripped digests move


def f8_arm(d):
    R = '.ufo/waves/round-48/l1/scores/c1-final-33f65a91.json'
    edit(d, R, f8)
    nb = open(os.path.join(d, R), 'rb').read()
    raw = sha(nb)
    st = sha(nb[:-1] if nb.endswith(b'\n') else nb)
    edit(d, LESSON, lambda x: re.sub(
        rb'c1_raw=[0-9a-f]{64} c1_stripped=[0-9a-f]{64} (c2_raw=[0-9a-f]{64} c2_stripped=[0-9a-f]{64}) report_c1=[0-9a-f]{8}',
        lambda m: ('c1_raw=%s c1_stripped=%s ' % (raw, st)).encode() + m.group(1) +
        (' report_c1=%s' % st[:8]).encode(), x, count=1))


ARMS = [
    ('F1-A2-dead-forged', 'lesson', lambda d: edit(d, LESSON, rep1(
        'dead=663f30ee7516942a0120e7de68fe88356e680822', 'dead=663f30ee00000000000000000000000000000000')),
     'A2 dead hash is not bound to the round-48 report; any non-commit with the same 8-hex prefix passes'),
    ('F2-A8-identified-forged', 'sources', lambda d: edit(d, 'corpus/SOURCES.md', lambda x: x.replace(
        b'Identified 2, screened 2, included 2', b'Identified 57, screened 2, included 2', 1)),
     'A8 identified count is not re-derived (only screened = included + excluded and identified >= screened)'),
    ('F3-A3-pointer-dropped', 'lesson', lambda d: edit(d, LESSON, rep1(
        'log_33f65a91=3440,3441,3444 ', '')),
     'A3 checks only the pointer keys present; a dropped hash that names LOG lines passes'),
    ('F4-A1-duplicate-line', 'lesson', lambda d: edit(d, LESSON, rep1(
        '- A1 declared=', '- A1 declared=0f06251bf6a3a6964c715f67243d4df12e854258 stale=b6f7ca2a6391964dfdedd477cd560bd42159873a\n- A1 declared=')),
     'a second, wrong A1 line before the true one: parser keeps the last line and stays green'),
    ('F5-A6-snapshot-forged-pin-rewritten', 'snapshot', lambda d: (
        edit(d, 'corpus/evidence/round-49/c2/popper.html', f5),
        edit(d, 'corpus/SOURCES.md', row_edit('2c2d48c6891418c46c372a780ce2e76c00bcc9716bb7603f169976d61b6ec207',
             sha(open(os.path.join(d, 'corpus/evidence/round-49/c2/popper.html'), 'rb').read()), 'S147'))),
     'A6 trusts the committed snapshot bytes and their pin; the sha256 is not checked against the fetched source'),
    ('F6-A7-teaches-inverted', 'sources', lambda d: edit(d, 'corpus/SOURCES.md', row_edit(
        'EX_USAGE is 64, not 2', 'EX_USAGE is 2, not 64', 'S148')),
     'A7 teaches cell checked by token presence (EX_USAGE and 64); the inverted statement passes the atom'),
    ('F7-A4-round48-artifact-edited', 'artifact', lambda d: edit(
        d, '.ufo/waves/round-48/r48-w1-results.json', f7) or edit(
        d, LESSON, rep1('seats=75 reports=72 missing=C1Battery,C1Meaning,ScribeReportNumbers',
                        'seats=74 reports=72 missing=C1Battery,ScribeReportNumbers')),
     'A4 re-derives from the round-48 results file at REV, not LANE_BASE; a 74-seat file passes'),
    ('F8-A5-receipt-edited', 'artifact', lambda d: f8_arm(d),
     'A5 derives digests from the round-48 receipt at REV, not LANE_BASE; a re-digested receipt and its lesson line pass'),
    ('F9-freeze-tool-edited-after-freeze', 'tool', lambda d: edit(
        d, 'tools/round-49/c2-mismatch.py', lambda x: x + b'# edit after freeze\n'),
     'a tool edit after FREEZE must exit 2 frozen_path_changed'),
]


def score(d, rev, battery):
    args = ['python3', '-I', '-B', CTR, '--root', d, '--rev', rev, '--freeze', FREEZE]
    if battery:
        args.append('--battery')
    p = sh(args, cwd=d)
    try:
        j = json.loads(p.stdout.decode())
    except ValueError:
        j = {}
    return {'exit': p.returncode, 'stdout_sha256': sha(p.stdout), 'reason': j.get('reason'),
            'mismatches': j.get('mismatches'),
            'green_atoms': sorted(k for k, v in j.get('atoms', {}).items() if v.get('ok')),
            'battery_failing': (j.get('battery') or {}).get('failing')}


out = {}
for name, _, fn, why in ARMS:
    d = clone(name)
    fn(d)
    rev = commit(d)
    out[name] = {'why': why, 'rev': rev, 'plain': score(d, rev, False), 'battery': score(d, rev, True)}
    print(name, json.dumps(out[name]['plain'], sort_keys=True), '| battery', json.dumps(out[name]['battery'], sort_keys=True)[:300])
    sh(['rm', '-rf', d])
json.dump(out, open(os.path.join(S, 'forge-results.json'), 'w'), indent=1, sort_keys=True)
