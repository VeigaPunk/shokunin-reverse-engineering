import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
D = ROOT/'out'
raw = bytes.fromhex((D/'codesize.runtime.hex').read_text().strip().removeprefix('0x'))
ops = {0x39:'CODECOPY'}
def dis(code):
    i=0; out=[]
    while i < len(code):
        pc=i; op=code[i]; i+=1
        if 0x60 <= op <= 0x7f:
            n=op-0x5f; imm=code[i:i+n]; i+=n
            out.append((pc, f'PUSH{n}', imm.hex()))
        else: out.append((pc, ops.get(op, f'0x{op:02x}'), ''))
    return out
ins=dis(raw)
copy_i=next(i for i,x in enumerate(ins) if x[1]=='CODECOPY')
size=int(ins[copy_i-3][2],16)
base=int(ins[copy_i-2][2],16)
dest=int(ins[copy_i-1][2],16)
tail=raw[base:]
header, records_blob=tail[:size], tail[size:]
assert size == 5 and len(records_blob) % 7 == 0
ids=json.loads((D/'codesize.methodids.json').read_text())
expected={v.removeprefix('0x') for v in ids.values()}
print(f'runtime_bytes={len(raw)} sha256={hashlib.sha256(raw).hexdigest()}')
print(f'first_literal_CODECOPY_pc={ins[copy_i][0]} source={base} (0x{base:04x}) size={size} dest={dest} (0x{dest:02x})')
print(f'table_header_hex={header.hex()} table_tail_bytes={len(tail)} record_bytes={len(records_blob)} record_width=7 records={len(records_blob)//7}')
selectors=set()
for i in range(0,len(records_blob),7):
    rec=records_blob[i:i+7]
    sel=rec[:4].hex(); jump=int.from_bytes(rec[4:6],'big'); marker=rec[6]
    selectors.add(sel)
    print(f'record_{i//7}: file_offset={base+size+i} selector=0x{sel} target={jump} (0x{jump:04x}) target_opcode=0x{raw[jump]:02x} marker=0x{marker:02x}')
print(f'record_selectors_equal_compiler_methodids={selectors == expected}')
print(f'all_targets_are_JUMPDEST={all(raw[int.from_bytes(records_blob[i+4:i+6],"big")] == 0x5b for i in range(0,len(records_blob),7))}')
