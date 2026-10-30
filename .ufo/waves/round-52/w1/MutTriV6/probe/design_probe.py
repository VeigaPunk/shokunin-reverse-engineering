#!/usr/bin/env python3
"""Design-dependence probe: which mutants are no-ops under which table design?

Design A (what the r52 claim implies): the legacy row's failing-handler cell DROPS
`squashfs_v3_ddwrt`; the new `legacy-body-unreadable` row sits BELOW the legacy row.
Design B: the legacy row KEEPS `squashfs_v3_ddwrt`; the new row sits ABOVE it.

For each design, mutate and measure D1/D2.  A mutant that is a no-op in one design
and red in the other is design-dependent, not a battery defect.
"""
import sys, json, os, datetime

sys.path.insert(0, '/fast/scratch/hyaku/kaidoku-r52/w1-MutTriV6')
import proto_v6 as P

OUT = sys.argv[1]
corpus = P.load_corpus()
fixtures = P.v6_fixtures()


def designA():
    return [list(r) for r in P.V6_ROWS]


def designB():
    rows = [list(r) for r in P.V6_ROWS]
    j = P.v5._row_index(rows, 'legacy-body-failure')
    rows[j][4] = 'squashfs_v1,squashfs_v2,squashfs_v3,squashfs_v3_ddwrt'
    i = P.v5._row_index(rows, 'legacy-body-unreadable')
    row = rows.pop(i)
    rows.insert(j, row)
    return rows


def m_del(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); del r[i]; return r
def m_cross(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); r[i][10] = 'cross-read-legacy'; return r
def m_glob_legacy(r):
    i = P.v5._row_index(r, 'legacy-body-failure'); r[i][4] = 'squashfs_v[123]*'; return r
def m_glob_newrow(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); r[i][4] = 'squashfs_v[123]*'; return r
def m_below_body(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); row = r.pop(i)
    j = P.v5._row_index(r, 'body-extractor-failure'); r.insert(j + 1, row); return r
def m_gap_exact(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); r[i][5] = 'extractor-failure'; return r


MUT = [
    ('unreadable-row-deleted', m_del),
    ('unreadable-action-cross-read-legacy', m_cross),
    ('legacy-failing-cell-broadened-v[123]*', m_glob_legacy),
    ('unreadable-failing-cell-broadened-v[123]*', m_glob_newrow),
    ('unreadable-row-below-body-row', m_below_body),
    ('unreadable-gap-kind-exact', m_gap_exact),
]

out = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'designs': {}}

for tag, builder in (('A-legacy-cell-drops-ddwrt_new-row-BELOW', designA),
                      ('B-legacy-cell-keeps-ddwrt_new-row-ABOVE', designB)):
    base = builder()
    br, bi = P.parse(base)
    bm, ba = P.score(br, corpus, fixtures)
    entry = {'base_D1': len(bm), 'base_D2': len(ba), 'rules': bi['rules'], 'mutations': []}
    for name, fn in MUT:
        r = [list(x) for x in base]
        fn(r)
        try:
            rules, info = P.parse(r)
        except Exception as exc:
            entry['mutations'].append({'mutation': name, 'parse_refused': str(exc)[:120]})
            continue
        mm, aa = P.score(rules, corpus, fixtures)
        entry['mutations'].append({
            'mutation': name, 'D1': len(mm), 'D2': len(aa),
            'D1_envelopes': [x['envelope'] for x in mm],
            'D2_envelopes': [x['envelope'] for x in aa],
            'no_op': (len(mm) == 0 and len(aa) == 0),
        })
    out['designs'][tag] = entry

with open(OUT, 'w', encoding='utf-8') as fh:
    json.dump(out, fh, indent=1, sort_keys=True)
    fh.write('\n')
for tag, entry in out['designs'].items():
    print(tag, 'base D1=%d D2=%d' % (entry['base_D1'], entry['base_D2']))
    for m in entry['mutations']:
        print('   %-44s D1=%-4s D2=%-4s noop=%s' % (
            m['mutation'], m.get('D1'), m.get('D2'), m.get('no_op')))
print('wrote', OUT)
