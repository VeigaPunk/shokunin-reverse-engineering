#!/usr/bin/env python3
"""freeze-drift: list commits that touched a frozen claim path after its freeze.

Round-38 mistake M38-1: the round-38 attempt-1 L1 amended the frozen
predicate and counter twice (79f69347, f1010f67) after wave-1 seats had
scored carriers with the first-freeze counter, and labelled the amendment
"pre-scoring". QUALITY criterion 79 makes this gate the check: a claim's
rule is the bytes of its first freeze commit; if this gate prints any commit
between the freeze and the measured revision, the claim is scored with the
first-freeze bytes and the amendment is reported, never adopted.

Usage:
  freeze-drift.py --root LANE --freeze FREEZE --rev REV [--json-out PATH] PATH...
  freeze-drift.py --selftest

PATH arguments are repo-relative paths or git pathspec globs (quote them);
default set when none is given: the round-38 kill-rule set (claims doc,
both counters, carriers manifest, oracle tables).

Reads only git objects (git log over FREEZE..REV). Exit 0: no drift;
1: drift (the commits are listed); 2: unevaluable (unknown revision, or
FREEZE is not an ancestor of REV).

--selftest builds a throwaway fixture repository under $TMPDIR and exercises
eight green/red constructs (clean history, counter edited after the freeze,
non-ancestor range, glob path edited, unknown revision, --json-out parity,
empty range, default path set). It prints SELFTEST cases=n pass=n fail=n and
exits 0 only when every case passes; it touches no lane path.
"""
import argparse, json, os, shutil, subprocess, sys, tempfile

DEFAULT = [
    'plans/round-38-claims.md',
    'tools/round-38/c1-counter.py',
    'tools/round-38/c2-counter.py',
    '.ufo/waves/round-38/c1/carriers.json',
    'corpus/evidence/round-37/c1/*/oracle.tsv',
]

TOOL = os.path.abspath(__file__)


def git(root, *args):
    return subprocess.run(['git', '-C', root, *args], capture_output=True, text=True)


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if '--selftest' in argv:
        return selftest()
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--freeze', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--json-out')
    ap.add_argument('paths', nargs='*')
    a = ap.parse_args(argv)
    paths = a.paths or DEFAULT
    res = {'tool': 'freeze-drift', 'freeze': a.freeze, 'rev': a.rev, 'paths': paths}
    for r in (a.freeze, a.rev):
        if git(a.root, 'cat-file', '-e', f'{r}^{{commit}}').returncode:
            res.update(verdict='unevaluable', reason=f'unknown revision {r}')
            return finish(res, a.json_out, 2)
    if git(a.root, 'merge-base', '--is-ancestor', a.freeze, a.rev).returncode:
        res.update(verdict='unevaluable', reason='freeze is not an ancestor of rev')
        return finish(res, a.json_out, 2)
    log = git(a.root, 'log', '--format=%H%x09%cI%x09%s', '--name-only', '--no-renames',
              f'{a.freeze}..{a.rev}', '--', *[f':(glob){p}' for p in paths])
    if log.returncode:
        res.update(verdict='unevaluable', reason='git log failed: ' + log.stderr.strip()[:300])
        return finish(res, a.json_out, 2)
    drift, cur = [], None
    for line in log.stdout.splitlines():
        if '\t' in line:
            h, when, subj = line.split('\t', 2)
            cur = {'commit': h, 'committed': when, 'subject': subj, 'paths': []}
            drift.append(cur)
        elif line.strip() and cur is not None:
            cur['paths'].append(line.strip())
    res['drift'] = drift
    # Does REV still ship the freeze bytes? (a restore after drift leaves a commit list but no net diff)
    net = git(a.root, 'diff', '--name-only', '--no-renames', a.freeze, a.rev, '--', *[f':(glob){p}' for p in paths])
    res['net_changed'] = [x for x in net.stdout.splitlines() if x.strip()]
    res['ships_freeze_bytes'] = not res['net_changed']
    res['verdict'] = 'drift' if drift else 'clean'
    return finish(res, a.json_out, 1 if drift else 0)


