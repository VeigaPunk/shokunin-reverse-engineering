#!/usr/bin/env python3
"""CritCounterV2 offline probe (R52-C1 attack). Read-only over the lane tree.

Loads the round-50 counter's own disposition_check (frozen bytes, read, not run as a
score) and scores candidate gap rules over the COMMITTED round-50 envelopes and the
committed round-50 non-regular oracle tables. No REA rerun, no git mutation.

Usage: python3 -I -B probe-r52-law.py <LANE>
"""
import importlib.util
import json
import os
import sys

LANE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
os.chdir(LANE)
spec = importlib.util.spec_from_file_location('r50c', 'tools/round-50/c1-counter.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

IDS = ('g7581', 'g7582', 'c6490', 'c6430')
DEV = ('char-device', 'fifo', 'socket', 'block-device')
R50 = json.load(open('tools/round-50/gap-rule.json'))


def law():
    r = json.loads(json.dumps(R50))
    r['claim'] = 'R52-C1'
    for k in DEV:
        r['allowed'][k] = []
        r['required'][k] = False
    r['removed'].pop('silent', None)
    return r


def load_rows(k):
    rows = []
    for line in open('tools/round-50/oracle/%s.nonregular.tsv' % k):
        p = line.rstrip('\n').split('\t')
        if len(p) >= 2:
            rows.append((p[0], p[1], p[2] if len(p) > 2 else None))
    return rows


def score(rule, label, extra_rows=None):
    model, probs = m.gap_rule_model(json.dumps(rule))
    passed, why_all = [], {}
    for k in IDS:
        env = json.load(open('corpus/evidence/round-50/c1/%s/after.json' % k))
        rows = load_rows(k)
        if extra_rows:
            rows = rows + extra_rows
        root, _ = m.subject_root(env, None)
        od = (env.get('parameters') or {}).get('output_directory')
        ok, why = m.disposition_check(m.gaps(env), m.diagnostics(env), rows, model, root, od)
        why_all[k] = why
        if ok:
            passed.append(k)
    print('%-34s gaps_ok %d of 4 %s problems=%s' % (label, len(passed), passed, probs))
    return passed, why_all


def shape_claimed(rule):
    """The shape clause as the claim words it: no device detail under removed.silent,
    and allowed for device kinds is the empty list."""
    silent = (rule.get('removed') or {}).get('silent') or {}
    bad_silent = [k for k, v in silent.items() if k in DEV and v]
    bad_allowed = [k for k in DEV if (rule.get('allowed') or {}).get(k) != []]
    return not bad_silent and not bad_allowed


def shape_extended(rule):
    """Shape plus the removal and structural limbs the claim does not name."""
    removed_kinds = set((rule.get('removed') or {}).get('kinds') or [])
    structural = set((rule.get('structural') or {}).keys())
    return shape_claimed(rule) and not (removed_kinds & set(DEV)) and not (structural & set(DEV))


print('== controls ==')
score(R50, 'CTL-OLD round-50 rule')
score(law(), 'CTL-NEW round-52 law rule')

print('== mutants ==')
details = sorted({d for k in ('g7581', 'g7582') for _, kind, d in load_rows(k)
                  if kind == 'char-device' and d})
M1 = law()
M1['required']['char-device'] = True
M1['removed']['silent'] = {'char-device': details}
score(M1, 'M1 all-13 whitelist')
print('   M1 shape_claimed=%s shape_extended=%s silent=%d details'
      % (shape_claimed(M1), shape_extended(M1), len(details)))

M2_row = [('dev/ttyS0', 'char-device', '4:64')]
score(law(), 'M2 law + 14th device (no gap)', extra_rows=M2_row)
score(M1, 'M2 whitelist + 14th device', extra_rows=M2_row)

M3 = json.loads(json.dumps(R50))
M3['required']['char-device'] = True
M3['removed']['silent'] = {'char-device': ['247:0']}
score(M3, 'M3 required + 247:0 only')

print('== shape-clause gaps (law-shaped but not caught) ==')
K1 = law()
K1['removed']['kinds'] = ['symlink', 'char-device']
K1['required']['char-device'] = True
print('K1 removed.kinds+=char-device: shape_claimed=%s shape_extended=%s'
      % (shape_claimed(K1), shape_extended(K1)))
K2 = law()
K2['structural']['char-device'] = 0
print('K2 structural.char-device=0:   shape_claimed=%s shape_extended=%s'
      % (shape_claimed(K2), shape_extended(K2)))
K3 = json.loads(json.dumps(R50))
K3['allowed']['char-device'] = ['unpublished-entry']
K3['required']['char-device'] = False
K3['removed'].pop('silent', None)
print('K3 permissive allowed.char-device: shape_claimed=%s shape_extended=%s'
      % (shape_claimed(K3), shape_extended(K3)))
