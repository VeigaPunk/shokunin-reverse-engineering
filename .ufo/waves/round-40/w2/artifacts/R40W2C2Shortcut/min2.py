import importlib.util, json, os, itertools, fnmatch
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec=importlib.util.spec_from_file_location('t', LANE+'/tools/round-40/sqfs-triage-v2.py')
t=importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
H=LANE+'/corpus/evidence/round-40/c2/heldout'
man=json.load(open(H+'/manifest.json'))
envs=[]
for c in man['carriers']:
    p=os.path.join(H,c['id'],'envelope.json')
    obj=json.load(open(p)); f=t.features(t.envelope_data(obj,p))
    f['P']='>0' if f['P']>0 else '0'
    envs.append({'id':c['id'],'class':c['class'],'pair':(c['label'],c['action']),'f':f})
PASS=('unclassified','none')
COLS=['OP','PV','H','G','D','BE','SR','P']
def cands(f):
    out={'OP':[f['OP']],'PV':[f['PV']]}
    h=f['H']
    out['H']=[('none',)] if not h else [('set',tuple(h)),('pattern','squashfs_v4_*')]
    out['G']=[('set',tuple(f['G']))]; out['D']=[('set',tuple(f['D']))]
    out['BE']=[f['BE']]; out['SR']=[f['SR']]; out['P']=[f['P']]
    return out
def match(cellvals,f):
    for col,val in cellvals.items():
        if col=='H':
            if val[0]=='none':
                if f['H']: return False
            elif val[0]=='pattern':
                if not any(fnmatch.fnmatchcase(x,val[1]) for x in f['H']): return False
            else:
                if tuple(f['H'])!=val[1]: return False
        elif col in ('G','D'):
            if tuple(f[col])!=val[1]: return False
        else:
            if f[col]!=val: return False
    return True
def minimal(forbidden=()):
    total=0; chosen={}
    for pair in sorted({e['pair'] for e in envs}):
        if pair==PASS: continue
        members=[e for e in envs if e['pair']==pair]
        others=[e for e in envs if e['pair']!=pair]
        f=members[0]['f']; c=cands(f)
        cols=[x for x in COLS if x not in forbidden]
        best=None
        for n in range(0,len(cols)+1):
            for combo in itertools.combinations(cols,n):
                for vals in itertools.product(*[c[col] for col in combo]):
                    cells=dict(zip(combo,vals))
                    if all(match(cells,e['f']) for e in members) and not any(match(cells,e['f']) for e in others):
                        best=(n,cells); break
                if best: break
            if best: break
        if not best: return None,None
        total+=best[0]; chosen[pair]=best[1]
    return total,chosen
tot,chosen=minimal()
print('MIN TOTAL non-* cells (unclassified row = none):',tot)
for pair,cells in chosen.items():
    print('  %-40s %d  %s'%('/'.join(pair),len(cells),{k:(v[1] if isinstance(v,tuple) and len(v)==2 and v[0] in('set','pattern') else v) for k,v in cells.items()}))
print()
for f in [('PV',),('OP',),('OP','PV'),('H',),('P',),('BE',),('SR',),('G',),('D',),('OP','PV','H','G','D','BE','SR','P')]:
    tt,_=minimal(forbidden=f)
    print('forbid %-12s -> %s'%(','.join(f),tt))
json.dump({str(k):{kk:(list(vv) if isinstance(vv,tuple) else vv) for kk,vv in v.items()} for k,v in (chosen or {}).items()},open('min-selected.json','w'),indent=1)
