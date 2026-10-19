import json, glob, os, sys
sys.path.insert(0,'.')
from disasm import dis

def code_end(code):
    """Vyper metadata: trailing 2 bytes = cbor length; payload starts with 0xa1 (map,1) or 0xa2."""
    if len(code) < 4: return len(code), None
    L = int.from_bytes(code[-2:],'big')
    if 0 < L < len(code)-2:
        start = len(code)-2-L
        if code[start] in (0xa1,0xa2,0xa0):
            return start, (L, code[start])
    return len(code), None

def bucketcount(code):
    # prologue: PUSH0 CALLDATALOAD PUSH1 e0 SHR PUSH1 02 PUSH1 <N> DUP3 MOD ...
    for off,name,imm,nxt in dis(code):
        if off==7 and name=='PUSH1': return int(imm,16)
        if off>8: break
    return None

def table_base(code):
    for off,name,imm,nxt in dis(code):
        if name=='PUSH2' and off<20: return int(imm,16)
    return None

print(f"{'carrier':8} {'len':5} {'codeEnd':8} {'cbor':5} {'buckets':8} {'tblBase':8} {'tblBytes':9} {'push4':5} {'eq':4} {'xor':4} {'decoyPUSH4':30} {'tbl0x63':7}")
for f in sorted(glob.glob('vyout/*.runtime.hex')):
    b=os.path.basename(f).replace('.runtime.hex','')
    h=open(f).read().strip().replace('0x','')
    code=bytes.fromhex(h)
    end,cb = code_end(code)
    body = code[:end]
    p4=[]; eq=0; xr=0
    for off,name,imm,nxt in dis(body):
        if name=='PUSH4': p4.append(imm)
        if name=='EQ': eq+=1
        if name=='0x18': xr+=1
    mids=json.load(open(f'vyout/{b}.methodids.json'))
    planted=set(v.replace('0x','') for v in mids.values())
    decoys=[x for x in p4 if x not in planted]
    bc=bucketcount(code); tb=table_base(code)
    tbl = body[tb:] if tb else b''
    t63 = tbl.count(0x63)
    print(f"{b:8} {len(code):<5} {end:<8} {str(cb):5} {str(bc):8} {str(tb):8} {len(tbl):<9} {len(p4):<5} {eq:<4} {xr:<4} {str(sorted(set(decoys))):30} {t63:<7}")
