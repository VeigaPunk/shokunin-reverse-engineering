#!/usr/bin/env python3
"""Probe 2: what actually discriminates the r52 law rule from neighbours?

Offline; reads the lane read-only. Answers:
  A. Do the committed round-50 envelopes carry ANY gap landing on a char-device
     row?  (i.e. is the law's `allowed[char-device] == []` fail-closed clause
     witnessed by any committed receipt, or is it untested?)
  B. Which minimal edits of the candidate law rule still score 4/4 under the
     round-50 counter's disposition logic?  (the discriminating surface)
  C. The M2 fixture: a 14th unlisted char-device row under the law rule vs a
     13-detail detail-whitelist.
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

NONREG = {}
for cid in IDS:
    raw = open(os.path.join(LANE, 'tools/round-50/oracle/%s.nonregular.tsv' % cid),
               'rb').read()
    rows, err = M.parse_nonregular(raw)
    assert err is None, err
    NONREG[cid] = rows

ENV = {cid: json.load(open(os.path.join(LANE, 'corpus/evidence/round-50/c1/%s/after.json'
                                       % cid))) for cid in IDS}


def verdict(rule, nonreg_over=None):
    model, probs = M.gap_rule_model(json.dumps(rule).encode())
    out = {}
    for cid in IDS:
        env = ENV[cid]
        nonreg = NONREG[cid]
        if nonreg_over and cid in nonreg_over:
            nonreg = nonreg + nonreg_over[cid]
        root, _ = M.subject_root(env, None)
        od = (env.get('parameters') or {}).get('output_directory')
        ok, why = M.disposition_check(
            (env.get('normalized_result') or {}).get('extraction_gaps') or [],
            M.diagnostics(env), nonreg, model, root, od)
        esc = M.nonregular_published(M.published(env), nonreg, root)
        out[cid] = (bool(ok) and root is not None and not esc, why)
    return sum(1 for v in out.values() if v[0]), out, probs


print('=== A. do committed envelopes carry a gap on a char-device row? ===')
for cid in IDS:
    env = ENV[cid]
    root, _ = M.subject_root(env, None)
    rows_at = {}
    for rel, kind, detail in NONREG[cid]:
        rows_at.setdefault(M.strip_rel(rel), []).append((rel, kind))
    dev_gaps = []
    for g in (env.get('normalized_result') or {}).get('extraction_gaps') or []:
        rp = g.get('relative_path')
        if rp is None:
            continue
        rel = M.extract_rel(rp, root)
        hits = rows_at.get(rel, []) if rel else []
        if len(hits) == 1 and hits[0][1] == 'char-device':
            dev_gaps.append((g.get('kind'), rel))
    ndev = sum(1 for _r, k, _d in NONREG[cid] if k == 'char-device')
    print('  %-6s char-device census rows=%2d  gaps landing on a device row=%d %s'
          % (cid, ndev, len(dev_gaps), dev_gaps[:3]))

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

dev_details = sorted({r[2] for r in NONREG['g7581'] if r[1] == 'char-device'})
print('\n=== B. discriminating surface of the law rule (4/4 = GREEN) ===')
VARIANTS = []
VARIANTS.append(('LAW (candidate)', LAW))
VARIANTS.append(('CTL-OLD: round-50 rule', R50))

v = copy.deepcopy(LAW)
v['removed']['silent'] = {'char-device': dev_details}
v['required']['char-device'] = True
v['allowed']['char-device'] = ['unpublished-entry']
VARIANTS.append(('M1: all-%d whitelist' % len(dev_details), v))

v = copy.deepcopy(LAW)
v['removed']['silent'] = {'char-device': dev_details[:2]}
v['required']['char-device'] = True
v['allowed']['char-device'] = ['unpublished-entry']
VARIANTS.append(('M4: 2-detail subset whitelist', v))

v = copy.deepcopy(LAW)
v['removed']['silent'] = {'char-device': ['247:0']}
v['required']['char-device'] = True
v['allowed']['char-device'] = ['unpublished-entry']
VARIANTS.append(('M3: required=true, silent 247:0 only', v))

v = copy.deepcopy(LAW)
v['required']['char-device'] = True
VARIANTS.append(('V1: required char-device=TRUE, silent empty, allowed[]', v))

v = copy.deepcopy(LAW)
v['allowed']['char-device'] = ['unpublished-entry']
VARIANTS.append(('V2: allowed[char-device]=[unpublished-entry] (r50-like)', v))

v = copy.deepcopy(LAW)
del v['required']
VARIANTS.append(('V3: `required` key absent entirely', v))

v = copy.deepcopy(LAW)
v['removed']['silent'] = {'symlink': ['empty-target']}
VARIANTS.append(('V4: + silent symlink empty-target', v))

v = copy.deepcopy(LAW)
v['structural'] = {}
VARIANTS.append(('V5: structural {} (no depth-limited allowance)', v))

v = copy.deepcopy(LAW)
v['structural'] = {'depth-limited': 5, 'unknown-chunk-handler': 5}
VARIANTS.append(('V6: structural allowances 5/5 (over-generous)', v))

v = copy.deepcopy(LAW)
v['removed'] = {'diagnostic': 'MaliciousSymlinkRemoved', 'kinds': ['symlink',
                'char-device'], 'disposition': 'exclusive', 'silent': {}}
VARIANTS.append(('V7: removed.kinds += char-device', v))

for label, rule in VARIANTS:
    n, out, probs = verdict(rule)
    note = out['g7581'][1][:70]
    print('  %-52s %d/4  %s%s' % (label, n, 'PARSE-PROB ' if probs else '', note))

print('\n=== C. M2 fixture: a 14th unlisted char-device row ===')
fourteenth = [('dev/ttyS0', 'char-device', '4:64')]
over = {cid: fourteenth for cid in IDS}
for label, rule in (('LAW', LAW),
                    ('M1 whitelist (13 details)', VARIANTS[2][1])):
    n, out, probs = verdict(rule, over)
    print('  %-30s %d/4   g7581: %s' % (label, n, out['g7581'][1][:80]))

print('\n=== C3. does the 14th row reach the disposition logic under LAW? ===')
n, out, probs = verdict(LAW, over)
print('     LAW 4/4 with a 14th device row ->', n == 4,
      '| g7581 note:', out['g7581'][1][:90])
