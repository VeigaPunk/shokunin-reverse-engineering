#!/usr/bin/env python3
"""Two-scope witness measurement (corpus + fixtures) for both candidate designs.

v5's `corpus_control` reports RED / VACUOUS / GREEN per scope, because a mutant that
only moves a branch the corpus does not carry is vacuous there, not passed.  This probe
does the same for v6, under both candidate table designs.
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
def m_above_legacy(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); row = r.pop(i)
    j = P.v5._row_index(r, 'legacy-body-failure'); r.insert(j, row); return r
def m_gap_exact(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); r[i][5] = 'extractor-failure'; return r
def m_guard_del(r):
    i = P.v5._row_index(r, 'clean-unverified'); del r[i]; return r
def m_actions_swap(r):
    i = P.v5._row_index(r, 'clean-unverified'); j = P.v5._row_index(r, 'no-reader-failure')
    r[i][10], r[j][10] = r[j][10], r[i][10]; return r
def m_broadcom_clean(r):
    i = P.v5._row_index(r, 'clean-unverified')
    r[i][3] = ','.join(p for p in r[i][3].split(',') if p != 'squashfs_v3_broadcom'); return r
def m_legacy_del(r):
    i = P.v5._row_index(r, 'legacy-body-failure'); del r[i]; return r
def m_noreader_del(r):
    i = P.v5._row_index(r, 'no-reader-failure'); del r[i]; return r
def m_swap_with_legacy(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); j = P.v5._row_index(r, 'legacy-body-failure')
    r[i][10], r[j][10] = r[j][10], r[i][10]; return r
def m_swap_with_noreader(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); j = P.v5._row_index(r, 'no-reader-failure')
    r[i][10], r[j][10] = r[j][10], r[i][10]; return r


MUT = [
    ('M1-unreadable-row-deleted', m_del),
    ('M2-unreadable-action-cross-read-legacy', m_cross),
    ('M3-legacy-failing-cell-broadened-v[123]*', m_glob_legacy),
    ('M4-unreadable-failing-cell-broadened-v[123]*', m_glob_newrow),
    ('M5-unreadable-row-below-body-row', m_below_body),
    ('M6-unreadable-row-above-legacy-row', m_above_legacy),
    ('M7-unreadable-gap-kind-exact', m_gap_exact),
    ('M8-clean-unverified-guard-row-deleted', m_guard_del),
    ('M9-v5-new-row-actions-swapped', m_actions_swap),
    ('M10-no-reader-family-moved-to-clean', m_broadcom_clean),
    ('M11-legacy-body-failure-row-deleted', m_legacy_del),
    ('M12-no-reader-failure-row-deleted', m_noreader_del),
    ('M13-swap-unreadable-action-with-legacy', m_swap_with_legacy),
    ('M14-swap-unreadable-action-with-no-reader-failure', m_swap_with_noreader),
]

out = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'scope_note': 'corpus = the frozen 126-envelope held-out dir; fixtures = the v6 '
                     'selftest fixture set (v5 set + the ddwrt FAILED-body pair)',
       'designs': {}}

for tag, builder in (('A-legacy-cell-drops-ddwrt_new-row-BELOW', designA),
                      ('B-legacy-cell-keeps-ddwrt_new-row-ABOVE', designB)):
    base = builder()
    br, _ = P.parse(base)
    bp = P.pairs(br, fixtures)
    bm, ba = P.score(br, corpus, fixtures)
    entry = {'base': {'corpus_D1': len(bm), 'corpus_D2': len(ba)},
             'fixture_pairs': {k: list(v) for k, v in sorted(bp.items())},
             'mutations': []}
    for name, fn in MUT:
        r = [list(x) for x in base]
        fn(r)
        try:
            rules, _ = P.parse(r)
        except Exception as exc:
            entry['mutations'].append({'mutation': name, 'parse_refused': str(exc)[:120]})
            continue
        mm, aa = P.score(rules, corpus, fixtures)
        p = P.pairs(rules, fixtures)
        flipped = sorted(n for n in bp if bp[n] != p.get(n))
        entry['mutations'].append({
            'mutation': name,
            'corpus_D1': len(mm), 'corpus_D2': len(aa),
            'corpus_red': bool(mm or aa),
            'fixtures_flipped': flipped,
            'fixtures_red': bool(flipped),
            'red_somewhere': bool(mm or aa or flipped),
            'vacuous_everywhere': not (mm or aa or flipped),
        })
    out['designs'][tag] = entry

with open(OUT, 'w', encoding='utf-8') as fh:
    json.dump(out, fh, indent=1, sort_keys=True)
    fh.write('\n')

for tag, entry in out['designs'].items():
    print('==', tag)
    for m in entry['mutations']:
        print('   %-46s corpusD1=%-4s corpusD2=%-4s fix=%-2d  REDsomewhere=%s' % (
            m['mutation'], m.get('corpus_D1'), m.get('corpus_D2'),
            len(m.get('fixtures_flipped', [])), m.get('red_somewhere')))
print('wrote', OUT)
