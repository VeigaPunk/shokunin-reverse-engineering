#!/usr/bin/env python3
"""R42C2Mutants -- private mutation-test harness for the A1 v4 precedence.

NOT a deliverable and not an oracle for any other seat: this is a
precedence-derived reference (transcribed only from plans/round-42-claims.md
amendment A1, steps 1-15) used to prove that each proposed v4 selftest case
kills its mutant and passes a correct implementation.  The v4 deliverables
remain tools/round-42/sqfs-triage-v4.py and indep-eval-v4.py (wave 2).

Usage: ref-v4.py --selftest   (ok/FAIL lines, exit 1 on any failure)
"""
import argparse
import fnmatch
import json
import sys

LEGACY_PATTERNS = ('squashfs_v1*', 'squashfs_v2*', 'squashfs_v3*')
SYMLINK_TYPENAME = 'MaliciousSymlinkRemoved'


def envelope_data(obj):
    if isinstance(obj, dict) and 'subject' not in obj and isinstance(obj.get('data'), dict):
        return obj['data']
    return obj


def features(d):
    nr = d.get('normalized_result') or {}
    chunks = nr.get('chunks') or []
    gaps = nr.get('extraction_gaps') or []
    # A1: H = chunk handlers + gap handlers (nulls dropped)
    H = []
    for c in chunks:
        h = c.get('handler')
        if isinstance(h, str):
            H.append(h)
    for g in gaps:
        h = g.get('handler')
        if isinstance(h, str):
            H.append(h)
    F = sorted({h for h in H if h.startswith('squashfs_')})
    L = sorted({h for h in F
                if any(fnmatch.fnmatchcase(h, p) for p in LEGACY_PATTERNS)})
    G = sorted({g.get('kind') for g in gaps if isinstance(g.get('kind'), str)})
    D = sorted({x for g in gaps for x in (g.get('dependencies') or [])})
    efh = sorted({g.get('handler') for g in gaps
                  if g.get('kind') == 'extractor-failure'
                  and isinstance(g.get('handler'), str)})
    HF = efh if efh else list(F)
    diags = nr.get('diagnostics') or []
    cmds = []
    for dg in diags:
        rep = dg.get('report') if isinstance(dg, dict) and isinstance(dg.get('report'), dict) \
            else (dg if isinstance(dg, dict) else None)
        if isinstance(rep, dict) and isinstance(rep.get('command'), str):
            cmds.append(rep['command'])
    if cmds:
        BE = 'yes' if any('-be' in c.split() for c in cmds) else 'no'
    else:
        BE = 'n/a'
    SR = any(isinstance(holder, dict) and holder.get('__typename__') == SYMLINK_TYPENAME
             for dg in diags if isinstance(dg, dict)
             for holder in (dg, dg.get('report') if isinstance(dg.get('report'), dict) else None))
    P = len(nr['files']) if isinstance(nr.get('files'), list) else 0
    return {'OP': d.get('operation'), 'PR': (d.get('provider') or {}).get('id'),
            'H': H, 'F': F, 'L': L, 'G': G, 'D': D, 'HF': HF, 'BE': BE,
            'SR': SR, 'P': P}


def classify(f):
    G = set(f['G'])
    D = set(f['D'])
    F = set(f['F'])
    L = set(f['L'])
    HF = set(f['HF'])
    if f['OP'] != 'extract_firmware' or f['PR'] != 'unblob':
        return ('unclassified', 'none')                                     # 1
    if not F and 'depth-limited' in G:
        return ('container-depth-limited', 'raise-depth')                   # 2
    if not F:
        return ('no-squashfs-chunk', 'inspect-input')                       # 3
    if 'missing-extractor-dependency' in G:
        if 'sasquatch-v4be' in D:
            return ('dep-missing-be', 'install-extractor-be')               # 4
        if 'sasquatch' in D:
            return ('dep-missing-le', 'install-extractor-le')               # 4
    if 'extractor-failure' in G and f['P'] > 0:
        return ('partial-body-failure', 'salvage-partial')                  # 5
    if 'extractor-failure' in G and f['P'] == 0 and f['BE'] == 'no' \
            and 'squashfs_v4_be' in HF:
        return ('avm-marker-be-dropped', 'wrap-extractor-be')               # 6
    if 'extractor-failure' in G and f['P'] == 0 and HF & L:
        return ('legacy-body-failure', 'cross-read-legacy')                 # 7
    if 'extractor-failure' in G and f['P'] == 0:
        return ('body-extractor-failure', 'preserve-failure')               # 8
    if 'unknown-chunk-handler' in G:
        return ('unknown-residue', 'isolate-residue')                       # 9
    if 'depth-limited' in G:
        return ('depth-limited', 'raise-depth')                             # 10
    if f['SR'] and 'unpublished-entry' in G:
        return ('mixed-symlinks', 'audit-symlinks')                         # 11
    if f['SR'] and not G:
        return ('escaping-symlink-removed', 'expect-link-absent')           # 12
    if G == {'unpublished-entry'}:
        return ('in-tree-symlink-metadata', 'count-gap')                    # 13
    if not G:
        return ('clean', 'none') if f['P'] > 0 \
            else ('clean-empty', 'confirm-empty')                           # 14
    return ('unclassified', 'none')                                         # 15


