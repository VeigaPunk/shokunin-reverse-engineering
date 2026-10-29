import re,subprocess,sys
L="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"; REV=sys.argv[1] if len(sys.argv)>1 else "7c678ae6d97aedb969fd253b52b3d2882ef1e186"
def g(*a): return subprocess.run(["git","-C",L,*a],check=True,capture_output=True,text=True).stdout
files=[p for p in g("ls-tree","-r","--name-only",REV,"corpus/knowledge").split("\n") if p.endswith(".md")]
stems={p.rsplit("/",1)[1][:-3] for p in files}
rd=g("show",f"{REV}:corpus/README.md")
m=re.search(r"^## Coverage map\n(.*?)(?=^## )",rd,re.S|re.M); sec=m.group(1)
mapped={s for s in stems if s in sec}
mapped_re=set(re.findall(r"2026-10-\d{2}-[a-z0-9-]+",sec))&stems
sc=g("show",f"{REV}:SCORECARD.md").split("\n")
row=[l for l in sc if l.startswith("| coverage |")][0]
cell=row.split("|")[3]
print("files",len(files),"stems",len(stems),"mapped(substr)",len(mapped),"mapped(re)",len(mapped_re))
print("row cell first fraction",re.search(r"(\d+)/(\d+) knowledge files mapped",cell).groups())
print("missing",sorted(stems-mapped_re)); print("dangling",sorted(set(re.findall(r"2026-10-\d{2}-[a-z0-9-]+",sec))-stems)[:5])
print("row line no", sc.index(row)+1)
