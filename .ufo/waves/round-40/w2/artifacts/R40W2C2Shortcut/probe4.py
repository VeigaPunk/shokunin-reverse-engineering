import json, os, sys, glob, shutil, tempfile
sys.path.insert(0,'.')
from harness import *
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
work=tempfile.mkdtemp(dir='/fast/scratch/hyaku/kaidoku-r40/R40W2C2Shortcut')
held=materialize('held',work)
# 1) controls scored on the COMMITTED HELD-OUT set (recorded scores are on dev)
ctl=LANE+'/.ufo/waves/round-40/controls/c2'
print('control tables scored on held-out envelopes:')
for f in sorted(os.listdir(ctl)):
    if not f.endswith('.md'): continue
    r=score(os.path.join(ctl,f),held)
    print('  %-12s exit=%d matched=%2d/26 wrong=%s'%(f,r['exit'],r['matched'],','.join(r['wrong'])))
# 2) real envelopes with unique filenames
real=[]
for pat,lab in (('corpus/evidence/round-40/c1/*/after.json','r40'),
                ('corpus/evidence/round-39/c1/*/after.json','r39'),
                ('corpus/evidence/round-36/c1/*/after.json','r36')):
    for p in sorted(glob.glob(os.path.join(LANE,pat))):
        name=lab+'-'+p.split('/')[-2]
        dest=os.path.join(work,name+'.json'); shutil.copyfile(p,dest)
        real.append((name,'real','?','?',dest))
r=score(LANE+'/SKILL.md',real)
print('\ncommitted v2 table on real squashfs envelopes:')
for n,g in sorted(r['got'].items()): print('  %-8s -> %s'%(n,g))
