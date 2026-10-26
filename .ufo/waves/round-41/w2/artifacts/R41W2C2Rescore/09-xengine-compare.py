import importlib.util, json, os, sys
spec = importlib.util.spec_from_file_location(
    'cc', '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-41/c2-counter.py')
cc = importlib.util.module_from_spec(spec); spec.loader.exec_module(cc)
HELD = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-41/c2/heldout'
man = json.load(open(os.path.join(HELD, 'manifest.json')))
mine = json.load(open('indep.txt'))
mrow = {r['id']: r for r in mine['rows']}
diff = []
for c in man['carriers']:
    cid = c['id']
    env = json.load(open(os.path.join(HELD, cid, 'envelope.json')))
    cobs = cc.observed_features(env)
    mobs = mrow[cid]['observed']
    if mobs is None:
        diff.append((cid, 'mine-none')); continue
    for k in ('handler_set', 'gap_kinds', 'gap_dependencies', 'be_argv',
              'symlink_removed', 'published'):
        if cobs[k] != mobs[k]:
            diff.append((cid, k, cobs[k], mobs[k]))
    if cobs['extraction_failed'] != mobs.get('extraction_failed'):
        pass
print(json.dumps({'n': len(man['carriers']), 'engine_vs_indep_diffs': diff}, indent=1))
# also: does any envelope carry a non-squashfs handler or a handler on a gap?
odd = set(); gaph = set()
for c in man['carriers']:
    env = json.load(open(os.path.join(HELD, c['id'], 'envelope.json')))
    nr = env.get('normalized_result') or {}
    for ch in nr.get('chunks') or []:
        h = ch.get('handler')
        if isinstance(h, str) and not h.startswith('squashfs'):
            odd.add((c['id'], h))
    for g in nr.get('extraction_gaps') or []:
        if isinstance(g.get('handler'), str):
            gaph.add((c['id'], g['handler']))
print(json.dumps({'nonsquashfs_chunk_handlers': sorted(odd),
                  'gaps_with_handler': sorted(gaph)}, indent=1))
