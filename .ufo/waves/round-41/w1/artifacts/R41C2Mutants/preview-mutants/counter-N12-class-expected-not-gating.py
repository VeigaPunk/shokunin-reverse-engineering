#!/usr/bin/env python3
"""v3-counter-preview — R41C2Mutants reference preview, NOT the frozen contract.

Executes the two round-41 counter clauses named in plans/round-41-claims.md
(DRAFT) that the round-40 counter does not have:

  * evaluator-vs-table comparison — the counter must compare the interpreter's
    (label, action) pair for EVERY held-out envelope against the independent
    evaluator's pair (round-40 closure D3);
  * class_expected binding — the generator's own class expectation must agree
    with the evaluator on every envelope; a disagreement is reported and fails
    the claim.

(restore-does-not-unblock is exercised on the real round-40 counter — see
R41-N01/N14 — because that machinery already exists there.)

Stub executables stand in for the v3 interpreter (reads a JSON "table") and the
independent evaluator (reads its own map, never the table).  Deviations are
injected per case.  CLI: --fixture DIR | --selftest.  Exit 0 met / 1 not met /
2 unevaluable / 1 selftest failure.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

STUB_INTERP = r'''#!/usr/bin/env python3
import argparse, json, sys
ap = argparse.ArgumentParser()
ap.add_argument('--skill', required=True)
ap.add_argument('envs', nargs='*')
a = ap.parse_args()
table = json.load(open(a.skill))
for p in a.envs:
    env = json.load(open(p))
    pair = (table.get('override', {}).get(env['stub_id'])
            or table['classes'][env['stub_class']])
    sys.stdout.write('%s\t%s\t%s\n' % (p, pair[0], pair[1]))
'''

STUB_EVAL = r'''#!/usr/bin/env python3
import argparse, json, sys
ap = argparse.ArgumentParser()
ap.add_argument('--map', required=True)
ap.add_argument('envs', nargs='*')
a = ap.parse_args()
m = json.load(open(a.map))
for p in a.envs:
    env = json.load(open(p))
    if env['stub_id'] in m.get('crash', []):
        sys.stderr.write('evaluator exploded on %s\n' % env['stub_id'])
        sys.exit(3)
    pair = (m.get('override', {}).get(env['stub_id'])
            or m['classes'][env['true_class']])
    sys.stdout.write('%s\t%s\t%s\n' % (p, pair[0], pair[1]))
'''


def pairs_equal(a, b):
    return a is not None and b is not None and list(a) == list(b)


def run_pair(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if p.returncode != 0:
        return None
    lines = [l for l in p.stdout.splitlines() if l.strip()]
    if len(lines) != 1:
        return None
    parts = lines[0].split('\t')
    return (parts[1], parts[2]) if len(parts) >= 3 else None


def score(fdir):
    man = json.load(open(os.path.join(fdir, 'manifest.json')))
    carriers = [c for c in man.get('carriers', []) if isinstance(c, dict)]
    ids = [c['id'] for c in carriers]
    tpair = {}
    epair = {}
    for c in carriers:
        env = os.path.join(fdir, c['envelope'])
        pi = run_pair([sys.executable, '-I', '-B', os.path.join(fdir, 'interp.py'),
                       '--skill', os.path.join(fdir, 'skill.json'), env])
        pe = run_pair([sys.executable, '-I', '-B', os.path.join(fdir, 'evaluator.py'),
                       '--map', os.path.join(fdir, 'evalmap.json'), env])
        tpair[c['id']] = pi
        epair[c['id']] = pe
    b = {}
    b['envelopes_scored'] = bool(carriers) and all(
        tpair.get(cid) is not None and epair.get(cid) is not None for cid in ids)
    b['table_matches_evaluator'] = bool(carriers) and all(
        pairs_equal(tpair.get(cid), epair.get(cid)) for cid in ids)
    b['class_expected_agrees'] = bool(carriers) and all(
        pairs_equal((c.get('expected_label'), c.get('expected_action')),
                    epair.get(c['id']))
        for c in carriers)
    bindings_ok = all(v is True for k, v in b.items()
                      if k != 'class_expected_agrees')
    met = bool(carriers) and bindings_ok
    res = {'n': len(carriers), 'bindings': b,
           'bindings_false': sorted(k for k, v in b.items() if v is not True),
           'met_target': met, 'exit_code': 0 if met else 1}
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(prog='v3-counter-preview.py')
    ap.add_argument('--fixture')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.fixture:
        print('usage: --fixture DIR (or --selftest)', file=sys.stderr)
        return 2
    res = score(a.fixture)
    print(json.dumps(res, sort_keys=True))
    return res['exit_code']


# ------------------------------------------------------------------ selftest
BASE_PAIRS = {'cla': ['label-a', 'act-a'], 'clb': ['label-b', 'act-b']}


def _write(path, obj):
    with open(path, 'w') as fh:
        if isinstance(obj, str):
            fh.write(obj)
        else:
            json.dump(obj, fh, indent=1, sort_keys=True)


def build_fixture(work, name, interp_override=None, eval_override=None,
                  eval_crash=(), expect_override=None, classes=('cla', 'clb')):
    d = os.path.join(work, name)
    os.makedirs(os.path.join(d, 'env'))
    _write(os.path.join(d, 'interp.py'), STUB_INTERP)
    _write(os.path.join(d, 'evaluator.py'), STUB_EVAL)
    _write(os.path.join(d, 'skill.json'),
           {'classes': dict(BASE_PAIRS), 'override': interp_override or {}})
    _write(os.path.join(d, 'evalmap.json'),
           {'classes': dict(BASE_PAIRS), 'override': eval_override or {},
            'crash': list(eval_crash)})
    carriers = []
    for ci, cls in enumerate(classes):
        for k in (1, 2):
            cid = 'H%d' % (ci * 2 + k)
            _write(os.path.join(d, 'env', cid + '.json'),
                   {'stub_id': cid, 'stub_class': cls, 'true_class': cls})
            exp = list(BASE_PAIRS[cls])
            if expect_override and cid in expect_override:
                exp = list(expect_override[cid])
            carriers.append({'id': cid, 'class': cls, 'arm': 'after',
                             'expected_label': exp[0], 'expected_action': exp[1],
                             'envelope': 'env/%s.json' % cid})
    _write(os.path.join(d, 'manifest.json'),
           {'classes': list(classes), 'carriers': carriers})
    return d


CASES = []


def case(fn):
    CASES.append(fn)
    return fn


def _run_case(work, name, params, want_exit, want_false=()):
    d = build_fixture(work, name.replace(' ', '-'), **params)
    p = subprocess.run([sys.executable, '-I', '-B', os.path.abspath(__file__),
                        '--fixture', d], capture_output=True, text=True)
    doc = None
    for line in p.stdout.splitlines():
        if line.strip().startswith('{'):
            doc = json.loads(line)
    if doc is None:
        raise AssertionError('%s: no receipt (stderr=%r)' % (name, p.stderr[-200:]))
    if p.returncode != want_exit:
        raise AssertionError('%s: want exit %d got %d' % (name, want_exit, p.returncode))
    if doc.get('exit_code') != p.returncode:
        raise AssertionError('%s: receipt exit_code %r != %d'
                             % (name, doc.get('exit_code'), p.returncode))
    for k in want_false:
        if k not in (doc.get('bindings_false') or []):
            raise AssertionError('%s: binding %s not false (bindings_false=%r)'
                                 % (name, k, doc.get('bindings_false')))
    return doc


@case
def c_green(work):
    _run_case(work, 'green', dict(), 0)


@case
def c_table_label_deviates(work):
    """The table gives one class a wrong label; evaluator and generator agree."""
    _run_case(work, 'table-label-deviates',
              dict(interp_override={'H1': ['label-x', 'act-a'],
                                    'H2': ['label-x', 'act-a']}),
              1, want_false=('table_matches_evaluator',))


@case
def c_eval_action_deviates_generator_agrees(work):
    """Evaluator and generator agree on a wrong action; the table has the right
    one.  The full-pair evaluator-vs-table comparison must fail the run."""
    dev = ['label-a', 'act-x']
    _run_case(work, 'eval-action-dev',
              dict(eval_override={'H1': dev, 'H2': dev},
                   expect_override={'H1': dev, 'H2': dev}),
              1, want_false=('table_matches_evaluator',))


@case
def c_evaluator_crashes(work):
    """A crashed evaluator leaves the envelope unscored; the run must not pass."""
    _run_case(work, 'eval-crash', dict(eval_crash=('H1', 'H2')), 1,
              want_false=('envelopes_scored',))


@case
def c_eval_deviates_on_second_replicate(work):
    """The evaluator deviates on the second replicate of one class and the
    generator's expectation agrees with the deviation; every envelope must be
    compared, so the run fails."""
    dev = ['label-a', 'act-x']
    _run_case(work, 'eval-dev-second-replicate',
              dict(eval_override={'H2': dev}, expect_override={'H2': dev}),
              1, want_false=('table_matches_evaluator',))


@case
def c_generator_label_disagrees(work):
    """The generator's class expectation disagrees with the evaluator on a
    label; reported and failed."""
    _run_case(work, 'gen-label-disagrees',
              dict(expect_override={'H1': ['label-x', 'act-a'],
                                    'H2': ['label-x', 'act-a']}),
              1, want_false=('class_expected_agrees',))


@case
def c_generator_disagrees_on_second_replicate(work):
    """Table and evaluator agree on a deviated second replicate; the generator's
    expectation is the correct pair — the class_expected binding must catch it."""
    dev = ['label-a', 'act-x']
    _run_case(work, 'gen-dev-second-replicate',
              dict(interp_override={'H2': dev}, eval_override={'H2': dev}),
              1, want_false=('class_expected_agrees',))


def selftest():
    work = tempfile.mkdtemp(dir=os.environ.get('TMPDIR') or None,
                            prefix='v3-counter-preview-selftest.')
    failures = []
    for fn in CASES:
        try:
            fn(work)
        except AssertionError as exc:
            failures.append(str(exc))
        except Exception as exc:  # noqa: BLE001
            failures.append('%s: %s' % (fn.__name__, exc))
    print('SELFTEST cases=%d pass=%d fail=%d'
          % (len(CASES), len(CASES) - len(failures), len(failures)))
    for f in failures:
        print('FAIL %s' % f)
    return 0 if not failures else 1


if __name__ == '__main__':
    sys.exit(main())
