import subprocess,json,os,sys,re
D='/fast/scratch/hyaku/kaidoku-r49/W2C2Registry/fx'
REV='29883d4ec35a31a8393c4ffb220888c44c0bb022'; FZ='decc5697bfd4ec1e9de4a762ad199d9bd9c4230d'
def g(*a,**k): return subprocess.run(['git','-C',D,*a],capture_output=True,**k)
assert g('rev-parse','--show-toplevel',text=True).stdout.strip()==D
def sub(path,fn):
    p=os.path.join(D,path); b=open(p,'rb').read(); n=fn(b); assert n!=b,(path); open(p,'wb').write(n)
def rowsub(n,old,new):
    def f(b):
        L=b.split(b'\n')
        for i,l in enumerate(L):
            if l.startswith(b'| S%d '%n):
                assert old.encode() in l,(n,old); L[i]=l.replace(old.encode(),new.encode(),1); return b'\n'.join(L)
        raise Exception('no row')
    return f
SRC='corpus/SOURCES.md'
M={
'R1 S147 sha pin flip':[(SRC,rowsub(147,'sha256 `2c2d48c6','sha256 `2c2d48c7'))],
'R2 S148 sha pin flip':[(SRC,rowsub(148,'`d9db4b96','`d9db4b97'))],
'R3 S149 sha pin flip':[(SRC,rowsub(149,'`1fc793a2','`1fc793a3'))],
'R4 S149 snapshot bytes +1':[('corpus/evidence/round-49/c2/freebsd-sysexits.html',lambda b:b+b'\n')],
'R5 S148 url 3head.htm':[(SRC,rowsub(148,'3head.html','3head.htm'))],
'R6 S145 locator tamper':[(SRC,rowsub(145,'2. The Problem','3. The Problem'))],
'R7 S146 teaches tamper':[(SRC,rowsub(146,'Would have grounded','Would have NOT grounded'))],
'R8 S149 status->mined':[(SRC,rowsub(149,'| rejected |','| mined |'))],
'R9 S147 supersedes->follows':[(SRC,rowsub(147,'supersedes S145','follows S145'))],
'R10 S147 word count 21->20':[(SRC,rowsub(147,'(21 words)','(20 words)'))],
'R11 S148 used-by -> —':[(SRC,rowsub(148,'| corpus/lessons/round-49.md |','| — |'))],
'R12 S149 row deleted':[(SRC,lambda b:b'\n'.join(l for l in b.split(b'\n') if not l.startswith(b'| S149 ')))],
'R13 S138 used-by r49 removed':[(SRC,rowsub(138,', corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md',''))],
'R14 S147 locator -> Problem of Demarcation':[(SRC,rowsub(147,'`2. Backdrop to Popper’s Thought`, the heading above both quotes','`3. The Problem of Demarcation`, the heading above both quotes'))],
'R15 S148 quote altered (EX_USAGE 65)':[(SRC,rowsub(148,'EX_USAGE 64 /*','EX_USAGE 65 /*'))],
'R16 S147 opened date +1':[(SRC,rowsub(147,'| 2026-10-28 | 365d','| 2026-10-27 | 365d'))],
'R17 S149 tier C->A':[(SRC,rowsub(149,'| docs | C |','| docs | A |'))],
'R18 S145 byte change (whitespace)':[(SRC,rowsub(145,'demarcation of an empirical','demarcation of  an empirical'))],
'R19 snapshot popper swap=freebsd bytes':[('corpus/evidence/round-49/c2/popper.html',lambda b:open(D+'/corpus/evidence/round-49/c2/freebsd-sysexits.html','rb').read())],
'R20 S147 recheck 365d->on-request':[(SRC,rowsub(147,'| 365d |','| on-request |'))],
}
res=[]
for name,edits in M.items():
    g('checkout','-q','--detach',REV); g('reset','-q','--hard',REV)
    for p,f in edits: sub(p,f)
    g('add','-A'); r=g('commit','-q','-m','mut','--no-gpg-sign'); 
    if r.returncode: print(name,'commit failed',r.stderr); continue
    rev=g('rev-parse','HEAD',text=True).stdout.strip()
    r=subprocess.run(['python3','-I','-B','tools/round-49/c2-mismatch.py','--root',D,'--rev',rev,'--freeze',FZ],cwd=D,capture_output=True,text=True,env={**os.environ,'GIT_NO_REPLACE_OBJECTS':'1'})
    try: j=json.loads(r.stdout)
    except Exception: j=None
    bad={k:v['why'] for k,v in (j or {}).get('atoms',{}).items() if not v['ok']}
    print(f"{name} | exit {r.returncode} | mism {j and j['mismatches']} | {json.dumps(bad)[:330]}",flush=True)
g('checkout','-q','--detach',REV)
