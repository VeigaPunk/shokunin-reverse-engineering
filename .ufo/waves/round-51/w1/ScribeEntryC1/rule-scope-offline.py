#!/usr/bin/env python3
"""Offline rule-scoped disposition evaluation for R51-C1 (ScribeEntryC1, wave 1).

Read-only over COMMITTED bytes in the lane: the four round-50 envelopes
(`corpus/evidence/round-50/c1/<id>/after.json`), the four frozen non-regular oracle
tables (`tools/round-50/oracle/<id>.nonregular.tsv`) and the round-50 counter's own
`gap_rule_model` / `disposition_check` (imported from `tools/round-50/c1-counter.py`).

It does NOT run REA, does NOT fetch vendor bytes, and does NOT write to the lane. It
answers one question only: over the committed round-50 envelopes, how many carriers
does each named gap rule accept on the three-family disposition check
(`gaps_ok`)? That is the CTL-OLD / CTL-NEW arm of the claims' pre-freeze controls
(wave-1 amendments F2/F9), computed here as a receipt; the L1's own control run is
the authoritative one.

Usage:  python3 -I -B rule-scope-offline.py --lane <LANE> --rule NAME=PATH [--rule ...]
Exit:   0 the evaluation ran (per-rule carrier counts printed), 1 a usage/IO error,
        2 the rule or a carrier input could not be parsed (could-not-evaluate).
"""
import argparse
import importlib.util
import json
import os
import sys

CARRIERS = ('c6430', 'c6490', 'g7581', 'g7582')


def load_counter(lane):
    path = os.path.join(lane, 'tools', 'round-50', 'c1-counter.py')
    spec = importlib.util.spec_from_file_location('r50ctr', path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules['r50ctr'] = mod
    spec.loader.exec_module(mod)
    return mod


def nonreg_rows(path):
    rows = []
    with open(path, encoding='utf-8') as fh:
        for line in fh:
            c = line.rstrip('\n').split('\t')
            if len(c) >= 2 and c[1]:
                rows.append((c[0], c[1], c[2] if len(c) > 2 else ''))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--rule', action='append', default=[],
                    help='NAME=PATH of a gap-rule JSON file')
    args = ap.parse_args()

    if not args.rule:
        print('no --rule given', file=sys.stderr)
        return 1
    try:
        ctr = load_counter(args.lane)
    except Exception as exc:                                  # noqa: BLE001
        print('counter import failed: %s' % exc, file=sys.stderr)
        return 2

    models = {}
    for spec in args.rule:
        name, _, path = spec.partition('=')
        if not name or not path:
            print('bad --rule %r (want NAME=PATH)' % spec, file=sys.stderr)
            return 1
        try:
            with open(path, encoding='utf-8') as fh:
                doc = json.load(fh)
        except Exception as exc:                              # noqa: BLE001
            print('rule %s unreadable: %s' % (name, exc), file=sys.stderr)
            return 2
        model, problems = ctr.gap_rule_model(json.dumps(doc))
        models[name] = model
        print('rule %s problems %r' % (name, problems))

    print('carrier rule gaps_ok detail')
    for cid in CARRIERS:
        env_path = os.path.join(args.lane, 'corpus', 'evidence', 'round-50', 'c1',
                                cid, 'after.json')
        tab_path = os.path.join(args.lane, 'tools', 'round-50', 'oracle',
                                '%s.nonregular.tsv' % cid)
        try:
            with open(env_path, encoding='utf-8') as fh:
                env = json.load(fh)
            rows = nonreg_rows(tab_path)
        except Exception as exc:                              # noqa: BLE001
            print('carrier %s unreadable: %s' % (cid, exc), file=sys.stderr)
            return 2
        gaps = ctr.gaps(env)
        diags = ctr.diagnostics(env)
        od = (env.get('parameters') or {}).get('output_directory')
        root, _how = ctr.subject_root(env)
        for name, model in models.items():
            ok, why = ctr.disposition_check(gaps, diags, rows, model, root, od)
            print('%s %s %s %s' % (cid, name, ok, why[:160]))
    for name in models:
        matched = 0
        for cid in CARRIERS:
            env_path = os.path.join(args.lane, 'corpus', 'evidence', 'round-50', 'c1',
                                    cid, 'after.json')
            tab_path = os.path.join(args.lane, 'tools', 'round-50', 'oracle',
                                    '%s.nonregular.tsv' % cid)
            with open(env_path, encoding='utf-8') as fh:
                env = json.load(fh)
            rows = nonreg_rows(tab_path)
            gaps = ctr.gaps(env)
            diags = ctr.diagnostics(env)
            od = (env.get('parameters') or {}).get('output_directory')
            root, _how = ctr.subject_root(env)
            ok, _why = ctr.disposition_check(gaps, diags, rows, models[name], root, od)
            matched += 1 if ok else 0
        print('matched %s %d of %d' % (name, matched, len(CARRIERS)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
