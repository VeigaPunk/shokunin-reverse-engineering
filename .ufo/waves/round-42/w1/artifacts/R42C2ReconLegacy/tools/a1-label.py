#!/usr/bin/env python3
"""a1-label.py -- transcription of the round-42 DRAFT label precedence, amendment A1
(plans/round-42-claims.md lines 66-136, 2026-10-26 ~22:20Z).

Independent of the lane's tools: reads REA envelopes only. Not the freeze evaluator;
this exists so wave 1 can state, per envelope, what the A1 text implies.

Features (A1): OP, PR, H, F, L, G, D, HF, BE, SR, P.
"""
import argparse
import json
import re
import sys

L_PAT = re.compile(r'^squashfs_(v1|v2|v3)')


def features(data):
    n = data.get('normalized_result') or {}
    op = data.get('operation')
    prov = data.get('provider')
    pr = prov.get('id') if isinstance(prov, dict) else prov
    chunks = n.get('chunks') or []
    gaps = n.get('extraction_gaps') or []
    H = sorted({c.get('handler') for c in chunks if c.get('handler')} |
               {g.get('handler') for g in gaps if g.get('handler')})
    F = sorted(h for h in H if h.startswith('squashfs_'))
    L = sorted(h for h in F if L_PAT.match(h))
    G = sorted({g.get('kind') for g in gaps if g.get('kind')})
    D = sorted({x for g in gaps for x in (g.get('dependencies') or [])})
    HF = sorted({g.get('handler') for g in gaps
                 if g.get('kind') == 'extractor-failure' and g.get('handler')})
    if not HF:
        HF = F
    argvs = []
    for x in n.get('diagnostics') or []:
        rep = x.get('report') or {}
        cmd = rep.get('command')
        if isinstance(cmd, list):
            argvs.append(cmd)
        elif isinstance(cmd, str):
            argvs.append(cmd.split())
    be = 'n/a' if not argvs else ('yes' if any('-be' in a for a in argvs) else 'no')
    sr = 'yes' if any('MaliciousSymlinkRemoved' in json.dumps(x) for x in (n.get('diagnostics') or [])) else 'no'
    P = len(n.get('files') or [])
    return dict(OP=op, PR=pr, H=H, F=F, L=L, G=G, D=D, HF=HF, BE=be, SR=sr, P=P)


def label(f):
    OP, PR = f['OP'], f['PR']
    F, L, G, D, HF = f['F'], f['L'], f['G'], f['D'], f['HF']
    BE, SR, P = f['BE'], f['SR'], f['P']
    if OP != 'extract_firmware' or PR != 'unblob':
        return 1, ('unclassified', 'none')
    if not F and 'depth-limited' in G:
        return 2, ('container-depth-limited', 'raise-depth')
    if not F:
        return 3, ('no-squashfs-chunk', 'inspect-input')
    if 'missing-extractor-dependency' in G:
        if 'sasquatch-v4be' in D:
            return 4, ('dep-missing-be', 'install-extractor-be')
        if 'sasquatch' in D:
            return 4, ('dep-missing-le', 'install-extractor-le')
    if 'extractor-failure' in G and P > 0:
        return 5, ('partial-body-failure', 'salvage-partial')
    if 'extractor-failure' in G and P == 0 and BE == 'no' and 'squashfs_v4_be' in HF:
        return 6, ('avm-marker-be-dropped', 'wrap-extractor-be')
    if 'extractor-failure' in G and P == 0 and set(HF) & set(L):
        return 7, ('legacy-body-failure', 'cross-read-legacy')
    if 'extractor-failure' in G and P == 0:
        return 8, ('body-extractor-failure', 'preserve-failure')
    if 'unknown-chunk-handler' in G:
        return 9, ('unknown-residue', 'isolate-residue')
    if 'depth-limited' in G:
        return 10, ('depth-limited', 'raise-depth')
    if SR == 'yes' and 'unpublished-entry' in G:
        return 11, ('mixed-symlinks', 'audit-symlinks')
    if SR == 'yes' and not G:
        return 12, ('escaping-symlink-removed', 'expect-link-absent')
    if set(G) == {'unpublished-entry'}:
        return 13, ('in-tree-symlink-metadata', 'count-gap')
    if not G:
        return 14, (('clean', 'none') if P > 0 else ('clean-empty', 'confirm-empty'))
    return 15, ('unclassified', 'none')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('envelopes', nargs='+')
    a = ap.parse_args()
    for p in a.envelopes:
        e = json.load(open(p))
        if not e.get('ok') or not isinstance(e.get('data'), dict):
            print(json.dumps({'envelope': p, 'ok': e.get('ok'), 'error': e.get('error')}))
            continue
        f = features(e['data'])
        step, pair = label(f)
        print(json.dumps({'envelope': p, 'step': step, 'pair': list(pair), 'features': f}))


if __name__ == '__main__':
    main()
