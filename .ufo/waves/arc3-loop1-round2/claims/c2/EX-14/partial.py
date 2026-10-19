import importlib.util, re, os, hashlib
CENSUS="/var/tmp/ex14/census.py"; ROOT="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
def fresh():
    s=importlib.util.spec_from_file_location("c",CENSUS); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
NEVER=re.compile(r"(?!x)x")
def run(neuter=()):
    C=fresh()
    if "PIN" in neuter: C.PIN=NEVER
    if "VER" in neuter: C.VER=NEVER
    if "PTR" in neuter: C.PTR=NEVER
    live=C.live_pins(); out={}; counts={}
    for f in sorted({s[0] for s in C.SCOPE}):
        lines=open(os.path.join(ROOT,f),encoding="utf-8",errors="replace").read().splitlines()
        counts[f]={"lines":len(lines),"loci":len(C.classify(f,lines,live,out))}
    dets=[(r["file"],d["line"],d["disp"],d["kind"],d["value"]) for disp,recs in out.items() if disp not in ("g11","g7") for r in recs for d in r["asserts"]]
    cur=[d for d in dets if d[2]=="current-ok"]
    floor_A=len(cur)>0; floor_C=sum(c["loci"] for c in counts.values())>0
    return counts,len(dets),len(cur),floor_A,floor_C
print("census sha256:", hashlib.sha256(open(CENSUS,"rb").read()).hexdigest())
print("%-22s %-34s %5s %5s %6s %8s %8s" % ("neuter","counts(loci)","dets","cur","floorA","floorC","blocks"))
for neuter in ((),("PIN",),("VER",),("PTR",),("PIN","VER"),("PIN","PTR"),("VER","PTR"),("PIN","VER","PTR")):
    counts,d,c,fa,fc=run(neuter)
    print("%-22s %-34s %5d %5d %6s %8s %8d" % ("+".join(neuter) or "(none)", json.dumps({k:v["loci"] for k,v in counts.items()}) if False else "P%d S%d K%d"%(counts["PROVINCE.md"]["loci"],counts["SCORECARD.md"]["loci"],counts["SKILL.md"]["loci"]), d, c, "PASS" if fa else "FAIL", "PASS" if fc else "FAIL", sum(v["loci"] for v in counts.values())))
