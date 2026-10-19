"""Attack 2: decoy census. Every PUSH4 immediate in the code region, classified:
   dispatched (has XOR-chain leg) vs non-dispatch decoy. Report any decoy the probe reported."""
import json, glob, os, sys
sys.path.insert(0,'.')
from disasm import dis
from vyrecon import vyper_dispatch
rows=[]
for f in sorted(glob.glob('probe/*.6.4.0.json')):
    b=os.path.basename(f).replace('.6.4.0.json','')
    rp=f'vyout/{b}.runtime.hex'
    if not os.path.exists(rp): continue
    code=bytes.fromhex(open(rp).read().strip().replace('0x',''))
    sels, legs, tbl, entries = vyper_dispatch(code)
    d=dis(code)
    allp4=[(o,i) for o,n,i,nx in d if n=='PUSH4']
    # also catch selector-shaped byte patterns NOT at PUSH4 boundary (embedded in data)
    raw_embeds=[]
    for target in ['a9059cbb','095ea7b3','2ae1431c']:
        tb=bytes.fromhex(target); st=0
        while True:
            k=code.find(tb,st)
            if k<0: break
            at_push4 = any(o+1==k for o,i in allp4)
            raw_embeds.append((target,k,at_push4))
            st=k+1
    j=json.load(open(f)); dd=j.get('data',j)
    probe=set(x['selector'].replace('0x','') for x in dd['normalized_result']['functions'])
    decoy=[i for o,i in allp4 if i not in sels]
    decoy_reported=[i for i in decoy if i in probe]
    rows.append((b,len(allp4),len(sels),decoy,decoy_reported,raw_embeds))
    print(f"--- {b}: PUSH4s={len(allp4)} dispatched={len(sels)} decoys={decoy} decoy_reported={decoy_reported}")
    for t,k,at in raw_embeds:
        print(f"      embedded {t} @byte {k} (at PUSH4 operand: {at})")
