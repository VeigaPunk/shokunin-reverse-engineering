#!/usr/bin/env python3
"""EX-11 independent opcode-boundary walker: no reuse of EX-7's dispatch-walk.py."""
import json, sys, hashlib
NAMES = {0x00:'STOP',0x01:'ADD',0x02:'MUL',0x03:'SUB',0x04:'DIV',0x10:'LT',0x11:'GT',0x14:'EQ',0x15:'ISZERO',0x1c:'SHR',0x35:'CALLDATALOAD',0x36:'CALLDATASIZE',0x52:'MSTORE',0x56:'JUMP',0x57:'JUMPI',0x5b:'JUMPDEST',0x5f:'PUSH0',0x80:'DUP1',0x81:'DUP2',0x90:'SWAP1',0xfd:'REVERT',0xfe:'INVALID',0x34:'CALLVALUE',0x33:'CALLER',0x32:'ORIGIN',0x30:'ADDRESS',0x50:'POP',0x5a:'GAS'}
def opname(o):
    if 0x63<=o<=0x7f: return 'PUSH%d'%(o-0x5f)
    if 0x60<=o<=0x62: return 'PUSH%d'%(o-0x5f)
    return NAMES.get(o,'0x%02x'%o)
def disasm(code):
    pc=0; out=[]
    while pc<len(code):
        o=code[pc]
        n = (o-0x5f) if 0x60<=o<=0x7f else 0
        imm = code[pc+1:pc+1+n]
        out.append({'pc':pc,'op':o,'name':opname(o),'imm':imm.hex(),'imm_int':int.from_bytes(imm,'big') if imm else None})
        pc += 1+n
    return out
def main(path, abi_path=None):
    raw=open(path,'rb').read()
    try:
        txt=raw.decode('ascii').strip()
        code=bytes.fromhex(txt)
    except (UnicodeDecodeError, ValueError):
        code=raw
    ins=disasm(code)
    push4=[i for i in ins if i['op']==0x63]
    sel=set()
    if abi_path:
        mi=json.load(open(abi_path)); sel=set(mi.values())
    # EQ legs: look for triplets EQ(0x14) PUSH2 JUMPI inside a DUP1 ... pattern
    eq_legs=[]
    for k,i in enumerate(ins):
        if i['op']==0x14 and k+2 < len(ins) and 0x60<=ins[k+1]['op']<=0x63 and ins[k+2]['op']==0x57:
            eq_legs.append({'eq_pc':i['pc'],'dst':ins[k+1]['imm_int'],'dst_width':ins[k+1]['op']-0x5f,'imm':None})
    # attach the PUSH4 preceding each EQ leg (search backwards within 6 bytes for op 0x63)
    by_pc={x['pc']:x for x in ins}
    for leg in eq_legs:
        for delta in range(1,14):
            x=by_pc.get(leg['eq_pc']-delta)
            if x and x['op']==0x63: leg['imm']=x['imm']; leg['push4_pc']=x['pc']; break
        if 'push4_pc' not in leg: leg['push4_pc']=None
    # SUB terminator: PUSH4 imm SUB PUSH2 dst JUMPI
    subs=[]
    idx={x['pc']:k for k,x in enumerate(ins)}
    for i in push4:
        k=idx[i['pc']]
        if k+3 < len(ins) and ins[k+1]['op']==0x03 and 0x60<=ins[k+2]['op']<=0x63 and ins[k+3]['op']==0x57:
            subs.append({'push4_pc':i['pc'],'imm':i['imm'],'dst':ins[k+2]['imm_int'],'ctx':code[i['pc']:i['pc']+10].hex()})
    # GT legs
    gt=[]
    for k,i in enumerate(ins):
        if i['op']==0x11 and k+2 < len(ins) and 0x60<=ins[k+1]['op']<=0x63 and ins[k+2]['op']==0x57:
            imm=None; ppc=None
            for delta in range(1,14):
                x=by_pc.get(i['pc']-delta)
                if x and x['op']==0x63: imm=x['imm']; ppc=x['pc']; break
            gt.append({'gt_pc':i['pc'],'dst':ins[k+1]['imm_int'],'imm':imm,'push4_pc':ppc})
    seq=[l['imm'] for l in eq_legs if l['imm']]
    def spc(l): return l['push4_pc'] if l['push4_pc'] is not None else l['eq_pc']
    gaps=[spc(eq_legs[k+1])-spc(eq_legs[k]) for k in range(len(eq_legs)-1)]
    jumpdests=set(i['pc'] for i in ins if i['op']==0x5b)
    push2_targets=set(i['imm_int'] for i in ins if i['op']==0x61)
    res={
      'file':path,'runtime_len':len(code),'sha256':hashlib.sha256(code).hexdigest(),
      'head_hex':code[:40].hex(),
      'push4_count':len(push4),'push4_imms':[i['imm'] for i in push4],
      'push4_selector_hits':sum(1 for i in push4 if i['imm'] in sel),
      'eq_legs':eq_legs,'eq_imms':seq,
      'eq_sorted_ascending':seq==sorted(seq),
      'eq_gaps':gaps,'eq_all_dst_jumpdest':all(l['dst'] in jumpdests for l in eq_legs),
      'eq_dsts':[l['dst'] for l in eq_legs],
      'sub_legs':subs,'gt_legs':gt,
      'non_selector_push4':[{'pc':i['pc'],'imm':i['imm']} for i in push4 if i['imm'] not in sel],
      'tail_hex':code[-80:].hex(),
      'guard_hex':code[0:32].hex(),
    }
    print(json.dumps(res,indent=1))
    return res
if __name__=='__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv)>2 else None)
