#!/usr/bin/env python3
"""Offline probe of the R52-C1 law encoding against COMMITTED round-50 bytes.

Imports the committed round-50 counter (read-only) and exercises:
  - disposition_check() with candidate rules over the four committed envelopes
  - census gap/unpublished coverage of the 28 device rows
  - counterexamples to the CTL-NEW control
No REA, no network, no writes outside this scratch.
"""
import importlib.util
import json
import os
import sys
import copy

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
SPEC = os.path.join(LANE, 'tools/round-50/c1-counter.py')

spec = importlib.util.spec_from_file_location('r50c1', SPEC)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

IDS = ('g7581', 'g7582', 'c6490', 'c6430')
OUT = {}

def load(cid):
    env = json.load(open(f'{LANE}/corpus/evidence/round-50/c1/{cid}/after.json'))
    raw = open(f'{LANE}/tools/round-50/oracle/{cid}.nonregular.tsv', 'rb').read()
    nonreg, err = m.parse_nonregular(raw)
    assert err is None, err
    return env, nonreg

def rule_model(doc):
    model, probs = m.gap_rule_model(json.dumps(doc).encode())
    # the v2 rule parser must accept both claim labels (F10); the v1 parser
    # only knows R50-C1, so drop that one problem for this offline probe.
    probs = [p for p in probs if '!= R50-C1' not in p]
    return model, probs

def verdict(doc, cid, env=None, nonreg=None, gaps=None, diags=None, root=None, od=None):
    if env is None:
        env, nonreg = load(cid)
    model, probs = rule_model(doc)
    if gaps is None:
        gaps = m.gaps(env)
    if diags is None:
        diags = m.diagnostics(env)
    if root is None:
        root, _how = m.subject_root(env)
    ok, why = m.disposition_check(gaps, diags, nonreg, model, root, od)
    return ok, why, probs

R50_RULE = json.load(open(f'{LANE}/tools/round-50/gap-rule.json'))

# ---- the R52 law rule as the claims describe it ----------------------
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

# ---- counterexample rules --------------------------------------------
TOLERANT = copy.deepcopy(LAW)          # same shape, but tolerates a device gap
TOLERANT['allowed']['char-device'] = ['unpublished-entry']
TOLERANT['allowed']['fifo'] = ['unpublished-entry']
TOLERANT['allowed']['socket'] = ['unpublished-entry']

OMITTED = copy.deepcopy(LAW)            # device kinds not mentioned at all
for k in ('char-device', 'block-device', 'fifo', 'socket'):
    OMITTED['allowed'].pop(k, None)
    OMITTED['required'].pop(k, None)

WHITELIST13 = copy.deepcopy(R50_RULE)   # M1: all-thirteen whitelist
WHITELIST13['required']['char-device'] = True
WHITELIST13['allowed']['char-device'] = []
WHITELIST13['removed']['silent'] = {'char-device': [
    '247:0', '136:0', '136:1', '136:2', '136:3', '136:4', '136:5', '136:6',
    '136:7', '230:0', '3:0', '3:1', '3:2']}

rows = []
def rec(name, doc, **kw):
    res = {}
    for cid in IDS:
        ok, why, probs = verdict(doc, cid, **kw)
        res[cid] = {'ok': ok, 'why': why[:160], 'probs': probs}
    n = sum(1 for v in res.values() if v['ok'])
    rows.append((name, n, res))
    print(f'== {name}: {n}/4 dispositions green')
    for cid in IDS:
        print(f'   {cid}: ok={res[cid]["ok"]} {res[cid]["why"]}')
        if res[cid]['probs']:
            print(f'      probs: {res[cid]["probs"]}')
    return res

rec('CTL-OLD (round-50 rule)', R50_RULE)
rec('CTL-NEW (law rule)', LAW)
rec('TOLERANT (law shape but device gap allowed)', TOLERANT)
rec('OMITTED (device kinds not mentioned)', OMITTED)
rec('WHITELIST13 (M1)', WHITELIST13)