def run_env(env):
    return classify(features(envelope_data(env)))


def env(chunks=(), gaps=(), files=3, diags=(), op='extract_firmware', pr='unblob',
        drop_files=False, raw=None):
    nr = {'chunks': list(chunks), 'extraction_gaps': list(gaps),
          'diagnostics': list(diags)}
    if not drop_files:
        nr['files'] = [{'relative_path': 'f%02d' % i, 'size': 1}
                       for i in range(files)]
    d = {'operation': op, 'provider': {'id': pr}, 'normalized_result': nr}
    if raw is not None:
        d['raw_result'] = raw
    return d


V4_BE = {'handler': 'squashfs_v4_be', 'extraction_failed': False}
V4_LE = {'handler': 'squashfs_v4_le', 'extraction_failed': False}
V3_DD = {'handler': 'squashfs_v3_ddwrt', 'extraction_failed': False}
V3_LE = {'handler': 'squashfs_v3_le', 'extraction_failed': False}
TRX = {'handler': 'trx_v1'}
GZIP = {'handler': 'gzip'}
EF = {'kind': 'extractor-failure', 'dependencies': []}
EF_TRX = {'kind': 'extractor-failure', 'handler': 'trx_v1', 'dependencies': []}
EF_V3LE = {'kind': 'extractor-failure', 'handler': 'squashfs_v3_le',
           'dependencies': []}
DEP = lambda *names: {'kind': 'missing-extractor-dependency',
                      'dependencies': list(names)}  # noqa: E731
DEPTH = {'kind': 'depth-limited', 'dependencies': []}
UE = {'kind': 'unpublished-entry', 'dependencies': []}
UNK = {'kind': 'unknown-chunk-handler', 'dependencies': []}
CMD_NOBE = [{'report': {'command': 'sasquatch -no-exit-code -f -d /o /i'}}]
CMD_BE = [{'report': {'command': 'sasquatch-v4be -be -no-exit-code -f -d /o /i'}}]
CMD_BESUB = [{'report': {'command': 'sasquatch-v4be -be=1 -f -d /o /i'}}]
CMD_LE = [{'report': {'command': 'sasquatch -le -f -d /o /i'}}]
SR_DIAG = [{'report': {'command': 'x', '__typename__': SYMLINK_TYPENAME}}]
SR_DIAG_ONLY = [{'__typename__': SYMLINK_TYPENAME}]

