import os,re,shutil,sys
A='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/w1/artifacts'
S='/fast/scratch/hyaku/kaidoku-r49/C1DocCheck'
BA='R49C1Doc/block-a-province-round-49-core-row.md'
BB='R49C1Doc/block-b-province-frontier-note.md'
BC='R49C1Doc/block-c-readme-coverage-map-row.md'
EN='R49EntryDraft/corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md'
ENTRY='corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md'
STEM='2026-10-28-r49-squashfs-v1v2-core'
def rd(n): return open(os.path.join(A,n),encoding='utf-8').read()
M={}
def m1(): return {BA: rd(BA).replace('## Round-49 additions to Core\n','',1)}
def m2(): return {BA: rd(BA).replace('squashfs_v2','squashfs_vtwo')}
def m2b(): return {BA: rd(BA).replace('squashfs_v2','squashfs_v2_nonstandard')}
def m3(): return {BA: rd(BA).replace(ENTRY,'(entry path dropped)')}
def m4(): return {BB: rd(BB).replace(STEM,'(stem dropped)')}
def m5():
    t=rd(EN).split('\n'); t=[l for l in t if not l.startswith('source: S139')]
    return {EN:'\n'.join(t)}
def m6(): return {BC: '\n'}
def m4b(): return {BB: rd(BB).replace('Round-49 frontier note','Round-49 note')}
def m3b(): return {BA: rd(BA).replace('SquashFS v1 and v2','X').replace('SquashFS v1/v2','X').replace('SquashFS v1 and','X')}
def m4c(): return {BB: rd(BB).replace('SquashFS v1/v2','X')}   # stem still holds squashfs-v1
def m6b(): return {BC: rd(BC).replace(STEM,'(stem dropped)')}
def m5b():
    t=rd(EN).split('\n'); t=[l for l in t if not l.startswith('source: S138')]
    return {EN:'\n'.join(t)}
for k,v in list(globals().items()):
    if re.fullmatch(r'm\d+[a-z]?',k): M[k]=v
name=sys.argv[1]; d=os.path.join(S,'doc-'+name)
shutil.rmtree(d,ignore_errors=True)
for sub in ('R49C1Doc','R49EntryDraft'): shutil.copytree(os.path.join(A,sub),os.path.join(d,sub))
for rel,txt in M[name]().items():
    old=rd(rel); assert old!=txt or name=='m0',name
    open(os.path.join(d,rel),'w',encoding='utf-8').write(txt)
print(d)