def finish(res, out, code):
    text = json.dumps(res, indent=1)
    if out:
        with open(out, 'w') as f:
            f.write(text + '\n')
    print(text)
    return code


# --------------------------------------------------------------- selftest --
# The fixture reproduces the round-38 instrument shape (claims doc, both
# counters, the harness, the carriers manifest, one oracle) so the default
# path set is exercised too. Nothing here reads or writes a lane path.

FIXTURE = {
    'plans/round-38-claims.md': '# claims (fixture)\n',
    'tools/round-38/c1-counter.py': '#!/usr/bin/env python3\nprint("counter v0")\n',
    'tools/round-38/c2-counter.py': '#!/usr/bin/env python3\nprint("counter2 v0")\n',
    'tools/round-38/c1-run.sh': '#!/bin/sh\necho run v0\n',
    '.ufo/waves/round-38/c1/carriers.json': '{"carriers": []}\n',
    'corpus/evidence/round-37/c1/K1/oracle.tsv': 'K1\t0\n',
}
PATHS = list(FIXTURE)


def _g(root, *args):
    return subprocess.run(['git', '-C', root, *args], capture_output=True, text=True,
                          env={**os.environ, 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_TERMINAL_PROMPT': '0'})


def _put(root, rel, text):
    f = os.path.join(root, rel)
    os.makedirs(os.path.dirname(f) or root, exist_ok=True)
    with open(f, 'w') as fh:
        fh.write(text)


def _commit(root, msg):
    p = _g(root, 'add', '-A')
    if p.returncode:
        raise RuntimeError('git add: ' + p.stderr)
    p = _g(root, '-c', 'user.name=fx', '-c', 'user.email=fx@fx', '-c', 'commit.gpgsign=false',
           'commit', '-q', '--no-verify', '-m', msg)
    if p.returncode:
        raise RuntimeError('git commit: ' + p.stderr)
    return _g(root, 'rev-parse', 'HEAD').stdout.strip()


def _fixture(base):
    d = tempfile.mkdtemp(prefix='fx.', dir=base)
    p = _g(d, 'init', '-q', '-b', 'main')
    if p.returncode:
        raise RuntimeError('git init: ' + p.stderr)
    top = _g(d, 'rev-parse', '--show-toplevel').stdout.strip()
    if os.path.realpath(top) != os.path.realpath(d):
        raise RuntimeError(f'fixture toplevel {top!r} != {d!r}')
    for rel, text in FIXTURE.items():
        _put(d, rel, text)
    c = {}
    c['c0'] = _commit(d, 'base: frozen instruments')
    _put(d, 'notes.txt', 'unrelated note\n')
    c['c1'] = _commit(d, 'unrelated note after the freeze')
    _put(d, 'tools/round-38/c1-counter.py', '#!/usr/bin/env python3\nprint("counter v1")\n')
    c['c2'] = _commit(d, 'amend the counter after the freeze')
    _put(d, 'corpus/evidence/round-37/c1/K1/oracle.tsv', 'K1\t1\n')
    c['c3'] = _commit(d, 'amend an oracle after the freeze')
    _put(d, 'plans/round-38-claims.md', '# claims (amended)\n')
    c['c4'] = _commit(d, 'amend the claims after the freeze')
    return d, c


def _invoke(argv):
    return subprocess.run([sys.executable, '-I', '-B', TOOL, *argv], capture_output=True, text=True)


def selftest():
    base = os.environ.get('TMPDIR') or tempfile.gettempdir()
    os.makedirs(base, exist_ok=True)
    d = c = None
    cases = []
    try:
        d, c = _fixture(base)
        jout = os.path.join(base, 'freeze-drift.selftest.out.json')
        if os.path.exists(jout):
            os.remove(jout)

        def root_rev(freeze, rev, *extra):
            return ['--root', d, '--freeze', freeze, '--rev', rev, *extra]

        def case(name, expect, argv, *preds):
            cases.append({'name': name, 'expect': expect, 'argv': argv, 'preds': preds})

        def verdict_is(want):
            return lambda p, j: (isinstance(j, dict) and j.get('verdict') == want,
                                 f'verdict {None if not isinstance(j, dict) else j.get("verdict")!r} != {want!r}')

        def reason_is(want):
            return lambda p, j: (isinstance(j, dict) and j.get('reason') == want,
                                 f'reason {None if not isinstance(j, dict) else j.get("reason")!r} != {want!r}')

        def drift_empty():
            return lambda p, j: (isinstance(j, dict) and j.get('drift') == [], 'drift is not []')

        def drift_commits(want):
            return lambda p, j: (isinstance(j, dict) and [x.get('commit') for x in j.get('drift', [])] == want,
                                 f'drift commits != {want}')

        def drift_names(path):
            return lambda p, j: (isinstance(j, dict) and
                                 any(path in x.get('paths', []) for x in j.get('drift', [])),
                                 f'{path} not attributed in drift paths')

        def json_out_parity(p, j):
            try:
                with open(jout) as fh:
                    text = fh.read()
            except OSError as e:
                return False, f'json-out unreadable: {e}'
            return (text == p.stdout, 'json-out file differs from stdout')

        case('clean-history', 0, root_rev(c['c0'], c['c1'], *PATHS),
             verdict_is('clean'), drift_empty())
        case('counter-edited-after-freeze', 1, root_rev(c['c0'], c['c2'], *PATHS),
             verdict_is('drift'), drift_commits([c['c2']]),
             drift_names('tools/round-38/c1-counter.py'))
        case('non-ancestor-range', 2, root_rev(c['c3'], c['c1'], *PATHS),
             verdict_is('unevaluable'), reason_is('freeze is not an ancestor of rev'))
        case('glob-path-edited', 1, root_rev(c['c0'], c['c3'], *PATHS),
             verdict_is('drift'), drift_names('corpus/evidence/round-37/c1/K1/oracle.tsv'))
        case('unknown-revision', 2, root_rev(c['c0'], '0' * 40, *PATHS),
             verdict_is('unevaluable'),
             lambda p, j: (isinstance(j, dict) and str(j.get('reason', '')).startswith('unknown revision'),
                           'reason does not name the unknown revision'))
        case('json-out-parity', 1, root_rev(c['c0'], c['c2'], '--json-out', jout, *PATHS),
             verdict_is('drift'), json_out_parity)
        case('empty-range', 0, root_rev(c['c0'], c['c0'], *PATHS),
             verdict_is('clean'), drift_empty())
        case('default-path-set', 1, root_rev(c['c0'], c['c2']),
             verdict_is('drift'), drift_names('tools/round-38/c1-counter.py'))

        passed = 0
        for k in cases:
            p = _invoke(k['argv'])
            try:
                j = json.loads(p.stdout)
            except Exception:
                j = None
            why = []
            if p.returncode != k['expect']:
                why.append(f'exit {p.returncode} != {k["expect"]}')
            if not isinstance(j, dict):
                why.append('stdout is not one JSON object' + (f': {p.stderr.strip()[:160]}' if p.stderr.strip() else ''))
            else:
                for pred in k['preds']:
                    try:
                        ok, msg = pred(p, j)
                    except Exception as e:  # a predicate that blows up is a failed case, not a crash
                        ok, msg = False, f'predicate raised {e!r}'
                    if not ok:
                        why.append(msg)
            ok = not why
            passed += ok
            print(f"case {k['name']}: expect exit={k['expect']} got {p.returncode} {'PASS' if ok else 'FAIL'}")
            for w in why:
                print('  - ' + w)
        print(f'SELFTEST cases={len(cases)} pass={passed} fail={len(cases) - passed}')
        return 0 if passed == len(cases) else 1
    finally:
        if os.path.exists(os.path.join(base, 'freeze-drift.selftest.out.json')):
            os.remove(os.path.join(base, 'freeze-drift.selftest.out.json'))
        if d:
            shutil.rmtree(d, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
