#!/usr/bin/env python3
import hashlib, pathlib, sys

N = {
 0x00:'STOP',0x01:'ADD',0x02:'MUL',0x03:'SUB',0x04:'DIV',0x05:'SDIV',0x06:'MOD',
 0x07:'SMOD',0x08:'ADDMOD',0x09:'MULMOD',0x0a:'EXP',0x10:'LT',0x11:'GT',0x12:'SLT',
 0x13:'SGT',0x14:'EQ',0x15:'ISZERO',0x16:'AND',0x17:'OR',0x18:'XOR',0x19:'NOT',
 0x1a:'BYTE',0x1b:'SHL',0x1c:'SHR',0x20:'KECCAK256',0x30:'ADDRESS',0x31:'BALANCE',
 0x32:'ORIGIN',0x33:'CALLER',0x34:'CALLVALUE',0x35:'CALLDATALOAD',0x36:'CALLDATASIZE',
 0x37:'CALLDATACOPY',0x38:'CODESIZE',0x39:'CODECOPY',0x3a:'GASPRICE',0x40:'BLOCKHASH',
 0x41:'COINBASE',0x42:'TIMESTAMP',0x43:'NUMBER',0x44:'PREVRANDAO',0x45:'GASLIMIT',
 0x46:'CHAINID',0x47:'SELFBALANCE',0x48:'BASEFEE',0x50:'POP',0x51:'MLOAD',0x52:'MSTORE',
 0x53:'MSTORE8',0x54:'SLOAD',0x55:'SSTORE',0x56:'JUMP',0x57:'JUMPI',0x58:'PC',
 0x5a:'GAS',0x5b:'JUMPDEST',0x5f:'PUSH0',0xf0:'CREATE',0xf1:'CALL',0xf3:'RETURN',
 0xfa:'STATICCALL',0xfd:'REVERT',0xfe:'INVALID',0xff:'SELFDESTRUCT'}
for i in range(1,17): N[0x7f+i] = f'DUP{i}'
for i in range(1,17): N[0x8f+i] = f'SWAP{i}'
for i in range(0x60,0x80): N[i] = f'PUSH{i-0x5f}'

def decode(p):
    raw = p.read_text().strip()
    if raw.startswith('0x'): raw=raw[2:]
    code=bytes.fromhex(raw); out=[]; i=0
    while i<len(code):
        pc=i; op=code[i]; i+=1
        if 0x60<=op<=0x7f:
            n=op-0x5f; imm=code[i:i+n]; i+=n
            out.append((pc,N[op],imm.hex(),i))
        else: out.append((pc,N.get(op,f'0x{op:02x}'),'',i))
    return code,out

for arg in sys.argv[1:]:
    p=pathlib.Path(arg); code,ins=decode(p); by={pc:i for i,(pc,*_) in enumerate(ins)}
    push4=[(pc,imm) for pc,n,imm,_ in ins if n=='PUSH4']
    print(f'FILE={p.name} bytes={len(code)} sha256={hashlib.sha256(code).hexdigest()} hex_file_bytes={p.stat().st_size}')
    print(f'PUSH4_COUNT={len(push4)} PUSH4={push4}')
    print('OP_COUNTS='+' '.join(f'{name}:{sum(1 for _,n,_,_ in ins if n==name)}' for name in ('EQ','XOR','MOD','CODECOPY','JUMPDEST','JUMPI')))
    print('EQ_WINDOWS:')
    for j,(pc,n,imm,nxt) in enumerate(ins):
        if n=='EQ':
            lo=max(0,j-5); hi=min(len(ins),j+5)
            print('  '+' '.join(f'{x:04x}:{y}'+(f' {z}' if z else '') for x,y,z,_ in ins[lo:hi]))
    print('PREFIX:')
    print('  '+' '.join(f'{pc:04x}:{n}'+(f' {imm}' if imm else '') for pc,n,imm,_ in ins[:min(100,len(ins))]))
    print('---')
