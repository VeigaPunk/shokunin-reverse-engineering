import sys
PUSH1_32 = list(range(0x60,0x80))
NAMES = {0x00:'STOP',0x01:'ADD',0x06:'MOD',0x0a:'EXP',0x10:'LT',0x11:'GT',0x14:'EQ',0x15:'ISZERO',
 0x1b:'SHL',0x1c:'SHR',0x35:'CALLDATALOAD',0x36:'CALLDATASIZE',0x37:'CALLDATACOPY',0x39:'CODECOPY',
 0x51:'MLOAD',0x52:'MSTORE',0x54:'SLOAD',0x55:'SSTORE',0x56:'JUMP',0x57:'JUMPI',0x5b:'JUMPDEST',
 0x5f:'PUSH0',0xf3:'RETURN',0xfd:'REVERT',0xfe:'INVALID',0xff:'SELFDESTRUCT'}
for i in range(16): NAMES[0x80+i]=f'DUP{i+1}'
for i in range(16): NAMES[0x90+i]=f'SWAP{i+1}'
for i in range(0xa0,0xa5): NAMES[i]=f'LOG{i-0xa0}'
for i in range(0x60,0x80): NAMES[i]=f'PUSH{i-0x5f}'

def dis(code):
    i=0; out=[]
    while i < len(code):
        op=code[i]; start=i
        if 0x60 <= op <= 0x7f:
            n=op-0x5f
            imm=code[i+1:i+1+n]
            out.append((start,NAMES[op],imm.hex(),i+1+n))
            i+=1+n
        else:
            out.append((start,NAMES.get(op,f'0x{op:02x}'),'',i+1))
            i+=1
    return out
if __name__=='__main__':
    h=open(sys.argv[1]).read().strip()
    if h.startswith('0x'): h=h[2:]
    code=bytes.fromhex(h)
    lo=int(sys.argv[2]) if len(sys.argv)>2 else 0
    hi=int(sys.argv[3]) if len(sys.argv)>3 else len(code)
    for off,name,imm,nxt in dis(code):
        if lo<=off<hi:
            print(f"{off:5} {name:10} {imm[:24]:24} -> {nxt}")
