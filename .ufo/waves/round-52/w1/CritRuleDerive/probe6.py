#!/usr/bin/env python3
"""Probe 6: the decisive counterexamples.

C1  law_shape_ok (as the claims define it) does NOT constrain removed.kinds ->
    a rule that names char-device as a REMOVABLE kind accepts a device-row
    removal diagnostic as a legal disposition, i.e. a device entry carries a
    disposition, contradicting the law.  Does every frozen control still pass?
C2  the claims' F10 grammar fix covers gap_rule_model but the v1 counter has a
    SECOND, separate claim check in carriers_spec().
C3  the unpublished_entries channel: is it in the rule-scoped controls' scope?
"""
import importlib.util, json, os, copy, inspect

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

# C1: law_shape_ok as the claims define it
def law_shape_ok(doc):
    """The claims' wording: no device detail under removed.silent, and
    allowed for those kinds is the empty list."""
    dev = ('char-device','block-device','fifo','socket')
    reasons = []
    silent = (doc.get('removed') or {}).get('silent') or {}
    for k in dev:
        if silent.get(k):
            reasons.append('silent[%s] names device details' % k)
        if (doc.get('allowed') or {}).get(k) != []:
            reasons.append('allowed[%s] is not the empty list' % k)
    return (not reasons), reasons

# the counterexample rule: identical to the law, but removed.kinds also names
# char-device (and fifo/socket/block-device)
EVIL = copy.deepcopy(LAW)
EVIL['removed']['kinds'] = ['symlink', 'char-device', 'fifo', 'socket', 'block-device']

print('== C1: law_shape_ok (claims wording) on the LAW and on EVIL')
for nm, d in (('LAW', LAW), ('EVIL (removed.kinds names device kinds)', EVIL)):
    ok, why = law_shape_ok(d)
    print(f'   {nm}: law_shape_ok={ok} {why}')

print('\n== C1b: EVIL over the committed corpus (CTL-NEW must still be 4/4)')
for cid in IDS:
    env, nonreg, od = load(cid)
    mm, probs = model(EVIL)
    root, _ = m.subject_root(env)
    ok, why = m.disposition_check(m.gaps(env), m.diagnostics(env), nonreg, mm, root, od)
    print(f'   {cid}: ok={ok} | {why[:120]}')

print('\n== C1c: EVIL + a MaliciousSymlinkRemoved diagnostic on a device row')
env, nonreg, od = load('g7581')
root, _ = m.subject_root(env)
diags = copy.deepcopy(m.diagnostics(env))
diags.append({'input_path': '$input',
              'report': {'__typename__': 'MaliciousSymlinkRemoved', 'severity': 'WARNING',
                         'link': od + '/' + root + '/dev/led', 'target': '/dev/null'}})
for nm, d in (('LAW', LAW), ('EVIL', EVIL)):
    mm, _ = model(d)
    ok, why = m.disposition_check(m.gaps(env), diags, nonreg, mm, root, od)
    print(f'   {nm}: ok={ok} | {why[:150]}')
print('   -> under EVIL a device row carries a REMOVAL disposition; the law says it')
print('      carries no disposition at all, yet EVIL passes law_shape_ok and CTL-NEW.')

print('\n== C1d: EVIL + a fourteenth device (M2 fixture) -> still green?')
extra = nonreg + [('dev/ttyS0', 'char-device', '4:64')]
mm, _ = model(EVIL)
ok, why = m.disposition_check(m.gaps(env), m.diagnostics(env), extra, mm, root, od)
print(f'   EVIL + 14th device: ok={ok} | {why[:130]}')

print('\n== C2: the second claim check (carriers_spec) the claims\' F10 does not mention')
src = inspect.getsource(m.carriers_spec)
print(src[:700])
print('   gap_rule_model also checks the claim label:',
      'claim' in inspect.getsource(m.gap_rule_model))

print('\n== C3: is unpublished_entries in the rule-scoped control scope?')
print('   disposition_check reads unpublished_entries:',
      'unpublished_entries' in inspect.getsource(m.disposition_check))
print('   but projection compares it:',
      'unpublished_entries' in inspect.getsource(m.projection))
print('   PROJECTION_KEYS:', m.PROJECTION_KEYS)
print('   -> a device row reported in unpublished_entries[] is invisible to the')
print('      rule-scoped controls (gaps_ok / nonregular_unpublished_ok) and would')
print('      only surface as a projection difference at the data run.')

print('\n== C3b: measure it: inject a char-device into unpublished_entries')
env2 = copy.deepcopy(env)
env2['normalized_result']['unpublished_entries'].append(
    {'relative_path': root + '/dev/led', 'kind': 'char-device'})
mm, _ = model(LAW)
ok, why = m.disposition_check(m.gaps(env2), m.diagnostics(env2), nonreg, mm, root, od)
print(f'   LAW + device in unpublished_entries: disposition ok={ok} | {why[:100]}')
files = m.published(env2)
print(f'   nonregular_published: {m.nonregular_published(files, nonreg, root)}')
print('   -> the device entry now carries a disposition (an unpublished-entry record)')
print('      and the frozen rule still scores green.')
