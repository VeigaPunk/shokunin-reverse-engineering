#!/usr/bin/env python3
"""Definitive per-mutant scope classification for the v6 battery (design A).

Classifies each mutant as:
  RED-CORPUS   : flips a corpus pair / audit finding
  CORPUS-VACUOUS: flips only in the fixture scope (corpus green, fixtures red)
  NO-OP        : flips nothing in either scope
Also reports whether the mutant is witnessed once the EXTRA synthetic fixtures
(the reader-backed ddwrt FAILED body, the multi-gap ddwrt FAILED body) are added.
"""
import sys, json, os, datetime

sys.path.insert(0, '/fast/scratch/hyaku/kaidoku-r52/w1-MutTriV6')
import proto_v6 as P

OUT = sys.argv[1]
corpus = P.load_corpus()
base_fixtures = P.v6_fixtures()


def multi_gap_env():
    env = P.v5._env(handler='squashfs_v3_ddwrt', gaps=['extractor-failure'], be='-be', files=0)
    env['normalized_result']['extraction_gaps'] = [
        {'kind': 'extractor-failure', '__typename__': 'ExtractionGap'},
        {'kind': 'depth-limited', '__typename__': 'ExtractionGap'}]
    return env


extra_fixtures = base_fixtures + [
    ('v3ddwrt-multigap', multi_gap_env(), ('legacy-body-unreadable', 'preserve-unresolved')),
]


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
def m_swap_legacy(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); j = P.v5._row_index(r, 'legacy-body-failure')
    r[i][10], r[j][10] = r[j][10], r[i][10]; return r
def m_swap_noreader(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); j = P.v5._row_index(r, 'no-reader-failure')
    r[i][10], r[j][10] = r[j][10], r[i][10]; return r
def m_widen_noreader(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable')
    r[i][4] = ('squashfs_v3_ddwrt,squashfs_v2_nonstandard,'
               'squashfs_v3_broadcom,squashfs_v3_nonstandard'); return r
def m_widen_vstar(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); r[i][4] = 'squashfs_v*'; return r
def m_widen_v3star(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); r[i][4] = 'squashfs_v3*'; return r
def m_label_rename(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); r[i][0] = 'legacy-body-unreadable-v2'; return r
def m_action_none(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); r[i][10] = 'none'; return r
def m_blank_handler(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); r[i][3] = ''; return r
def m_blank_action(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); r[i][10] = ''; return r


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
    ('M13-swap-unreadable-action-with-legacy', m_swap_legacy),
    ('M14-swap-unreadable-action-with-no-reader-failure', m_swap_noreader),
    ('M15-widen-to-whole-no-reader-set', m_widen_noreader),
    ('M16-widen-to-squashfs_v*', m_widen_vstar),
    ('M17-widen-to-squashfs_v3*', m_widen_v3star),
    ('M18-unreadable-label-renamed', m_label_rename),
    ('M19-unreadable-action-none', m_action_none),
    ('M20-unreadable-handler-cell-blanked', m_blank_handler),
    ('M21-unreadable-action-cell-blanked', m_blank_action),
]


def classify(base_rows, fixtures):
    br, _ = P.parse(base_rows)
    bp = P.pairs(br, fixtures)
    rows = []
    for name, fn in MUT:
        r = [list(x) for x in base_rows]
        fn(r)
        try:
            rules, _ = P.parse(r)
        except Exception as exc:
            rows.append({'mutation': name, 'classification': 'PARSE-REFUSED',
                         'detail': str(exc)[:120]})
            continue
        mm, aa = P.score(rules, corpus, fixtures)
        p = P.pairs(rules, fixtures)
        flipped = sorted(n for n in bp if bp[n] != p.get(n))
        corpus_red = bool(mm or aa)
        fix_red = bool(flipped)
        cls = ('RED-CORPUS' if corpus_red else
               ('CORPUS-VACUOUS' if fix_red else 'NO-OP'))
        rows.append({'mutation': name, 'classification': cls,
                     'corpus_D1': len(mm), 'corpus_D2': len(aa),
                     'corpus_envelopes': [x['envelope'] for x in mm],
                     'audit_envelopes': [x['envelope'] for x in aa],
                     'fixtures_flipped': flipped})
    return rows


out = {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'design': 'A: legacy failing-handler cell drops squashfs_v3_ddwrt; '
              'legacy-body-unreadable row immediately below legacy-body-failure',
    'with_base_fixture_set': classify(P.V6_ROWS, base_fixtures),
    'with_extra_synthetic_fixtures': classify(P.V6_ROWS, extra_fixtures),
    'extra_fixtures_added': ['v3ddwrt-multigap'],
}
for scope in ('with_base_fixture_set', 'with_extra_synthetic_fixtures'):
    counts = {}
    for m in out[scope]:
        counts[m['classification']] = counts.get(m['classification'], 0) + 1
    out[scope + '_counts'] = counts

with open(OUT, 'w', encoding='utf-8') as fh:
    json.dump(out, fh, indent=1, sort_keys=True)
    fh.write('\n')

for scope in ('with_base_fixture_set', 'with_extra_synthetic_fixtures'):
    print('==', scope, out[scope + '_counts'])
    for m in out[scope]:
        print('   %-48s %-16s corpusD1=%-4s corpusD2=%-4s fix=%s' % (
            m['mutation'], m['classification'], m.get('corpus_D1'), m.get('corpus_D2'),
            m.get('fixtures_flipped')))
print('wrote', OUT)
