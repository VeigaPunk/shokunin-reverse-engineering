import re, subprocess, collections
ROOT='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
BASE='77091b492cc53f8743bd0701b1e7d5e66123dd84'; REV='0fc6113376a156fddc3ec385386d71c3a4a9f690'
DOCS=['SCORECARD.md','SHONEN.md','PROVINCE.md','LOG.md','corpus/README.md','corpus/QUALITY.md','corpus/lessons/round-38.md','corpus/SOURCES.md']
def show(rev,p):
    r=subprocess.run(['git','-C',ROOT,'show',f'{rev}:{p}'],capture_output=True)
    return r.stdout.decode() if r.returncode==0 else None
def exists(rev,p):
    return subprocess.run(['git','-C',ROOT,'cat-file','-e',f'{rev}:{p}'],capture_output=True).returncode==0
LANE=re.compile(r'^(corpus/|tools/|plans/|evidence/|scripts/|considerthese/|kaidoku-r26/|\.ufo/|SCORECARD\.md|SHONEN\.md|SKILL\.md|PROVINCE\.md|LOG\.md|README\.md|MINT\.md|AGENTS\.md)')
TOK=re.compile(r'`([^`\n]+)`'); PTR=re.compile(r'^([A-Za-z0-9_.][A-Za-z0-9_./+-]*?)(?::(\d+)(?:-(\d+))?)?$')
def toks(rev,doc):
    t=show(rev,doc)
    if t is None: return None
    out=set()
    for tok in TOK.findall(t):
        tok=tok.strip(); m=PTR.match(tok)
        if not m or tok.startswith(('/','~')): continue
        if LANE.match(m.group(1)): out.add(tok)
    return out
def res(rev,tok):
    m=PTR.match(tok); p=m.group(1).rstrip('/'); a,b=m.group(2),m.group(3)
    if not exists(rev,p): return False,'missing path'
    if a is None: return True,''
    t=show(rev,p); n=len(t.splitlines()) if t is not None else 0
    lo,hi=int(a),int(b or a)
    if not (1<=lo<=hi<=n): return False,f'range {a}-{b} vs {n} lines'
    return True,''
allnew=collections.Counter()
for doc in DOCS:
    tb=toks(BASE,doc); tr=toks(REV,doc)
    if tr is None: print(doc,'ABSENT at REV'); continue
    new=sorted(tr-(tb or set()))
    bad_new=[]; bad_old=[]
    for tok in new:
        ok,why=res(REV,tok)
        if not ok: bad_new.append((tok,why))
    for tok in sorted(tr-(tb or set()) if False else (tr & (tb or set()))):
        ok,why=res(REV,tok)
        if not ok: bad_old.append((tok,why))
    print(f'--- {doc}: tokens base={len(tb or [])} rev={len(tr)} new={len(new)} NEW-UNRESOLVED={len(bad_new)} INHERITED-UNRESOLVED={len(bad_old)}')
    for t,w in bad_new: print('   NEW-UNRESOLVED',t,'|',w); allnew[t]+=1
    for t,w in bad_old[:6]: print('   inherited-unresolved',t,'|',w)
    if len(bad_old)>6: print(f'   ... {len(bad_old)-6} more inherited')
print('TOTAL new unresolved tokens:', sum(allnew.values()))
