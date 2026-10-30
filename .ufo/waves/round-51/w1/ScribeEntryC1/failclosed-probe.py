#!/usr/bin/env python3
"""Fail-closed probe for the R51-C1 device-accounting law (ScribeEntryC1, wave 1).

Read-only over COMMITTED bytes: the round-50 envelope for `g7581`
(`corpus/evidence/round-50/c1/g7581/after.json`), the frozen non-regular oracle
table (`tools/round-50/oracle/g7581.nonregular.tsv`), and the round-50 counter's own
`gap_rule_model` / `disposition_check` (imported from `tools/round-50/c1-counter.py`).
No REA, no download, no lane write.

Question answered: does a named rule shape FAIL CLOSED when a device row acquires a
gap? The law says a device row carries no disposition at all and a gap landing on a
device row is a violation, so the rule must reject such a gap. The probe injects one
synthetic `unpublished-entry` gap on `dev/led` (the real path shape: `relative_path`
is the chunk-root-prefixed path, `input_path` is `$output/...`) and re-scores.

Rule shapes compared:
  R50-frozen        tools/round-50/gap-rule.json
  V2a-ExecRuleDerive the wave-1 derivation draft (allowed char-device=[unpublished-entry])
  V2b-F3-shape      device kinds allowed=[] , required char-device=false , no silent list

Usage: python3 -I -B failclosed-probe.py --lane <LANE>
Exit: 0 the probe ran, 1 usage error, 2 an input could not be read.
"""
import argparse
import copy
import importlib.util
import json
import os
import sys

CARRIER = 'g7581'


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


def shapes(base):
    out = {'R50-frozen': copy.deepcopy(base)}
    law = copy.deepcopy(base)
    law['claim'] = 'R51-C1'
    for kind in ('char-device', 'block-device', 'fifo', 'socket'):
        law['allowed'][kind] = []
    law['required']['char-device'] = False
    law['removed']['silent'] = {}
    out['V2b-F3-shape'] = law
    draft_path = os.path.join('.ufo', 'waves', 'round-51', 'w1',
                              'ExecRuleDerive', 'gap-rule-v2.json')
    if os.path.exists(draft_path):
        with open(draft_path, encoding='utf-8') as fh:
            draft = json.load(fh)
        draft['claim'] = 'R51-C1'
        out['V2a-ExecRuleDerive'] = draft
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    args = ap.parse_args()
    try:
        ctr = load_counter(args.lane)
    except Exception as exc:                                  # noqa: BLE001
        print('counter import failed: %s' % exc, file=sys.stderr)
        return 2
    try:
        with open(os.path.join(args.lane, 'tools', 'round-50', 'gap-rule.json'),
                  encoding='utf-8') as fh:
            base = json.load(fh)
        with open(os.path.join(args.lane, 'corpus', 'evidence', 'round-50', 'c1',
                               CARRIER, 'after.json'), encoding='utf-8') as fh:
            env = json.load(fh)
        rows = nonreg_rows(os.path.join(args.lane, 'tools', 'round-50', 'oracle',
                                        '%s.nonregular.tsv' % CARRIER))
    except Exception as exc:                                  # noqa: BLE001
        print('input unreadable: %s' % exc, file=sys.stderr)
        return 2

    od = (env.get('parameters') or {}).get('output_directory')
    root, _how = ctr.subject_root(env)
    gaps = ctr.gaps(env)
    diags = ctr.diagnostics(env)

    injected = copy.deepcopy(gaps)
    injected.append({
        'kind': 'unpublished-entry',
        'input_path': '$output/%s/dev/led' % root,
        'relative_path': '%s/dev/led' % root,
        'handler': None, 'provider_id': None, 'range': None,
        'root_file_range': None, 'dependencies': [],
        'continuation_id': '0' * 64,
    })

    for name, doc in shapes(base).items():
        model, problems = ctr.gap_rule_model(json.dumps(doc))
        clean_ok, clean_why = ctr.disposition_check(gaps, diags, rows, model, root, od)
        inj_ok, inj_why = ctr.disposition_check(injected, diags, rows, model, root, od)
        print('%s | problems=%r | clean=%s | injected_device_gap=%s | %s'
              % (name, problems, clean_ok, inj_ok, inj_why[:150]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
