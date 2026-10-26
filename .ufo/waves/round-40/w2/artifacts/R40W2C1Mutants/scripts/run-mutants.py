#!/usr/bin/env python3
"""Run selftest + real verdict for each mutant; restore pristine bytes after each.

Usage: run-mutants.py counter|extra
"""
import hashlib
import json
import os
import subprocess
import sys

S = '/fast/scratch/hyaku/kaidoku-r40/R40W2C1Mutants'
BASE = os.path.join(S, 'base')
OUT = os.path.join(S, 'out')
PKG = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
CACHE = os.path.join(S, 'cache')
REV = '42c10a58cb2cae3a4a0122af35a0cf95ac718043'
FREEZE = '7fce308631a8b457d6b7c5a4b39a923c4e9a49de'
BASE_REV = 'fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f'

PRISTINE_SHA = {
    'c1-counter.py': '8d288e4cf203d74557aa81df556d6a95c1bcde99acabf189638c4142b6f17e81',
    'c1-extra.py': '5ba40129f5ec96448c217e4fb22c885dff85fee4745c39389caf6cf6cab7fbb0',
}
CLAUSES = ('carrier_present', 'carrier_pin_ok', 'layout_ok', 'oracle_ok',
           'nonregular_ok', 'receipt_present', 'receipt_fresh', 'subject_pin_ok',
           'operation_ok', 'handler_ok', 'chunks_ok', 'oracle_hits_ok',
           'gaps_ok', 'nonregular_unpublished_ok', 'run_provenance_ok',
           'evidence_id_ok', 'projection_ok')
BOOL_BINDINGS = ('province_core_section', 'province_core_row', 'frontier_note',
                 'entry_present', 'sourced', 'coverage_map_row', 'carriers_spec_ok',
                 'gap_rule_ok', 'compression_coverage', 'frozen_tables_valid')

which = sys.argv[1]
fname = 'c1-counter.py' if which == 'counter' else 'c1-extra.py'
target = os.path.join(BASE, 'tools/round-40', fname)
pristine = open(target, 'rb').read()
assert hashlib.sha256(pristine).hexdigest() == PRISTINE_SHA[fname]

manifest = json.load(open(os.path.join(S, 'mutants', 'manifest.json')))
mutants = [m for m in manifest if (which == 'counter') == (m['file'] == 'c1-counter.py')]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def verdict(json_path, rc):
    d = json.load(open(json_path))
    if 'unevaluable' in d or d.get('exit_code') == 2:
        return {'rc': d.get('exit_code', rc), 'unevaluable': d.get('unevaluable'),
                'reason': d.get('reason')}
    if 'carriers' in d:
        failing = {k: sorted(x for x in CLAUSES if v.get(x) is not True)
                   for k, v in sorted(d['carriers'].items()) if not v['matched']}
        fb = sorted(k for k in BOOL_BINDINGS if d['bindings'].get(k) is not True)
        return {'rc': rc, 'matched': d['carriers_matched'], 'met_target': d['met_target'],
                'unchanged': [d['carriers_unchanged'], d['gap_rule_unchanged']],
                'drift': d['frozen_path_changed'], 'failing': failing,
                'false_bindings': fb}
    fb = sorted(k for k, v in d['bindings'].items() if v is not True)
    return {'rc': rc, 'met': d['met'], 'false_bindings': fb,
            'detail': {k: (v if not isinstance(v, dict) else
                           {kk: vv for kk, vv in v.items() if kk != 'cited'})
                       for k, v in d['detail'].items()}}


for m in mutants:
    mid = m['id']
    mut_path = os.path.join(S, 'mutants', '%s-%s.py' % (mid, which))
    rec = {'id': mid, 'clause': m['clause']}
    try:
        with open(target, 'wb') as fh:
            fh.write(open(mut_path, 'rb').read())
        assert sha(open(target, 'rb').read()) == m['sha256_mutant']

        if which == 'counter':
            st_argv = [sys.executable, '-I', '-B', target, '--selftest', '--pkg65', PKG]
            real_argv = [sys.executable, '-I', '-B', target,
                         '--root', BASE, '--rev', REV, '--freeze', FREEZE,
                         '--pkg65', PKG, '--carrier-cache', CACHE,
                         '--json-out', os.path.join(OUT, 'mut-%s-c1.json' % mid)]
        else:
            st_argv = [sys.executable, '-I', '-B', target, '--selftest']
            real_argv = [sys.executable, '-I', '-B', target,
                         '--root', BASE, '--rev', REV, '--freeze', FREEZE,
                         '--base', BASE_REV, '--carrier-cache', CACHE,
                         '--json-out', os.path.join(OUT, 'mut-%s-extra.json' % mid)]
        p = subprocess.run(st_argv, capture_output=True, timeout=600)
        rec['selftest_rc'] = p.returncode
        st_text = p.stdout.decode(errors='replace')
        stj = [l for l in st_text.strip().splitlines() if l.strip()]
        if which == 'counter':
            try:
                rec['selftest_failures'] = json.loads(stj[-1])['failures']
                rec['selftest_line'] = stj[-1]
            except (json.JSONDecodeError, IndexError, KeyError):
                rec['selftest_failures'] = ['<unparsed>']
                rec['selftest_line'] = (stj[-1] if stj else '') + \
                    ' || STDERR: ' + p.stderr.decode(errors='replace')[-300:]
        else:
            rec['selftest_failures'] = [l for l in stj if l.startswith('FAIL')]
            rec['selftest_line'] = stj[-1] if stj else ''

        q = subprocess.run(real_argv, capture_output=True, timeout=1800)
        rec['real_stdout_head'] = q.stdout.decode(errors='replace').strip()[:200]
        vj = os.path.join(OUT, ('mut-%s-c1.json' if which == 'counter'
                                else 'mut-%s-extra.json') % mid)
        rec['verdict'] = verdict(vj, q.returncode) if os.path.exists(vj) else \
            {'rc': q.returncode, 'no_json': True,
             'stderr': q.stderr.decode(errors='replace')[:400]}
    finally:
        with open(target, 'wb') as fh:
            fh.write(pristine)
        assert sha(open(target, 'rb').read()) == PRISTINE_SHA[fname]
        rec['restored_sha256'] = sha(pristine)

    with open(os.path.join(OUT, 'sum-%s.json' % mid), 'w') as fh:
        json.dump(rec, fh, indent=1)
    v = rec['verdict']
    brief = ('unevaluable ' + str(v.get('reason')) if 'unevaluable' in v else
             'rc=%s matched=%s failing=%s' % (v.get('rc'), v.get('matched'), v.get('failing')))
    print('%s\tst=%d\t%s\t%s' % (mid, rec['selftest_rc'], brief,
                                 (rec['selftest_failures'] or '')[:1]))

with open(target, 'wb') as fh:
    fh.write(pristine)
print('DONE %s (%d mutants, target bytes pristine)' % (which, len(mutants)))
