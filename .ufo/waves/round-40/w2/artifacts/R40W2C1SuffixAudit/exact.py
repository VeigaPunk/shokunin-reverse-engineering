import importlib.util, json
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec=importlib.util.spec_from_file_location('cc',LANE+'/tools/round-40/c1-counter.py')
cc=importlib.util.module_from_spec(spec); spec.loader.exec_module(cc)

def T(p,n=2):
    out=[]
    for l in open(LANE+'/'+p):
        c=l.rstrip('\n').split('\t')
        if len(c)>=n and c[0]: out.append(tuple(c[:n]))
    return out

def parts(p):
    if not isinstance(p,str): return None
    if p.startswith('$output/'): p=p[len('$output/'):]
    ps=[x for x in p.split('/') if x not in ('','.')]
    return ps

def root_of(env):
    nr=env.get('normalized_result') or {}
    roots=set()
    for d in nr.get('derivations') or []:
        ch=parts(d.get('child_path'))
        if ch and len(ch)==1 and ch[0].endswith('_extract'): roots.add(ch[0])
    return roots

def rel_from(root,p):
    ps=parts(p)
    if ps is None or root is None: return None
    if '..' in ps: return None
    if ps==[root]: return ''
    if len(ps)>1 and ps[0]==root: return '/'.join(ps[1:])
    return None

for cid in ('V1','V2','L1','L2'):
    env=json.load(open(LANE+f'/corpus/evidence/round-40/c1/{cid}/after.json'))
    nr=env['normalized_result']; roots=root_of(env)
    root=sorted(roots)[0] if len(roots)==1 else None
    O=T(f'corpus/evidence/round-40/c1/{cid}/oracle.tsv')
    N=T(f'corpus/evidence/round-40/c1/{cid}/nonregular.tsv')
    files=[(f['relative_path'],f.get('sha256',''),f.get('size')) for f in nr['files']]
    rels={rel_from(root,p) for p,_,_ in files}
    exact=sum(1 for r,s in O if s in {fs for p,fs,_ in files if rel_from(root,p)==r})
    loose=cc.oracle_hits(O,[(p,s,sz) for p,s,sz in files])
    # oracle rows whose current hit is suffix-only
    suffix_only=[]
    for r,s in O:
        hitloose=any(s==fs and cc.same_rel(p,r) for p,fs,_ in files)
        hitexact=any(s==fs and rel_from(root,p)==r for p,fs,_ in files)
        if hitloose and not hitexact: suffix_only.append(r)
    np_loose=cc.nonregular_published(files,N)
    np_exact=[p for p,_,_ in files if any(rel_from(root,p)==r for r,_ in N)]
    gaps=nr['extraction_gaps']
    model=json.load(open(LANE+'/.ufo/waves/round-40/c1/gap-rule.json'))
    # exact gap resolution
    seen=[];bad=[]
    for g in gaps:
        rp=g.get('relative_path')
        if rp is None: continue
        h=[r for r,_ in N if rel_from(root,rp)==r]
        if len(h)!=1: bad.append((rp,len(h)))
        else: seen.append(h[0])
    missing=[r for r,k in N if model['required'].get(k) and r not in seen]
    print(f'{cid}: root={root!r} files={len(files)} roots_found={len(roots)}')
    print(f'   oracle loose={loose}/{len(O)} exact={exact}/{len(O)} suffix_only_hits={len(suffix_only)} {suffix_only[:3]}')
    print(f'   nonreg_published loose={np_loose} exact={np_exact}')
    print(f'   gap exact unresolved={bad} missing_required={missing}')
