#!/usr/bin/env python3
"""intended-doc: bind a repaired self-assessment pointer to its intended document.

Round-38 mistake M38-6: the frozen R38-C2 counter accepts any pointer whose
path exists, so materialising a stub file at the unresolved base path
(`evidence/doctor/doctor-6.5.0.txt`, no PROVINCE edit) scores the same
"1 -> 0 mismatches" as the real repair (wave-2 seat R38W2C2Controls, S2).
QUALITY 81 makes this the check: the pointer in the named unit must name
the intended path frozen with the claim, and that path's git tree/blob at the
measured revision must equal its object at the base, i.e. the document already
existed and was not written by the claimant.

Usage:
  intended-doc.py --root LANE --rev REV --base BASE --file PROVINCE.md \
      --unit 'REA MCP server' --intended .ufo/waves/round-19/evidence/doctor/
  intended-doc.py --selftest

Reads only git objects. Exit 0: bound; 1: not bound (reasons listed); 2: unevaluable.

--selftest builds a throwaway fixture repository under $TMPDIR and exercises
nine green/red constructs (bound, pointer names another path, stub materialised
at the intended path, intended path absent at both ends, intended document
edited after the base, duplicate unit rows, unit row absent, missing --file,
unknown revision). It prints SELFTEST cases=n pass=n fail=n and exits 0 only
when every case passes; it touches no lane path.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile

TOKEN = re.compile(r'`([^`\s]+)`')

TOOL = os.path.abspath(__file__)


def git(root, *a):
    return subprocess.run(['git', '-C', root, *a], capture_output=True, text=True)


def obj(root, rev, path):
    p = git(root, 'rev-parse', '--verify', '-q', f'{rev}:{path.rstrip("/")}')
    return p.stdout.strip() if p.returncode == 0 else None


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if '--selftest' in argv:
        return selftest()
    ap = argparse.ArgumentParser()
    for k in ('root', 'rev', 'base', 'file', 'unit', 'intended'):
        ap.add_argument('--' + k, required=True)
    a = ap.parse_args(argv)
    res = {'tool': 'intended-doc', 'rev': a.rev, 'base': a.base, 'file': a.file, 'unit': a.unit, 'intended': a.intended}
    text = git(a.root, 'show', f'{a.rev}:{a.file}')
    if text.returncode or obj(a.root, a.base, a.file) is None:
        res['verdict'] = 'unevaluable'
        print(json.dumps(res))
        return 2
    rows = [l for l in text.stdout.splitlines() if l.lstrip().startswith('|') and l.strip().strip('|').split('|')[0].strip() == a.unit]
    reasons = []
    if len(rows) != 1:
        reasons.append(f'unit rows found: {len(rows)} (need exactly 1)')
    toks = TOKEN.findall(rows[0]) if len(rows) == 1 else []
    if a.intended not in toks:
        reasons.append('intended path not named in the unit row')
    at_rev, at_base = obj(a.root, a.rev, a.intended), obj(a.root, a.base, a.intended)
    res['object_at_rev'], res['object_at_base'] = at_rev, at_base
    if at_base is None:
        reasons.append('intended document absent at base (written by the claimant?)')
    elif at_rev != at_base:
        reasons.append('intended document changed between base and rev')
    res['reasons'] = reasons
    res['verdict'] = 'bound' if not reasons else 'not-bound'
    print(json.dumps(res, indent=1))
    return 0 if not reasons else 1


# --------------------------------------------------------------- selftest --
# Fixture shape follows the round-38 unit row: one markdown table row whose
# first cell is the unit name and whose pointer is a single backticked path.
# Nothing here reads or writes a lane path.

UNIT = 'REA MCP server'
INTENDED = 'docs/doctor/'
HEAD = '# PROVINCE (fixture)\n\n| unit | pointer |\n| --- | --- |\n'


def _table(rows):
    return HEAD + ''.join(f'| {u} | `{p}` |\n' if p is not None else f'| {u} | none |\n' for u, p in rows)


OTHER = ('Other', 'docs/other/')
DOCTOR = 'docs/doctor/README.txt'
OTHERDOC = 'docs/other/README.txt'


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
    c = {}
    _put(d, DOCTOR, 'doctor evidence (fixture)\n')
    _put(d, OTHERDOC, 'other evidence (fixture)\n')
    _put(d, 'PROVINCE.md', _table([(UNIT, 'docs/nowhere/'), OTHER]))
    c['c0'] = _commit(d, 'base: pointer names an unresolved path')
    _put(d, 'PROVINCE.md', _table([(UNIT, INTENDED), OTHER]))
    c['c1'] = _commit(d, 'pointer repaired to the intended document')
    _put(d, 'PROVINCE.md', _table([(UNIT, 'docs/stub/'), OTHER]))
    _put(d, 'docs/stub/README.txt', 'stub written by the claimant\n')
    c['c2'] = _commit(d, 'stub materialised at a new path and named')
    _put(d, 'PROVINCE.md', _table([(UNIT, INTENDED), OTHER]))
    _put(d, DOCTOR, 'doctor evidence (fixture)\ndoctor evidence (rewritten by the claimant)\n')
    c['c3'] = _commit(d, 'intended document edited after the base')
    _put(d, 'PROVINCE.md', _table([(UNIT, 'docs/other/'), OTHER]))
    c['c4'] = _commit(d, 'pointer names a different existing document')
    _put(d, 'PROVINCE.md', _table([OTHER]))
    c['c5'] = _commit(d, 'unit row removed')
    _put(d, 'PROVINCE.md', _table([(UNIT, INTENDED), (UNIT, 'docs/other/'), OTHER]))
    c['c6'] = _commit(d, 'duplicate unit rows')
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

        def argv_for(rev, intended=INTENDED, file='PROVINCE.md', base_rev=None):
            return ['--root', d, '--rev', rev, '--base', base_rev or c['c0'],
                    '--file', file, '--unit', UNIT, '--intended', intended]

        def case(name, expect, argv, *preds):
            cases.append({'name': name, 'expect': expect, 'argv': argv, 'preds': preds})

        def verdict_is(want):
            return lambda j: (j.get('verdict') == want, f'verdict {j.get("verdict")!r} != {want!r}')

        def reasons_contain(fragment):
            return lambda j: (any(fragment in r for r in j.get('reasons', [])),
                              f'no reason contains {fragment!r}; reasons={j.get("reasons")}')

        def reasons_empty(j):
            return (j.get('reasons') == [], f'reasons not empty: {j.get("reasons")}')

        def objects_equal(j):
            return (j.get('object_at_rev') is not None and j.get('object_at_rev') == j.get('object_at_base'),
                    'object_at_rev != object_at_base')

        case('bound', 0, argv_for(c['c1']),
             verdict_is('bound'), reasons_empty, objects_equal)
        case('pointer-names-another-path', 1, argv_for(c['c4']),
             verdict_is('not-bound'), reasons_contain('intended path not named in the unit row'))
        case('stub-at-intended-path', 1, argv_for(c['c2'], intended='docs/stub/'),
             verdict_is('not-bound'), reasons_contain('absent at base'))
        case('intended-path-missing', 1, argv_for(c['c0'], intended='docs/nowhere/'),
             verdict_is('not-bound'), reasons_contain('absent at base'))
        case('intended-doc-edited-after-base', 1, argv_for(c['c3']),
             verdict_is('not-bound'), reasons_contain('changed between base and rev'))
        case('duplicate-unit-rows', 1, argv_for(c['c6']),
             verdict_is('not-bound'), reasons_contain('unit rows found: 2'))
        case('unit-row-absent', 1, argv_for(c['c5']),
             verdict_is('not-bound'), reasons_contain('unit rows found: 0'))
        case('file-absent-at-base', 2, argv_for(c['c1'], file='NOTICES.md'),
             verdict_is('unevaluable'))
        case('unknown-revision', 2, argv_for('0' * 40),
             verdict_is('unevaluable'))

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
                        ok, msg = pred(j)
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
        if d:
            shutil.rmtree(d, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
