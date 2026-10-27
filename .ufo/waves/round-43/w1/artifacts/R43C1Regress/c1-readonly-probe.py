#!/usr/bin/env python3
"""R43C1Regress reader-only probe of the frozen round-42 C1 counter.

WHY THIS EXISTS
---------------
The round-43 dispatch binds every seat with a "Reserved inputs" rule: never run
REA, unblob, sasquatch or any extractor on a PUBLISHED third-party firmware
image (OpenWrt / DD-WRT / AVM downloads) **or anything carved from it**; readers
only (`unsquashfs -s|-lls`, `7z l`, pure superblock probes).

The round-42 C1 counter's `projection_ok` clause is exactly such an extractor
run: `tools/round-42/c1-counter.py` re-runs REA 6.5.0 `extract-firmware` on the
*carved* published carrier bytes (the four OpenWrt 8.09.x / DD-WRT v24 rootfs
carves).  A seat may therefore NOT exercise that clause.

This probe isolates it.  It imports the FROZEN counter bytes (sha256
0f5052f99a976cfdd391d3e8330b644ca403b146095ca73e14f3859ab9d1483c, identical at
d1681696 / eb8215ac / 6b9e64fe) and calls its own `measure()` with the frozen
`rerun` injection point (the same hook `--selftest` uses), passing a stub that
NEVER starts an extractor: it records that it was reached and returns the
counter's own non-`ok` status.  Every other clause therefore evaluates over the
REAL published carrier bytes with readers only (superblock probe + sha256).

The probe writes nothing outside its `--out` file and its private scratch
directory ($HYAKU_SCRATCH).  It does not mutate the lane or the VCS.

Usage
  c1-readonly-probe.py --counter PATH --root LANE --rev REV --freeze FREEZE
                        --pkg65 REA_PKG_ROOT --carrier-cache DIR --out FILE
"""
import argparse
import hashlib
import importlib.util
import json
import os
import sys


def load_counter(path):
    spec = importlib.util.spec_from_file_location('r42_c1_counter', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--counter', required=True)
    ap.add_argument('--root', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--freeze', required=True)
    ap.add_argument('--pkg65', required=True)
    ap.add_argument('--carrier-cache', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args(argv)

    raw_counter = open(a.counter, 'rb').read()
    counter_sha = hashlib.sha256(raw_counter).hexdigest()
    mod = load_counter(a.counter)

    reached = []

    def readonly_rerun(carrier_bytes, cid, params=None):
        # NEVER starts an extractor: the reserved-inputs rule forbids running
        # REA/unblob/sasquatch on published-carrier carve bytes.
        reached.append({
            'id': cid,
            'bytes': len(carrier_bytes) if carrier_bytes is not None else 0,
            'sha256': hashlib.sha256(carrier_bytes).hexdigest()
                      if carrier_bytes is not None else None,
            'replayed_params': params if isinstance(params, dict) else None,
            'extractor_started': False,
            'note': 'reader-only probe: the extractor arm is deliberately not '
                    'executed (round-43 reserved-inputs rule)',
        })
        return 'no_data', {'ok': False, 'extractor_started': False,
                           'reason': 'reserved-inputs: extractor not run'}

    res = mod.measure(a.root, a.rev, a.freeze, a.pkg65,
                       rerun=readonly_rerun, carrier_cache=a.carrier_cache)

    res['probe'] = {
        'counter_sha256': counter_sha,
        'counter_path': os.path.abspath(a.counter),
        'rerun_arm_reached_for': sorted(r['id'] for r in reached),
        'rerun_calls': reached,
        'extractor_started': False,
        'reader_only': True,
    }
    res['argv'] = sys.argv
    res['exit_code'] = 0 if res.get('met_target') else 1

    with open(a.out, 'w') as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
    print(json.dumps({'probe': 'r43c1regress-readonly',
                      'revision': res.get('revision'),
                      'carriers_matched': res.get('carriers_matched'),
                      'target': res.get('target'),
                      'met_target': res.get('met_target'),
                      'exit_code': res['exit_code'],
                      'rerun_reached': sorted(r['id'] for r in reached)},
                     sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
