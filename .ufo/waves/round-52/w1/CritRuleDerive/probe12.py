#!/usr/bin/env python3
"""Probe 12: mirror-channel check + corrected depth histogram + reach table."""
import importlib.util, json, os, collections

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec = importlib.util.spec_from_file_location('r50c1', os.path.join(LANE, 'tools/round-50/c1-counter.py'))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

for cid in ('g7581', 'g7582', 'c6490', 'c6430'):
    env = json.load(open(f'{LANE}/corpus/evidence/round-50/c1/{cid}/after.json'))
    nonreg, _ = m.parse_nonregular(open(f'{LANE}/tools/round-50/oracle/{cid}.nonregular.tsv','rb').read())
    root, _ = m.subject_root(env)
    nr = env['normalized_result']
    gaps = m.gaps(env)
    gap_rel = {m.extract_rel(g.get('relative_path'), root) for g in gaps if g.get('relative_path')}
    ue_rel = {m.strip_rel(m.extract_rel(u.get('relative_path'), root) or '')
              for u in (nr.get('unpublished_entries') or [])}
    print(f'== {cid}')
    print(f'   path-resolved gaps={len(gap_rel)}  unpublished_entries={len(ue_rel)}  '
          f'identical sets: {gap_rel == ue_rel}  gap-only={len(gap_rel-ue_rel)} ue-only={len(ue_rel-gap_rel)}')
    depths = collections.Counter(fp.count('/') for fp, _s, _z in m.published(env))
    print(f'   published relative_path depth histogram: {dict(sorted(depths.items()))}')
    devs = [r for r in nonreg if r[1] == 'char-device']
    reached, unreached = [], []
    for rel, kind, detail in devs:
        parent = rel.rsplit('/', 1)[0]
        has = any(p == parent or p.startswith(parent + '/')
                  for p in gap_rel | ue_rel
                  | {m.extract_rel(fp, root) for fp, _s, _z in m.published(env)})
        (reached if has else unreached).append(rel)
    print(f'   device rows={len(devs)}  parent dir HAS an extractor-side record: {len(reached)} '
          f'{reached}')
    print(f'   device rows whose parent dir has NO extractor-side record: {len(unreached)} {unreached}')
    print(f'   census rows under dev/pts/: '
          f'{[(r[0], r[1]) for r in nonreg if r[0].startswith("dev/pts/")]}')
    print()
