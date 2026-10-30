#!/usr/bin/env python3
"""MutTriV6 probe D - the PRECEDENCE CONSTRAINT on the v6 table.

The executability audit and the pair detector only see the ddwrt FAILED body if the
legacy-body-failure row is still ABOVE the new legacy-body-unreadable row.  This probe
measures the broadened-glob mutant under both placements so the constraint is measured,
not asserted.
"""
import importlib.util
import json
import os
import sys
from datetime import datetime, timezone

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
V5 = os.path.join(LANE, 'tools/round-50-c3/sqfs-triage-v5.py')
ENV = os.path.join(LANE, '.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes')
OUTDIR = os.environ.get('PROBE_OUT', '/fast/scratch/hyaku/kaidoku-r51/w1-MutTriV6/out')


def load_v5():
    spec = importlib.util.spec_from_file_location('v5', V5)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    v5 = load_v5()
    entries = v5.envelope_entries(ENV)
    ddwrt = frozenset(('squashfs_v3_ddwrt',))
    base_eval = v5.evaluate
    NO_READER = ('dmg_Z3_v3ddwrt_inode_table',)

    def evaluate_v6(feat):
        g = set(feat['G'])
        if ('extractor-failure' in g and feat['P'] == 0
                and v5._meets(set(feat['HF']), ddwrt)):
            return 'legacy-body-unreadable', 'preserve-unresolved', 7
        return base_eval(feat)

    NEW = ['legacy-body-unreadable', 'extract_firmware', 'unblob', 'squashfs_*',
           'squashfs_v3_ddwrt', 'extractor-failure+', '*', '*', '*', '0',
           'preserve-unresolved',
           'the failing chunk is a reader-backed v1-v3 body whose readers ALL refuse '
           '-> no second reader exists, so prescribe no cross-read: keep the failure '
           'unresolved',
           'R51-C2']

    def build(placement, broaden):
        rows = [list(r) for r in v5.V5_ROWS]
        i = [n for n, r in enumerate(rows) if r[0] == 'legacy-body-failure'][0]
        rows[i][4] = 'squashfs_v[123]*' if broaden else 'squashfs_v1,squashfs_v2,squashfs_v3'
        rows.insert(i if placement == 'before' else i + 1, list(NEW))
        return rows

    def score(rows):
        text = v5.render_table(rows, v5.V5_ACTIONS, v5.MARKER_V5)
        rules, _ = v5.parse_skill(text)
        pm, av = [], []
        for eid, path in entries:
            feat = v5.load_envelope(path)
            tl, ta = v5.decision(v5.classify(rules, feat))
            el, ea, _ = evaluate_v6(feat)
            if tl != el or ta != ea:
                pm.append(eid)
            if ('extractor-failure' in set(feat['G']) and feat['P'] == 0
                    and ta == 'cross-read-legacy' and eid in NO_READER):
                av.append(eid)
        return len(pm), pm, len(av), av

    report = {'probe': 'MutTriV6 probe D - the v6 table precedence constraint',
              'utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
              'cases': []}
    for placement in ('after', 'before'):
        for broaden in (False, True):
            pm_n, pm, av_n, av = score(build(placement, broaden))
            report['cases'].append({
                'unreadable_row_placement': placement,
                'legacy_glob_broadened': broaden,
                'pair_mismatches': pm_n, 'mismatch_envelopes': pm,
                'audit_violations': av_n, 'audit_violation_ids': av,
                'observed': 'RED (mutation detected)' if (pm_n or av_n) else 'GREEN (NO-OP)',
            })
    out = os.path.join(OUTDIR, 'probe-v6-precedence.json')
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(report, fh, indent=1, sort_keys=True)
        fh.write('\n')
    for c in report['cases']:
        print('%-8s broaden=%-5s pm=%-3d audit=%-3d %s'
              % (c['unreadable_row_placement'], c['legacy_glob_broadened'],
                 c['pair_mismatches'], c['audit_violations'], c['observed']))
    print('json: %s' % out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
