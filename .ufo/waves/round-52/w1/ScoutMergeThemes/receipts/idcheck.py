import re
def rows(p):
    out={}
    for line in open(p,encoding='utf-8'):
        if not line.startswith('|'): continue
        c=[x.strip() for x in line.strip().strip('|').split('|')]
        if len(c)<3 or not re.fullmatch(r'S\d+',c[0]): continue
        out[c[0]]=c
    return out
pkg=rows('/home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md')
lane=rows('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md')
pids=sorted(pkg,key=lambda s:int(s[1:])); lids=sorted(lane,key=lambda s:int(s[1:]))
coll=[i for i in pids if i in lane]
lnums=sorted(int(i[1:]) for i in lids)
print("package rows:",len(pkg),"ids",pids[0],"..",pids[-1])
print("lane rows:",len(lane),"max S%d"%max(lnums),"next free S%d"%(max(lnums)+1))
print("numeric id collisions (package id already used in lane):",len(coll),coll[0],"..",coll[-1])
free=[i for i in pids if i not in lane]
print("package rows with a free numeric id:",len(free),"->",free[0],"..",free[-1])
print("renumber-by-document map for the 3 candidate entries' rows:")
for rid in ['S106','S107','S122','S189','S190','S191','S192','S216','S217','S218','S219','S220','S223']:
    c=pkg[rid]
    used=c[11] if len(c)>=12 else ''
    url=c[1].split(' — ')[-1] if ' — ' in c[1] else c[1]
    held=[l for l in lids if url.split('//')[-1].rstrip('/') and url.split('//')[-1].rstrip('/') in lane[l][1]]
    print("  %s used-by=%-45s lane-holds-same-document=%s"%(rid,used.replace('corpus/knowledge/',''),held))
