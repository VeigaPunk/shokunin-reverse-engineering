#!/usr/bin/env python3
"""label_v4.py -- a transcription of the round-42 DRAFT label precedence
(plans/round-42-claims.md R42-C2 "Draft label precedence", steps 1-13).

Independent of the lane's tools: it reads only REA envelopes and the draft text.
Not the freeze evaluator (tools/round-42/indep-eval-v4.py does not exist yet);
this exists so wave 1 can say, per envelope, what the draft text implies.
"""
import argparse
import json
import re
import sys

V123 = re.compile(r'^squashfs_v[123]')


def features(data):
    n = data.get('normalized_result') or {}
    op = data.get('operation')
    prov = data.get('provider')
    pr = prov.get('id') if isinstance(prov, dict) else prov
    chunks = n.get('chunks') or []
    gaps = n.get('extraction_gaps') or []
    H = sorted({c.get('handler') for c in chunks if c.get('handler')} |
               {g.get('handler') for g in gaps if g.get('handler')})
    G = sorted({g.get('kind') for g in gaps if g.get('kind')})
    D = sorted({x for g in gaps for x in (g.get('dependencies') or [])})
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
    failing = [c.get('handler') for c in chunks if c.get('extraction_failed') and c.get('handler')]
    failing += [g.get('handler') for g in gaps if g.get('kind') == 'extractor-failure' and g.get('handler')]
    return dict(OP=op, PR=pr, H=H, G=G, D=D, BE=be, SR=sr, P=P,
                F=sorted(h for h in H if h.startswith('squashfs_')),
                failing=sorted(set(failing)))


def label(f):
    OP, PR, H, G, D, BE, SR, P, F = (f['OP'], f['PR'], f['H'], f['G'], f['D'],
                                     f['BE'], f['SR'], f['P'], f['F'])
    if OP != 'extract_firmware' or PR != 'unblob':
        return 1, ('unclassified', 'none')
    if not F:
        return 2, ('no-squashfs-chunk', 'inspect-input')
    if 'missing-extractor-dependency' in G:
        if 'sasquatch-v4be' in D:
            return 3, ('dep-missing-be', 'install-extractor-be')
        if 'sasquatch' in D:
            return 3, ('dep-missing-le', 'install-extractor-le')
    if 'extractor-failure' in G and P > 0:
        return 4, ('partial-body-failure', 'salvage-partial')
    if 'extractor-failure' in G and P == 0 and BE == 'no':
        if f['failing'] == ['squashfs_v4_be'] or 'squashfs_v4_be' in f['failing']:
            return 5, ('avm-marker-be-dropped', 'wrap-extractor-be')
        if any(V123.match(h) for h in f['failing']):
            return 6, ('legacy-body-failure', 'cross-read-legacy')
    if 'extractor-failure' in G and P == 0:
        return 7, ('body-extractor-failure', 'preserve-failure')
    if 'depth-limited' in G:
        return 8, ('depth-limited', 'raise-depth')
    if SR == 'yes' and 'unpublished-entry' in G:
        return 9, ('mixed-symlinks', 'audit-symlinks')
    if SR == 'yes' and not G:
        return 10, ('escaping-symlink-removed', 'expect-link-absent')
    if set(G) == {'unpublished-entry'}:
        return 11, ('in-tree-symlink-metadata', 'count-gap')
    if not G:
        if P > 0:
            return 12, ('clean', 'none')
        return 12, ('clean-empty', 'confirm-empty')
    return 13, ('unclassified', 'none')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', action='store_true')
    ap.add_argument('envelopes', nargs='+')
    a = ap.parse_args()
    for p in a.envelopes:
        e = json.load(open(p))
        if not e.get('ok') or not isinstance(e.get('data'), dict):
            print(json.dumps({'envelope': p, 'ok': e.get('ok'), 'error': e.get('error')}))
            continue
        f = features(e['data'])
        step, pair = label(f)
        print(json.dumps({'envelope': p, 'step': step, 'pair': pair,
                          'features': {k: f[k] for k in ('OP', 'PR', 'H', 'G', 'D', 'BE', 'SR', 'P', 'F', 'failing')}}))


if __name__ == '__main__':
    main()
