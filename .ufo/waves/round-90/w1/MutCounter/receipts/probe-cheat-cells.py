"""Rebuild the counter's 14 scored cells plus N1/N2/N3 fixtures and run one
repair command on each, scoring the same arms the counter scores (without REA,
which is deterministic given the unpack pin).  argv: repair_cmd out_json"""
import hashlib, importlib.util, json, os, shutil, struct, subprocess, sys, tempfile
LANE="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S="/fast/scratch/hyaku/kaidoku-r90/MutCounter"
CARRIERS=[{"id":"jq","source":"/usr/bin/jq","sha256":"e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806","p1":True},
          {"id":"xxd","source":"/usr/bin/xxd","sha256":"7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65","p1":True},
          {"id":"libz","source":"/usr/lib/libz.so.1.3.2","sha256":"6c78c5e58c3bb49a1cd151a95cdf1a17fe07a91a57a59e0279b984c533075ca9","p1":False},
          {"id":"dinit","source":"/usr/bin/docker-init","sha256":"0bd49c8d4da5601ce955c24a515917c9a132404df633c1e2fa28855cc2e3e115","p1":True}]
def load(p,n):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
rep=load(LANE+"/tools/round-87/upx-magic-repair.py","r87"); r88=load(LANE+"/tools/round-88/upx-chain-repair.py","r88")
spec=importlib.util.spec_from_file_location("bat",LANE+"/tools/round-90/upx-later-block-battery.py")
bat=importlib.util.module_from_spec(spec); spec.loader.exec_module(bat)
cmd=sys.argv[1]; outjson=sys.argv[2]
root=tempfile.mkdtemp(prefix="cells-",dir=S)
env={"HOME":root+"/home","LANG":"C","PATH":os.environ["PATH"],"TMPDIR":root+"/tmp"}
os.makedirs(env["HOME"]); os.makedirs(env["TMPDIR"])
cells=[]; ctrl={}
for c in CARRIERS:
    d=os.path.join(root,c["id"]); os.makedirs(d)
    orig=os.path.join(d,"orig"); shutil.copy2(c["source"],orig)
    packed=os.path.join(d,"packed")
    subprocess.run(["/usr/bin/upx","--best","-q","-o",packed,orig],check=True,capture_output=True)
    pbytes=open(packed,"rb").read(); pin=hashlib.sha256(pbytes).hexdigest()
    b0,blocks=bat.layout(pbytes,rep,r88)
    def score(tag,blk,value,base=None):
        t=bytearray(pbytes); struct.pack_into("<I",t,blk["block"]+4,value)
        box=tempfile.mkdtemp(prefix="box-",dir=root); src=box+"/in"; dst=box+"/out"
        open(src,"wb").write(t)
        r=subprocess.run([sys.executable,"-I","-B",cmd,"--in",src,"--out",dst],env=env,capture_output=True,text=True)
        out=open(dst,"rb").read() if r.returncode==0 and os.path.isfile(dst) else None
        arms={"repair_rc0":out is not None}
        if out is not None:
            ok,why=bat.window_only(bytes(t),out,{"block":blk["block"]})
            arms["field_only"]=ok
            arms["identity"]=hashlib.sha256(out).hexdigest()==pin
            rt=tempfile.mkstemp(dir=root)[1]; open(rt,"wb").write(out)
            arms["test_ok"]=subprocess.run(["/usr/bin/upx","-t","-q",rt],env=env,capture_output=True).returncode==0
            up=rt+".u"; dd=subprocess.run(["/usr/bin/upx","-d","-q","-o",up,rt],env=env,capture_output=True)
            arms["unpack_pin"]=dd.returncode==0 and hashlib.sha256(open(up,"rb").read()).hexdigest()==c["sha256"]
        cells.append({"carrier":c["id"],"cell":tag,"rc":r.returncode,"arms":arms,
                      "recovered":out is not None and all(v for v in arms.values()),
                      "stderr":r.stdout.strip()[-90:]})
    if c["p1"]:
        blk=blocks[1]
        for delta in (-7,7):
            score(f"P1{delta:+d}",blk,blk["sz_cpr"]+delta)
    score("P2",blocks[0],blocks[0]["sz_cpr"]-7)
    score("P3",blocks[0],0)
    # N1 plain, N2 payload flip, N3 intact
    box=tempfile.mkdtemp(prefix="box-",dir=root); src=box+"/in"; dst=box+"/out"
    open(src,"wb").write(open(orig,"rb").read())
    r=subprocess.run([sys.executable,"-I","-B",cmd,"--in",src,"--out",dst],env=env,capture_output=True)
    ctrl[f"N1-{c['id']}"]={"rc":r.returncode,"refused":r.returncode!=0}
    corrupt=bytearray(pbytes); corrupt[blocks[1]["block"]+12+blocks[1]["sz_cpr"]//2]^=0xFF
    box=tempfile.mkdtemp(prefix="box-",dir=root); src=box+"/in"; dst=box+"/out"
    open(src,"wb").write(corrupt)
    r=subprocess.run([sys.executable,"-I","-B",cmd,"--in",src,"--out",dst],env=env,capture_output=True)
    clean=None
    if r.returncode==0 and os.path.isfile(dst):
        clean=subprocess.run(["/usr/bin/upx","-t","-q",dst],env=env,capture_output=True).returncode==0
    ctrl[f"N2-{c['id']}"]={"rc":r.returncode,"packer_clean":clean,"not_recovered":not(r.returncode==0 and clean)}
    box=tempfile.mkdtemp(prefix="box-",dir=root); src=box+"/in"; dst=box+"/out"
    open(src,"wb").write(pbytes)
    r=subprocess.run([sys.executable,"-I","-B",cmd,"--in",src,"--out",dst],env=env,capture_output=True)
    ctrl[f"N3-{c['id']}"]={"rc":r.returncode,"identical":r.returncode==0 and os.path.isfile(dst) and open(dst,"rb").read()==pbytes}
res={"cells":cells,"controls":ctrl,
     "counts":{"P1":sum(1 for x in cells if x["cell"].startswith("P1") and x["recovered"]),
               "P1of":sum(1 for x in cells if x["cell"].startswith("P1")),
               "P2":sum(1 for x in cells if x["cell"]=="P2" and x["recovered"]),
               "P3":sum(1 for x in cells if x["cell"]=="P3" and x["recovered"])},
     "controls_ok":{"N1":all(v["refused"] for v in ctrl.values() if "N1" in k) if False else None}}
res["controls_ok"]={"N1":all(v["refused"] for k,v in ctrl.items() if k.startswith("N1")),
                    "N2":all(v["not_recovered"] for k,v in ctrl.items() if k.startswith("N2")),
                    "N3":all(v["identical"] for k,v in ctrl.items() if k.startswith("N3"))}
json.dump(res,open(outjson,"w"),indent=1)
print(json.dumps({"counts":res["counts"],"controls_ok":res["controls_ok"]}))
for x in cells:
    if not x["recovered"]: print("NOT-RECOVERED",x["carrier"],x["cell"],x["rc"],x["arms"],x["stderr"])
