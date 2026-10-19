import json, sys
# minimal opcode table for push widths and named ops we care about
PUSH = {i: i-0x5f for i in range(0x60, 0x80)}
def ops(code):
    out=[]; i=0; n=len(code)
    while i<n:
        op=code[i]; size=PUSH.get(op,0)
        imm=code[i+1:i+1+size]
        out.append((i,op,imm))
        i += 1+size
    return out
def walk(path):
    code=open(path,'rb').read()
    ins=ops(code)
    pushes=[(pc,op,imm) for pc,op,imm in ins if 0x63<=op<=0x67]  # PUSH4..PUSH8
    p4=[(pc,imm) for pc,op,imm in pushes if op==0x63]
    # find dispatch prologue: 5f 35 60 e0 1c
    head=code[:64].hex()
    pro_pc=None
    for pc in range(len(code)-5):
        if code[pc:pc+5]==bytes.fromhex('5f3560e01c'): pro_pc=pc; break
    # guard: PUSH1 4 CALLDATASIZE LT/GT ISZERO? PUSH2 dst JUMPI
    guard=None
    for idx,(pc,op,imm) in enumerate(ins):
        if op==0x60 and imm==b'\x04' and idx+1<len(ins) and ins[idx+1][1]==0x36:
            seq=ins[idx:idx+8]
            guard={'at':pc,'seq':[(p,hex(o),m.hex()) for p,o,m in seq]}
            break
    # EQ legs of form DUP1 PUSH4 <sel> EQ PUSH2 dst JUMPI
    eq=[]
    for idx,(pc,op,imm) in enumerate(ins):
        if op==0x63 and idx>=1 and ins[idx-1][1]==0x80 and idx+1<len(ins) and ins[idx+1][1]==0x14:
            nxt=ins[idx+2:idx+4]
            dst=None
            if len(nxt)==2 and nxt[0][1]==0x61 and nxt[1][1]==0x57:
                dst=int.from_bytes(nxt[0][2],'big')
            eq.append({'selector':imm.hex(),'site_pc':pc,'dst':dst})
    # SUB legs: PUSH4 <sel> SUB PUSH2 dst JUMPI
    sub=[]
    for idx,(pc,op,imm) in enumerate(ins):
        if op==0x63 and idx+1<len(ins) and ins[idx+1][1]==0x03:
            nxt=ins[idx+2:idx+4]
            dst=None
            if len(nxt)==2 and nxt[0][1]==0x61 and nxt[1][1]==0x57:
                dst=int.from_bytes(nxt[0][2],'big')
            sub.append({'selector':imm.hex(),'site_pc':pc,'dst':dst,'prev_op':hex(ins[idx-1][1]) if idx else None})
    # GT pivots: PUSH4 <sel> GT PUSH2 ...
    gt=[]
    for idx,(pc,op,imm) in enumerate(ins):
        if op==0x63 and idx+1<len(ins) and ins[idx+1][1]==0x11:
            gt.append({'selector':imm.hex(),'site_pc':pc})
    # all PUSH4 immediates
    allp4=[(pc,imm.hex()) for pc,imm in p4]
    # sortedness of EQ
    sels=[e['selector'] for e in eq]
    dsts=[e['dst'] for e in eq]
    jumpdests={pc for pc,op,imm in ins if op==0x5b}
    return {'path':path,'len':len(code),'head':head,'prologue_pc':pro_pc,
            'guard':guard,'eq_count':len(eq),'eq':eq,
            'eq_sorted_ascending': sels==sorted(sels),
            'eq_pc_gaps':[eq[i+1]['site_pc']-eq[i]['site_pc'] for i in range(len(eq)-1)],
            'all_eq_dst_jumpdest': all(d in jumpdests for d in dsts if d is not None),
            'sub_legs':sub,'gt_pivots':gt,
            'push4_sites':len(allp4),'push4_distinct':len({s for _,s in allp4}),
            'push4_all':allp4,
            'dst_are_jumpdests':{str(d):(d in jumpdests) for d in dsts if d is not None},
            'sub_dst_is_jumpdest':{str(s['dst']):(s['dst'] in jumpdests) for s in sub if s['dst'] is not None}}
if __name__=='__main__':
    print(json.dumps(walk(sys.argv[1]), indent=1))
