#!/usr/bin/env python3
"""Probe 3: M1 whitelist alone, the device-gap fixture (M5 candidate),
the structural-channel escape, and the unpublished_entries / projection channel.
"""
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
TOLERANT = copy.deepcopy(LAW); TOLERANT['allowed']['char-device'] = ['unpublished-entry']
WHITELIST13 = copy.deepcopy(R50)
WHITELIST13['required']['char-device'] = True
WHITELIST13['allowed']['char-device'] = []
WHITELIST13['removed']['silent'] = {'char-device': ['247:0','136:0','136:1','136:2','136:3','136:4',
                                                    '136:5','136:6','136:7','230:0','3:0','3:1','3:2']}

print('== M1 (all-thirteen whitelist) over the committed corpus, disposition only')
for cid in IDS:
    env, nonreg, od = load(cid)
    mm, probs = model(WHITELIST13)
    root, _ = m.subject_root(env)
    ok, why = m.disposition_check(m.gaps(env), m.diagnostics(env), nonreg, mm, root, od)
    print(f'   {cid}: ok={ok} | {why[:130]}')
print('   -> M1 is disposition-GREEN: its redness can only come from law_shape_ok')

print('\n== M5 candidate: fixture envelope carrying a device gap (g7581 dev/pts/0)')
env, nonreg, od = load('g7581')
root, _ = m.subject_root(env)
gaps = copy.deepcopy(m.gaps(env))
gaps.append({'kind':'unpublished-entry','input_path':'$output/'+root+'/dev/pts/0',
             'relative_path':root+'/dev/pts/0','handler':None,'provider_id':None,'range':None,
             'root_file_range':None,'dependencies':[],'continuation_id':'synthetic-device-gap'})
for nm, d in (('LAW', LAW), ('TOLERANT', TOLERANT), ('WHITELIST13', WHITELIST13)):
    mm, _ = model(d)
    ok, why = m.disposition_check(gaps, m.diagnostics(env), nonreg, mm, root, od)
    print(f'   {nm}: ok={ok} | {why[:120]}')

print('\n== structural-channel escape: the device gap REPLACES the depth-limited gap')
gaps2 = [g for g in copy.deepcopy(m.gaps(env)) if g.get('kind') != 'depth-limited']
gaps2.append({'kind':'depth-limited','input_path':'$output/'+root+'/dev/pts/0',
              'relative_path':None,'handler':None,'provider_id':None,'range':None,
              'root_file_range':None,'dependencies':[],'continuation_id':'synthetic'})
for nm, d in (('LAW', LAW),):
    mm, _ = model(d)
    ok, why = m.disposition_check(gaps2, m.diagnostics(env), nonreg, mm, root, od)
    print(f'   {nm}: ok={ok} | {why[:140]}')

print('\n== removal-channel escape: a MaliciousSymlinkRemoved diagnostic on a device row')
d2 = copy.deepcopy(m.diagnostics(env))
print('   sample diagnostic:', json.dumps(d2[0])[:300])
print('   diagnostic_rel of sample:', m.diagnostic_rel(d2[0], root, od))

print('\n== does the published-file channel ever contain a device row? (materialisation check)')
for cid in IDS:
    env, nonreg, od = load(cid)
    files = m.published(env)
    root, _ = m.subject_root(env)
    hits = m.nonregular_published(files, nonreg, root)
    devs = {m.strip_rel(r[0]) for r in nonreg if r[1] == 'char-device'}
    pubrels = {m.extract_rel(fp, root) for fp, _s, _z in files}
    print(f'   {cid}: published={len(files)} nonregular_published={len(hits)} '
          f'device-rows-among-published={len(devs & pubrels)}')

print('\n== projection channel: is unpublished_entries part of the compared projection?')
print('   PROJECTION_KEYS =', m.PROJECTION_KEYS)
print('   PROJECTION_KEYS_BY_PROFILE =', m.PROJECTION_KEYS_BY_PROFILE)
import inspect
src = inspect.getsource(m.projection)
print('   projection() mentions unpublished_entries:', 'unpublished_entries' in src)

print('\n== receipt_paths(): does it include unpublished_entries paths? (path_shape scope)')
rp = m.receipt_paths(env)
print('   receipt_paths count', len(rp), 'sample', rp[:3])
print('   receipt_paths source mentions unpublished_entries:',
      'unpublished_entries' in inspect.getsource(m.receipt_paths))

print('\n== the depth-limited gap: is its input_path the CHUNK ROOT (not the stop point)?')
for cid in IDS:
    env, nonreg, od = load(cid)
    for g in m.gaps(env):
        if g.get('relative_path') is None:
            root2, _ = m.subject_root(env)
            print(f'   {cid}: input_path={g.get("input_path")!r} relative_path={g.get("relative_path")!r} '
                  f'continuation_id={g.get("continuation_id")!r}')
            print(f'        subject root = {root2!r}  output_directory={od!r}')
            break
cids = set()
for cid in IDS:
    env, _n, _o = load(cid)
    for g in m.gaps(env):
        if g.get('relative_path') is None:
            cids.add(g.get('continuation_id'))
print('   distinct continuation_id values across the four carriers:', len(cids), cids)

print('\n== do the device rows live in a subtree with no regular file? (F7 reachability)')
for cid in IDS:
    env, nonreg, od = load(cid)
    files = m.published(env)
    root, _ = m.subject_root(env)
    pubrels = {m.extract_rel(fp, root) for fp, _s, _z in files}
    devs = [r for r in nonreg if r[1] == 'char-device']
    orphan = [r[0] for r in devs
              if not any(pr.startswith(r[0].rsplit('/',1)[0] + '/') for pr in pubrels)]
    print(f'   {cid}: {len(devs)} device rows; device rows whose parent subtree holds '
          f'no published regular file: {orphan}')
