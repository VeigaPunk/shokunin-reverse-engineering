#!/usr/bin/env python3
"""Static model of unblob 26.6.4 extractor.fix_symlink over the oracle's symlink table.
A symlink is 'removal-candidate' when resolving it (relative: path.resolve(); absolute: outdir/lstrip(target).resolve())
traverses at least one *absolute-target* symlink hop that unblob has not yet rewritten (a not-yet-fixed absolute link is
followed on the HOST root by Path.resolve(), landing outside outdir -> is_safe_path False -> MaliciousSymlinkRemoved),
or a lexical escape (..) above the root, or a loop.
usage: static-candidates.py NONREG.tsv OUT.json [OBSERVED_UNION.json]"""
import sys, json, posixpath, collections
rows=[l.rstrip('\n').split('\t') for l in open(sys.argv[1]) if l.strip()]
links={r[0]:(r[2] if len(r)>2 else '') for r in rows if r[1]=='symlink'}
dirs={r[0] for r in rows if r[1]=='dir'}
def resolve(start_dir, target, hops, depth=0):
    """lexical resolve of target relative to start_dir (image-relative, '' = root). Returns final path or None if escapes/loop."""
    if depth>40: return None
    parts=[]
    base=[] if target.startswith('/') else [p for p in start_dir.split('/') if p]
    comps=base+[p for p in target.split('/') if p]
    out=[]
    i=0; queue=list(comps)
    while queue:
        c=queue.pop(0)
        if c=='.': continue
        if c=='..':
            if not out: return None
            out.pop(); continue
        out.append(c)
        p='/'.join(out)
        if p in links and (queue or True):
            # symlink hop (final or intermediate)
            hops.append(p)
            t=links[p]
            if t=='' : return None
            out.pop()
            r=resolve('/'.join(out), t, hops, depth+1) if not t.startswith('/') else resolve('', t, hops, depth+1)
            if r is None: return None
            out=[x for x in r.split('/') if x]
    return '/'.join(out)
cls=collections.Counter(); cand={}
for rel,t in links.items():
    hops=[]
    d=posixpath.dirname(rel)
    first_abs=t.startswith('/')
    fin=resolve(d,t,hops)
    # hops traversed beyond S itself
    abs_hops=[h for h in hops if links[h].startswith('/') and h!=rel]
    lexical_escape = fin is None and not hops
    kind=('absolute' if first_abs else 'relative')
    c='chain-via-absolute-hop' if abs_hops else ('escape-or-loop' if fin is None else 'direct')
    cls[(kind,c)]+=1
    if abs_hops or fin is None: cand[rel]=dict(target=t,hops=hops,abs_hops=abs_hops,final=fin)
print(dict(cls)); print('candidates',len(cand),'of',len(links))
res={'classes':{'%s/%s'%k:v for k,v in cls.items()},'n_links':len(links),'n_abs':sum(1 for t in links.values() if t.startswith('/')),'n_rel':sum(1 for t in links.values() if t and not t.startswith('/')),'n_empty':sum(1 for t in links.values() if t==''),'candidates':cand}
if len(sys.argv)>3:
    obs=set(json.load(open(sys.argv[3])))
    res['observed_union_subset_of_candidates']=obs<=set(cand); res['observed_union']=sorted(obs); res['outside']=sorted(obs-set(cand))
    print('observed union',len(obs),'subset of candidates:',obs<=set(cand),'outside:',sorted(obs-set(cand)))
json.dump(res,open(sys.argv[2],'w'),indent=1)
