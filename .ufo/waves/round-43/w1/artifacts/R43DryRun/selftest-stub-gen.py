#!/usr/bin/env python3
"""Self-test double for dry-run-r43.sh's G3/G6 gates -- NOT a lane tool.

This file exists so the harness's *pass* paths can be exercised without the real
round-43 tools (which the L1 installs).  It implements exactly the contract the
harness asserts and nothing else:

  * `--seed --out --classes --run --scratch` writes a manifest whose carriers each
    carry the six-field tuple under the single key `declared_features`, plus
    `generator.tuple_check` with per-carrier {observed, declared, equal: true}.
  * `--check-manifest PATH [--envelopes DIR]` re-checks a manifest against the
    envelopes recorded beside it: any carrier whose declared tuple differs from the
    observed one makes the process exit 3 `declared_tuple_unobserved` and write
    nothing; agreement exits 0.
  * `--out DIR --verify` is the same check against DIR/manifest.json.

No REA, no carrier bytes, no fixtures.  Use it only via
`DRY_GEN=<abs path to this file> bash dry-run-r43.sh LANE WORK`.
"""
import argparse
import json
import os
import sys

FIELDS = ('handler_set', 'gap_kinds', 'gap_dependencies', 'be_argv',
          'symlink_removed', 'published')
CLASSES = {
    'clean-be':          {'handler_set': ['squashfs_v4_be'], 'gap_kinds': [], 'gap_dependencies': [], 'be_argv': 'n/a', 'symlink_removed': False, 'published': 'nonzero'},
    'clean-le':          {'handler_set': ['squashfs_v4_le'], 'gap_kinds': [], 'gap_dependencies': [], 'be_argv': 'n/a', 'symlink_removed': False, 'published': 'nonzero'},
    'body-extractor-failure': {'handler_set': ['squashfs_v4_be'], 'gap_kinds': ['extractor-failure'], 'gap_dependencies': [], 'be_argv': 'yes', 'symlink_removed': False, 'published': 'zero'},
    'partial-body-failure': {'handler_set': ['squashfs_v4_be'], 'gap_kinds': ['extractor-failure'], 'gap_dependencies': [], 'be_argv': 'yes', 'symlink_removed': False, 'published': 'nonzero'},
    'depth-limited-mixed': {'handler_set': ['squashfs_v4_be'], 'gap_kinds': ['depth-limited', 'unpublished-entry'], 'gap_dependencies': [], 'be_argv': 'n/a', 'symlink_removed': True, 'published': 'nonzero'},
    'legacy-body-failure': {'handler_set': ['squashfs_v3'], 'gap_kinds': ['extractor-failure'], 'gap_dependencies': [], 'be_argv': 'no', 'symlink_removed': False, 'published': 'zero'},
    'combo':             {'handler_set': ['squashfs_v3', 'squashfs_v4_le'], 'gap_kinds': ['depth-limited'], 'gap_dependencies': [], 'be_argv': 'n/a', 'symlink_removed': False, 'published': 'nonzero'},
}


def observed_from_record(rec):
    src = rec.get('observed') if isinstance(rec.get('observed'), dict) else rec
    return {k: src.get(k) for k in FIELDS}


