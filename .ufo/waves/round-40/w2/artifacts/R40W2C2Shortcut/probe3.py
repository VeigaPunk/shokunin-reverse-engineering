import json, os, sys, glob, itertools
sys.path.insert(0,'.')
from harness import *
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
import importlib.util
spec=importlib.util.spec_from_file_location('t',LANE+'/tools/round-40/sqfs-triage-v2.py')
t=importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
real=[]
for pat,label in (('corpus/evidence/round-40/c1/*/after.json','r40'),
                  ('corpus/evidence/round-39/c1/*/after.json','r39'),
                  ('corpus/evidence/round-36/c1/*/after.json','r36')):
    for p in sorted(glob.glob(os.path.join(LANE,pat))):
        real.append((label+'-'+p.split('/')[-2], 'real','?','?',p))
print('real envelopes:',len(real))
sk=os.path.join('/fast/scratch/hyaku/kaidoku-r40/R40W2C2Shortcut','sk-real.md')
r=score(LANE+'/SKILL.md', real)
print('exit',r['exit'],'stderr',r['stderr'][:200])
for p in real:
    o=json.load(open(p[4])); f=t.features(t.envelope_data(o,p[4]))
    print('  %-8s G=%-45s D=%-18s SR=%-3s BE=%-3s P=%-5d -> %s'%(p[0],f['G'],f['D'],f['SR'],f['BE'],f['P'],r['got'].get(p[4].split('/')[-2])))
# distance matrix over the 13 held-out signatures
man=json.load(open(LANE+'/corpus/evidence/round-40/c2/heldout/manifest.json'))
sig={}
for c in man['carriers']:
    p=os.path.join(LANE,'corpus/evidence/round-40/c2/heldout',c['id'],'envelope.json')
    f=t.features(t.envelope_data(json.load(open(p)),p)); f['P']='>0' if f['P']>0 else '0'
    sig.setdefault(c['class'],set()).add((f['OP'],f['PV'],tuple(f['H']),tuple(f['G']),tuple(f['D']),f['BE'],f['SR'],f['P']))
print('\nper-class signature count (after P collapse):',{k:len(v) for k,v in sig.items()})
keys=list(sig)
one=[]
for a,b in itertools.combinations(keys,2):
    fa=list(sig[a])[0]; fb=list(sig[b])[0]
    d=[i for i in range(8) if fa[i]!=fb[i]]
    if len(d)==1: one.append((a,b,['OP','PV','H','G','D','BE','SR','P'][d[0]]))
print('pairs separated by exactly ONE feature:',len(one))
for x in one: print('   ',x[0],'vs',x[1],'->',x[2])
