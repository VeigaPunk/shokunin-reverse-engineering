import importlib.util, os, struct, sys, tempfile, secrets, json
LANE="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
def load(p,n):
    sp=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
rep = load(os.path.join(LANE,"tools/round-87/upx-magic-repair.py"),"r87h")
r88 = load(os.path.join(LANE,"tools/round-88/upx-chain-repair.py"),"r88h")
r90 = load(os.path.join(LANE,"tools/round-90/upx-break-repair.py"),"r90h")
v2  = load(os.path.join(LANE,"tools/round-92/stop-boundary-battery-v2.py"),"v2h")
v3  = load(os.path.join(LANE,"tools/round-93/stop-boundary-repair-battery-v3.py"),"v3h")
raw=open("/usr/bin/env","rb").read()
nonce=secrets.token_hex(8); mut,mi=v3.mutate_source(raw,nonce)
p=os.path.join(tempfile.mkdtemp(),"s.bin"); open(p,"wb").write(mut); os.chmod(p,0o755)
work=tempfile.mkdtemp(); P=v2.pack(p,work,v2.env_for(work))
b0,blocks=v2.layout(P,rep,r88); last=blocks[-1]
ph_off,ph=rep.find_packheader(P)
lo=max(1,last["sz_cpr"]-16); hi=min(last["sz_unc"],last["sz_cpr"]+16)
print("stored",last["sz_cpr"],"window",lo,hi,"ph_off",ph_off)
# for each candidate v, walk the chain with v substituted and record where it lands
res=[]
for v in range(lo,hi+1):
    t=bytearray(P); struct.pack_into("<I",t,last["block"]+4,v); t=bytes(t)
    try:
        found=r90.longest_prefix(t,rep,r88)
    except Exception as e:
        found=None
    landed=None
    if found is not None:
        m_,b0_,ph2_,blocks2_,meth_=found
        landed=(len(blocks2_), blocks2_[-1]["block"] if blocks2_ else None)
    res.append((v,landed))
for v,l in res: print("v",v,"walk->",l)
# which v makes the chain land EXACTLY on ph_off after the last block?
print("pristine v would be", last["sz_cpr"])
