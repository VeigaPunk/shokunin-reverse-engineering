import json, os, re
REF='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-40/c1'
def same_rel(c,r): return bool(c) and bool(r) and (c==r or c.endswith('/'+r))
def tsv(p):
    return [l.rstrip('\n').split('\t') for l in open(p) if l.strip()]
out={}
for cid in ('V1','V2','L1','L2'):
    d=json.load(open(os.path.join(REF,cid,'after.json')))
    nr=d.get('normalized_result') or {}
    files=[(f.get('relative_path'),f.get('sha256'),f.get('size')) for f in nr.get('files') or []]
    gaps=nr.get('extraction_gaps') or []
    oracle=[(r[0],r[1],int(r[2])) for r in tsv(os.path.join(REF,cid,'oracle.tsv'))]
    nonreg=[(r[0],r[1],r[2] if len(r)>2 else '') for r in tsv(os.path.join(REF,cid,'nonregular.tsv'))]
    missing=[o for o in oracle if not any(o[1]==f[1] and same_rel(f[0],o[0]) for f in files)]
    exact_sym=[]; suffix_sym=[]
    for fp,fsha,_ in files:
        for rel,kind,_t in nonreg:
            if same_rel(fp,rel):
                (exact_sym if fp==rel else suffix_sym).append((fp,rel,kind))
    gapkinds={}
    for g in gaps: gapkinds[g.get('kind')]=gapkinds.get(g.get('kind'),0)+1
    syms=sum(1 for r in nonreg if r[1]=='symlink')
    out[cid]=dict(published=len(files), oracle=len(oracle), oracle_missing=missing[:5],
                  oracle_missing_n=len(missing),
                  symlink_gaps=sum(1 for g in gaps if g.get('kind')=='unpublished-entry' and g.get('relative_path') and any(same_rel(g['relative_path'],r[0]) and r[1]=='symlink' for r in nonreg)),
                  gaps=gapkinds, symlinks=syms,
                  # every gap must name exactly one non-regular entry
                  gap_paths_resolved=[(g.get('relative_path'), [r[0] for r in nonreg if g.get('relative_path') and same_rel(g['relative_path'],r[0])]) for g in gaps],
                  exact_nonregular_hits=exact_sym, suffix_only_matches=suffix_sym,
                  chunk_handlers=[c.get('handler') for c in nr.get('chunks') or []],
                  chunk_failed=[c.get('handler') for c in nr.get('chunks') or [] if c.get('extraction_failed')],
                  evidence_id=d.get('evidence_id'), subject=(d.get('subject') or {}).get('sha256'),
                  params=(d.get('parameters') or {}).get('output_directory'))
print(json.dumps(out,indent=1))
