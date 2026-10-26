#!/usr/bin/env python3
"""Draft R42-C2 label precedence (steps 1-13 of plans/round-42-claims.md) applied to envelopes."""
import json, sys, os
sys.path.insert(0, '/fast/scratch/hyaku/kaidoku-r42/R42C2ReconCombo')

V1_3 = ('squashfs_v1','squashfs_v2','squashfs_v2_nonstandard','squashfs_v3','squashfs_v3_ddwrt','squashfs_v3_broadcom','squashfs_v3_nonstandard')
SQUASH_PREFIX = 'squashfs_'

def feats(doc):
    data = doc.get('data') or doc
    nr = data.get('normalized_result') or {}
    op = data.get('operation'); pr = (data.get('provider') or {}).get('id')
    H=[]; G=set(); D=set(); argv=[]; sr=False
    for c in (nr.get('chunks') or []):
        if isinstance(c,dict) and c.get('handler'): H.append(c['handler'])
    for g in (nr.get('extraction_gaps') or []):
        if not isinstance(g,dict): continue
        if g.get('handler'): H.append(g['handler'])
        if g.get('kind'): G.add(g['kind'])
        for dep in (g.get('dependencies') or []): D.add(dep)
    for d in (nr.get('diagnostics') or []):
        if not isinstance(d,dict): continue
        r=d.get('report') or {}
        if r.get('__typename__')=='MaliciousSymlinkRemoved': sr=True
        cmd=r.get('command')
        if isinstance(cmd,str): argv.append(cmd)
        elif isinstance(cmd,list): argv.extend(str(t) for t in cmd)
    BE = 'yes' if any('-be' in a for a in argv) else ('no' if argv else 'n/a')
    P = len(nr.get('files') or [])
    return dict(OP=op, PR=pr, H=sorted(set(H)), G=sorted(G), D=sorted(D), BE=BE, SR=sr, P=P)

def label(f):
    F = {h for h in f['H'] if h.startswith(SQUASH_PREFIX)}
    if f['OP'] != 'extract_firmware' or f['PR'] != 'unblob':
        return ('unclassified','none',1)
    if not F:
        return ('no-squashfs-chunk','inspect-input',2)
    if 'missing-extractor-dependency' in f['G']:
        if 'sasquatch-v4be' in f['D']:
            return ('dep-missing-be','install-extractor-be',3)
        if 'sasquatch' in f['D']:
            return ('dep-missing-le','install-extractor-le',3)
    if 'extractor-failure' in f['G'] and f['P'] > 0:
        return ('partial-body-failure','salvage-partial',4)
    if 'extractor-failure' in f['G'] and f['P'] == 0 and f['BE'] == 'no' and 'squashfs_v4_be' in F:
        return ('avm-marker-be-dropped','wrap-extractor-be',5)
    failing = [h for h in f['H'] if h.startswith('squashfs_')]
    if 'extractor-failure' in f['G'] and f['P'] == 0 and any(h in V1_3 for h in failing):
        return ('legacy-body-failure','cross-read-legacy',6)
    if 'extractor-failure' in f['G'] and f['P'] == 0:
        return ('body-extractor-failure','preserve-failure',7)
    if 'depth-limited' in f['G']:
        return ('depth-limited','raise-depth',8)
    if f['SR'] and 'unpublished-entry' in f['G']:
        return ('mixed-symlinks','audit-symlinks',9)
    if f['SR'] and not f['G']:
        return ('escaping-symlink-removed','expect-link-absent',10)
    if set(f['G']) == {'unpublished-entry'}:
        return ('in-tree-symlink-metadata','count-gap',11)
    if not f['G']:
        return ('clean','none',12) if f['P'] > 0 else ('clean-empty','confirm-empty',12)
    return ('unclassified','none',13)

def main():
    paths = sys.argv[1:]
    for p in paths:
        doc = json.load(open(p))
        f = feats(doc)
        lbl = label(f)
        print(f"{os.path.basename(os.path.dirname(p))}: {json.dumps(f, sort_keys=True)} -> {lbl[0]}/{lbl[1]} (step {lbl[2]})")

if __name__ == '__main__':
    main()