PAIR_CASES = [
    ('s1-op', env(op='analyze'), ('unclassified', 'none')),
    ('s1b-provider', env(pr='binwalk'), ('unclassified', 'none')),
    ('s2-container-trx', env(chunks=[TRX], gaps=[DEPTH], files=3),
     ('container-depth-limited', 'raise-depth')),
    ('s2b-container-gzip', env(chunks=[GZIP], gaps=[DEPTH], files=2),
     ('container-depth-limited', 'raise-depth')),
    ('s3-no-squashfs', env(chunks=[GZIP], files=1),
     ('no-squashfs-chunk', 'inspect-input')),
    ('s4a-dep-be', env(chunks=[V4_LE], gaps=[DEP('sasquatch-v4be')]),
     ('dep-missing-be', 'install-extractor-be')),
    ('s4b-dep-le', env(chunks=[V4_LE], gaps=[DEP('sasquatch')]),
     ('dep-missing-le', 'install-extractor-le')),
    ('s4c-dep-membership-le', env(chunks=[V4_LE], gaps=[DEP('sasquatch', 'unsquashfs')]),
     ('dep-missing-le', 'install-extractor-le')),
    ('s4d-dep-membership-be', env(chunks=[V4_LE], gaps=[DEP('sasquatch-v4be', 'unsquashfs')]),
     ('dep-missing-be', 'install-extractor-be')),
    ('s4e-dep-plus-partial', env(chunks=[V4_BE], gaps=[DEP('sasquatch-v4be'), EF],
                                 files=3, diags=CMD_BE),
     ('dep-missing-be', 'install-extractor-be')),
    ('s5-partial', env(chunks=[V4_BE], gaps=[EF], files=2, diags=CMD_BE),
     ('partial-body-failure', 'salvage-partial')),
    ('s6-avm-marker', env(chunks=[V4_BE], gaps=[EF], files=0, diags=CMD_NOBE),
     ('avm-marker-be-dropped', 'wrap-extractor-be')),
    ('s6b-be-yes', env(chunks=[V4_BE], gaps=[EF], files=0, diags=CMD_BE),
     ('body-extractor-failure', 'preserve-failure')),
    ('s6d-no-argv-avm-blocked', env(chunks=[V4_BE], gaps=[EF], files=0),
     ('body-extractor-failure', 'preserve-failure')),
    ('s6c-hf-trx', env(chunks=[V4_BE], gaps=[EF_TRX], files=0, diags=CMD_NOBE),
     ('body-extractor-failure', 'preserve-failure')),
    ('s7-legacy-ddwrt', env(chunks=[V3_DD], gaps=[EF], files=0),
     ('legacy-body-failure', 'cross-read-legacy')),
    ('s7b-legacy-le', env(chunks=[V3_LE], gaps=[EF], files=0, diags=CMD_LE),
     ('legacy-body-failure', 'cross-read-legacy')),
    ('s7c-legacy-gap-handler', env(chunks=[], gaps=[EF_V3LE], files=0),
     ('legacy-body-failure', 'cross-read-legacy')),
    ('s8-v4le-body', env(chunks=[V4_LE], gaps=[EF], files=0, diags=CMD_NOBE),
     ('body-extractor-failure', 'preserve-failure')),
    ('s9-residue-plus-depth', env(chunks=[V4_BE], gaps=[UNK, DEPTH], files=2),
     ('unknown-residue', 'isolate-residue')),
    ('s9b-residue-only', env(chunks=[V4_BE], gaps=[UNK], files=1),
     ('unknown-residue', 'isolate-residue')),
    ('s10-depth', env(chunks=[V4_BE], gaps=[DEPTH], files=2),
     ('depth-limited', 'raise-depth')),
    ('s11-mixed', env(chunks=[V4_BE], gaps=[UE], diags=SR_DIAG),
     ('mixed-symlinks', 'audit-symlinks')),
    ('s12-escaping', env(chunks=[V4_BE], diags=SR_DIAG),
     ('escaping-symlink-removed', 'expect-link-absent')),
    ('s12b-diag-level-holder', env(chunks=[V4_BE], diags=SR_DIAG_ONLY),
     ('escaping-symlink-removed', 'expect-link-absent')),
    ('s12c-stdout-only-sr', env(chunks=[V4_BE],
                                raw={'execution': {'stdout': {'text': SYMLINK_TYPENAME}}}),
     ('clean', 'none')),
    ('s13-in-tree', env(chunks=[V4_BE], gaps=[UE]),
     ('in-tree-symlink-metadata', 'count-gap')),
    ('s14-clean', env(chunks=[V4_BE], files=5), ('clean', 'none')),
    ('s14b-clean-empty', env(chunks=[V4_BE], files=0),
     ('clean-empty', 'confirm-empty')),
    ('s14c-files-absent', env(chunks=[V4_BE], drop_files=True),
     ('clean-empty', 'confirm-empty')),
    ('s15-unclassified', env(chunks=[V4_BE], gaps=[DEP('zstd')]),
     ('unclassified', 'none')),
]

FEATURE_CASES = [
    ('f-p-counts-every-file', env(files=5), 'P', 5),
    ('f-p-absent-is-zero', env(drop_files=True), 'P', 0),
    ('f-be-token-not-substring', env(diags=CMD_BESUB), 'BE', 'no'),
    ('f-be-none-recorded', env(), 'BE', 'n/a'),
    ('f-h-includes-gap-handlers', env(gaps=[EF_V3LE]), 'F', ['squashfs_v3_le']),
    ('f-legacy-family-glob', env(chunks=[{'handler': 'squashfs_v3_broadcom'}]),
     'L', ['squashfs_v3_broadcom']),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--envelopes')
    ap.add_argument('envs', nargs='*')
    a = ap.parse_args()
    if a.selftest:
        bad = 0
        for name, e, want in PAIR_CASES:
            got = run_env(e)
            if got != want:
                bad += 1
                print('FAIL %s: got %r want %r' % (name, got, want))
            else:
                print('ok %s' % name)
        for name, e, key, want in FEATURE_CASES:
            got = features(envelope_data(e)).get(key)
            if got != want:
                bad += 1
                print('FAIL %s: got %r want %r' % (name, got, want))
            else:
                print('ok %s' % name)
        print('REF-SELFTEST cases=%d fail=%d' % (len(PAIR_CASES) + len(FEATURE_CASES), bad))
        return 1 if bad else 0
    paths = list(a.envs)
    if not paths and a.envelopes:
        import os
        paths = [os.path.join(a.envelopes, n) for n in sorted(os.listdir(a.envelopes))
                 if n.endswith('.json')]
    for p in paths:
        with open(p, encoding='utf-8') as fh:
            d = json.load(fh)
        print('%s\t%s\t%s' % (p, *run_env(d)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
