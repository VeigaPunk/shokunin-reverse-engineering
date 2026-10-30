#!/usr/bin/env python3
"""Probe 2: rule-scoped disposition verdict over the committed round-50
envelopes, with the output_directory passed (so removal diagnostics resolve),
plus the unpublished_entries channel and the M2 fourteenth-device fixture.
"""
import importlib.util, json, os, copy

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec = importlib.util.spec_from_file_location('r50c1', os.path.join(LANE, 'tools/round-50/c1-counter.py'))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

IDS = ('g7581', 'g7582', 'c6490', 'c6430')

def load(cid):
    env = json.load(open(f'{LANE}/corpus/evidence/round-50/c1/{cid}/after.json'))
    raw = open(f'{LANE}/tools/round-50/oracle/{cid}.nonregular.tsv', 'rb').read()
    nonreg, err = m.parse_nonregular(raw); assert err is None, err
    od = (env.get('parameters') or {}).get('output_directory')
    return env, nonreg, od

R50 = json.load(open(f'{LANE}/tools/round-50/gap-rule.json'))

LAW = {
    'claim': 'R52-C1',
    'allowed': {'symlink': ['unpublished-entry'], 'char-device': [], 'block-device': [],
                'fifo': [], 'socket': [], 'dir': []},
    'required': {'symlink': True, 'char-device': False, 'block-device': False,
                 'fifo': False, 'socket': False, 'dir': False},
    'removed': {'diagnostic': 'MaliciousSymlinkRemoved', 'kinds': ['symlink'],
                'disposition': 'exclusive', 'silent': {}},
    'structural': {'depth-limited': 1, 'unknown-chunk-handler': 0},
}
TOLERANT = copy.deepcopy(LAW)
TOLERANT['allowed']['char-device'] = ['unpublished-entry']
OMITTED = copy.deepcopy(LAW)
for k in ('char-device', 'block-device', 'fifo', 'socket'):
    OMITTED['allowed'].pop(k); OMITTED['required'].pop(k)
LAW_REQ_TRUE = copy.deepcopy(LAW); LAW_REQ_TRUE['required']['char-device'] = True
LAW_REQ_TRUE_SILENT = copy.deepcopy(LAW_REQ_TRUE)
LAW_REQ_TRUE_SILENT['removed']['silent'] = {'char-device': ['247:0']}

def model(doc):
    mm, probs = m.gap_rule_model(json.dumps(doc).encode())
    return mm, [p for p in probs if '!= R50-C1' not in p]

def run(name, doc):
    n = 0; detail = {}
    for cid in IDS:
        env, nonreg, od = load(cid)
        mm, probs = model(doc)
        root, _ = m.subject_root(env)
        ok, why = m.disposition_check(m.gaps(env), m.diagnostics(env), nonreg, mm, root, od)
        detail[cid] = (ok, why, probs)
        n += 1 if ok else 0
    print(f'== {name}: {n}/4 green')
    for cid in IDS:
        ok, why, probs = detail[cid]
        print(f'   {cid}: ok={ok} | {why[:150]}')
        if probs: print(f'      probs {probs}')
    return n, detail

res = {}
for nm, d in (('CTL-OLD round-50 rule', R50),
               ('CTL-NEW law rule', LAW),
               ('TOLERANT (device gap allowed)', TOLERANT),
               ('OMITTED (device kinds absent)', OMITTED),
               ('LAW + required[char-device]=true, silent={}', LAW_REQ_TRUE),
               ('LAW + required[char-device]=true, silent={247:0}', LAW_REQ_TRUE_SILENT)):
    res[nm] = run(nm, d)

print('\n== unpublished_entries channel in the committed envelopes')
for cid in IDS:
    env, nonreg, od = load(cid)
    nr = env.get('normalized_result') or {}
    ue = nr.get('unpublished_entries')
    print(f'   {cid}: unpublished_entries type={type(ue).__name__} '
          f'len={len(ue) if isinstance(ue,list) else "n/a"}')
    if isinstance(ue, list) and ue:
        print('      sample:', json.dumps(ue[0])[:220])
        kinds = {}
        for u in ue:
            if isinstance(u, dict):
                k = u.get('kind') or u.get('type') or '?'
                kinds[k] = kinds.get(k, 0) + 1
        print('      kinds:', kinds)
        print('      keys of first entry:', sorted(ue[0].keys()) if isinstance(ue[0], dict) else None)

