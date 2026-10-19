import sys, json, pathlib
OPS = {0x00:'STOP',0x01:'ADD',0x02:'MUL',0x03:'SUB',0x04:'DIV',0x05:'SDIV',0x06:'MOD',0x07:'SMOD',
0x10:'LT',0x11:'GT',0x14:'EQ',0x15:'ISZERO',0x16:'AND',0x1b:'SHL',0x1c:'SHR',0x34:'CALLVALUE',0x35:'CALLDATALOAD',0x36:'CALLDATASIZE',0x50:'POP',0x52:'MSTORE',0x56:'JUMP',0x57:'JUMPI',0x5b:'JUMPDEST',0x5f:'PUSH0',0x80:'DUP1',0x81:'DUP2',0x90:'SWAP1',0xfd:'REVERT'}
def disasm(code):
    pc=0; out=[]
    while pc < len(code):
        op=code[pc]; start=pc; pc+=1
        if 0x60 <= op <= 0x7f:
            n=op-0x5f; imm=code[pc:pc+n]; pc+=n
            out.append((start, 'PUSH%d'%n, imm))
        else:
            out.append((start, OPS.get(op,'0x%02x'%op), None))
    return out
def p4sites(ins): return [(pc, int.from_bytes(imm,'big')) for pc,op,imm in ins if op=='PUSH4']
def push2(ins, pc):
    for p,op,imm in ins:
        if p==pc and op=='PUSH2': return int.from_bytes(imm,'big')
    return None
def analyze(path):
    code=pathlib.Path(path).read_bytes()
    ins=disasm(code); by={pc:(op,imm) for pc,op,imm in ins}
    # EQ chain legs: DUP1 PUSH4 x EQ PUSH2 y JUMPI at p, p+1, p+6, p+11, p+12
    eq=[]; sub=[]
    for p,op,imm in ins:
        if op=='DUP1' and p+10 in by and by[p+1][0]=='PUSH4' and by[p+6][0]=='EQ' \
           and by[p+7][0]=='PUSH2' and by[p+10][0]=='JUMPI':
            eq.append((p, int.from_bytes(by[p+1][1],'big'), int.from_bytes(by[p+7][1],'big')))
        if op=='PUSH4' and p+5 in by and by[p+5][0]=='SUB' and p+6 in by and by[p+6][0]=='PUSH2' \
           and p+9 in by and by[p+9][0]=='JUMPI':
            sub.append((p, int.from_bytes(imm,'big'), int.from_bytes(by[p+6][1],'big')))
    sites=p4sites(ins)
    dsts=[d for _,_,d in eq]
    jd=[pc for pc,op,imm in ins if op=='JUMPDEST']
    return dict(path=str(path), size=len(code), push4_sites=len(sites),
        push4_values=['%08x'%v for _,v in sites],
        eq_legs=len(eq), eq_gaps=sorted({eq[i+1][0]-eq[i][0] for i in range(len(eq)-1)}),
        eq_dsts=dsts, eq_dsts_all_jumpdest=all(d in jd for d in dsts),
        eq_selectors_sorted=[('%08x'%s) for _,s,_ in eq]==sorted('%08x'%s for _,s,_ in eq),
        sub_legs=[('%08x'%s, d, p) for p,s,d in sub],
        sub_dst_jumpdest=[d in jd for _,_,d in sub],
        prologue=code[:24].hex(), gt_sites=sum(1 for pc,op,imm in ins if op=='GT'))
for arg in sys.argv[1:]:
    print(json.dumps(analyze(arg), sort_keys=True))