OUT['base'] = [(n, k) for n, k, _ in rows]

# ---- counterexample: a future extractor emits a device gap ------------
print('\n== gap injection: a future extractor emits an unpublished-entry gap '
      'on dev/pts/0 (a FRITZ!Box device row)')
for name, doc in (('LAW', LAW), ('TOLERANT', TOLERANT), ('R50', R50_RULE)):
    for cid in ('g7581', 'c6490'):
        env, nonreg = load(cid)
        gaps = copy.deepcopy(m.gaps(env))
        root, _ = m.subject_root(env)
        # find the device row and synthesise a gap for it
        dev = [r for r in nonreg if r[1] == 'char-device']
        assert dev, cid
        rel = dev[0][0]
        gaps.append({'kind': 'unpublished-entry',
                     'input_path': '$output/' + root + '/' + rel,
                     'relative_path': root + '/' + rel,
                     'handler': None, 'provider_id': None, 'range': None,
                     'root_file_range': None, 'dependencies': [],
                     'continuation_id': 'synthetic-device-gap'})
        ok, why, _ = verdict(doc, cid, env=env, nonreg=nonreg, gaps=gaps, root=root)
        print(f'   {name:9s} {cid}: ok={ok}  {why[:110]}')
        OUT.setdefault('inject', []).append((name, cid, ok, why[:200]))

# ---- census coverage of the device rows -------------------------------
print('\n== census coverage of the 28 device rows')
tot = 0
for cid in IDS:
    env, nonreg = load(cid)
    gaps = m.gaps(env)
    diags = m.diagnostics(env)
    root, _ = m.subject_root(env)
    gap_rels = {m.extract_rel(g.get('relative_path'), root)
                for g in gaps if g.get('relative_path')}
    files = m.published(env)
    pub = {m.extract_rel(fp, root) for fp, _s, _z in files}
    nr = env.get('normalized_result') or {}
    unpub = nr.get('unpublished_entries') or []
    unpub_rels = set()
    for u in unpub:
        if isinstance(u, dict):
            unpub_rels.add(m.strip_rel(u.get('relative_path') or u.get('path') or ''))
        elif isinstance(u, str):
            unpub_rels.add(m.strip_rel(u))
    devs = [r for r in nonreg if r[1] in ('char-device', 'block-device',
                                          'fifo', 'socket')]
    hit_gap = [r[0] for r in devs if m.strip_rel(r[0]) in gap_rels]
    hit_pub = [r[0] for r in devs if m.strip_rel(r[0]) in pub]
    hit_unpub = [r[0] for r in devs if m.strip_rel(r[0]) in unpub_rels]
    print(f'   {cid}: {len(devs)} device rows; gap={hit_gap} published={hit_pub} '
          f'unpublished_entries={hit_unpub}')
    tot += len(devs)
    # kinds present
    kinds = sorted({r[1] for r in nonreg})
    print(f'      census kinds: {kinds}  entries={len(nonreg)}')
print(f'   total device rows = {tot}')

# ---- what does `published` contain? are symlink/device paths listed? ----
print('\n== published-file shape (does a materialized device show up?)')
env, nonreg = load('g7581')
files = m.published(env)
root, _ = m.subject_root(env)
rels = [m.extract_rel(fp, root) for fp, _s, _z in files]
print('   published count', len(rels))
print('   any device path published?',
      [r for r in rels if r and ('dev/' in r)][:5])
sym = [r for r in nonreg if r[1] == 'symlink'][:3]
print('   sample symlink rows', sym)
print('   are symlink paths among published?',
      [r for r in sym if m.strip_rel(r[0]) in set(rels)][:3])
print('   total symlink rows', sum(1 for r in nonreg if r[1] == 'symlink'))

json.dump(OUT, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  'probe-out.json'), 'w'), indent=1)
print('\nwrote probe-out.json')
