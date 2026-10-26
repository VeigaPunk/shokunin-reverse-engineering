import importlib.util, json, copy
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
cc=load('cc',LANE+'/tools/round-40/c1-counter.py'); R=load('rule','rule.py')
model=json.load(open(LANE+'/.ufo/waves/round-40/c1/gap-rule.json'))
def T(p,n=2):
    o=[]
    for l in open(LANE+'/'+p):
        c=l.rstrip('\n').split('\t')
        if len(c)>=n and c[0]: o.append(tuple(c[:n]))
    return o
def check(cid, env):
    root,why=R.chunk_root(env)
    O=T(f'corpus/evidence/round-40/c1/{cid}/oracle.tsv'); N=T(f'corpus/evidence/round-40/c1/{cid}/nonregular.tsv')
    files=[(f['relative_path'],f.get('sha256',''),f.get('size')) for f in env['normalized_result']['files']]
    oh=sum(1 for r,s in O if any(R.same_entry(p,r,root) and s==fs for p,fs,_ in files))
    np=[p for p,_,_ in files if any(R.same_entry(p,r,root) for r,_ in N)]
    seen=[];bad=[]
    for g in env['normalized_result']['extraction_gaps']:
        rp=g.get('relative_path')
        if rp is None: continue
        h=[r for r,_ in N if R.same_entry(rp,r,root)]
        if len(h)!=1: bad.append((rp,len(h)))
        else: seen.append(h[0])
    miss=[r for r,k in N if model['required'].get(k) and r not in seen]
    print(f'{cid}: root={root!r} {why or ""} oracle={oh}/{len(O)} nonreg_pub={np} unresolved={bad} missing_required={len(miss)}')
for cid in ('V1','V2','L1','L2'):
    check(cid, json.load(open(LANE+f'/corpus/evidence/round-40/c1/{cid}/after.json')))

print('-- projection under new rule (L2 committed vs fresh rerun) --')
def proj(env):
    root,why=R.chunk_root(env); nr=env['normalized_result']
    out={'root':root,'files':sorted([R.entry_rel(f['relative_path'],root),f.get('sha256'),f.get('size')] for f in nr['files']),
         'gaps':sorted([[g['kind'],R.entry_rel(g['relative_path'],root)] for g in nr['extraction_gaps']]),
         'unpub':sorted([[u['kind'],R.entry_rel(u['relative_path'],root)] for u in nr['unpublished_entries']])}
    return out
a=json.load(open(LANE+'/corpus/evidence/round-40/c1/L2/after.json'))
b=json.load(open('rr/rea.json')); b=b.get('data') or b
print(' committed vs fresh equal:', proj(a)==proj(b))
c=copy.deepcopy(a); nr=c['normalized_result']
for k in ('files','extraction_gaps','unpublished_entries'):
    for x in nr[k]:
        p=x.get('relative_path')
        if isinstance(p,str) and p.startswith('firmware.bin_extract/'):
            x['relative_path']=p[len('firmware.bin_extract/'):]
        elif p=='firmware.bin_extract': x['relative_path']=''
print(' rootless receipt equals honest:', proj(c)==proj(a), '| root:', R.chunk_root(c))
d=copy.deepcopy(a)
for f in d['normalized_result']['files']: f['relative_path']=f['relative_path'].replace('firmware.bin_extract','carrier.bin_extract',1)
for g in d['normalized_result']['extraction_gaps']:
    if g.get('relative_path'): g['relative_path']=g['relative_path'].replace('firmware.bin_extract','carrier.bin_extract',1)
for u in d['normalized_result']['unpublished_entries']: u['relative_path']=u['relative_path'].replace('firmware.bin_extract','carrier.bin_extract',1)
for dv in d['normalized_result']['derivations']: dv['child_path']='$output/carrier.bin_extract'
print(' renamed-root receipt equals honest (root-independent below root):', proj(d)==proj(a))
