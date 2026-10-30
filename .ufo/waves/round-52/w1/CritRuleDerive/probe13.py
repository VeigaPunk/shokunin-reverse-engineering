#!/usr/bin/env python3
"""Probe 13: final — required on non-char device kinds; carriers-table label."""
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

LAW = {'claim':'R52-C1',
  'allowed': {'symlink':['unpublished-entry'],'char-device':[],'block-device':[],'fifo':[],'socket':[],'dir':[]},
  'required': {'symlink':True,'char-device':False,'block-device':False,'fifo':False,'socket':False,'dir':False},
  'removed': {'diagnostic':'MaliciousSymlinkRemoved','kinds':['symlink'],'disposition':'exclusive','silent':{}},
  'structural': {'depth-limited':1,'unknown-chunk-handler':0}}

def n_green(doc):
    n = 0
    for cid in IDS:
        env, nonreg, od = load(cid)
        mm, _ = m.gap_rule_model(json.dumps(doc).encode())
        root, _ = m.subject_root(env)
        ok, _w = m.disposition_check(m.gaps(env), m.diagnostics(env), nonreg, mm, root, od)
        n += 1 if ok else 0
    return n

def shape(doc):
    DEV = ('char-device','block-device','fifo','socket')
    notes = []
    silent = (doc.get('removed') or {}).get('silent') or {}
    for k in DEV:
        if (doc.get('allowed') or {}).get(k): notes.append('allowed[%r]' % k)
        if silent.get(k): notes.append('silent[%r]' % k)
    if (doc.get('required') or {}).get('char-device') is not False:
        notes.append("required['char-device']")
    return (not notes), notes

print('== required on the NON-char device kinds: law_shape_ok (r51 draft) + CTL-NEW')
for k in ('block-device', 'fifo', 'socket'):
    d = copy.deepcopy(LAW); d['required'][k] = True
    s, notes = shape(d)
    print(f'   required[{k!r}]=True : law_shape_ok={s} {notes}  CTL-NEW={n_green(d)}/4 green'
          f'  (no such row exists in the corpus)')

print('\n== the EVIL removal-kinds rule: law_shape_ok + CTL-NEW + M2 + device removal')
EVIL = copy.deepcopy(LAW)
EVIL['removed']['kinds'] = ['symlink','char-device','block-device','fifo','socket']
s, notes = shape(EVIL)
print(f'   law_shape_ok={s} {notes}   CTL-NEW={n_green(EVIL)}/4 green')
env, nonreg, od = load('g7581')
root, _ = m.subject_root(env)
diags = copy.deepcopy(m.diagnostics(env))
diags.append({'input_path': '$input', 'report': {'__typename__':'MaliciousSymlinkRemoved',
             'severity':'WARNING','link': od + '/' + root + '/dev/led','target':'/dev/null'}})
for nm, d in (('LAW', LAW), ('EVIL', EVIL)):
    mm, _ = m.gap_rule_model(json.dumps(d).encode())
    ok, why = m.disposition_check(m.gaps(env), diags, nonreg, mm, root, od)
    print(f'   {nm:5s} with a device-row removal: ok={ok} | {why[:110]}')

print('\n== OMITTED rule (device kinds absent): CTL-NEW + law_shape_ok (r51 draft)')
OM = copy.deepcopy(LAW)
for k in ('char-device','block-device','fifo','socket'):
    OM['allowed'].pop(k); OM['required'].pop(k)
s, notes = shape(OM)
print(f'   law_shape_ok (r51 draft: required[char-device] must be False) = {s} {notes}')
print(f'   CTL-NEW = {n_green(OM)}/4 green   <- CTL-NEW ALONE cannot tell it from the law')

print('\n== the carriers-table claim label is a SECOND grammar site')
import inspect
src = inspect.getsource(m.carriers_spec)
print('   carriers_spec claim check present in the v1 counter:',
      "spec.get('claim') != 'R50-C1'" in src)
print('   the R52 claims F10 names only `gap_rule_model`; the v1 counter has TWO checks:')
print('     gap_rule_model  (c1-counter.py:790-791)')
print('     carriers_spec   (c1-counter.py:876-877)')
print('   the frozen carriers tables carry per-round labels:')
for p in ('.ufo/waves/round-41/c1/carriers.json', 'tools/round-49/carriers.json',
          'tools/round-50/carriers.json'):
    d = json.load(open(os.path.join(LANE, p)))
    print(f'     {p}: claim={d.get("claim")!r}')
