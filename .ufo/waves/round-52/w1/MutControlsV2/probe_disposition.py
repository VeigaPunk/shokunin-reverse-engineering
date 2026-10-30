#!/usr/bin/env python3
"""Offline probe: exercise the round-50 counter's OWN disposition logic over the
committed round-50 envelopes, under candidate round-52 rules.

Read-only on the lane. Imports tools/round-50/c1-counter.py as a module
(its __main__ guard keeps it from running main()).
"""
import hashlib
import importlib.util
import json
import os
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
COUNTER = os.path.join(LANE, 'tools/round-50/c1-counter.py')
RECEIPTS = os.path.join(LANE, 'corpus/evidence/round-50/c1')
IDS = ('c6430', 'c6490', 'g7581', 'g7582')


def load_counter():
    spec = importlib.util.spec_from_file_location('r50counter', COUNTER)
    mod = importlib.util.module_from_spec(spec)
    sys.modules['r50counter'] = mod
    spec.loader.exec_module(mod)
    return mod


M = load_counter()


def nonreg_for(cid):
    raw = open(os.path.join(LANE, 'tools/round-50/oracle/%s.nonregular.tsv' % cid), 'rb').read()
    rows, err = M.parse_nonregular(raw)
    assert err is None, err
    return rows


def envelope(cid):
    return json.load(open(os.path.join(RECEIPTS, cid, 'after.json')))


def gaps(env):
    return (env.get('normalized_result') or {}).get('extraction_gaps') or []


def score(rule_doc, label, ids=IDS):
    model, probs = M.gap_rule_model(json.dumps(rule_doc).encode())
    out = {}
    for cid in ids:
        env = envelope(cid)
        nonreg = nonreg_for(cid)
        root, how = M.subject_root(env, None)
        od = (env.get('parameters') or {}).get('output_directory')
        ok, why = M.disposition_check(gaps(env), M.diagnostics(env), nonreg,
                                      model, root, od)
        files = M.published(env)
        esc = M.nonregular_published(files, nonreg, root)
        unpublished_ok = (root is not None and not esc)
        out[cid] = {'gaps_ok': bool(ok), 'why': why,
                    'nonregular_unpublished_ok': bool(unpublished_ok),
                    'root': root}
    # rule-scoped disposition verdict, per the claims: gaps_ok AND
    # nonregular_unpublished_ok
    disp = {c: (out[c]['gaps_ok'] and out[c]['nonregular_unpublished_ok'])
            for c in out}
    green = sum(1 for v in disp.values() if v)
    return {'label': label, 'parse_problems': probs, 'dispositions': disp,
            'green': green, 'total': len(disp), 'detail': out}


def show(r):
    print('== %s' % r['label'])
    print('   parse_problems: %r' % (r['parse_problems'],))
    for c in sorted(r['detail']):
        d = r['detail'][c]
        print('   %-6s gaps_ok=%-5s unpub_ok=%-5s disp=%-5s  %s'
              % (c, d['gaps_ok'], d['nonregular_unpublished_ok'],
                 r['dispositions'][c], d['why'][:110]))
    print('   -> %d of %d dispositions' % (r['green'], r['total']))
    print()


R50 = json.load(open(os.path.join(LANE, 'tools/round-50/gap-rule.json')))

# candidate r52 law rule: char-device/fifo/socket/block carry no disposition,
# no detail whitelist, allowed for device kinds is the empty list.
LAW = {
    'claim': 'R52-C1',
    'allowed': {
        'symlink': ['unpublished-entry'],
        'char-device': [],
        'block-device': [],
        'fifo': [],
        'socket': [],
        'dir': [],
    },
    'required': {
        'symlink': True,
        'char-device': False,
        'block-device': False,
        'fifo': False,
        'socket': False,
        'dir': False,
    },
    'removed': {
        'diagnostic': 'MaliciousSymlinkRemoved',
        'kinds': ['symlink'],
        'disposition': 'exclusive',
        'silent': {},
    },
    'structural': {'depth-limited': 1, 'unknown-chunk-handler': 0},
}

results = []
results.append(score(R50, 'CTL-OLD arm: round-50 rule'))
results.append(score(LAW, 'CTL-NEW arm: candidate round-52 law rule'))

# M1: all-thirteen whitelist (shape-illegal by the law_shape_ok clause)
dev_details = sorted({r[2] for r in nonreg_for('g7581') if r[1] == 'char-device'})
m1 = json.loads(json.dumps(LAW))
m1['removed']['silent'] = {'char-device': dev_details}
m1['required']['char-device'] = True
m1['allowed']['char-device'] = ['unpublished-entry']
results.append(score(m1, 'M1 arm: all-thirteen detail whitelist (%d details)'
                     % len(dev_details)))

# M4: strict-subset whitelist (subset of the 13)
m4 = json.loads(json.dumps(m1))
m4['removed']['silent'] = {'char-device': dev_details[:2]}
results.append(score(m4, 'M4 arm: strict-subset detail whitelist (%d details)'
                     % len(dev_details[:2])))

# M3: required.char-device=true with only 247:0 silent  (regression)
m3 = json.loads(json.dumps(LAW))
m3['removed']['silent'] = {'char-device': ['247:0']}
m3['required']['char-device'] = True
m3['allowed']['char-device'] = ['unpublished-entry']
results.append(score(m3, 'M3 arm: required char-device=true, silent 247:0'))

# CTL-JUNK: every kind required, impossible allowance
junk = json.loads(json.dumps(LAW))
junk['allowed'] = {k: ['no-such-gap-kind'] for k in LAW['allowed']}
junk['required'] = {k: True for k in LAW['required']}
results.append(score(junk, 'CTL-JUNK arm: every kind required, impossible allowance'))

print('SUMMARY')
for r in results:
    print('  %-70s %d/%d  %s'
          % (r['label'][:70], r['green'], r['total'],
             {c: r['dispositions'][c] for c in sorted(r['dispositions'])}))
