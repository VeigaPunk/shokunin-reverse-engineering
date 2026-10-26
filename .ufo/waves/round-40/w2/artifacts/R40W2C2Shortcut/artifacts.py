import json, os, sys, glob, shutil, tempfile, subprocess
sys.path.insert(0,'.')
from harness import *
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
OUT=LANE+'/.ufo/waves/round-40/w2/artifacts/R40W2C2Shortcut'
os.makedirs(OUT,exist_ok=True)
work=tempfile.mkdtemp(dir='/fast/scratch/hyaku/kaidoku-r40/R40W2C2Shortcut')
held=materialize('held',work)
# lattice + feature dump
for f in ('lattice.json','feat.json'):
    shutil.copyfile(f, os.path.join(OUT,f))
# ablation table (rerun cheaply from committed cells)
cells=json.load(open('committed-cells.json'))['cells']
COLS=['label','operation','provider','handler','gap kinds','dependencies','-be','symlink removed','published files','action','cause','source']
lines=['variant\tmatched\tn\twrong_classes']
def sc(rows,tag):
    sk=skill_file([list(r) for r in rows], os.path.join(work,'sk-'+tag+'.md'))
    r=score(sk,held); lines.append('%s\t%d\t%d\t%s'%(tag,r['matched'],r['n'],','.join(r['wrong'])))
sc(cells,'committed-rebuilt')
for i in range(1,9):
    m=[list(r) for r in cells]
    for r in m: r[i]='*'
    sc(m,'zero-'+COLS[i].replace(' ','_'))
for r0 in cells:
    sc([r for r in cells if r is not r0],'drop-'+r0[0])
open(os.path.join(OUT,'ablation.tsv'),'w').write('\n'.join(lines)+'\n')
# real envelope triage
real=[]
for pat,lab in (('corpus/evidence/round-40/c1/*/after.json','r40'),
                ('corpus/evidence/round-39/c1/*/after.json','r39'),
                ('corpus/evidence/round-36/c1/*/after.json','r36')):
    for p in sorted(glob.glob(os.path.join(LANE,pat))):
        name=lab+'-'+p.split('/')[-2]
        d=os.path.join(work,name+'.json'); shutil.copyfile(p,d)
        real.append((name,'real','?','?',d))
r=score(LANE+'/SKILL.md',real)
import importlib.util
spec=importlib.util.spec_from_file_location('t',LANE+'/tools/round-40/sqfs-triage-v2.py')
t=importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
out=['id\tgap_kinds\tdeps\tbe\tsymlink_removed\tpublished\tlabel\taction']
for p in real:
    f=t.features(t.envelope_data(json.load(open(p[4])),p[4]))
    g=r['got'].get(p[0],('?','?'))
    out.append('%s\t%s\t%s\t%s\t%s\t%d\t%s\t%s'%(p[0],'+'.join(f['G']) or '-','+'.join(f['D']) or '-',f['BE'],f['SR'],f['P'],g[0],g[1]))
open(os.path.join(OUT,'real-envelope-triage.tsv'),'w').write('\n'.join(out)+'\n')
print('\n'.join(out))
# multi-gap probes
def mut(cid, gap, name):
    src=[e for e in held if e[0]==cid][0][4]
    o=json.load(open(src)); nr=o['normalized_result']
    nr['extraction_gaps']=list(nr.get('extraction_gaps') or [])+[gap]
    fp=os.path.join(work,name+'.json'); json.dump(o,open(fp,'w'))
    return (name,'probe','x','x',fp)
probes=[mut('H17',{'kind':'missing-extractor-dependency','dependencies':['sasquatch']},'X1-avm-plus-dep-gap'),
        mut('H13',{'kind':'unpublished-entry'},'X2-depbe-plus-unpublished'),
        mut('H01',{'kind':'depth-limited'},'X3-cleanbe-plus-depth-limited'),
        mut('H21',{'kind':'missing-extractor-dependency','dependencies':['sasquatch']},'X4-partial-plus-dep-gap'),
        mut('H07',{'kind':'extractor-failure'},'X5-escaping-plus-extractor-failure'),
        mut('H09',{'kind':'depth-limited'},'X6-intree-plus-depth-limited')]
rp=score(LANE+'/SKILL.md',probes)
pl=['probe\tmutated_from\tcommitted_label\tcommitted_action\tsemantic_expectation']
exp={'X1-avm-plus-dep-gap':'failure stays dominant -> wrap-extractor-be/preserve-failure family, not none',
     'X2-depbe-plus-unpublished':'install-extractor-be with the in-tree gaps counted',
     'X3-cleanbe-plus-depth-limited':'count-gap/structural note, not none',
     'X4-partial-plus-dep-gap':'salvage-partial plus the missing dependency',
     'X5-escaping-plus-extractor-failure':'expect-link-absent AND the published-file loss',
     'X6-intree-plus-depth-limited':'count-gap (two structural gap kinds)'}
for p,src in zip(probes,['H17','H13','H01','H21','H07','H09']):
    g=rp['got'].get(p[0],('?','?'))
    pl.append('%s\t%s\t%s\t%s\t%s'%(p[0],src,g[0],g[1],exp[p[0]]))
open(os.path.join(OUT,'multi-gap-probes.tsv'),'w').write('\n'.join(pl)+'\n')
print('\n'.join(pl))
# repro receipt copy + summary
shutil.copyfile('c2-repro.json', os.path.join(OUT,'c2-counter-repro-at-42c10a58.json'))
d=json.load(open('c2-repro.json'))
json.dump({'argv':'python3 -I -B tools/round-40/c2-counter.py --root LANE --rev 42c10a58 --freeze 7fce3086 --json-out ...',
           'exit_code':d['exit_code'],'matched':d['matched'],'n':d['n'],'met_target':d['met_target'],
           'bindings_count':len(d['bindings']),'bindings_false':d['bindings_false'],
           'distinct_decisions':d['distinct_decisions'],'decision_pairs':d['decision_pairs'],
           'all_regenerated_equal_manifest':all(c['regenerated_sha256']==c['manifest_sha256'] for c in d['carriers'])},
          open(os.path.join(OUT,'c2-counter-repro-summary.json'),'w'),indent=1)
