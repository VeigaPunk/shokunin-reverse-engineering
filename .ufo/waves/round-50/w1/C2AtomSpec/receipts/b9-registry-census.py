import re,subprocess,sys,json
L="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"; REV=sys.argv[1] if len(sys.argv)>1 else "7c678ae6d97aedb969fd253b52b3d2882ef1e186"
def g(*a): return subprocess.run(["git","-C",L,*a],check=True,capture_output=True,text=True).stdout
sk=g("show",f"{REV}:SKILL.md")
assert sk.count("<!-- instrument-registry v2 -->")==1 and sk.count("<!-- /instrument-registry -->")==1
sec=sk.split("<!-- instrument-registry v2 -->",1)[1].split("<!-- /instrument-registry -->",1)[0]
rows=[l for l in sec.split("\n") if l.startswith("|")]
hdr=[r for r in rows if r.startswith("| tool |")]
print("headers",len(hdr),"rows",len(rows))
cell0={}
for r in rows:
    c=[x.strip() for x in r.strip().strip("|").split("|")]
    m=re.fullmatch(r"`(tools/[^`]+)`",c[0])
    if m: cell0.setdefault(m.group(1),[]).append(c)
print("backticked-path rows",sum(len(v) for v in cell0.values()),"distinct",len(cell0))
paths=[p for p in g("ls-tree","-r","--name-only",REV,"tools/round-49","tools/round-50").split() if p.endswith((".py",".sh"))]
print("r49/50 py|sh paths",paths)
for p in paths: print(p, "ROW" if p in cell0 else "MISSING")
# also r46-48
allp=[p for r in range(41,50) for p in g("ls-tree","-r","--name-only",REV,f"tools/round-{r}").split() if p.endswith((".py",".sh"))]
miss=[p for p in allp if p not in cell0]
print("round41-49 py|sh paths",len(allp),"missing rows",len(miss)); print("\n".join(miss))
