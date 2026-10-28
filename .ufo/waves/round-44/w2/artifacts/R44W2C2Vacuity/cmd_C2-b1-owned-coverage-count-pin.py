import json,os,re,subprocess,sys
REV=sys.argv[1]; FREEZE=sys.argv[2]; REPO=sys.argv[3]
EID='C2-b1-owned-coverage-count-pin'
def show(path,rev=None):
    r=subprocess.run(["git","-C",REPO,"show",f"{rev or REV}:{path}"],capture_output=True,text=True)
    return r.stdout if r.returncode==0 else None
def exists(path,rev=None):
    return subprocess.run(["git","-C",REPO,"cat-file","-e",f"{rev or REV}:{path}"],capture_output=True).returncode==0
def correction(txt,eid):
    ls=(txt or "").splitlines()
    for i,l in enumerate(ls):
        if ("<!-- c2-correction: "+eid+" -->") in l:
            for j in range(i+1,min(i+10,len(ls))):
                m=re.match(r"\s*c2-correction-value:\s*(.+?)\s*$",ls[j])
                if m: return m.group(1)
    return None
def section(text,prefix):
    ls=(text or "").splitlines()
    for i,l in enumerate(ls):
        if l.startswith(prefix):
            out=[l]
            for k in range(i+1,len(ls)):
                if ls[k].startswith("## "): break
                out.append(ls[k])
            return "\n".join(out)
    return None
def find_row(text,prefix,key):
    ls=(text or "").splitlines()
    start=0
    if prefix:
        for i,l in enumerate(ls):
            if l.startswith(prefix): start=i+1; break
        else: return None
    k=start
    while k<len(ls) and not ls[k].startswith("## "):
        l=ls[k]
        if l.startswith("|"):
            c=[x.strip() for x in l.strip().strip("|").split("|")]
            if c and c[0]==key: return l
        k+=1
    return None
def find_box(text,key):
    ls=(text or "").splitlines()
    for i,l in enumerate(ls):
        m=re.match(r"^- \[[ x~]\] (.*)$",l)
        if m and m.group(1).strip().startswith(key):
            out=[l]
            for k in range(i+1,len(ls)):
                if ls[k].startswith("  "): out.append(ls[k])
                else: break
            return "\n".join(out)
    return None
def find_line(text,needle):
    for l in (text or "").splitlines():
        if needle in l: return l
    return None
def heading_range(path,prefix,rev,stop):
    t=show(path,rev); ls=(t or "").splitlines()
    st=next((k for k,l in enumerate(ls) if l.startswith(prefix)),None)
    if st is None: return None
    last=st
    for k in range(st+1,len(ls)):
        if stop(ls[k]): break
        if ls[k].strip(): last=k
    return "%d-%d"%(st+1,last+1)
def command_a(rev):
    out=subprocess.check_output(["git","-C",REPO,"ls-tree","-r","--name-only",rev,"--","corpus/knowledge"],text=True).splitlines()
    files={p.rsplit("/",1)[-1][:-3] for p in out if p.endswith(".md")}
    readme=show("corpus/README.md",rev) or ""
    sec=readme.split("## Coverage map\n",1)[1].split("\n## ",1)[0] if "## Coverage map\n" in readme else ""
    mapped=set(re.findall(r"2026-10-\d{2}-[a-z0-9-]+",sec))
    skill=show("SKILL.md",rev) or ""
    craft=skill.split("## Queue-drain craft ",1)[1].split("\n## ",1)[0] if "## Queue-drain craft " in skill else ""
    rules=re.split(r"(?m)^- \*\*",craft)[1:]
    pat=r"corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?"
    resolved=0
    for rule in rules:
        refs=re.findall(pat,rule); ok=bool(refs)
        for name,f,l in refs:
            t=show("corpus/knowledge/"+name,rev)
            if t is None: ok=False; continue
            s,e=int(f or 1),int(l or f or 1)
            ok=ok and 1<=s<=e<=len(t.splitlines())
        resolved+=ok
    return {"mapped":len(files&mapped),"files":len(files),"missing":sorted(files-mapped),
            "dangling":sorted(mapped-files),"rules":len(rules),"resolved":resolved,
            "coverage_score":round(10*len(files&mapped)/len(files),2) if files else 0.0,
            "depth_score":round(10*resolved/len(rules),2) if rules else 0.0}
def triage_table(rev,marker):
    sk=show("SKILL.md",rev) or ""; ls=sk.splitlines()
    idx=[i for i,l in enumerate(ls) if marker in l]
    if not idx: return None
    i=idx[0]; tbl=[]; j=i+1
    while j<len(ls):
        if ls[j].strip().startswith("|"): tbl.append(ls[j])
        elif tbl: break
        j+=1
    if not tbl: return None
    cols=len(tbl[0].strip().strip("|").split("|"))
    rows=[l for l in tbl[1:] if not re.fullmatch(r"[|\s:\-]*",l)]
    return {"cols":cols,"rows":len(rows)}
def emit(observed,derived,detail=""):
    print(json.dumps({"id":EID,"observed":observed,"derived":derived,"detail":detail}))


STMT=show('SCORECARD.md',REV)
line=None
if '':
    line=find_box(STMT,'')
elif 'coverage':
    line=find_row(STMT,'## Owned axes','coverage')
else:
    line=find_line(STMT,'craft section')
if line is None:
    emit("UNSUPPORTED:statement-not-found",None,"statement not located at REV"); raise SystemExit(0)
ms=list(re.finditer('(\\d+)/(\\d+) knowledge files mapped',line))
if not ms:
    emit("UNSUPPORTED:pattern-not-found",None,"stated pattern absent from the statement"); raise SystemExit(0)
m=ms[min(1,len(ms))-1]
stated=(m.group(1)+'/'+m.group(2))
eff=correction(STMT,EID)
if eff is not None: stated=eff
REV2='e1c83313'
if REV2=="FREEZE_TREE": REV2=os.environ.get("HYAKU_FREEZE") or FREEZE
A=command_a(REV2); derived="%d/%d"%(A["mapped"],A["files"])
observed=stated if (stated is not None and derived is not None and stated==derived) else ("UNSUPPORTED:"+str(stated))
emit(observed,derived,"'pinned clause re-derived at its own revision'")
