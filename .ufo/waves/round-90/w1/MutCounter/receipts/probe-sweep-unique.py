"""Re-run of the sz_cpr uniqueness sweep with a unique probe file per task
(the first pass shared 12 slots across 12 threads: a race that could hide or
invent hits).  For each carrier and each of block 0 / block 1, write the field
over 0..sz_unc plus 64 above-range values plus 2000 random 32-bit values and
record every value whose file passes `upx -t -q`."""
import hashlib, json, os, random, struct, subprocess, sys, uuid
from concurrent.futures import ThreadPoolExecutor
import importlib.util
S="/fast/scratch/hyaku/kaidoku-r90/MutCounter"
LANE="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
def load(p,n):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
rep=load(LANE+"/tools/round-87/upx-magic-repair.py","r87"); r88=load(LANE+"/tools/round-88/upx-chain-repair.py","r88")
spec=importlib.util.spec_from_file_location("bat",LANE+"/tools/round-90/upx-later-block-battery.py")
bat=importlib.util.module_from_spec(spec); spec.loader.exec_module(bat)
random.seed(90)
def probe(args):
    tag, packed, off, v = args
    b=bytearray(packed); struct.pack_into("<I",b,off+4,v)
    p=f"{S}/pk/u-{uuid.uuid4().hex}.bin"; open(p,"wb").write(b)
    try:
        r=subprocess.run(["/usr/bin/upx","-t","-q",p],capture_output=True)
        if r.returncode!=0: return None
        d=subprocess.run(["/usr/bin/upx","-d","-q","-o",p+".u",p],capture_output=True)
        sha=hashlib.sha256(open(p+".u","rb").read()).hexdigest() if d.returncode==0 else None
        return {"carrier":tag,"block_off":off,"value":v,"unpack_sha256":sha}
    finally:
        for f in (p,p+".u"):
            try: os.unlink(f)
            except OSError: pass
out=[]
for cid,path,orig in (("jq",f"{S}/pk/jq","/usr/bin/jq"),("xxd",f"{S}/pk/xxd.packed",f"{S}/pk/xxd.orig"),
                      ("libz",f"{S}/pk/libz.packed",f"{S}/pk/libz.orig"),("dinit",f"{S}/pk/dinit.packed",f"{S}/pk/dinit.orig")):
    packed=open(path,"rb").read(); pin=hashlib.sha256(open(orig,"rb").read()).hexdigest()
    b0,blocks=bat.layout(packed,rep,r88)
    for bi in (0,1):
        blk=blocks[bi]; su,sc=blk["sz_unc"],blk["sz_cpr"]
        vals=list(range(0,su+1))+[su+1+j for j in range(64)]+[random.getrandbits(32) for _ in range(2000)]
        hits=[]
        with ThreadPoolExecutor(max_workers=12) as ex:
            for r in ex.map(probe,[(cid,packed,blk["block"],v) for v in vals]):
                if r: hits.append(r)
        stored=[h for h in hits if h["value"]==sc]
        other=[h for h in hits if h["value"]!=sc]
        rec={"carrier":cid,"block_index":bi,"block_off":blk["block"],"sz_unc":su,"sz_cpr":sc,
             "values_tested":len(vals),"stored_passes_upx_t":bool(stored),
             "stored_unpack_sha256":stored[0]["unpack_sha256"] if stored else None,
             "proc_pin":pin,
             "other_values_passing_upx_t":[h["value"] for h in other],
             "stored_is_unique":bool(stored) and not other and
                 (stored[0]["unpack_sha256"]==pin if stored else False)}
        print(json.dumps(rec),flush=True); out.append(rec)
json.dump(out,open(f"{S}/sweep-unique2.json","w"),indent=1)
print("STORED_UNIQUE_ALL", all(r["stored_is_unique"] for r in out))
