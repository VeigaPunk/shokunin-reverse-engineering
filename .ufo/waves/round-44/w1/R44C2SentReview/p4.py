import re,subprocess,sys,collections
sys.path.insert(0,'.')
import importlib.util
spec=importlib.util.spec_from_file_location('r38','r38c2.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
L='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'; B='c29360e3ba5381a5ab69e372d0d9577970f85018'
cache={}
docs={'SCORECARD':'SCORECARD.md.base','SHONEN':'SHONEN.md.base','corpus/README':'README.md.base','LOG':'LOG.md.base','PROVINCE':'PROVINCE.md.base','SKILL':'SKILL.md.base'}
for n,f in docs.items():
    lines=open(f).read().split('\n')
    tot=0;bad=[];rng=0;badrng=[]
    for ln,l in enumerate(lines,1):
        for tok,path,a,b in m.pointers(l):
            if '<' in path or '*' in path: continue
            tot+=1
            if a: rng+=1
            ok=m.resolves(L,B,path,a,b,cache)
            if not ok:
                (badrng if a else bad).append((ln,tok))
    print(n,'pointers',tot,'with-range',rng,'unresolved-path',len(bad),'unresolved-range',len(badrng))
    print('  path ex:',bad[:6]); print('  range ex:',badrng[:6])
print('======')
for n in ('SCORECARD','corpus/README','SKILL'):
    lines=open(docs[n]).read().split('\n')
    for ln,l in enumerate(lines,1):
        for tok,path,a,b in m.pointers(l):
            if '<' in path or '*' in path: continue
            if not m.resolves(L,B,path,a,b,cache):
                i=l.find(tok); print(n,ln,tok,'||',l[max(0,i-110):i+len(tok)+60].replace('\n',' '))
