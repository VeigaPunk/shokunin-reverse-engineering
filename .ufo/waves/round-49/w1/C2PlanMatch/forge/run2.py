import sys, importlib.util, hashlib
spec=importlib.util.spec_from_file_location('r', '/fast/scratch/hyaku/kaidoku-r49/C2PlanMatch/forge/run.py')
src=open('/fast/scratch/hyaku/kaidoku-r49/C2PlanMatch/forge/run.py').read().split("LES='corpus/lessons/round-49.md'")[0]
exec(src)
LES='corpus/lessons/round-49.md'
out={}
def f_a6_row_only(d):
    q1="falsifiability as his criterion for demarcating science from non-science: if a theory is incompatible with possible empirical observations it is scientific"
    fake=f'<html><body><h2>2. Backdrop to Popper’s Thought</h2><p>{q1}.</p><h2>3. The Problem of Demarcation</h2></body></html>'.encode()
    old=sha(rd(d,'corpus/evidence/round-49/c2/popper.html')); new=sha(fake)
    wr(d,'corpus/evidence/round-49/c2/popper.html',fake)
    t=rd(d,'corpus/SOURCES.md').decode().split('\n')
    hit=0
    for i,l in enumerate(t):
        if l.lstrip().startswith('| S147 '):
            assert old in l; t[i]=l.replace(old,new); hit+=1
    assert hit==1
    wr(d,'corpus/SOURCES.md','\n'.join(t).encode())
def f_a7_inverted(d):
    t=rd(d,'corpus/SOURCES.md').decode()
    assert 'EX_USAGE is 64, not 2' in t
    wr(d,'corpus/SOURCES.md',t.replace('EX_USAGE is 64, not 2','EX_USAGE is 2, not 64',1).encode())
for n,f in [('F_A6_forged_snapshot_row_only',f_a6_row_only),('F_A7_inverted_teaches',f_a7_inverted)]:
    d=fork(n); f(d); rev=commit(d,'forgery '+n); r=count(d,rev,battery=(n.startswith('F_A7')))
    out[n]=dict(rev=rev,**r); print(n,json.dumps(out[n])[:900],flush=True)
json.dump(out,open(S+'/forge/results2.json','w'),indent=1,ensure_ascii=False)