print('\n== is unpublished_entries consulted by disposition_check?')
import inspect
src = inspect.getsource(m.disposition_check)
print('   "unpublished" appears in disposition_check source:', 'unpublished' in src)
print('   counter references to unpublished_entries:')
import subprocess
out = subprocess.run(['grep', '-n', 'unpublished_entries', os.path.join(LANE, 'tools/round-50/c1-counter.py')],
                     capture_output=True, text=True).stdout
print(out.rstrip() or '   (none)')

print('\n== M2: a fixture census with a fourteenth unlisted device (dev/ttyS0 4:64)')
WHITELIST13 = copy.deepcopy(R50)
WHITELIST13['required']['char-device'] = True
WHITELIST13['allowed']['char-device'] = []
WHITELIST13['removed']['silent'] = {'char-device': [
    '247:0', '136:0', '136:1', '136:2', '136:3', '136:4', '136:5', '136:6',
    '136:7', '230:0', '3:0', '3:1', '3:2']}
for cid in ('g7581',):
    env, nonreg, od = load(cid)
    root, _ = m.subject_root(env)
    extra = nonreg + [('dev/ttyS0', 'char-device', '4:64')]
    for nm, d in (('LAW', LAW), ('WHITELIST13 (M1/M4)', WHITELIST13),
                  ('TOLERANT', TOLERANT), ('OMITTED', OMITTED)):
        mm, _ = model(d)
        ok, why = m.disposition_check(m.gaps(env), m.diagnostics(env), extra, mm, root, od)
        print(f'   {nm}: ok={ok} | {why[:130]}')

print('\n== gap injection: future extractor emits a device gap (dev/pts/0 on g7581)')
env, nonreg, od = load('g7581')
root, _ = m.subject_root(env)
gaps = copy.deepcopy(m.gaps(env))
gaps.append({'kind': 'unpublished-entry', 'input_path': '$output/' + root + '/dev/pts/0',
             'relative_path': root + '/dev/pts/0', 'handler': None, 'provider_id': None,
             'range': None, 'root_file_range': None, 'dependencies': [],
             'continuation_id': 'synthetic'})
for nm, d in (('LAW', LAW), ('TOLERANT', TOLERANT), ('OMITTED', OMITTED)):
    mm, _ = model(d)
    ok, why = m.disposition_check(gaps, m.diagnostics(env), nonreg, mm, root, od)
    print(f'   {nm}: ok={ok} | {why[:140]}')

print('\n== gap kind rename: same device gap but kind="device-node" (not in allowed at all)')
gaps2 = copy.deepcopy(gaps); gaps2[-1]['kind'] = 'device-node'
for nm, d in (('LAW', LAW), ('TOLERANT', TOLERANT)):
    mm, _ = model(d)
    ok, why = m.disposition_check(gaps2, m.diagnostics(env), nonreg, mm, root, od)
    print(f'   {nm}: ok={ok} | {why[:140]}')

print('\n== gap on a path that maps to no census row (dev/newthing 99:0)')
gaps3 = copy.deepcopy(m.gaps(env))
gaps3.append({'kind': 'unpublished-entry', 'input_path': '$output/' + root + '/dev/newthing',
               'relative_path': root + '/dev/newthing', 'handler': None, 'provider_id': None,
               'range': None, 'root_file_range': None, 'dependencies': [],
               'continuation_id': 'synthetic'})
for nm, d in (('LAW', LAW), ('TOLERANT', TOLERANT)):
    mm, _ = model(d)
    ok, why = m.disposition_check(gaps3, m.diagnostics(env), nonreg, mm, root, od)
    print(f'   {nm}: ok={ok} | {why[:140]}')

print('\n== structural channel: a null-path gap of kind depth-limited (device gap laundered)')
gaps4 = copy.deepcopy(m.gaps(env))
gaps4.append({'kind': 'depth-limited', 'input_path': '$output/' + root + '/dev/pts/0',
               'relative_path': None, 'handler': None, 'provider_id': None, 'range': None,
               'root_file_range': None, 'dependencies': [], 'continuation_id': 'synthetic'})
for nm, d in (('LAW', LAW),):
    mm, _ = model(d)
    ok, why = m.disposition_check(gaps4, m.diagnostics(env), nonreg, mm, root, od)
    print(f'   {nm}: ok={ok} | {why[:140]}')

print('\n== depth-limited gap record in the committed envelope (F8 fields)')
for cid in IDS:
    env, nonreg, od = load(cid)
    for g in m.gaps(env):
        if g.get('relative_path') is None:
            print(f'   {cid}: {json.dumps(g)}')
            break
