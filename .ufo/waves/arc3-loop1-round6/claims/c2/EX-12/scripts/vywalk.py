import json,sys,hashlib

NAMES={0x00:'STOP',0x01:'ADD',0x02:'MUL',0x03:'SUB',0x04:'DIV',0x05:'SDIV',0x06:'MOD',0x07:'SMOD',
0x08:'ADDMOD',0x09:'MULMOD',0x0a:'EXP',0x0b:'SIGNEXTEND',0x10:'LT',0x11:'GT',0x12:'SLT',0x13:'SGT',
0x14:'EQ',0x15:'ISZERO',0x16:'AND',0x17:'OR',0x18:'XOR',0x19:'NOT',0x1a:'BYTE',0x1b:'SHL',0x1c:'SHR',
0x1d:'SAR',0x20:'KECCAK256',0x30:'ADDRESS',0x31:'BALANCE',0x32:'ORIGIN',0x33:'CALLER',0x34:'CALLVALUE',
0x35:'CALLDATALOAD',0x36:'CALLDATASIZE',0x37:'CALLDATACOPY',0x38:'CODESIZE',0x39:'CODECOPY',0x3a:'GASPRICE',
0x3b:'EXTCODESIZE',0x3c:'EXTCODECOPY',0x3d:'RETURNDATASIZE',0x3e:'RETURNDATACOPY',0x3f:'EXTCODEHASH',
0x40:'BLOCKHASH',0x41:'COINBASE',0x42:'TIMESTAMP',0x43:'NUMBER',0x44:'PREVRANDAO',0x45:'GASLIMIT',
0x46:'CHAINID',0x47:'SELFBALANCE',0x48:'BASEFEE',0x50:'POP',0x51:'MLOAD',0x52:'MSTORE',0x53:'MSTORE8',
0x54:'SLOAD',0x55:'SSTORE',0x56:'JUMP',0x57:'JUMPI',0x58:'PC',0x59:'MSIZE',0x5a:'GAS',0x5b:'JUMPDEST',
0x5f:'PUSH0',0xf0:'CREATE',0xf1:'CALL',0xf2:'CALLCODE',0xf3:'RETURN',0xf4:'DELEGATECALL',0xf5:'CREATE2',
0xfa:'STATICCALL',0xfd:'REVERT',0xfe:'INVALID',0xff:'SELFDESTRUCT'}
def nm(op):
    if 0x60<=op<=0x7f: return f'PUSH{op-0x5f}'
    if 0x80<=op<=0x8f: return f'DUP{op-0x7f}'
    if 0x90<=op<=0x9f: return f'SWAP{op-0x8f}'
    if 0xa0<=op<=0xa4: return f'LOG{op-0xa0}'
    return NAMES.get(op,f'0x{op:02x}')
def decode(code):
    ops=[];pc=0
    while pc<len(code):
        op=code[pc]; w=op-0x5f if 0x60<=op<=0x7f else 0
        ops.append((pc,op,code[pc+1:pc+1+w])); pc+=1+w
    return ops

def analyze(path):
    code=open(path,'rb').read(); ops=decode(code)
    dis=lambda i:(ops[i][0],nm(ops[i][1]),ops[i][2].hex())
    push4=[(pc,imm.hex()) for pc,op,imm in ops if op==0x63]
    xor_sites=[]; eq_sites=[]; gt_sites=[]; sub_sites=[]
    for i,(pc,op,imm) in enumerate(ops):
        if op==0x18 and i>0 and nm(ops[i-1][1]) in ('DUP1','DUP2','DUP3','DUP4','DUP5'):
            xor_sites.append(pc)
        if op==0x14: eq_sites.append(pc)
        if op==0x11: gt_sites.append(pc)
        if op==0x03: sub_sites.append(pc)
    # MOD-prologue: find PUSH1 n; DUP3; MOD (0x06)
    mods=[(pc,ops[i-1][2].hex() if i>0 else None) for i,(pc,op,imm) in enumerate(ops) if op==0x06]
    # jump-table prologue detection: CODECOPY right after PUSH1 0x1e; capture preceding PUSH2 base
    tables=[]
    for i,(pc,op,imm) in enumerate(ops):
        if op==0x39 and i>=1 and ops[i-1][1]==0x60 and ops[i-1][2]==b'\x1e':
            base=None
            for j in range(i-1,max(-1,i-8),-1):
                if ops[j][1]==0x61: base=int.from_bytes(ops[j][2],'big'); break
            tables.append({'codecopy_pc':pc,'table_base':base})
    return {'path':str(path),'len':len(code),'sha256':hashlib.sha256(code).hexdigest(),
            'push4_sites':len(push4),'push4_distinct':len({s for _,s in push4}),
            'push4':push4,'xor_sites':len(xor_sites),'eq_sites':len(eq_sites),
            'gt_sites':len(gt_sites),'sub_sites':len(sub_sites),'mod_sites':len(mods),
            'tables':tables,'first40_hex':code[:40].hex(),
            'first12':[dis(i) for i in range(min(12,len(ops)))],
            'tail_hex':code[-40:].hex()}
if __name__=='__main__':
    print(json.dumps([analyze(p) for p in sys.argv[1:]],indent=1))
