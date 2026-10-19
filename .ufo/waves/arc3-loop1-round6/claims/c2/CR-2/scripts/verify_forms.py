#!/usr/bin/env python3
"""Verify the three Vyper 0.4.3 dispatch forms on the two r6 carriers.

Usage: run from a dir containing out/ (CarrierV) and out2/ (Ex09Vault)
built by the r6 compile flags. Prints structural facts only; no probe data.
"""
import pathlib, sys
sys.path.insert(0,'scripts')
from evmdis import disasm

def check_chain(root, leg, kind):
    code=(pathlib.Path(root)/leg/'runtime.bin').read_bytes()
    ins=list(disasm(code)); legs=[]
    for idx,(s,n,i,h) in enumerate(ins):
        if n!='PUSH4' or h=='08c379a0': continue
        tail=[n2 for q,n2,i2,h2 in ins[idx+1:idx+6]]
        legs.append((s,h,tail))
    want = ['DUP2','XOR','PUSH2','JUMPI'] if kind=='A' else ['DUP2','EQ','ISZERO','PUSH2','JUMPI']
    print(f'{root} {leg}: PUSH4 selector legs={len(legs)} shape_ok={all(t[:len(want)]==want for _,_,t in legs)}')
    if kind=='B':
        tg=[]
        for idx,(s,n,i,h) in enumerate(ins):
            if n=='PUSH4' and h!='08c379a0':
                tg.append([x for x in ins[idx+1:idx+6] if x[1]=='PUSH2'][0][2])
        print(f'  next-test targets={tg} all_jumpdest={all(code[t]==0x5b for t in tg)}')

check_chain('out','default','A'); check_chain('out2','default','A')
check_chain('out','noopt','B'); check_chain('out2','noopt','B')

for carrier,root in (('CarrierV','out'),('Ex09Vault','out2')):
    code=(pathlib.Path(root)/'codesize'/'runtime.bin').read_bytes()
    ins=list(disasm(code))
    first_copy=next(idx for idx,(s,n,i,h) in enumerate(ins) if n=='CODECOPY')
    nb = 2 if any(n=='DUP4' for s,n,i,h in ins[:first_copy]) else 1
    base=[i for s,n,i,h in ins if n=='PUSH2' and s<30 and i<len(code)][0]
    print(f'{carrier} codesize: len={len(code)} buckets={nb} table_base={base:#x}')
    allok=True; dests=[]
    for b in range(nb):
        e=code[base+5*b:base+5*b+5]
        mult=(e[0]<<8)|e[1]; cnt=e[4]; start=(e[2]<<8)|e[3]
        print(f'  bucket {b}: entry={e.hex()} mult={mult:#06x} count={cnt} rec_base={start:#06x}')
        for i in range(cnt):
            r=code[start+7*i:start+7*i+7]
            sel=int.from_bytes(r[:4],'big'); dest=(r[4]<<8)|r[5]; flags=r[6]
            slot=((mult*sel)>>24)%cnt
            allok = allok and slot==i
            dests.append(dest)
            print(f'    slot{i}: {r.hex()} sel={sel:08x} dest={dest:#06x} flags={flags:#02x} hash_slot={slot}')
    print(f'  perfect-hash slot identity on every record: {allok}')
    print(f'  all {len(dests)} record dests are JUMPDEST: {all(code[d]==0x5b for d in dests)}')
