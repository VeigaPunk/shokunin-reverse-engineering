#!/usr/bin/env python3
"""MutTriV6 probe C - the v6 BEFORE-ARM expectation, measured on the base table.

Reads SKILL.md at the declared base (git show, read-only) and scores it with the v6
evaluator + the v6 executability audit over the 126 frozen envelopes.  This is the
before-arm the R51-C2 claim asserts: exit 1, executability_violations 1 naming
dmg_Z3_v3ddwrt_inode_table, census_outside 13.
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
V5 = os.path.join(LANE, 'tools/round-50-c3/sqfs-triage-v5.py')
ENV = os.path.join(LANE, '.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes')
OUTDIR = os.environ.get('PROBE_OUT', '/fast/scratch/hyaku/kaidoku-r51/w1-MutTriV6/out')
BASES = ['1aa273694f4409d3432fbcd73e83a33bee0dd8e9',
         'f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab']
REG_OPEN = '<!-- instrument-registry v2 -->'
REG_CLOSE = '<!-- /instrument-registry -->'


def load_v5():
    spec = importlib.util.spec_from_file_location('v5', V5)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git_show(rev, path):
    p = subprocess.run(['git', '-C', LANE, 'show', '%s:%s' % (rev, path)],
                       capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else None


def reg_paths(text):
    o = text.find(REG_OPEN)
    c = text.find(REG_CLOSE)
    out = []
    for line in text[o:c].split('\n'):
        s = line.strip()
        if not s.startswith('|'):
            continue
        cells = [x.strip().strip('`') for x in s.strip('|').split('|')]
        if cells and cells[0].startswith('tools/'):
            out.append(cells[0])
    return out


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    v5 = load_v5()
    entries = v5.envelope_entries(ENV)
    ddwrt = frozenset(('squashfs_v3_ddwrt',))
    base_eval = v5.evaluate

    def evaluate_v6(feat):
        g = set(feat['G'])
        if ('extractor-failure' in g and feat['P'] == 0
                and v5._meets(set(feat['HF']), ddwrt)):
            return 'legacy-body-unreadable', 'preserve-unresolved', 7
        return base_eval(feat)

    NO_READER = ('dmg_Z3_v3ddwrt_inode_table',)
    report = {'probe': 'MutTriV6 probe C - v6 before-arm on the base table',
              'utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
              'bases': []}
    for rev in BASES:
        text = git_show(rev, 'SKILL.md')
        rules, info = v5.parse_skill(text)
        mm5, mm6, av = [], [], []
        for eid, path in entries:
            feat = v5.load_envelope(path)
            tl, ta = v5.decision(v5.classify(rules, feat))
            el5, ea5, _ = base_eval(feat)
            el6, ea6, _ = evaluate_v6(feat)
            if tl != el5 or ta != ea5:
                mm5.append(eid)
            if tl != el6 or ta != ea6:
                mm6.append({'envelope': eid, 'table': [tl, ta], 'v6': [el6, ea6]})
            if ('extractor-failure' in set(feat['G']) and feat['P'] == 0
                    and ta == 'cross-read-legacy' and eid in NO_READER):
                av.append(eid)
        census = json.loads(git_show(rev, 'tools/round-48/census2.json'))
        rp = reg_paths(text)
        outside = sorted(set(rp) - set(census['paths']))
        report['bases'].append({
            'rev': rev,
            'skill_sha256': hashlib.sha256(text.encode('utf-8')).hexdigest(),
            'table_version': info['version'], 'rules': info['rules'],
            'v5_evaluator_pair_mismatches': len(mm5),
            'v6_evaluator_pair_mismatches': len(mm6),
            'v6_mismatch_detail': mm6,
            'v6_audit_violations': len(av), 'v6_audit_violation_ids': av,
            'registry_paths': len(rp), 'census2_paths': len(census['paths']),
            'census_outside': len(outside), 'census_outside_paths': outside,
        })
    out = os.path.join(OUTDIR, 'probe-v6-before-arm.json')
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(report, fh, indent=1, sort_keys=True)
        fh.write('\n')
    for b in report['bases']:
        print(json.dumps({k: v for k, v in b.items()
                          if k not in ('census_outside_paths', 'v6_mismatch_detail')},
                         sort_keys=True))
    print('json: %s' % out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
