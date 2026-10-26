import json, os, sys, tempfile, copy
sys.path.insert(0,'.')
from harness import *
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
import importlib.util
spec=importlib.util.spec_from_file_location('t',LANE+'/tools/round-40/sqfs-triage-v2.py')
t=importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
text=open(LANE+'/SKILL.md').read()
rules,info=t.parse_skill(text)
cells=[list(r['cells']) for r in rules]
work=tempfile.mkdtemp(dir='/fast/scratch/hyaku/kaidoku-r40/R40W2C2Shortcut')
held=materialize('held',work)
def score_rows(rows, tag):
    sk=skill_file(rows, os.path.join(work,'sk-%s.md'%tag))
    r=score(sk,held)
    print('%-24s exit=%d matched=%d/%d wrong=%s %s'%(tag,r['exit'],r['matched'],r['n'],r['wrong'],r['stderr'][:100]))
    return r
score_rows(cells,'committed-rebuilt')
COLS=['label','operation','provider','handler','gap kinds','dependencies','-be','symlink removed','published files','action','cause','source']
for i in range(1,9):
    m=[list(r) for r in cells]
    for r in m: r[i]='*'
    score_rows(m,'zero-'+COLS[i].replace(' ','_'))
# drop rows
for j,r0 in enumerate(cells):
    m=[list(r) for r in cells if r is not r0]
    score_rows(m,'drop-'+r0[0])
# order: escaping before mixed
m=[list(r) for r in cells]
esc=[r for r in m if r[0]=='escaping-symlink-removed'][0]
mx=[r for r in m if r[0]=='mixed-symlinks'][0]
m2=[r for r in m if r[0] not in ('escaping-symlink-removed','mixed-symlinks')]
i_mx=m.index(mx); i_esc=m.index(esc)
ins=min(i_mx,i_esc)
m2[ins:ins]=[esc,mx]
score_rows(m2,'escaping-before-mixed')
json.dump({'cells':cells},open('committed-cells.json','w'),indent=1)
