import re,subprocess,sys,json
REPO=sys.argv[1]; REV=sys.argv[2]
def show(path,rev):
    r=subprocess.run(["git","-C",REPO,"show",f"{rev}:{path}"],capture_output=True,text=True)
    return r.stdout if r.returncode==0 else None
out=subprocess.check_output(["git","-C",REPO,"ls-tree","-r","--name-only",REV,"--","corpus/knowledge"],text=True).splitlines()
files={p.rsplit("/",1)[-1][:-3] for p in out if p.endswith(".md")}
readme=show("corpus/README.md",REV) or ""
sec=readme.split("## Coverage map\n",1)[1].split("\n## ",1)[0] if "## Coverage map\n" in readme else ""
mapped=set(re.findall(r"2026-10-\d{2}-[a-z0-9-]+",sec))
skill=show("SKILL.md",REV) or ""
craft=skill.split("## Queue-drain craft ",1)[1].split("\n## ",1)[0] if "## Queue-drain craft " in skill else ""
rules=re.split(r"(?m)^- \*\*",craft)[1:]
pat=r"corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?"
resolved=0
for rule in rules:
    refs=re.findall(pat,rule); ok=bool(refs)
    for name,f,l in refs:
        t=show("corpus/knowledge/"+name,REV)
        if t is None: ok=False; continue
        s,e=int(f or 1),int(l or f or 1)
        ok=ok and 1<=s<=e<=len(t.splitlines())
    resolved+=ok
print(json.dumps({"rev":REV,"mapped":len(files&mapped),"files":len(files),"value":"%d/%d"%(len(files&mapped),len(files)),"missing":sorted(files-mapped),"dangling":sorted(mapped-files),"rules":len(rules),"resolved":resolved}))
