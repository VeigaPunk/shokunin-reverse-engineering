#!/usr/bin/env python3
"""R40W2C1Gaps: attack the frozen gap rule against the four C1 receipts."""
import importlib.util, json, os, sys, collections

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec = importlib.util.spec_from_file_location('c1c', LANE + '/tools/round-40/c1-counter.py')
c1c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1c)

rule_raw = open(LANE + '/.ufo/waves/round-40/c1/gap-rule.json', 'rb').read()
model, probs = c1c.gap_rule_model(rule_raw)
print('== gap_rule_model problems:', probs)
print('== model:', json.dumps(model, sort_keys=True))
print()

def env_of(path):
    d = json.load(open(path))
    if isinstance(d, dict) and isinstance(d.get('data'), dict):
        return d['data']
    return d

def diags(env):
    nr = env.get('normalized_result') or {}
    out = []
    for d in nr.get('diagnostics') or []:
        if isinstance(d, dict):
            r = d.get('report') or {}
            out.append(r.get('__typename__') or '<none>')
    return collections.Counter(out)

def raw_diags(env):
    """typename occurrences anywhere under raw_result too."""
    txt = json.dumps((env.get('raw_result') or {}))
    return txt.count('MaliciousSymlinkRemoved')

summary = {}
for cid in ('V1', 'V2', 'L1', 'L2'):
    base = LANE + '/corpus/evidence/round-40/c1/' + cid
    after = env_of(base + '/after.json')
    run = env_of(base + '/run.json')
    nonreg, nerr = c1c.parse_nonregular(open(base + '/nonregular.tsv', 'rb').read())
    oracle, oerr = c1c.parse_oracle(open(base + '/oracle.tsv', 'rb').read())
    nr = after.get('normalized_result') or {}
    gaps_list = c1c.gaps(after)
    files = c1c.published(after)

    print('=' * 70)
    print('CARRIER', cid, '| nonreg entries:', len(nonreg), '| oracle:', len(oracle),
          '| published:', len(files), '| gaps:', len(gaps_list))
    kinds = collections.Counter(k for _, k in nonreg)
    print('  table kinds:', dict(kinds))
    print('  table kind strings sample:', sorted({k for _, k in nonreg}))

    # structural gaps
    struct = [(g.get('kind'), g.get('dependencies')) for g in gaps_list
              if isinstance(g, dict) and g.get('relative_path') is None]
    print('  structural (null-path) gaps:', struct)

    # path gaps: resolve each
    per_entry = collections.Counter()
    resolved = []
    anomalies = []
    for i, g in enumerate(gaps_list):
        if not isinstance(g, dict):
            anomalies.append(('non-object gap', i)); continue
        kind = g.get('kind'); rp = g.get('relative_path')
        if rp is None:
            continue
        hits = [r for r, _ in nonreg if c1c.same_rel(rp, r)]
        ek = dict(nonreg)[hits[0]] if len(hits) == 1 else None
        resolved.append((i, kind, rp, len(hits), ek))
        if len(hits) == 1:
            per_entry[hits[0]] += 1
        else:
            anomalies.append(('hits=%d' % len(hits), kind, rp))
    bad_res = [r for r in resolved if r[3] != 1]
    print('  path gaps:', len(resolved), '| unresolved/multi-hit:', bad_res[:5])
    # every unpublished-entry on a symlink?
    nonsym = [(k, rp) for _, k, rp, h, ek in resolved if h == 1 and k == 'unpublished-entry' and ek != 'symlink']
    print('  unpublished-entry gaps NOT on a symlink entry:', nonsym)
    # devices/dirs in gap list?
    dev_dir = [(k, rp) for _, k, rp, h, ek in resolved if h == 1 and ek in ('dir', 'char-device', 'block-device')]
    print('  gaps resolving to dir/device entries:', dev_dir)
    # per-entry gap counts
    cnt = collections.Counter(per_entry.values())
    print('  gaps-per-entry histogram:', dict(cnt))
    multi = {e: n for e, n in per_entry.items() if n != 1}
    print('  entries with !=1 path gap:', multi)
    ungapped_symlinks = [r for r, k in nonreg if k == 'symlink' and per_entry[r] == 0]
    print('  symlinks with no gap:', ungapped_symlinks)
    ungapped_other = [(r, k) for r, k in nonreg if k != 'symlink' and per_entry[r] == 0]
    print('  non-symlink entries with no gap (count):', len(ungapped_other),
          '| kinds:', sorted({k for _, k in ungapped_other}))

    # gap path shapes
    extract_pref = [rp for _, _, rp, h, ek in resolved if h == 1 and '_extract' in (rp or '')]
    print('  gap paths containing _extract:', len(extract_pref), extract_pref[:3])

    # duplicate exact gaps
    sig = collections.Counter(json.dumps(g, sort_keys=True) for g in gaps_list if isinstance(g, dict))
    dups = {k: v for k, v in sig.items() if v > 1}
    print('  exact duplicate gap objects:', len(dups))

    # diagnostics
    dc = diags(after)
    print('  after.json diagnostics:', dict(dc), '| raw MaliciousSymlinkRemoved count:', raw_diags(after))
    dcr = diags(run)
    print('  run.json diagnostics:', dict(dcr), '| raw MaliciousSymlinkRemoved count:', raw_diags(run))

    # unpublished_entries field
    unpub = nr.get('unpublished_entries') or []
    print('  unpublished_entries field:', len(unpub), 'rows; kinds:',
          dict(collections.Counter(u.get('kind') for u in unpub if isinstance(u, dict))))

    # published vs nonreg (the L2 issue)
    esc = c1c.nonregular_published(files, nonreg)
    print('  published files suffix-matching nonreg entries:', esc[:5], '(n=%d)' % len(esc))

    # run.json gaps vs after.json gaps (rel-suffix projection)
    def gap_proj(e):
        out = []
        for g in c1c.gaps(e):
            if isinstance(g, dict):
                out.append((g.get('kind'), c1c.rel_suffix(g.get('relative_path'))))
        return sorted(out, key=json.dumps)
    ga, gr = gap_proj(after), gap_proj(run)
    print('  rerun gaps == committed gaps (suffix proj):', ga == gr,
          '| committed:', len(ga), 'rerun:', len(gr))
    if ga != gr:
        onlya = [x for x in ga if x not in gr][:3]
        onlyr = [x for x in gr if x not in ga][:3]
        print('    committed_only:', onlya, 'rerun_only:', onlyr)

    # the counter's own verdict
    ok, why = c1c.gap_check(gaps_list, nonreg, model)
    print('  gap_check =>', ok, '|', why)

    # suffix-collision pairs inside the table (fragility scan)
    coll = []
    for r1, k1 in nonreg:
        for r2, k2 in nonreg:
            if r1 != r2 and c1c.same_rel(r1, r2):
                coll.append((r2, k2, '->', r1, k1))
    print('  in-table suffix collisions:', len(coll), coll[:5])

    # oracle rows colliding with nonreg paths (suffix)
    oc = []
    for rel, _sha in oracle:
        for r, k in nonreg:
            if c1c.same_rel(rel, r):
                oc.append((rel, '->', r, k))
    print('  oracle paths suffix-matching nonreg entries:', len(oc), oc[:5])
    print()
    summary[cid] = dict(structural=struct, unresolved=bad_res, nonsym=nonsym,
                        multi=multi, dups=len(dups), esc=esc, coll=coll, oc=oc)

json.dump({k: {kk: (vv if not isinstance(vv, list) else vv[:20]) for kk, vv in v.items()}
           for k, v in summary.items()},
          open('/fast/scratch/hyaku/kaidoku-r40/R40W2C1Gaps/summary.json', 'w'), indent=1, default=str)
print('summary written')
