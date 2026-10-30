#!/usr/bin/env python3
"""Probe 4: extractor-side REACH evidence for the device rows.

The law's evidentiary basis is "28 of 28 char-device rows carry no extraction
gap and no published path".  This probe asks the harder question: is there any
extractor-side record at all under the device rows' directories (dev/, dev/pts/)?
Census rows come from the independent reader (unsquashfs), not from the
extractor, so a census row is NOT evidence the extractor reached it.
"""
import importlib.util, json, os, collections

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec = importlib.util.spec_from_file_location('r50c1', os.path.join(LANE, 'tools/round-50/c1-counter.py'))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

for cid in ('g7581', 'g7582', 'c6490', 'c6430'):
    env = json.load(open(f'{LANE}/corpus/evidence/round-50/c1/{cid}/after.json'))
    nonreg, _ = m.parse_nonregular(open(f'{LANE}/tools/round-50/oracle/{cid}.nonregular.tsv','rb').read())
    root, _ = m.subject_root(env)
    od = (env.get('parameters') or {}).get('output_directory')
    nr = env.get('normalized_result') or {}

    pub = {m.extract_rel(fp, root) for fp, _s, _z in m.published(env)}
    gaps = m.gaps(env)
    gap_rel = {m.extract_rel(g.get('relative_path'), root) for g in gaps if g.get('relative_path')}
    ue = nr.get('unpublished_entries') or []
    ue_rel = {m.strip_rel(m.extract_rel(u.get('relative_path'), root) or '') for u in ue if isinstance(u, dict)}
    diag_rel = {m.diagnostic_rel(d, root, od) for d in m.diagnostics(env)}
    diag_rel = {x for x in diag_rel if x}

    # extractor-side records, all three channels, grouped by top-level dir
    ext = set(pub) | {x for x in gap_rel if x} | ue_rel | diag_rel
    top = collections.Counter(x.split('/')[0] for x in ext)
    print(f'== {cid}: extractor-side records by top-level dir: {dict(sorted(top.items()))}')

    # any extractor-side record under dev/ ?
    under_dev = sorted(x for x in ext if x == 'dev' or x.startswith('dev/'))
    print(f'   records under dev/: {under_dev}')

    # the directories the device rows live in
    devs = [r for r in nonreg if r[1] == 'char-device']
    dirs = sorted({r[0].rsplit('/', 1)[0] for r in devs})
    print(f'   device-row directories: {dirs}')
    for d in dirs:
        rec = sorted(x for x in ext if x == d or x.startswith(d + '/'))
        census_rows = [r for r in nonreg if r[0] == d or r[0].startswith(d + '/')]
        print(f'      {d}: extractor-side records={len(rec)} {rec[:6]}')
        print(f'      {d}: census rows={len(census_rows)} kinds='
              f'{dict(collections.Counter(r[1] for r in census_rows))}')

    # is there ANY symlink row under dev/ in the census (i.e. would the
    # extractor have seen the directory at all)?
    census_dev = [r for r in nonreg if r[0] == 'dev' or r[0].startswith('dev/')]
    print(f'   census rows under dev/: {len(census_dev)} '
          f'{dict(collections.Counter(r[1] for r in census_dev))}')
    print(f'   census dev/ rows sample: {census_dev[:6]}')

    # the depth-limited gap: what path does it actually name?
    for g in gaps:
        if g.get('relative_path') is None:
            print(f'   depth-limited gap: input_path={g.get("input_path")!r} '
                  f'handler={g.get("handler")!r} continuation_id={g.get("continuation_id")[:16]}...')
            break
    print(f'   rea_parameters in receipt: {env.get("parameters")}')
    print()
