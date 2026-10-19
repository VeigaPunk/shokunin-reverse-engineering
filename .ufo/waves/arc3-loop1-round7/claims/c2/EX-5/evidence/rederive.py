from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ROT = ((0, 36, 3, 41, 18), (1, 44, 10, 45, 2), (62, 6, 43, 15, 61), (28, 55, 25, 21, 56), (27, 20, 39, 8, 14))
RC = (0x0000000000000001,0x0000000000008082,0x800000000000808A,0x8000000080008000,0x000000000000808B,0x0000000080000001,0x8000000080008081,0x8000000000008009,0x000000000000008A,0x0000000000000088,0x0000000080008009,0x000000008000000A,0x000000008000808B,0x800000000000008B,0x8000000000008089,0x8000000000008003,0x8000000000008002,0x8000000000000080,0x000000000000800A,0x800000008000000A,0x8000000080008081,0x8000000000008080,0x0000000080000001,0x8000000080008008)
MASK = (1 << 64) - 1

def rol(v, n):
    return v if n == 0 else ((v << n) | (v >> (64 - n))) & MASK

def keccak_f(a):
    for rc in RC:
        c = [a[x] ^ a[x+5] ^ a[x+10] ^ a[x+15] ^ a[x+20] for x in range(5)]
        d = [c[(x-1) % 5] ^ rol(c[(x+1) % 5], 1) for x in range(5)]
        for y in range(5):
            for x in range(5): a[x+5*y] ^= d[x]
        b = [0] * 25
        for y in range(5):
            for x in range(5): b[y + 5*((2*x+3*y) % 5)] = rol(a[x+5*y], ROT[x][y])
        for y in range(5):
            for x in range(5): a[x+5*y] = b[x+5*y] ^ ((~b[(x+1)%5+5*y]) & b[(x+2)%5+5*y])
        a[0] ^= rc

