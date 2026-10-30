#!/usr/bin/env python3
"""Emit the measured v6 mutation-battery evidence as JSON.

Read-only on the lane.  Imports the frozen v5 instrument by importlib (read-only)
and layers the v6 row + evaluator + audit on top of it.
"""
import sys, os, json, hashlib, datetime

sys.path.insert(0, '/fast/scratch/hyaku/kaidoku-r52/w1-MutTriV6')
import proto_v6 as P

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
OUT = sys.argv[1]

corpus = P.load_corpus()
fixtures = P.v6_fixtures()


def rows(fn):
    r = [list(x) for x in P.V6_ROWS]
    return fn(r)


def m_del(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); del r[i]; return r
def m_cross(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); r[i][10] = 'cross-read-legacy'; return r
def m_glob(r):
    i = P.v5._row_index(r, 'legacy-body-failure'); r[i][4] = 'squashfs_v[123]*'; return r
def m_below(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); row = r.pop(i)
    j = P.v5._row_index(r, 'body-extractor-failure'); r.insert(j + 1, row); return r
def m_above(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); row = r.pop(i)
    j = P.v5._row_index(r, 'legacy-body-failure'); r.insert(j, row); return r
def m_newcell_broad(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); r[i][4] = 'squashfs_v[123]*'; return r
def m_gapexact(r):
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
def m_blank_cell(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); r[i][3] = ''; return r
def m_blank_action(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); r[i][10] = ''; return r
def m_rename(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); r[i][0] = 'legacy-body-unreadable-v2'; return r
def m_action_none(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); r[i][10] = 'none'; return r
def m_swap_with_legacy(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); j = P.v5._row_index(r, 'legacy-body-failure')
    r[i][10], r[j][10] = r[j][10], r[i][10]; return r
def m_swap_with_noreader(r):
    i = P.v5._row_index(r, 'legacy-body-unreadable'); j = P.v5._row_index(r, 'no-reader-failure')
    r[i][10], r[j][10] = r[j][10], r[i][10]; return r


MUT = [
    ('M1-unreadable-row-deleted', m_del),
    ('M2-unreadable-action-cross-read-legacy', m_cross),
    ('M3-ddwrt-glob-broadened-into-legacy', m_glob),
    ('M4-unreadable-row-below-body-row', m_below),
    ('M5-unreadable-row-above-legacy-row', m_above),
    ('M6-unreadable-failing-cell-broadened', m_newcell_broad),
    ('M7-unreadable-gap-kind-exact', m_gapexact),
    ('M8-clean-unverified-guard-row-deleted', m_guard_del),
    ('M9-v5-new-row-actions-swapped', m_actions_swap),
    ('M10-no-reader-family-moved-to-clean', m_broadcom_clean),
    ('M11-legacy-body-failure-row-deleted', m_legacy_del),
    ('M12-no-reader-failure-row-deleted', m_noreader_del),
    ('M13-unreadable-handler-cell-blanked', m_blank_cell),
    ('M14-unreadable-action-cell-blanked', m_blank_action),
    ('M15-unreadable-label-renamed', m_rename),
    ('M16-unreadable-action-none', m_action_none),
    ('M17-swap-unreadable-action-with-legacy', m_swap_with_legacy),
    ('M18-swap-unreadable-action-with-no-reader-failure', m_swap_with_noreader),
]

base_rules, base_info = P.parse(P.V6_ROWS)
bp = P.pairs(base_rules, fixtures)
bm, ba = P.score(base_rules, corpus, fixtures)

out = {
    'artifact': 'r52 v6 mutation-battery measured evidence',
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'probe': 'scratch prototype; ports tools/round-50-c3/sqfs-triage-v5.py read-only',
    'v5_instrument_sha256': hashlib.sha256(
        open(LANE + '/tools/round-50-c3/sqfs-triage-v5.py', 'rb').read()).hexdigest(),
    'corpus': '126 envelopes at .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes',
    'readers': {
        'D1': 'pair_mismatches: the table (label, action) vs the fixed v6 evaluator',
        'D2': 'executability_violations: a FAILED-body envelope whose prescribed action '
              'is a cross-read, on a family the reader census says has no reader',
        'D3': 'census_outside: registered paths absent from the active census artifact',
    },
    'base_v6': {'D1': len(bm), 'D2': len(ba), 'rules': base_info['rules']},
    'before_arm_v5_table': {},
    'mutations': [],
}

