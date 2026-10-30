#!/usr/bin/env python3
"""MutTriV6 probe B - the FIXTURE-SCOPE expectations for the v6 selftest battery.

The v5 selftest asserts, for every committed mutation, the EXACT set of fixture pairs
it flips (`c_mutations_each_flip_their_own_pairs`).  Under v6 those sets change: the
ddwrt FAILED fixture now expects the new row, and the mutations that touch the legacy
row no longer move that fixture.  This probe MEASURES the v6 sets offline.

Read-only: tools/round-50-c3/sqfs-triage-v5.py (fixtures + parser + classifier).
"""
import hashlib
import importlib.util
import json
import os
import sys
from datetime import datetime, timezone

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
V5 = os.path.join(LANE, 'tools/round-50-c3/sqfs-triage-v5.py')
OUTDIR = os.environ.get('PROBE_OUT', '/fast/scratch/hyaku/kaidoku-r51/w1-MutTriV6/out')


def load_v5():
    spec = importlib.util.spec_from_file_location('v5', V5)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha256_file(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    v5 = load_v5()
    with open(os.path.join(LANE, 'tools/round-50-c3/sqfs-triage-v5.py'), 'rb') as fh:
        pass

    # ---------------- the v6 fixture set: v5's set with the ddwrt expectation moved
    FIX = []
    for name, env, want in v5.FIXTURES:
        if name == 'v3ddwrt-legacy':
            want = ('legacy-body-unreadable', 'preserve-unresolved')
        FIX.append((name, env, want))

    def pairs(rules):
        out = {}
        for name, env, _w in FIX:
            feat = v5.features(env)
            rule = v5.classify(rules, feat)
            out[name] = v5.decision(rule)
        return out

    def parse(rows):
        return v5.parse_skill(v5.SKELETON.format(block=v5._render(rows, v5.V5_ACTIONS,
                                                                   v5.MARKER_V5)))

    # the v6 table
    rows = [list(r) for r in v5.V5_ROWS]
    i = [n for n, r in enumerate(rows) if r[0] == 'legacy-body-failure'][0]
    rows[i][4] = 'squashfs_v1,squashfs_v2,squashfs_v3'
    rows.insert(i + 1, ['legacy-body-unreadable', 'extract_firmware', 'unblob',
                        'squashfs_*', 'squashfs_v3_ddwrt', 'extractor-failure+', '*',
                        '*', '*', '0', 'preserve-unresolved',
                        'the failing chunk is a reader-backed v1-v3 body whose readers '
                        'ALL refuse -> no second reader exists, so prescribe no '
                        'cross-read: keep the failure unresolved',
                        'R51-C2; round-51 plans/round-51-claims.md R51-C2'])
    base = rows

    def row_index(rs, label):
        return [n for n, r in enumerate(rs) if r[0] == label][0]

    def m_delete(rows, label):
        out = [list(r) for r in rows]
        del out[row_index(out, label)]
        return out

    def m_widen_legacy(rows):
        out = [list(r) for r in rows]
        out[row_index(out, 'legacy-body-failure')][4] = 'squashfs_v[123]*'
        return out

    def m_swap_unreadable_action(rows):
        out = [list(r) for r in rows]
        out[row_index(out, 'legacy-body-unreadable')][10] = 'cross-read-legacy'
        return out

    def m_swap_new_row_actions(rows):
        out = [list(r) for r in rows]
        i = row_index(out, 'clean-unverified')
        j = row_index(out, 'no-reader-failure')
        out[i][10], out[j][10] = out[j][10], out[i][10]
        return out

    def m_no_reader_family_to_clean(rows):
        out = [list(r) for r in rows]
        i = row_index(out, 'clean-unverified')
        parts = [p for p in out[i][3].split(',') if p != 'squashfs_v3_broadcom']
        out[i][3] = ','.join(parts)
        return out

    def m_precedence_swapped(rows):
        out = [list(r) for r in rows]
        i = row_index(out, 'clean-unverified')
        row = out.pop(i)
        j = row_index(out, 'clean')
        out.insert(j + 1, row)
        return out

    def m_no_reader_failure_deleted(rows):
        return m_delete(rows, 'no-reader-failure')

    def m_legacy_deleted(rows):
        return m_delete(rows, 'legacy-body-failure')

    def m_unreadable_deleted(rows):
        return m_delete(rows, 'legacy-body-unreadable')

    MUT = [
        ('guard-row-deleted', m_delete(base, 'clean-unverified')),
        ('legacy-glob-widened', m_widen_legacy(base)),
        ('unreadable-action-swapped', m_swap_unreadable_action(base)),
        ('unreadable-row-deleted', m_unreadable_deleted(base)),
        ('new-row-actions-swapped', m_swap_new_row_actions(base)),
        ('no-reader-family-moved-to-clean', m_no_reader_family_to_clean(base)),
        ('precedence-order-swapped', m_precedence_swapped(base)),
        ('no-reader-failure-row-deleted', m_no_reader_failure_deleted(base)),
        ('legacy-row-deleted', m_legacy_deleted(base)),
    ]

    base_rules, _ = parse(base)
    base_pairs = pairs(base_rules)
    report = {
        'probe': 'MutTriV6 probe B - v6 fixture-scope mutation expectations',
        'utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'v5_sha256': sha256_file(V5),
        'v6_fixture_expectations': {n: list(w) for n, _e, w in FIX},
        'v6_fixture_pairs': {n: list(p) for n, p in base_pairs.items()},
        'v6_fixture_wrong': {n: (list(base_pairs[n]), list(w))
                             for n, _e, w in FIX if base_pairs[n] != w},
        'mutants': [],
    }
    for name, rows in MUT:
        rules, _info = parse(rows)
        other = pairs(rules)
        flipped = {n for n in base_pairs if base_pairs[n] != other.get(n)}
        report['mutants'].append({'mutant': name, 'flipped_fixtures': sorted(flipped),
                                  'n_flipped': len(flipped)})
    out = os.path.join(OUTDIR, 'probe-v6-fixtures.json')
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(report, fh, indent=1, sort_keys=True)
        fh.write('\n')
    print(json.dumps(report, indent=1, sort_keys=True))
    print('json: %s' % out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
