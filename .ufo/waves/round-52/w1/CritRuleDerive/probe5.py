#!/usr/bin/env python3
"""Probe 5: the materialisation channel, the unpublished_entries channel,
and whether F8's remedy (input_path + continuation_id) localises the depth limit.
"""
import importlib.util, json, os, copy, hashlib

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec = importlib.util.spec_from_file_location('r50c1', os.path.join(LANE, 'tools/round-50/c1-counter.py'))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

R50 = json.load(open(f'{LANE}/tools/round-50/gap-rule.json'))
LAW = {'claim':'R52-C1',
  'allowed': {'symlink':['unpublished-entry'],'char-device':[],'block-device':[],'fifo':[],'socket':[],'dir':[]},
  'required': {'symlink':True,'char-device':False,'block-device':False,'fifo':False,'socket':False,'dir':False},
  'removed': {'diagnostic':'MaliciousSymlinkRemoved','kinds':['symlink'],'disposition':'exclusive','silent':{}},
  'structural': {'depth-limited':1,'unknown-chunk-handler':0}}

env = json.load(open(f'{LANE}/corpus/evidence/round-50/c1/g7581/after.json'))
nonreg, _ = m.parse_nonregular(open(f'{LANE}/tools/round-50/oracle/g7581.nonregular.tsv','rb').read())
od = (env.get('parameters') or {}).get('output_directory')
root, _ = m.subject_root(env)
nr = env.get('normalized_result') or {}
mm, _ = m.gap_rule_model(json.dumps(LAW).encode())

print('== normalized_result keys:', sorted(nr.keys()))
print('== a published file entry:', json.dumps((nr.get("files") or [None])[0])[:300])
print('== does `files` carry a type/kind field?',
      sorted((nr.get('files') or [{}])[0].keys()))

print('\n== ESCAPE 1: the extractor materialises the device node and emits NO gap')
# simulate: the device node exists in the extract tree.  Two candidate channels:
#  (a) it appears in `files` (published list)
files2 = copy.deepcopy(m.published(env))
files2.append((root + '/dev/led', '0' * 64, 0))
ok, why = m.disposition_check(m.gaps(env), m.diagnostics(env), nonreg, mm, root, od)
print(f'   disposition_check verdict (unchanged envelope): ok={ok} | {why[:100]}')
esc = m.nonregular_published(files2, nonreg, root)
print(f'   nonregular_published WITH the materialised device: {esc}')
print(f'   -> nonregular_unpublished_ok would be {not esc}')

print('\n== ESCAPE 2: the extractor reports the device in unpublished_entries (not a gap)')
env3 = copy.deepcopy(env)
env3['normalized_result']['unpublished_entries'].append(
    {'relative_path': root + '/dev/led', 'kind': 'char-device'})
ok, why = m.disposition_check(m.gaps(env3), m.diagnostics(env3), nonreg, mm, root, od)
print(f'   disposition_check verdict: ok={ok} | {why[:110]}')
print('   -> disposition_check reads unpublished_entries:',
      'unpublished' in __import__('inspect').getsource(m.disposition_check))

print('\n== ESCAPE 3: the extractor emits the device gap as a STRUCTURAL gap (relative_path=null)')
gaps3 = [g for g in copy.deepcopy(m.gaps(env)) if g.get('kind') != 'depth-limited']
gaps3.append({'kind': 'depth-limited', 'input_path': '$output/' + root + '/dev/pts/0',
              'relative_path': None, 'handler': None, 'provider_id': None, 'range': None,
              'root_file_range': None, 'dependencies': [], 'continuation_id': 'synthetic'})
ok, why = m.disposition_check(gaps3, m.diagnostics(env), nonreg, mm, root, od)
print(f'   verdict: ok={ok} | {why[:130]}  <-- structural channel, device gap invisible')

print('\n== F8 remedy check: does input_path / continuation_id localise the depth limit?')
cids, ips = set(), set()
for cid in ('g7581', 'g7582', 'c6490', 'c6430'):
    e = json.load(open(f'{LANE}/corpus/evidence/round-50/c1/{cid}/after.json'))
    for g in m.gaps(e):
        if g.get('relative_path') is None:
            cids.add(g.get('continuation_id')); ips.add(g.get('input_path'))
            print(f'   {cid}: input_path={g.get("input_path")!r} continuation_id={g.get("continuation_id")}')
print(f'   distinct input_path across the four carriers: {len(ips)} -> {ips}')
print(f'   distinct continuation_id across the four carriers: {len(cids)}')
for cand in ('$output/firmware.bin_extract', 'firmware.bin_extract', '$output/firmware.bin_extract/'):
    print(f'   sha256({cand!r}) = {hashlib.sha256(cand.encode()).hexdigest()[:16]}...')
print('   -> the continuation_id is IDENTICAL for four different carriers and the input_path is')
print('      the chunk ROOT, so neither names the subtree the depth limit stopped in.')

print('\n== the depth limit itself: rea_parameters.max_depth in the committed envelopes')
for cid in ('g7581', 'c6490'):
    e = json.load(open(f'{LANE}/corpus/evidence/round-50/c1/{cid}/after.json'))
    print(f'   {cid}: max_depth={(e.get("parameters") or {}).get("max_depth")}')

print('\n== REACH test per device row: does the extractor-side record set contain the row\'s directory?')
for cid in ('g7581', 'g7582', 'c6490', 'c6430'):
    e = json.load(open(f'{LANE}/corpus/evidence/round-50/c1/{cid}/after.json'))
    ng, _ = m.parse_nonregular(open(f'{LANE}/tools/round-50/oracle/{cid}.nonregular.tsv','rb').read())
    r, _ = m.subject_root(e)
    o = (e.get('parameters') or {}).get('output_directory')
    ext = {m.extract_rel(fp, r) for fp, _s, _z in m.published(e)}
    ext |= {m.extract_rel(g.get('relative_path'), r) for g in m.gaps(e) if g.get('relative_path')}
    ext |= {m.strip_rel(m.extract_rel(u.get('relative_path'), r) or '') for u in (e['normalized_result'].get('unpublished_entries') or [])}
    ext |= {x for x in (m.diagnostic_rel(d, r, o) for d in m.diagnostics(e)) if x}
    devs = [x for x in ng if x[1] == 'char-device']
    unreached = [x[0] for x in devs
                 if not any(p == x[0].rsplit('/', 1)[0] or p.startswith(x[0].rsplit('/', 1)[0] + '/')
                            for p in ext)]
    print(f'   {cid}: {len(devs)} device rows, {len(unreached)} in a directory with NO '
          f'extractor-side record: {unreached}')
