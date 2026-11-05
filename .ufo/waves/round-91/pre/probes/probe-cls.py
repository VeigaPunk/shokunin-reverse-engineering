import importlib.util, json, os, shutil, struct, subprocess, sys, tempfile
ROOT="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
WORK="/fast/scratch/hyaku/kaidoku-r91/l1/probe2"
CARRIERS=[("jq","/usr/bin/jq"),("xxd","/usr/bin/xxd"),("libz","/usr/lib/libz.so.1.3.2"),("dinit","/usr/bin/docker-init")]
def load(rel,name):
    sp=importlib.util.spec_from_file_location(name,os.path.join(ROOT,rel)); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
rep=load("tools/round-87/upx-magic-repair.py","r87"); r88=load("tools/round-88/upx-chain-repair.py","r88"); r90=load("tools/round-90/upx-break-repair.py","r90")
env={"HOME":os.path.join(WORK,"home"),"LANG":"C","PATH":os.environ.get("PATH") or "/usr/bin","TMPDIR":os.path.join(WORK,"tmp")}
for d in (env["HOME"],env["TMPDIR"]): os.makedirs(d,exist_ok=True)
def run(a,t=600):
    p=subprocess.run(a,capture_output=True,text=True,env=env,timeout=t); return p.returncode,(p.stdout+p.stderr).strip().splitlines()[-1:]
os.makedirs(WORK,exist_ok=True)
rows=[]
def classify(data):
    found=r90.longest_prefix(data,rep,r88)
    if found is None: return {"found":None}
    m,b0,ph,blocks,method=found
    ph_off,_=rep.find_packheader(data)
    ok,sinfo=r90.chain_ok(data,rep,b0,ph_off,ph)
    total=r90.accounted(data,r88,b0,ph_off,method,ph,sinfo) if ok else None
    last=blocks[-1]
    return {"nblocks":len(blocks),"stored_ok":ok,"total":total,"u_len":ph["u_len"],
            "sinfo":sinfo,"last":last,"last_end":last["block"]+12+last["sz_cpr"]}
for cid,src in CARRIERS:
    box=tempfile.mkdtemp(prefix=cid+"-",dir=WORK)
    dst=os.path.join(box,"in"); shutil.copy2(src,dst)
    rc,tail=run(["/usr/bin/upx","--best","-q","-o",os.path.join(box,"p"),dst])
    packed=open(os.path.join(box,"p"),"rb").read()
    rows.append({"carrier":cid,"case":"intact","cls":classify(packed)})
    c=classify(packed); last=c["last"]
    for delta in (-7,7):
        v=last["sz_cpr"]+delta
        if not (0<v<=last["sz_unc"]): continue
        t=bytearray(packed); struct.pack_into("<I",t,last["block"]+4,v)
        rows.append({"carrier":cid,"case":f"tamper{delta}","cls":classify(bytes(t))})
print(json.dumps(rows,indent=1))
