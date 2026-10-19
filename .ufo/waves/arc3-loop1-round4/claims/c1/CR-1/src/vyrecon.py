"""CR-1 r4: independent byte-level Vyper dispatch extractor + 3-way reconcile.
Derives the dispatch set from the BUCKET TABLE + XOR chain, not from the probe.
"""
import json, glob, os, sys
sys.path.insert(0,'.')
from disasm import dis

def vyper_dispatch(code):
    """Return (set_of_selectors, detail). Independent derivation:
       prologue: PUSH0 CALLDATALOAD PUSH1 e0 SHR [PUSH1 02 PUSH1 N DUP3 MOD PUSH1 01 SHL PUSH2 base ADD PUSH1 1e CODECOPY PUSH0 MLOAD JUMP]
       K1 shape has no table: falls straight to the chain.
       Chain leg: JUMPDEST PUSH4 <sel> DUP2 XOR PUSH2 <next> JUMPI ...
       Bucket table: 2*N bytes at `base`; each entry = 2-byte dest (big-endian) pointing at a JUMPDEST.
    """
    d = dis(code)
    by_off = {o[0]: o for o in d}
    sels = set(); legs = []; table_entries = []
    # find chain legs: PUSH4 followed by DUP2 XOR PUSH2 JUMPI
    for off, name, imm, nxt in d:
        if name == 'PUSH4':
            if (by_off.get(nxt) and by_off[nxt][1]=='DUP2'
                and by_off.get(nxt+1) and by_off[nxt+1][1]=='0x18'
                and by_off.get(nxt+2) and by_off[nxt+2][1]=='PUSH2'
                and by_off.get(nxt+5) and by_off[nxt+5][1]=='JUMPI'):
                sels.add(imm); legs.append((off, imm, by_off[nxt+2][2], nxt+6))
    # bucket table
    tblbase = None
    for off,name,imm,nxt in d:
        if off == 14 and name=='PUSH2': tblbase = int(imm,16); break
    if tblbase is not None:
        n = None
        for off,name,imm,nxt in d:
            if off == 7 and name=='PUSH1': n = int(imm,16); break
        for i in range(n):
            e = int.from_bytes(code[tblbase+2*i: tblbase+2*i+2],'big')
            table_entries.append((i,e, code[e] if e < len(code) else None))
    return sels, legs, tblbase, table_entries

def main():
    rows=[]
    for f in sorted(glob.glob('probe/*.6.4.0.json')):
        b=os.path.basename(f).replace('.6.4.0.json','')
        rp = f'vyout/{b}.runtime.hex'
        if not os.path.exists(rp): continue
        code = bytes.fromhex(open(rp).read().strip().replace('0x',''))
        sels, legs, tbl, entries = vyper_dispatch(code)
        j = json.load(open(f)); d = j.get('data', j)
        probe = set(x['selector'].replace('0x','') for x in d['normalized_result']['functions'])
        mids = json.load(open(f'vyout/{b}.methodids.json')) if os.path.exists(f'vyout/{b}.methodids.json') else {}
        planted = set(v.replace('0x','') for v in mids.values())
        miss_p = sorted(planted - probe); extra_p = sorted(probe - planted)
        miss_c = sorted(planted - sels);  extra_c = sorted(sels - planted)
        miss_pc = sorted(sels - probe);   extra_pc = sorted(probe - sels)
        # bucket entry validity: every non-zero entry must land on JUMPDEST
        bad = [(i,e,h) for (i,e,h) in entries if e != 0 and h != 0x5b]
        rows.append(dict(b=b, n=len(code), Kp=len(planted), Kn=len(probe), Kc=len(sels),
                         miss_p=miss_p, extra_p=extra_p, miss_c=miss_c, extra_c=extra_c,
                         miss_pc=miss_pc, extra_pc=extra_pc, tbl=tbl, nent=len(entries), bad=bad,
                         legs=legs))
    print(f"{'carrier':14} {'B':>5} {'Kp':>3} {'Kn':>3} {'Kc':>3} {'plant-miss':12} {'plant-extra':12} {'census-miss':12} {'census-extra':12} {'tblBad':6} verdict")
    allok=True
    for r in rows:
        ok = not (r['miss_p'] or r['extra_p'] or r['miss_c'] or r['extra_c'] or r['miss_pc'] or r['extra_pc'] or r['bad'])
        allok = allok and ok
        print(f"{r['b']:14} {r['n']:>5} {r['Kp']:>3} {r['Kn']:>3} {r['Kc']:>3} {str(r['miss_p']):12} {str(r['extra_p']):12} {str(r['miss_c']):12} {str(r['extra_c']):12} {len(r['bad']):<6} {'OK' if ok else 'FAIL'}")
    print("\nALL THREE-WAY K/K:", allok, f"| carriers={len(rows)}")
    if __name__ == '__main__':
        import os as _os
        _os.makedirs('recon', exist_ok=True)
        json.dump(rows, open('recon/vyrecon.json','w'), indent=1)


if __name__ == '__main__':
    main()
