#!/usr/bin/env python3
"""Probe 8: what exactly is the depth-limited gap?  Is the tree fully descended?
Does the census contain regular files under dev/ ?  Is dev/pts/ reached?"""
import importlib.util, json, os, collections

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec = importlib.util.spec_from_file_location('r50c1', os.path.join(LANE, 'tools/round-50/c1-counter.py'))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

for cid in ('g7581', 'c6490'):
    env = json.load(open(f'{LANE}/corpus/evidence/round-50/c1/{cid}/after.json'))
    oracle, oerr = m.parse_oracle(open(f'{LANE}/tools/round-50/oracle/{cid}.oracle.tsv','rb').read())
    nonreg, _ = m.parse_nonregular(open(f'{LANE}/tools/round-50/oracle/{cid}.nonregular.tsv','rb').read())
    root, _ = m.subject_root(env)
    files = m.published(env)
    hits = m.oracle_hits(oracle, files, root, m.nested_roots(env, root))
    print(f'== {cid}')
    print(f'   oracle regular files={len(oracle)} published={len(files)} oracle_hits={hits} '
          f'-> every oracle regular file published: {hits==len(oracle)}')
    depths = collections.Counter(p[0].count('/') for p, _s, _z in files)
    print(f'   published path depth histogram: {dict(sorted(depths.items()))}')
    orc_dev = [r[0] for r in oracle if r[0].startswith('dev/')]
    print(f'   oracle regular files under dev/: {len(orc_dev)} {orc_dev[:5]}')
    nr = env['normalized_result']
    print(f'   depth_limited_paths={nr.get("depth_limited_paths")}')
    print(f'   coverage={nr.get("coverage")}')
    conts = nr.get('extraction_continuations') or []
    print(f'   extraction_continuations: {len(conts)}')
    for c in conts:
        print(f'      id={c.get("id")[:12]}... instruction={str(c.get("instruction"))[:110]}')
    # is the depth-limited gap's continuation the "raise max_depth" one?
    dl = [g for g in m.gaps(env) if g.get('relative_path') is None]
    ids = {c.get('id') for c in conts}
    for g in dl:
        print(f'   depth-limited gap continuation_id in continuations: '
              f'{g.get("continuation_id") in ids}')
    # census: any dir row under dev/pts
    dirs = [r for r in nonreg if r[1] == 'dir']
    print(f'   census dir rows={len(dirs)}; under dev/: '
          f'{[r[0] for r in dirs if r[0].startswith("dev/")]}')
    # file analysis_depth values
    ad = collections.Counter(f.get('analysis_depth') for f in (nr.get('files') or []))
    print(f'   analysis_depth histogram: {dict(sorted(ad.items(), key=lambda kv: str(kv[0])))}')
    print()
