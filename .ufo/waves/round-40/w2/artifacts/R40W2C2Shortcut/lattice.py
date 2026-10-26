import importlib.util, json, os, itertools, fnmatch
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec=importlib.util.spec_from_file_location('t', LANE+'/tools/round-40/sqfs-triage-v2.py')
t=importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
H=LANE+'/corpus/evidence/round-40/c2/heldout'
man=json.load(open(H+'/manifest.json'))
envs=[]
for c in man['carriers']:
    p=os.path.join(H,c['id'],'envelope.json'); obj=json.load(open(p))
    f=t.features(t.envelope_data(obj,p)); f['P']='>0' if f['P']>0 else '0'
    envs.append({'id':c['id'],'class':c['class'],'pair':(c['label'],c['action']),'f':f})
PASS=('unclassified','none'); COLS=['OP','PV','H','G','D','BE','SR','P']
def cands(f):
    out={'OP':[f['OP']],'PV':[f['PV']]}
    h=f['H']
    out['H']=[('none',)] if not h else [('set',tuple(h)),('pattern','squashfs_v4_*')]
    out['G']=[('set',tuple(f['G']))]; out['D']=[('set',tuple(f['D']))]
    out['BE']=[f['BE']]; out['SR']=[f['SR']]; out['P']=[f['P']]
    return out
def match(cv,f):
    for col,val in cv.items():
        if col=='H':
            if val[0]=='none':
                if f['H']: return False
            elif val[0]=='pattern':
                if not any(fnmatch.fnmatchcase(x,val[1]) for x in f['H']): return False
            elif tuple(f['H'])!=val[1]: return False
        elif col in ('G','D'):
            if tuple(f[col])!=val[1]: return False
        elif f[col]!=val: return False
    return True
def solve(allowed):
    total=0; rows={}
    for pair in sorted({e['pair'] for e in envs}):
        if pair==PASS: continue
        mem=[e for e in envs if e['pair']==pair]; oth=[e for e in envs if e['pair']!=pair]
        f=mem[0]['f']; c=cands(f); cols=[x for x in COLS if x in allowed]
        best=None
        for n in range(0,len(cols)+1):
            for combo in itertools.combinations(cols,n):
                for vals in itertools.product(*[c[col] for col in combo]):
                    cells=dict(zip(combo,vals))
                    if all(match(cells,e['f']) for e in mem) and not any(match(cells,e['f']) for e in oth):
                        best=(n,cells)
                if best: break
            if best: break
        if not best: return None,None
        total+=best[0]; rows[pair]=best[1]
    return total,rows
res=[]
for k in range(1,9):
    for sub in itertools.combinations(COLS,k):
        tot,rows=solve(set(sub))
        if tot is not None: res.append((k,tot,sub))
res.sort()
print('column subsets that can separate all 11 pairs (size, min-cells, columns):')
for k,tot,sub in res[:14]: print('  %d cols %2d cells  %s'%(k,tot,','.join(sub)))
print('  ... total reachable subsets:',len(res))
best=sorted(res,key=lambda x:(x[1],x[0]))
print('cheapest by cells:',best[0])
json.dump([{'cols':list(s),'cells':c} for _,c,s in res], open('lattice.json','w'))
