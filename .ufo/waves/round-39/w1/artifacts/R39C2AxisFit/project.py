#!/usr/bin/env python3
"""Typed feature projection of the 12 dev envelopes; the table the C2 triage could read."""
import json, sys, glob, os
def row(path):
    d=json.load(open(path)); data=d['data']; nr=data['normalized_result']
    diags=nr.get('diagnostics') or []
    cmds=[(x.get('report') or {}).get('command') for x in diags]
    return dict(dev=os.path.basename(path)[4:-5], ok=data and d.get('ok'),
        sel_len=nr['selection']['length'], files=len(nr.get('files') or []),
        chunks=len(nr.get('chunks') or []),
        failed=sum(1 for c in nr.get('chunks') or [] if c.get('extraction_failed')),
        handlers=sorted({c.get('handler') or 'null' for c in nr.get('chunks') or []}),
        gaps=sorted({g['kind'] for g in nr.get('extraction_gaps') or []}),
        deps=sorted({x for g in (nr.get('extraction_gaps') or []) for x in (g.get('dependencies') or [])}),
        diags=sorted({(x.get('report') or {}).get('__typename__') for x in diags}),
        beflag=sorted({'has-be' if c and ' -be ' in c else ('no-be' if c else 'none') for c in cmds}),
        unpub=sorted({u.get('kind') for u in (nr.get('unpublished_entries') or [])}),
        coverage=nr.get('coverage'), published=nr.get('published_bytes'),
        subject=nr['selection']['sha256'][:12])
rows=[row(p) for p in sorted(glob.glob(os.path.join(sys.argv[1] if len(sys.argv)>1 else '.', 'env-*.json')))]
hdr=list(rows[0])
print('\t'.join(hdr))
for r in rows: print('\t'.join(str(r[k]) for k in hdr))
