import json, os, sys, tempfile, glob, copy
sys.path.insert(0,'.')
from harness import *
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
work=tempfile.mkdtemp(dir='/fast/scratch/hyaku/kaidoku-r40/R40W2C2Shortcut')
held=materialize('held',work)
# ---------- 1. multi-gap / structural-gap probes on the committed table
envs={e[0]:e for e in held}
def mutate(cid, add_gap=None, add_kind=None, name=None):
    src=envs[cid][4]
    o=json.load(open(src))
    nr=o['normalized_result']
    if add_gap:
        nr['extraction_gaps']=list(nr.get('extraction_gaps') or [])+[add_gap]
    fp=os.path.join(work,name+'.json'); json.dump(o,open(fp,'w'))
    return (name,envs[cid][1],envs[cid][2],envs[cid][3],fp)
probes=[
 mutate('H17', add_gap={'kind':'missing-extractor-dependency','dependencies':['sasquatch']}, name='X1-avm+dependency-gap'),
 mutate('H13', add_gap={'kind':'unpublished-entry'}, name='X2-depbe+unpublished'),
 mutate('H01', add_gap={'kind':'depth-limited'}, name='X3-cleanbe+depth-limited'),
 mutate('H21', add_gap={'kind':'missing-extractor-dependency','dependencies':['sasquatch']}, name='X4-partial+dependency-gap'),
 mutate('H07', add_gap={'kind':'extractor-failure'}, name='X5-escaping+extractor-failure'),
 mutate('H09', add_gap={'kind':'depth-limited'}, name='X6-intree+depth-limited'),
]
# expected semantic answer, by hand: a failure/dep gap is the dominant fact
print('--- committed v2 table on structural-gap probes (semantic expectation in comment)')
r=score(LANE+'/SKILL.md', probes)
for p in probes:
    print('  %-28s -> %-22s %-20s   (class %s)'%(p[0], r['got'].get(p[0],('?','?'))[0], r['got'].get(p[0],('?','?'))[1], p[1]))
# ---------- 2. the committed table on every REAL squashfs REA envelope in the lane
real=[]
for pat in ('corpus/evidence/round-40/c1/*/after.json','corpus/evidence/round-39/c1/*/after.json',
            'corpus/evidence/round-36/c1/*/after.json','corpus/evidence/round-36/*/after.json'):
    for p in sorted(glob.glob(os.path.join(LANE,pat))):
        real.append((p.split('/')[-2]+'@'+p.split('/')[-4], 'real', '?', '?', p))
r2=score(LANE+'/SKILL.md', real) if real else None
print('--- committed v2 table on real envelopes:',r2['exit'],'rows',len(real))
import importlib.util
spec=importlib.util.spec_from_file_location('t',LANE+'/tools/round-40/sqfs-triage-v2.py')
t=importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
for p in real:
    o=json.load(open(p[4]))
    try: f=t.features(t.envelope_data(o,p[4]))
    except Exception as e: print('  ',p[0],'ERR',e); continue
    got=r2['got'].get(os.path.basename(os.path.dirname(p[4])))
    print('  %-14s H=%s G=%s D=%s BE=%s SR=%s P=%d -> %s'%(p[0],f['H'],f['G'],f['D'],f['BE'],f['SR'],f['P'],got))