def keccak256(data: bytes) -> bytes:
    rate = 136
    padded = bytearray(data)
    padded.append(0x01)
    padded.extend(b'\x00' * ((rate - len(padded) % rate - 1) % rate))
    padded.append(0x80)
    a = [0] * 25
    for start in range(0, len(padded), rate):
        block = padded[start:start+rate]
        for i, value in enumerate(block): a[i // 8] ^= value << (8 * (i % 8))
        keccak_f(a)
    return b''.join(lane.to_bytes(8,'little') for lane in a)[:32]

NAMES = {0x00:'STOP',0x01:'ADD',0x02:'MUL',0x03:'SUB',0x04:'DIV',0x05:'SDIV',0x06:'MOD',0x08:'ADDMOD',0x09:'MULMOD',0x0a:'EXP',0x10:'LT',0x11:'GT',0x12:'SLT',0x13:'SGT',0x14:'EQ',0x15:'ISZERO',0x16:'AND',0x17:'OR',0x18:'XOR',0x19:'NOT',0x1a:'BYTE',0x1b:'SHL',0x1c:'SHR',0x20:'KECCAK256',0x35:'CALLDATALOAD',0x36:'CALLDATASIZE',0x37:'CALLDATACOPY',0x39:'CODECOPY',0x51:'MLOAD',0x52:'MSTORE',0x54:'SLOAD',0x55:'SSTORE',0x56:'JUMP',0x57:'JUMPI',0x5b:'JUMPDEST',0x5f:'PUSH0',0xf3:'RETURN',0xfd:'REVERT',0xfe:'INVALID',0xff:'SELFDESTRUCT'}
for i in range(16): NAMES[0x80+i] = f'DUP{i+1}'
for i in range(16): NAMES[0x90+i] = f'SWAP{i+1}'
for i in range(16): NAMES[0xa0+i] = f'LOG{i}'

def dis(code, stop=None):
    i = 0
    out = []
    stop = len(code) if stop is None else min(stop, len(code))
    while i < stop:
        pc = i
        op = code[i]
        i += 1
        if 0x60 <= op <= 0x7f:
            n = op - 0x5f
            imm = code[i:i+n]
            i += n
            out.append((pc, f'PUSH{n}', imm.hex(), i))
        else:
            out.append((pc, NAMES.get(op, f'0x{op:02x}'), '', i))
    return out

def runtime(form):
    return bytes.fromhex((ROOT/'out'/f'{form}.runtime.hex').read_text().strip().removeprefix('0x'))

assert keccak256(b'').hex() == 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470'
assert keccak256(b'transfer(address,uint256)')[:4].hex() == 'a9059cbb'
print('keccak_selftests=2/2 (empty-string and transfer(address,uint256))')
for form in ('noopt','codesize'):
    code = runtime(form)
    abi = json.loads((ROOT/'out'/f'{form}.abi.json').read_text())
    mid = json.loads((ROOT/'out'/f'{form}.methodids.json').read_text())
    sigs = []
    for x in abi:
        if x.get('type') == 'function':
            sig = x['name'] + '(' + ','.join(i['type'] for i in x['inputs']) + ')'
            sigs.append(sig)
    expected = {keccak256(s.encode())[:4].hex() for s in sigs}
    compiler_ids = {v.removeprefix('0x') for v in mid.values()}
    ins = dis(code)
    pushes4 = [(pc, imm) for pc, name, imm, _ in ins if name == 'PUSH4']
    eq = sum(name == 'EQ' for _, name, _, _ in ins)
    xor = sum(name == 'XOR' for _, name, _, _ in ins)
    jumppi = sum(name == 'JUMPI' for _, name, _, _ in ins)
    bytecode_sha = hashlib.sha256(code).hexdigest()
    carrier_sha = hashlib.sha256((ROOT/'out'/f'{form}.runtime.hex').read_bytes()).hexdigest()
    print(f'[{form}]')
    print(f'  runtime_bytes={len(code)} bytecode_sha256={bytecode_sha} carrier_sha256={carrier_sha}')
    print(f'  abi_function_count={len(sigs)} compiler_methodid_count={len(mid)} independent_keccak_selector_count={len(expected)}')
    print(f'  independent_keccak_equals_compiler_methodids={expected == compiler_ids}')
    print(f'  selector_set={sorted(expected)}')
    print(f'  opcode_counts: PUSH4={len(pushes4)} EQ={eq} XOR={xor} JUMPI={jumppi}')
    if form == 'noopt':
        print('  PUSH4_sites=' + ','.join(f'{pc}:0x{imm}' for pc,imm in pushes4))
        print('  comparison_windows:')
        for ix, row in enumerate(ins):
            if row[1] == 'PUSH4':
                print('    ' + ' '.join(f'{pc:04x}:{name}'+(f' 0x{imm}' if imm else '') for pc,name,imm,_ in ins[ix:ix+6]))
    else:
        copy = next(r for r in ins if r[1] == 'CODECOPY')
        prev = ins[ins.index(copy)-1]
        # Immediate CODECOPY source is the PUSH2 immediately before PUSH1 0x1b.
        base = int(next(r[2] for r in ins if r[1] == 'PUSH2'), 16)
        print(f'  first_codecopy_pc={copy[0]} data_base={base} data_bytes={len(code)-base} code_prefix={code[:base].hex()}')
        print(f'  tail_data_hex={code[base:].hex()}')
        print('  code_disassembly:')
        for pc,name,imm,_ in dis(code, base):
            print(f'    {pc:04x} {name:8} {imm}')
    probe = json.loads((ROOT/'probe'/f'{form}-6.7.0.json').read_text())
    got = {x['selector'].removeprefix('0x') for x in probe['normalized_result']['functions']}
    print(f'  REA_evidence_id={probe["evidence_id"]} probe_functions={len(got)} REA_selectors_equal_independent_set={got == expected}')
    print(f'  REA_decoded_sha256={probe["normalized_result"]["bytecode"]["sha256"]} equals_compiled_bytecode={probe["normalized_result"]["bytecode"]["sha256"] == bytecode_sha}')