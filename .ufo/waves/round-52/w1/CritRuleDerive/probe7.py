#!/usr/bin/env python3
"""Probe 7: M2 vacuity, law_shape_ok ambiguity, and the fifo/socket ground."""
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

LAW = {'claim':'R52-C1',
  'allowed': {'symlink':['unpublished-entry'],'char-device':[],'block-device':[],'fifo':[],'socket':[],'dir':[]},
  'required': {'symlink':True,'char-device':False,'block-device':False,'fifo':False,'socket':False,'dir':False},
  'removed': {'diagnostic':'MaliciousSymlinkRemoved','kinds':['symlink'],'disposition':'exclusive','silent':{}},
  'structural': {'depth-limited':1,'unknown-chunk-handler':0}}

# ---- M2: is it vacuous?  A "detail whitelist" in two shapes.
WHITELIST_REQ_TRUE = copy.deepcopy(LAW)          # required=true + 13 details silent
WHITELIST_REQ_TRUE['required']['char-device'] = True
WHITELIST_REQ_TRUE['removed']['silent'] = {'char-device': [
    '247:0','136:0','136:1','136:2','136:3','136:4','136:5','136:6','136:7',
    '230:0','3:0','3:1','3:2']}
WHITELIST_REQ_FALSE = copy.deepcopy(WHITELIST_REQ_TRUE)   # same, but required=false
WHITELIST_REQ_FALSE['required']['char-device'] = False

print('== M2: fourteenth device (dev/ttyS0 4:64) -- which whitelists go RED?')
for cid in ('g7581',):
    env, nonreg, od = load(cid)
    root, _ = m.subject_root(env)
    extra = nonreg + [('dev/ttyS0', 'char-device', '4:64')]
    for nm, d in (('LAW', LAW),
                  ('WHITELIST required=true + 13 details', WHITELIST_REQ_TRUE),
                  ('WHITELIST required=false + 13 details', WHITELIST_REQ_FALSE)):
        mm, _ = model(d)
        ok, why = m.disposition_check(m.gaps(env), m.diagnostics(env), extra, mm, root, od)
        print(f'   {nm:42s}: ok={ok} | {why[:100]}')
print('   -> the claims require M2 RED "under any detail whitelist"; the')
print('      required=false whitelist stays GREEN.  M2 discriminates only against')
print('      whitelists that ALSO set required[char-device]=true.')

print('\n== M2 over the committed corpus WITHOUT the 14th device (the CTL-NEW arm)')
for cid in IDS:
    env, nonreg, od = load(cid)
    root, _ = m.subject_root(env)
    mm, _ = model(WHITELIST_REQ_TRUE)
    ok, why = m.disposition_check(m.gaps(env), m.diagnostics(env), nonreg, mm, root, od)
    print(f'   {cid}: ok={ok} | {why[:90]}')
print('   -> the whitelist is disposition-GREEN on the committed corpus; only')
print('      law_shape_ok separates it from the law there.')

print('\n== law_shape_ok ambiguity: a rule that does not MENTION the device kinds')
OMITTED = copy.deepcopy(LAW)
for k in ('char-device','block-device','fifo','socket'):
    OMITTED['allowed'].pop(k); OMITTED['required'].pop(k)

def shape_strict(doc):
    dev = ('char-device','block-device','fifo','socket')
    r = []
    silent = (doc.get('removed') or {}).get('silent') or {}
    for k in dev:
        if silent.get(k): r.append('silent[%s]' % k)
        if k not in (doc.get('allowed') or {}) : r.append('allowed[%s] ABSENT' % k)
        elif (doc.get('allowed') or {})[k] != []: r.append('allowed[%s] not []' % k)
        if (doc.get('required') or {}).get(k) is not False: r.append('required[%s] not false' % k)
    return (not r), r

def shape_lenient(doc):
    """The claims' literal wording: `allowed.get(k, []) == []` -- absent counts."""
    dev = ('char-device','block-device','fifo','socket')
    r = []
    silent = (doc.get('removed') or {}).get('silent') or {}
    for k in dev:
        if silent.get(k): r.append('silent[%s]' % k)
        if (doc.get('allowed') or {}).get(k, []) != []: r.append('allowed[%s] not []' % k)
    return (not r), r

for nm, d in (('LAW', LAW), ('OMITTED', OMITTED)):
    print(f'   {nm}: strict={shape_strict(d)} lenient={shape_lenient(d)}')

print('\n== does the OMITTED rule pass CTL-NEW over the committed corpus?')
for cid in IDS:
    env, nonreg, od = load(cid)
    root, _ = m.subject_root(env)
    mm, probs = model(OMITTED)
    ok, why = m.disposition_check(m.gaps(env), m.diagnostics(env), nonreg, mm, root, od)
    print(f'   {cid}: ok={ok} | {why[:90]} | model probs={probs}')
print('   -> OMITTED (a rule that says NOTHING about device rows) is CTL-NEW 4/4')
print('      and passes a lenient law_shape_ok.  Only the STRICT reading of')
print('      law_shape_ok distinguishes it.')

print('\n== fifo/socket: what would the law rule do if a carrier HAD a fifo row?')
for cid in ('g7581',):
    env, nonreg, od = load(cid)
    root, _ = m.subject_root(env)
    # simulate: the extractor materialises the fifo and reports it as an
    # unpublished-entry gap (the metadata rule of SKILL.md block 26)
    gaps = copy.deepcopy(m.gaps(env))
    gaps.append({'kind':'unpublished-entry','input_path':'$output/'+root+'/dev/pipe0',
                 'relative_path':root+'/dev/pipe0','handler':None,'provider_id':None,
                 'range':None,'root_file_range':None,'dependencies':[],
                 'continuation_id':'synthetic-fifo'})
    withfifo = nonreg + [('dev/pipe0','fifo','')]
    for nm, d in (('LAW (allowed[fifo]=[])', LAW),):
        mm, _ = model(d)
        ok, why = m.disposition_check(gaps, m.diagnostics(env), withfifo, mm, root, od)
        print(f'   {nm}: ok={ok} | {why[:140]}')
    r50 = json.load(open(f'{LANE}/tools/round-50/gap-rule.json'))
    mm, _ = model(r50)
    ok, why = m.disposition_check(gaps, m.diagnostics(env), withfifo, mm, root, od)
    print(f'   ROUND-50 rule (allowed[fifo]=[unpublished-entry]): ok={ok} | {why[:140]}')
print('   -> the law rule would go RED on a fifo gap; the round-50 rule tolerates it.')
print('      S250 says the FIFO/socket creation branches are NOT root-gated, so an')
print('      unprivileged unsquashfs DOES create them; the law sentence therefore')
print('      over-claims its own cited source for fifo/socket.')
