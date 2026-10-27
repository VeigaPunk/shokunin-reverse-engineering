#!/usr/bin/env python3
"""R43C1Counter — the run.json binding measured on the 78 committed round-42 carriers.

The L1's dry-run blocker (R43DryRun D1) was that `runjson_digests` compared the
generator's `run.json.handlers` to the *squashfs-prefixed* subset of the observed
handlers, which is false on every carrier whose chunk set includes a non-squashfs
handler (`tar`). The fix compares it to the counter's own CHUNK handler list.

This probe evaluates both comparisons with the counter's own extraction
(`observed_features`), read from committed bytes only — no REA, no network.

  python3 -I -B runjson-probe.py <LANE>
"""
import importlib.util
import json
import os
import sys


def load_counter(lane):
    path = os.path.join(lane, '.ufo/waves/round-43/w1/artifacts/R43C1Counter/'
                              'c1-counter.py')
    spec = importlib.util.spec_from_file_location('c1counter', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv):
    lane = argv[1] if len(argv) > 1 else '.'
    m = load_counter(lane)
    root = os.path.join(lane, 'corpus/evidence/round-42/c2/heldout')
    old_bad, new_bad, n = [], [], 0
    for name in sorted(os.listdir(root)):
        d = os.path.join(root, name)
        if not os.path.isdir(d):
            continue
        env_p = os.path.join(d, 'envelope.json')
        run_p = os.path.join(d, 'run.json')
        if not (os.path.isfile(env_p) and os.path.isfile(run_p)):
            continue
        n += 1
        env = m.envelope_data(json.load(open(env_p)))
        rec = json.load(open(run_p))
        obs = m.observed_features(env) or {}
        want = sorted(rec.get('handlers') or [])
        squashfs_only = sorted(obs.get('squashfs_handlers') or [])
        chunk_all = sorted(obs.get('chunk_handlers') or [])
        if want != squashfs_only:
            old_bad.append((name, want, squashfs_only))
        if want != chunk_all:
            new_bad.append((name, want, chunk_all))
    print('carriers with run.json: %d' % n)
    print('OLD (handlers vs squashfs_handlers) mismatches: %d' % len(old_bad))
    for row in old_bad[:20]:
        print('   %-4s want=%-28s got=%s' % (row[0], row[1], row[2]))
    print('NEW (handlers vs chunk_handlers) mismatches: %d' % len(new_bad))
    for row in new_bad[:20]:
        print('   %-4s want=%-28s got=%s' % (row[0], row[1], row[2]))
    return 0 if not new_bad else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
