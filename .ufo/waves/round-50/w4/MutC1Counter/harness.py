#!/usr/bin/env python3
"""Offline counterfactual harness for the R50-C1 counter.

Runs the FROZEN counter's own `measure()` (imported from a file, never edited
in place) against a git root / rev / freeze, with the rerun clause replaced by
the counter's OWN sanctioned replay technique:

  the frozen counter's selftest helper `mk_same_runner` is documented as
  "a real run whose output is the given envelope (projection-equal by
  construction): used to isolate a rule clause from the rerun clause".
  This harness uses the frozen counter's own `rehost()` to build that replay
  envelope: a second-run shape with different absolute paths, a different
  staged directory name and a different evidence id, so the projection
  comparison still exercises the real normalisation instead of comparing an
  object with itself.

NO REA RUN HAPPENS. The oracle re-derivation uses the counter's own
`rederive_oracle` (/usr/bin/unsquashfs 4.7.5), memoised on disk across arms.

Usage:
  harness.py --counter PATH --root PATH --rev REV --freeze FREEZE
             --pkg65 PATH --carrier-cache DIR --work DIR --derived-cache DIR
             --out JSON --label NAME
"""
import argparse
import datetime
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

AFTERDIR = 'corpus/evidence/round-50/c1'


def load_counter(path):
    spec = importlib.util.spec_from_file_location('c1_counter_under_test', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--counter', required=True)
    ap.add_argument('--root', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--freeze', required=True)
    ap.add_argument('--pkg65', required=True)
    ap.add_argument('--carrier-cache', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--derived-cache', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--label', default='arm')
    a = ap.parse_args(argv)

    t_utc = datetime.datetime.now(datetime.timezone.utc).strftime(
        '%Y-%m-%dT%H:%M:%SZ')
    os.makedirs(a.work, exist_ok=True)
    os.makedirs(a.derived_cache, exist_ok=True)
    mod = load_counter(a.counter)
    mod.WORK_OVERRIDE = os.path.abspath(a.work)

    committed = {}

    def committed_env(cid):
        if cid not in committed:
            raw = mod.show(a.root, a.rev, '%s/%s/after.json' % (AFTERDIR, cid))
            committed[cid] = json.loads(raw) if raw else None
        return committed[cid]

    def replay_runner(carrier_bytes, cid, params=None):
        """The counter's own `rehost()` replay (see module docstring)."""
        env = committed_env(cid)
        if env is None:
            return ('error', {'error': {'code': 'no_committed_receipt',
                                        'message': 'no committed receipt for %s'
                                                   % cid}})
        e = json.loads(json.dumps(env))
        digest = sha256_bytes(carrier_bytes)
        e['subject']['digest']['sha256'] = digest
        e['normalized_result']['selection']['sha256'] = digest
        return ('ok', mod.rehost(e, 'offline-replay-' + cid))

    replay_runner.toolchain = {
        'kind': 'offline-replay',
        'note': "the frozen counter's own rehost() replay of the committed "
                'receipt; isolates the rule clause from the REA-rerun clause; '
                'NO REA RUN',
    }

    # oracle re-derivation: the counter's own second reader, memoised on disk
    derive_cache = {}
    derive_work = os.path.join(a.derived_cache, 'work')
    os.makedirs(derive_work, exist_ok=True)

    def memo_rederive(raw, cid):
        if cid not in derive_cache:
            cpath = os.path.join(a.derived_cache, cid + '.json')
            if os.path.isfile(cpath):
                derive_cache[cid] = [tuple(r) for r in json.load(open(cpath))]
            else:
                rows = mod.rederive_oracle(raw, derive_work, cid)
                with open(cpath, 'w') as fh:
                    json.dump([list(r) for r in rows], fh)
                derive_cache[cid] = rows
        return derive_cache[cid]

    cmd = ' '.join([sys.executable, '-I', '-B',
                    os.path.abspath(__file__),
                    '--counter', os.path.abspath(a.counter),
                    '--root', a.root, '--rev', a.rev, '--freeze', a.freeze,
                    '--pkg65', a.pkg65, '--carrier-cache', a.carrier_cache,
                    '--work', os.path.abspath(a.work),
                    '--derived-cache', os.path.abspath(a.derived_cache),
                    '--out', a.out, '--label', a.label])

    rec = {'label': a.label, 'utc': t_utc, 'command': cmd,
           'counter': os.path.abspath(a.counter),
           'counter_sha256': sha256_file(a.counter),
           'root': a.root, 'rev': a.rev, 'freeze': a.freeze,
           'rerun': 'offline rehost() replay of the committed receipt (no REA)',
           'rederive': "the counter's own rederive_oracle (unsquashfs 4.7.5)"}

    def emit(exit_code, meaning):
        rec['exit_code'] = exit_code
        rec['exit_meaning'] = meaning
        with open(a.out, 'w') as fh:
            json.dump(rec, fh, indent=1, sort_keys=True)
        print(json.dumps({k: rec[k] for k in
                          ('label', 'carriers_matched', 'target', 'met_target',
                           'exit_code', 'failing', 'bindings_false')
                          if k in rec}, sort_keys=True))

    try:
        res = mod.measure(a.root, a.rev, a.freeze, a.pkg65,
                          rerun=replay_runner, carrier_cache=a.carrier_cache,
                          rederive=memo_rederive)
    except mod.Unevaluable as e:
        rec.update({'unevaluable': str(e), 'reason': e.reason})
        emit(2, 'could-not-evaluate')
        print(json.dumps({'label': a.label, 'reason': e.reason,
                          'detail': str(e), 'exit_code': 2}, sort_keys=True))
        return 2
    except Exception as e:
        rec.update({'error': '%s: %s' % (type(e).__name__, e)})
        emit(2, 'could-not-evaluate')
        print(json.dumps({'label': a.label, 'error': rec['error'],
                          'exit_code': 2}, sort_keys=True))
        return 2

    fails, binds = mod.failing_lists(res)
    rec.update({
        'carriers_matched': res.get('carriers_matched'),
        'target': res.get('target'),
        'met_target': res.get('met_target'),
        'failing': fails,
        'bindings_false': binds,
        'frozen_path_changed': res.get('frozen_path_changed'),
        'carriers_unchanged': res.get('carriers_unchanged'),
        'gap_rule_unchanged': res.get('gap_rule_unchanged'),
        'gap_rule_problems': res.get('gap_rule_problems'),
        'frozen_tables_valid': res.get('frozen_tables_valid'),
        'bindings': res.get('bindings'),
        'per_carrier': {k: {kk: v.get(kk) for kk in
                            ('gaps_ok', 'gaps_note', 'projection_ok',
                             'projection_diff', 'oracle_hits_ok',
                             'oracle_rederived_ok', 'nonregular_unpublished_ok',
                             'carrier_pin_ok', 'carrier_fresh_ok', 'layout_ok',
                             'carve_ok', 'receipt_present', 'receipt_fresh',
                             'evidence_envelope_ok', 'evidence_id_ok',
                             'subject_pin_ok', 'operation_ok', 'handler_ok',
                             'chunks_ok', 'parameters_ok', 'run_provenance_ok',
                             'path_shape_ok', 'nonregular_entries',
                             'nonregular_kinds', 'published_files',
                             'oracle_files', 'oracle_hits',
                             'extra_published', 'matched')}
                    for k, v in (res.get('carriers') or {}).items()},
    })
    emit(0 if res.get('met_target') else 1,
         'met' if res.get('met_target') else 'not met')
    return rec['exit_code']


if __name__ == '__main__':
    sys.exit(main())