def check(dir_or_manifest, envelopes=None):
    """Return (rc, diff). rc 3 = the run did not observe a declared tuple."""
    base = dir_or_manifest
    man_path = base
    if os.path.isdir(base):
        man_path = os.path.join(base, 'manifest.json')
        if envelopes is None:
            envelopes = base
    if not os.path.isfile(man_path):
        print('check: no manifest at %s' % man_path, file=sys.stderr)
        return 2, []
    man = json.load(open(man_path, encoding='utf-8'))
    diffs = []
    for car in man.get('carriers') or []:
        declared = car.get('declared_features')
        if not isinstance(declared, dict):
            diffs.append({'id': car.get('id'), 'why': 'no declared_features'})
            continue
        rec_path = os.path.join(envelopes or os.path.dirname(man_path),
                                str(car.get('id')), 'run.json')
        if not os.path.isfile(rec_path):
            diffs.append({'id': car.get('id'), 'why': 'no observed record'})
            continue
        obs = observed_from_record(json.load(open(rec_path, encoding='utf-8')))
        diff = {k: {'declared': declared.get(k), 'observed': obs.get(k)}
                for k in FIELDS if declared.get(k) != obs.get(k)}
        if diff:
            diffs.append({'id': car.get('id'), 'diff': diff})
    if diffs:
        print('declared_tuple_unobserved: %d carrier(s)' % len(diffs))
        for d in diffs[:20]:
            print('  %s %s' % (d.get('id'), d.get('diff') or d.get('why')))
        return 3, diffs
    print('tuple check green: %d carrier(s), declared == observed' % len(man.get('carriers') or []))
    return 0, []


def generate(args):
    names = [n.strip() for n in (args.classes or '').split(',') if n.strip()]
    classes = [n for n in names if n in CLASSES]
    if not classes:
        print('no known class in --classes', file=sys.stderr)
        return 2
    out = os.path.abspath(args.out)
    os.makedirs(out, exist_ok=True)
    carriers = []
    for i, name in enumerate(classes, 1):
        cid = 'H%02d' % i
        cdir = os.path.join(out, cid)
        os.makedirs(cdir, exist_ok=True)
        tup = dict(CLASSES[name])
        with open(os.path.join(cdir, 'carrier.sqsh'), 'wb') as fh:
            fh.write(b'stub-%s-%s\n' % (args.seed.encode()[:16], name.encode()))
        rec = {'id': cid, 'class': name, 'observed': tup}
        json.dump(rec, open(os.path.join(cdir, 'run.json'), 'w'), indent=1, sort_keys=True)
        json.dump({'stub': True, 'id': cid, 'harness_selftest': True},
                  open(os.path.join(cdir, 'envelope.json'), 'w'), indent=1, sort_keys=True)
        carriers.append({
            'id': cid, 'class': name, 'arm': 'after',
            'carrier': '%s/carrier.sqsh' % cid, 'envelope': '%s/envelope.json' % cid,
            'declared_features': dict(tup), 'declared_extras': {'extraction_failed': False, 'max_depth': 3},
            'class_expected': {'label': name, 'reported_only': True},
        })
    manifest = {
        'seed': args.seed, 'round': 43, 'claim': 'R43-C1-selftest-double',
        'generator': {
            'name': os.path.basename(__file__),
            'sha256': __import__('hashlib').sha256(open(__file__, 'rb').read()).hexdigest(),
            'tuple_check': {
                'rule': 'declared == observed for every carrier (harness self-test double)',
                'carriers': [{'id': c['id'], 'observed': c['declared_features'],
                              'declared': c['declared_features'], 'equal': True} for c in carriers],
            },
        },
        'declared_schema': {'key': 'declared_features', 'fields': list(FIELDS)},
        'classes': classes,
        'carriers': carriers,
    }
    json.dump(manifest, open(os.path.join(out, 'manifest.json'), 'w'), indent=1, sort_keys=True)
    print('stub manifest %s carriers=%d' % (os.path.join(out, 'manifest.json'), len(carriers)))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed')
    ap.add_argument('--out')
    ap.add_argument('--classes')
    ap.add_argument('--run', action='store_true')
    ap.add_argument('--verify', action='store_true')
    ap.add_argument('--check-manifest')
    ap.add_argument('--envelopes')
    a = ap.parse_args(argv)
    if a.check_manifest:
        return check(a.check_manifest, a.envelopes)[0]
    if a.verify and a.out:
        return check(a.out)[0]
    if a.seed and a.out:
        return generate(a)
    print('usage: selftest-stub-gen.py --seed S --out DIR --classes a,b [--run] | '
          '--check-manifest PATH [--envelopes DIR] | --out DIR --verify', file=sys.stderr)
    return 2


if __name__ == '__main__':
    sys.exit(main())
