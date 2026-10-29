#!/usr/bin/env python3
"""Classify non-regular oracle entries per unblob rule and compare with an actual unblob extraction tree.
usage: classify.py NONREG.tsv EXTRACT_ROOT REPORT.json OUT.json"""
import sys, os, json, posixpath, stat, collections
nonreg, root, report, out = sys.argv[1:5]
rows=[l.rstrip('\n').split('\t') for l in open(nonreg) if l.strip()]
def classify_link(rel, tgt):
    """predict unblob fix_symlink outcome on the sasquatch-extracted tree"""
    if tgt=='' : return 'empty-target'
    if tgt.startswith('/'):
        # absolute: target = lstrip('/'), resolved inside outdir
        t=tgt.lstrip('/')
        p=posixpath.normpath(t)
        kind='absolute'
        escapes = p=='..' or p.startswith('../')
        return 'absolute-escaping' if escapes else 'absolute-inside'
    d=posixpath.dirname(rel)
    p=posixpath.normpath(posixpath.join(d,tgt))
    escapes = p=='..' or p.startswith('../')
    return 'relative-escaping' if escapes else 'relative-inside'
res=[]
for r in rows:
    rel,kind=r[0],r[1]; det=r[2] if len(r)>2 else ''
    cls = classify_link(rel,det) if kind=='symlink' else kind
    res.append((rel,kind,det,cls))
# actual tree
rep=json.load(open(report))
removed=collections.defaultdict(list)
def walk(o):
    if isinstance(o,dict):
        if o.get('__typename__')=='MaliciousSymlinkRemoved': removed[o['link']].append(o['target'])
        for v in o.values(): walk(v)
    elif isinstance(o,list):
        for v in o: walk(v)
walk(rep)
typenames=collections.Counter()
def walk2(o):
    if isinstance(o,dict):
        t=o.get('__typename__')
        if t and 'Report' in t or (t and t[0].isupper() and ('Removed' in t or 'Problem' in t or 'Failed' in t)): typenames[t]+=1
        for v in o.values(): walk2(v)
    elif isinstance(o,list):
        for v in o: walk2(v)
walk2(rep)
tab=collections.Counter(); detail=[]
for rel,kind,det,cls in res:
    p=os.path.join(root,rel)
    if os.path.islink(p): st='symlink-present'; new=os.readlink(p)
    elif os.path.lexists(p):
        m=os.lstat(p).st_mode
        st='dir' if stat.S_ISDIR(m) else 'reg' if stat.S_ISREG(m) else 'chr' if stat.S_ISCHR(m) else 'other'
        new=None
    else: st='absent'; new=None
    rmv = any(k.endswith('/'+rel) or k==rel for k in removed) # refined below
    tab[(kind,cls,st)]+=1
    detail.append(dict(rel=rel,kind=kind,detail=det,cls=cls,tree=st,new_target=new))
# exact diag mapping: diag link is absolute path in extract dir
diagrel=collections.Counter()
dmap={}
for link,tg in removed.items():
    i=link.find(os.path.basename(root.rstrip('/'))+'/')
    r=link[i+len(os.path.basename(root.rstrip('/')))+1:] if i>=0 else None
    dmap[r]=tg
for d in detail: d['diag']=d['rel'] in dmap
agg=collections.Counter((d['kind'],d['cls'],d['tree'],d['diag']) for d in detail)
json.dump({'agg':[list(k)+[v] for k,v in sorted(agg.items())],'typenames':typenames,'n_diag':len(dmap),'diag_unmatched':[r for r in dmap if r not in {d['rel'] for d in detail}],'detail':detail},open(out,'w'),indent=1,default=str)
for k,v in sorted(agg.items()): print(v,k)
print('typenames',dict(typenames),'diag',len(dmap),'unmatched',[r for r in dmap if r not in {d['rel'] for d in detail}])
