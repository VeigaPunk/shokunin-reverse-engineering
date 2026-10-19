import os, subprocess, json
LAB="/var/tmp/ex2-arc3r6"
gates={"v10":"pristine/c1-census-v10.py","PL4":"pl4-gate.py","PL2":"pl2-gate.py","RV3":"rv3-gate.py"}
trees=sorted(os.listdir(os.path.join(LAB,"trees")))
rows=[]; raw={}
for t in trees:
    r={}
    for gname,gpath in gates.items():
        cp=subprocess.run(["python3",gpath,"--root",os.path.join(LAB,"trees",t),"--json"],capture_output=True,text=True)
        open(os.path.join(LAB,"cells","%s__%s.json"%(t,gname)),"w").write(cp.stdout)
        j=json.loads(cp.stdout)
        fe=j.get("frontier_errors", j.get("frontier_stale",""))
        r[gname]={"exit":cp.returncode,"verdict":j["verdict"],"classes":j["declared_fail_classes"],
                  "stale":len(j["stale"]),"undeclared":len(j["undeclared"]),"unreadable":bool(j["unreadable"]),
                  "frontier_n":len(fe) if isinstance(fe,list) else 0,
                  "frontier":fe if isinstance(fe,list) else []}
    raw[t]=r
json.dump(raw,open(os.path.join(LAB,"matrix-all.json"),"w"),indent=1)
def cell(x):
    cls=",".join(c.replace("FRONTIER-","F-") for c in x["classes"]) or "-"
    return f"{x['verdict']}/{x['exit']} {cls}"
lines=[]
hdr="%-22s | %-20s | %-34s | %-32s | %-32s"%("tree","v10","PL-4","PL-2","RV-3")
lines.append(hdr); lines.append("-"*len(hdr))
for t in trees:
    lines.append("%-22s | %-20s | %-34s | %-32s | %-32s"%(t,cell(raw[t]["v10"]),cell(raw[t]["PL4"]),cell(raw[t]["PL2"]),cell(raw[t]["RV3"])))
open(os.path.join(LAB,"matrix-all.txt"),"w").write("\n".join(lines)+"\n")
print("\n".join(lines))
