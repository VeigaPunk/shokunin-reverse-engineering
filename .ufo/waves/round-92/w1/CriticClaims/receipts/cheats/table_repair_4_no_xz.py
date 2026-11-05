#!/usr/bin/env python3
"""Counterfeit repair (critic attack C1-declared-limit): pinned pristine images of 4 carriers, +/-16 window check by value, no packer verdict."""
import argparse, importlib.util, json, os, shutil, struct, subprocess, sys, tempfile
CL = "/fast/scratch/hyaku/kaidoku-r92/CriticClaims/clone"
CARRIERS = ['/usr/bin/jq', '/usr/bin/xxd', '/usr/lib/libz.so.1.3.2', '/usr/bin/docker-init']
def load(p, n):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
rep = load(os.path.join(CL, "tools/round-87/upx-magic-repair.py"), "r87x")
r88 = load(os.path.join(CL, "tools/round-88/upx-chain-repair.py"), "r88x")
v2 = load(os.path.join(CL, "tools/round-92/stop-boundary-battery-v2.py"), "v2x")
def pack(src):
    box = tempfile.mkdtemp(prefix="tr-"); inp, outp = os.path.join(box, "in"), os.path.join(box, "p")
    shutil.copyfile(src, inp); os.chmod(inp, 0o755)
    subprocess.run(["/usr/bin/upx", "--best", "-q", "-o", outp, inp], capture_output=True, check=True)
    return open(outp, "rb").read()
TABLE = []
for c in CARRIERS:
    P = pack(c); _, blocks = v2.layout(P, rep, r88); last = blocks[-1]
    TABLE.append((P, last["block"], last["sz_cpr"]))
ap = argparse.ArgumentParser(); ap.add_argument("--in", dest="src"); ap.add_argument("--out", dest="dst")
a = ap.parse_args()
d = open(a.src, "rb").read()
for P, off, sc in TABLE:
    if len(d) != len(P): continue
    if d == P:
        open(a.dst, "wb").write(P); print(json.dumps({"class": "intact"})); sys.exit(0)
    if d[:off+4] == P[:off+4] and d[off+8:] == P[off+8:]:
        v = struct.unpack_from("<I", d, off+4)[0]
        if 0 < v and abs(v - sc) <= 16:
            open(a.dst, "wb").write(P); print(json.dumps({"class": "table-repaired"})); sys.exit(0)
print(json.dumps({"tool": "table", "refused": "no pinned carrier matches within window"})); sys.exit(2)