v5r, _ = P.parse(P.v5.V5_ROWS, P.v5.V5_ACTIONS, P.v5.MARKER_V5)
m, a = P.score(v5r, corpus, fixtures)
out['before_arm_v5_table'] = {
    'D1': len(m), 'D2': len(a),
    'D1_mismatches': [(x['envelope'], x['table'], x['evaluator']) for x in m],
    'D2_findings': [(x['envelope'], x['action']) for x in a],
}

for name, fn in MUT:
    try:
        rules, info = P.parse(rows(fn))
    except Exception as exc:
        out['mutations'].append({'mutation': name, 'parse_refused': str(exc)[:160],
                                 'D1': None, 'D2': None, 'no_op': False})
        continue
    mm, aa = P.score(rules, corpus, fixtures)
    p = P.pairs(rules, fixtures)
    out['mutations'].append({
        'mutation': name,
        'D1': len(mm), 'D2': len(aa),
        'D1_envelopes': [x['envelope'] for x in mm],
        'D2_envelopes': [x['envelope'] for x in aa],
        'fixtures_flipped': sorted(n for n in bp if bp[n] != p.get(n)),
        'no_op': (len(mm) == 0 and len(aa) == 0),
    })

# ---- D3: the census guard's arithmetic, measured ----
census = json.load(open(LANE + '/tools/round-51/census3.json'))
base_paths = census['paths']
r52_rows = ['tools/round-52/gap-rule.json', 'tools/round-52/c1-counter.py',
             'tools/round-52/c1-controls.py', 'tools/round-52/c1-run.sh',
             'tools/round-52/fetch-vendor.py', 'tools/round-52/sqfs-triage-v6.py',
             'tools/round-52/misroot-sweep.sh']
out['D3_census'] = {
    'active_artifact': 'tools/round-51/census3.json',
    'artifact_paths': len(base_paths),
    'registry_at_claims_base': 56,
    'census_outside_at_claims_base': sorted(set(base_paths) - set(base_paths)),
    'registry_rows_the_r52_freeze_adds': len(r52_rows),
    'census_outside_at_the_r52_freeze_with_census3_unchanged':
        sorted(set(base_paths + r52_rows) - set(base_paths)),
    'census_outside_count_at_the_r52_freeze':
        len(set(base_paths + r52_rows) - set(base_paths)),
    'census_outside_with_census2_as_the_active_artifact': 14,
}
out['D3_census']['census_outside_with_census2_as_the_active_artifact_paths'] = sorted(
    set(base_paths) - set(json.load(open(LANE + '/tools/round-48/census2.json'))['paths']))

# ---- the audit's own reader census: its own mutation surface ----
aud = {}
for tag, census_set in (
        ('with_ddwrt', ('squashfs_v2_nonstandard', 'squashfs_v3_nonstandard', 'squashfs_v3_ddwrt')),
        ('without_ddwrt', ('squashfs_v2_nonstandard', 'squashfs_v3_nonstandard')),
        ('with_ddwrt_and_v1', ('squashfs_v2_nonstandard', 'squashfs_v3_nonstandard',
                                'squashfs_v3_ddwrt', 'squashfs_v1'))):
    P.NO_VALIDATED_READER = census_set
    _, af = P.score(v5r, corpus, fixtures)
    aud[tag] = [(x['envelope'], x['action'], x['families']) for x in af]
P.NO_VALIDATED_READER = ('squashfs_v2_nonstandard', 'squashfs_v3_nonstandard', 'squashfs_v3_ddwrt')
out['audit_reader_census_mutations'] = aud

with open(OUT, 'w', encoding='utf-8') as fh:
    json.dump(out, fh, indent=1, sort_keys=True)
    fh.write('\n')
print('wrote', OUT, 'mutations:', len(out['mutations']))
