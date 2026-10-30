#!/usr/bin/env python3
"""Probe 3: the law's fail-closed property and the shape-clause mutants.

Offline, lane read-only. Answers:
  D. Inject a gap landing on a char-device row (the law's fail-closed case:
     "a gap landing on a device row is a violation of the law"). Does any
     committed envelope witness this?  Is it caught by the law rule and NOT by
     the round-50 rule?
  E. The `allowed`-shape half of law_shape_ok: a rule with
     allowed['char-device'] = ['unpublished-entry'] and no silent detail.
  F. CTL-JUNK and an over-permissive mirror.
  G. CTL-OLD vs M3 behavioural identity (redundancy test).
  H. Wrong-carrier-set: which carriers were scored behind a count.
"""
import copy
import importlib.util
import json
import os
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
IDS = ('c6430', 'c6490', 'g7581', 'g7582')

spec = importlib.util.spec_from_file_location(
    'r50c', os.path.join(LANE, 'tools/round-50/c1-counter.py'))
M = importlib.util.module_from_spec(spec)
sys.modules['r50c'] = M
spec.loader.exec_module(M)

NONREG, ENV = {}, {}
for cid in IDS:
    raw = open(os.path.join(LANE, 'tools/round-50/oracle/%s.nonregular.tsv' % cid),
               'rb').read()
    rows, err = M.parse_nonregular(raw)
    assert err is None, err
    NONREG[cid] = rows
    ENV[cid] = json.load(open(os.path.join(
        LANE, 'corpus/evidence/round-50/c1/%s/after.json' % cid)))

LAW = {
    'claim': 'R52-C1',
    'allowed': {'symlink': ['unpublished-entry'], 'char-device': [],
                'block-device': [], 'fifo': [], 'socket': [], 'dir': []},
    'required': {'symlink': True, 'char-device': False, 'block-device': False,
                 'fifo': False, 'socket': False, 'dir': False},
    'removed': {'diagnostic': 'MaliciousSymlinkRemoved', 'kinds': ['symlink'],
                'disposition': 'exclusive', 'silent': {}},
    'structural': {'depth-limited': 1, 'unknown-chunk-handler': 0},
}
R50 = json.load(open(os.path.join(LANE, 'tools/round-50/gap-rule.json')))


def score_one(cid, rule, gaps_override=None, nonreg_override=None):
    model, probs = M.gap_rule_model(json.dumps(rule).encode())
    env = ENV[cid]
    nonreg = nonreg_override if nonreg_override is not None else NONREG[cid]
    root, _ = M.subject_root(env, None)
    od = (env.get('parameters') or {}).get('output_directory')
    g = gaps_override if gaps_override is not None else (
        (env.get('normalized_result') or {}).get('extraction_gaps') or [])
    ok, why = M.disposition_check(g, M.diagnostics(env), nonreg, model, root, od)
    esc = M.nonregular_published(M.published(env), nonreg, root)
    return bool(ok) and root is not None and not esc, why


def gaps_with_device_gap(cid):
    env = copy.deepcopy(ENV[cid])
    g = (env.get('normalized_result') or {}).get('extraction_gaps') or []
    dev = [r for r in NONREG[cid] if r[1] == 'char-device']
    rel = dev[0][0]
    g.append({'kind': 'unpublished-entry',
              'input_path': '$output/firmware.bin_extract/' + rel,
              'relative_path': 'firmware.bin_extract/' + rel,
              'handler': None, 'provider_id': None, 'range': None,
              'root_file_range': None, 'dependencies': [],
              'continuation_id': 'probe-device-gap'})
    return g


print('=== D. the law fail-closed case: a gap landing on a device row ===')
for cid in ('g7581', 'c6430'):
    g = gaps_with_device_gap(cid)
    ok_law, why_law = score_one(cid, LAW, gaps_override=g)
    ok_r50, why_r50 = score_one(cid, R50, gaps_override=g)
    ok_law0, _ = score_one(cid, LAW)
    print('  %-6s baseline LAW=%-5s | with device gap: LAW=%-5s  R50=%-5s'
          % (cid, ok_law0, ok_law, ok_r50))
    print('         LAW says: %s' % why_law[:100])
    print('         R50 says: %s' % why_r50[:100])

print('\n=== E. the `allowed`-shape half of law_shape_ok ===')
v = copy.deepcopy(LAW)
v['allowed']['char-device'] = ['unpublished-entry']
print('  allowed[char-device]=[unpublished-entry], no silent detail:')
for cid in ('g7581',):
    ok, why = score_one(cid, v)
    print('    %-6s disposition verdict = %-5s  (%s)' % (cid, ok, why[:70]))
print('  -> under the CLAIMED law_shape_ok this rule must be RED;')
print('     the round-50 disposition logic says GREEN (no device gap exists).')

print('\n=== F. CTL-JUNK and an over-permissive mirror ===')
junk = copy.deepcopy(LAW)
junk['allowed'] = {k: ['no-such-gap-kind'] for k in LAW['allowed']}
junk['required'] = {k: True for k in LAW['required']}
print('  CTL-JUNK (every kind required, impossible allowance):')
for cid in IDS:
    ok, why = score_one(cid, junk)
    print('    %-6s %-5s %s' % (cid, ok, why[:70]))

perm = copy.deepcopy(LAW)
perm['allowed'] = {k: ['unpublished-entry', 'extractor-failure',
                        'no-such-gap-kind'] for k in LAW['allowed']}
perm['required'] = {k: False for k in LAW['required']}
print('  OVER-PERMISSIVE mirror (required all False, every gap kind allowed):')
for cid in IDS:
    ok, why = score_one(cid, perm)
    print('    %-6s %-5s %s' % (cid, ok, why[:70]))

print('\n=== G. CTL-OLD (r50 rule) vs M3 (required=true, silent 247:0) ===')
m3 = copy.deepcopy(LAW)
m3['removed']['silent'] = {'char-device': ['247:0']}
m3['required']['char-device'] = True
m3['allowed']['char-device'] = ['unpublished-entry']
print('  %-8s %-10s %-10s' % ('carrier', 'CTL-OLD', 'M3'))
for cid in IDS:
    a, _ = score_one(cid, R50)
    b, _ = score_one(cid, m3)
    print('  %-8s %-10s %-10s  identical=%s' % (cid, a, b, a == b))

print('\n=== H. wrong-carrier-set (the carrier identity behind a count) ===')
sets = {'{c6430 x4}': ['c6430'] * 4,
        '{c6490 x4}': ['c6490'] * 4,
        '{g7581 x4}': ['g7581'] * 4,
        '{c6430,c6490 x2}': ['c6430', 'c6490', 'c6430', 'c6490']}
for label, members in sets.items():
    row = []
    for rule, rname in ((LAW, 'LAW'), (R50, 'R50')):
        n = sum(1 for cid in members if score_one(cid, rule)[0])
        row.append('%s=%d/4' % (rname, n))
    print('  %-20s %s' % (label, '  '.join(row)))
print('  -> under CTL-NEW (4/4) every one of these is GREEN;')
print('     under CTL-OLD (2/4) the cable-only sets are 4/4 => CTL-OLD catches')
print('     a collision set, but CTL-NEW alone binds NO carrier identity.')
