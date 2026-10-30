#!/usr/bin/env python3
"""Offline rule-shape variants for the R51-C1 law (ScribeEntryC1, wave 1).

Read-only over COMMITTED bytes and the round-50 counter's own `gap_rule_model` /
`disposition_check` (imported from `tools/round-50/c1-counter.py`). No REA, no
download, no lane write.

It scores several named rule variants over the committed round-50 envelopes and
the frozen non-regular oracle tables, and over a synthetic 14-device census
(a fixture carrier that carries one device the thirteen-detail whitelist does not
name), so that the M1-M4 mutation arms of the claims are decidable before the
freeze:

  V1-R50-frozen             the round-50 frozen rule (the before-arm)
  V2a-ExecRuleDerive        the wave-1 derivation draft (required char-device=false)
  V2b-F3-shape              F3 shape: device kinds allowed=[] , required char-device=false
  V2c-required-true         F3 shape but required char-device=true (contradiction probe)
  V2d-all13-whitelist       required char-device=true + all thirteen details silent
  V2e-strict-subset         required char-device=true + a strict subset of the thirteen

Usage: python3 -I -B rule-variants-offline.py --lane <LANE>
Exit: 0 the variants ran, 1 usage error, 2 an input could not be read.
"""
import argparse
import copy
import importlib.util
import json
import os
import sys

CARRIERS = ('c6430', 'c6490', 'g7581', 'g7582')
THIRTEEN = ['247:0', '136:0', '136:1', '136:2', '136:3', '136:4', '136:5',
             '136:6', '136:7', '230:0', '3:0', '3:1', '3:2']


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


def variants(base):
    out = {}
    out['V1-R50-frozen'] = copy.deepcopy(base)

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

    req_true = copy.deepcopy(law)
    req_true['required']['char-device'] = True
    out['V2c-required-true'] = req_true

    wl = copy.deepcopy(law)
    wl['required']['char-device'] = True
    wl['removed']['silent'] = {'char-device': list(THIRTEEN)}
    out['V2d-all13-whitelist'] = wl

    sub = copy.deepcopy(law)
    sub['required']['char-device'] = True
    sub['removed']['silent'] = {'char-device': [d for d in THIRTEEN if d != '230:0']}
    out['V2e-strict-subset'] = sub
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
    with open(os.path.join(args.lane, 'tools', 'round-50', 'gap-rule.json'),
              encoding='utf-8') as fh:
        base = json.load(fh)
    rules = variants(base)

    inputs = {}
    for cid in CARRIERS:
        with open(os.path.join(args.lane, 'corpus', 'evidence', 'round-50', 'c1',
                               cid, 'after.json'), encoding='utf-8') as fh:
            env = json.load(fh)
        rows = nonreg_rows(os.path.join(args.lane, 'tools', 'round-50', 'oracle',
                                        '%s.nonregular.tsv' % cid))
        inputs[cid] = (env, rows)

    # the M2 fixture: the g7581 census plus one device the thirteen do not name
    g_rows = inputs['g7581'][1] + [('dev/ttyS0', 'char-device', '4:64')]

    print('variant | census | matched | per-carrier | note')
    for name, doc in rules.items():
        model, problems = ctr.gap_rule_model(json.dumps(doc))
        for census_name, rows_override in (('13-row', None), ('14-row', g_rows)):
            matched = 0
            per = []
            for cid in CARRIERS:
                env, rows = inputs[cid]
                if rows_override is not None and cid == 'g7581':
                    rows = rows_override
                gaps = ctr.gaps(env)
                diags = ctr.diagnostics(env)
                od = (env.get('parameters') or {}).get('output_directory')
                root, _how = ctr.subject_root(env)
                ok, _why = ctr.disposition_check(gaps, diags, rows, model, root, od)
                matched += 1 if ok else 0
                per.append('%s=%s' % (cid, 'T' if ok else 'F'))
            print('%s | %s | %d/4 | %s | problems=%r'
                  % (name, census_name, matched, ' '.join(per), problems))
    return 0


if __name__ == '__main__':
    sys.exit(main())
