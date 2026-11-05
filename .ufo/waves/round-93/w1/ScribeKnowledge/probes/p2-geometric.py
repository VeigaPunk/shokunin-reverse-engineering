import importlib.util, os, struct, sys, subprocess, tempfile
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
def load(p,n):
    sp=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
rep = load(os.path.join(LANE,"tools/round-87/upx-magic-repair.py"),"r87g")
r88 = load(os.path.join(LANE,"tools/round-88/upx-chain-repair.py"),"r88g")
r90 = load(os.path.join(LANE,"tools/round-90/upx-break-repair.py"),"r90g")
v2  = load(os.path.join(LANE,"tools/round-92/stop-boundary-battery-v2.py"),"v2g")
src = "/usr/bin/env"
import secrets
raw = open(src,"rb").read()
# build a nonce-marked mutated source like v3 does
sys.path.insert(0,"")
v3 = load(os.path.join(LANE,"tools/round-93/stop-boundary-repair-battery-v3.py"),"v3g")
nonce = secrets.token_hex(8)
mut, minfo = v3.mutate_source(raw, nonce)
p = os.path.join(tempfile.mkdtemp(), "src.bin")
open(p,"wb").write(mut); os.chmod(p,0o755)
work = tempfile.mkdtemp()
P = v2.pack(p, work, v2.env_for(work))
b0, blocks = v2.layout(P, rep, r88)
last = blocks[-1]
ph_off, ph = rep.find_packheader(P)
print("last block offset", last["block"], "stored sz_cpr", last["sz_cpr"], "sz_unc", last["sz_unc"])
print("packheader offset", ph_off)
print("last.block+12+stored =", last["block"]+12+last["sz_cpr"], " == ph_off?", last["block"]+12+last["sz_cpr"]==ph_off)
print("u_len", ph.get("u_len"), "walk total", sum(b["sz_cpr"]+12 for b in blocks))
# enumerate candidates: which v in (stored-16, stored+16] satisfy the geometry?
geoms=[v for v in range(max(1,last["sz_cpr"]-16), min(last["sz_unc"],last["sz_cpr"]+16)+1) if last["block"]+12+v==ph_off]
print("geometric candidates (chain lands exactly on packheader):", geoms)
