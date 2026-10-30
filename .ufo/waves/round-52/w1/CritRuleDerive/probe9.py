#!/usr/bin/env python3
"""Probe 9: CTL-JUNK / CTL-DN shapes, and the full expected-verdict table for
the frozen control set over the committed corpus."""
import importlib.util, json, os, copy

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec = importlib.util.spec_from_file_location('r50c1', os.path.join(LANE, 'tools/round-50/c1-counter.py'))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
IDS = ('g7581', 'g7582', 'c6490', 'c6430')

def load(cid):
    env = json.load(open(f'{LANE}/corpus/evidence/round-50/c1/{cid}/after.json'))
    nonreg, err = m.parse_nonregular(open(f'{LANE}/tools/round-50/oracle/{cid}.nonregular.tsv','rb').read())
    assert err is None
    od = (env.get('parameters') or {}).get('output_directory')
    return env, nonreg, od

def model(doc):
    mm, probs = m.gap_rule_model(json.dumps(doc).encode())
    return mm, [p for p in probs if '!= R50-C1' not in p]

R50 = json.load(open(f'{LANE}/tools/round-50/gap-rule.json'))
LAW = {'claim':'R52-C1',
  'allowed': {'symlink':['unpublished-entry'],'char-device':[],'block-device':[],'fifo':[],'socket':[],'dir':[]},
  'required': {'symlink':True,'char-device':False,'block-device':False,'fifo':False,'socket':False,'dir':False},
  'removed': {'diagnostic':'MaliciousSymlinkRemoved','kinds':['symlink'],'disposition':'exclusive','silent':{}},
  'structural': {'depth-limited':1,'unknown-chunk-handler':0}}
JUNK = copy.deepcopy(LAW)
JUNK['required'] = {k: True for k in LAW['required']}
JUNK['allowed'] = {k: [] for k in LAW['allowed']}

def score(name, doc):
    n = 0; per = {}
    for cid in IDS:
        env, nonreg, od = load(cid)
        mm, probs = model(doc)
        root, _ = m.subject_root(env)
        ok, why = m.disposition_check(m.gaps(env), m.diagnostics(env), nonreg, mm, root, od)
        per[cid] = (ok, why[:100], probs)
        n += 1 if ok else 0
    print(f'{name:46s}: {n}/4 green')
    for cid in IDS:
        ok, why, probs = per[cid]
        print(f'    {cid}: ok={ok} {why}')
        if probs: print(f'       probs={probs}')
    return n

print('== control table over the committed corpus (disposition verdict)')
score('CTL-OLD  round-50 rule', R50)
score('CTL-NEW  law rule', LAW)
score('CTL-JUNK every kind required, no allowance', JUNK)

print('\n== CTL-DN: do-nothing fixture (no receipts) -- the counter must exit 1 or 2')
print('   (the counter raises Unevaluable when a receipt is absent: '
      'measure() sets receipt_present=False and gaps_ok stays unset)')
env, nonreg, od = load('g7581')
mm, _ = model(LAW)
# simulate "no receipts": an empty envelope
empty = {'normalized_result': {'files': [], 'extraction_gaps': [], 'diagnostics': []}}
root2, _ = m.subject_root(empty)
ok, why = m.disposition_check([], [], nonreg, mm, root2, None)
print(f'   disposition_check with an empty envelope: ok={ok} | {why[:140]}')

print('\n== the round-50 rule at its own freeze: carriers_matched 2 (the committed miss)')
p = f'{LANE}/.ufo/waves/round-50/l1/scores/c1-after-attempt2.json'
if os.path.exists(p):
    d = json.load(open(p))
    print('   committed round-50 miss receipt keys:', sorted(d.keys())[:14])
    for k in ('carriers_matched', 'exit_code', 'predicate', 'revision', 'freeze'):
        if k in d: print(f'      {k} = {d[k]}')
    per = d.get('per_carrier') or d.get('carriers') or {}
    if isinstance(per, dict):
        for cid, v in per.items():
            if isinstance(v, dict):
                print(f'      {cid}: gaps_ok={v.get("gaps_ok")} projection_ok={v.get("projection_ok")} '
                      f'carriers_matched_ok={v.get("carriers_matched_ok")}')
else:
    print('   (receipt not found)')
