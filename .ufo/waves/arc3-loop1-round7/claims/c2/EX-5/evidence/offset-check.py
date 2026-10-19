import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
D=ROOT/'out'
P=ROOT/'probe'
OP={0x39:'CODECOPY',0x5b:'JUMPDEST',0x34:'CALLVALUE',0x57:'JUMPI'}
def decode(path):
    return bytes.fromhex(path.read_text().strip().removeprefix('0x'))
def instructions(code):
    i=0; rows=[]
    while i<len(code):
        pc=i; op=code[i]; i+=1
        if 0x60<=op<=0x7f:
            n=op-0x5f; imm=code[i:i+n]; i+=n
            rows.append((pc, f'PUSH{n}', imm.hex()))
        else: rows.append((pc, OP.get(op, f'0x{op:02x}'), ''))
    return rows
for form in ('noopt','codesize'):
    code=decode(D/f'{form}.runtime.hex')
    probe=json.loads((P/f'{form}-6.7.0.json').read_text())
    offsets={x['selector'].removeprefix('0x'):x['bytecode_offset'] for x in probe['normalized_result']['functions']}
    ins=instructions(code)
    if form=='noopt':
        push4={imm:pc for pc,name,imm in ins if name=='PUSH4'}
        pairs=[]
        for sel,off in sorted(offsets.items()):
            pc=push4[sel]
            pairs.append((sel,pc,off,off-pc,code[off]))
        ok=all(pc+12==off and code[off]==0x34 for _,pc,off,_,_ in pairs)
        print(f'noopt: offset_rows={len(pairs)} rule=bytecode_offset=push4_pc+12 and code[offset]=CALLVALUE all={ok}')
        for sel,pc,off,delta,op in pairs: print(f'  selector=0x{sel} push4_pc={pc} offset={off} delta={delta} opcode=0x{op:02x}')
    else:
        copy_i=next(i for i,x in enumerate(ins) if x[1]=='CODECOPY')
        base=int(ins[copy_i-2][2],16); size=int(ins[copy_i-3][2],16)
        blob=code[base+size:]
        rows={blob[i:i+4].hex():int.from_bytes(blob[i+4:i+6],'big') for i in range(0,len(blob),7)}
        targets_ok=all(code[target]==0x5b for target in rows.values())
        common=len(set(offsets.values()))==1
        print(f'codesize: functions={len(offsets)} distinct_REA_bytecode_offsets={len(set(offsets.values()))} common_offset={next(iter(offsets.values()))} common_opcode=0x{code[next(iter(offsets.values()))]:02x}')
        print(f'  every_table_target_is_JUMPDEST={targets_ok} common_REA_offset_is_table_target={next(iter(offsets.values())) in set(rows.values())}')
        for sel,off in sorted(offsets.items()): print(f'  selector=0x{sel} REA_offset={off} table_target={rows[sel]} target_opcode=0x{code[rows[sel]]:02x}')
