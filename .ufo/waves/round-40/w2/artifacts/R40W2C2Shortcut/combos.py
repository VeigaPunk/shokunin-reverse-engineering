import json, os, sys, tempfile
sys.path.insert(0,'.')
from harness import *
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
work=tempfile.mkdtemp(dir='/fast/scratch/hyaku/kaidoku-r40/R40W2C2Shortcut')
held=materialize('held',work)
cells=json.load(open('committed-cells.json'))['cells']
def zero(idxs,tag):
    m=[list(r) for r in cells]
    for r in m:
        for i in idxs: r[i]='*'
    sk=skill_file(m, os.path.join(work,'sk-'+tag+'.md'))
    r=score(sk,held)
    print('%-22s matched=%d/26 wrong=%s'%(tag,r['matched'],r['wrong']))
    return r
zero((1,2),'zero-op+pv')
zero((1,2,5),'zero-op+pv+deps')
zero((1,2,5,4),'zero-op+pv+deps+gaps')
zero((1,5),'op+deps-star (pv kept)')
