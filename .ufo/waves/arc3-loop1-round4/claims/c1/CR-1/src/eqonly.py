"""A deliberately SOLC-SHAPED extractor: EQ;PUSH2;JUMPI only (the r1/r3 recipe).
   Demonstrates the shape-blind 'false honest-stop': it returns EMPTY on a fully-recovered Vyper carrier."""
import sys, json, glob, os
sys.path.insert(0,'.')
from disasm import dis
def eqonly(code):
    d=dis(code); by={o[0]:(o[1],o[2]) for o in d}
    sels=set()
    for off,n,imm,nx in d:
        if n!='PUSH4': continue
        j=nx; comp=None
        for _ in range(4):
            t=by.get(j)
            if not t: break
            if t[0]=='EQ': comp='EQ'; j+=1; continue
            if t[0] in ('GT','LT'): comp='GT'; j+=1; continue
            if t[0] in ('DUP1','DUP2','DUP3'): j+=1; continue
            break
        t=by.get(j)
        if comp=='EQ' and t and t[0] in ('PUSH1','PUSH2','PUSH3'):
            w=int(t[0][4:]); after=by.get(j+1+w)
            if after and after[0]=='JUMPI': sels.add(imm)
    return sels
print(f"{'carrier':14} {'EQonly':>7} {'probe':>6} {'planted':>8} {'false-honest-stop?':>20}")
for f in sorted(glob.glob('probe/*.6.4.0.json')):
    b=os.path.basename(f).replace('.6.4.0.json','')
    rp=f'vyout/{b}.runtime.hex'
    if not os.path.exists(rp): continue
    code=bytes.fromhex(open(rp).read().strip().replace('0x',''))
    e=eqonly(code)
    j=json.load(open(f)); d=j.get('data',j)
    p=set(x['selector'].replace('0x','') for x in d['normalized_result']['functions'])
    mids=f'vyout/{b}.methodids.json'
    pl=set(v.replace('0x','') for v in json.load(open(mids)).values()) if os.path.exists(mids) else set()
    flag = 'YES (probe K/K, EQ-only=0)' if (not e and p and p==pl) else ('shape-blind-empty' if not e and p else 'n/a')
    print(f"{b:14} {len(e):>7} {len(p):>6} {len(pl):>8} {flag:>20}")
