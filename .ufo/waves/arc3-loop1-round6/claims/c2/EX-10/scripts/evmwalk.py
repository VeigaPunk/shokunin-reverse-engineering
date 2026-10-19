#!/usr/bin/env python3
"""Minimal opcode-boundary disassembler + dispatcher characterizer (EX-10, arc3-r6)."""
import json, sys

OPS = {0x00:'STOP',0x01:'ADD',0x02:'MUL',0x03:'SUB',0x04:'DIV',0x05:'SDIV',0x06:'MOD',0x07:'SMOD',
0x08:'ADDMOD',0x09:'MULMOD',0x0a:'EXP',0x0b:'SIGNEXTEND',0x10:'LT',0x11:'GT',0x12:'SLT',0x13:'SGT',
0x14:'EQ',0x15:'ISZERO',0x16:'AND',0x17:'OR',0x18:'XOR',0x19:'NOT',0x1a:'BYTE',0x1b:'SHL',0x1c:'SHR',
0x1d:'SAR',0x20:'KECCAK256',0x30:'ADDRESS',0x31:'BALANCE',0x32:'ORIGIN',0x33:'CALLER',0x34:'CALLVALUE',
0x35:'CALLDATALOAD',0x36:'CALLDATASIZE',0x37:'CALLDATACOPY',0x38:'CODESIZE',0x39:'CODECOPY',0x3a:'GASPRICE',
0x3b:'EXTCODESIZE',0x3c:'EXTCODECOPY',0x3d:'RETURNDATASIZE',0x3e:'RETURNDATACOPY',0x3f:'EXTCODEHASH',
0x40:'BLOCKHASH',0x41:'COINBASE',0x42:'TIMESTAMP',0x43:'NUMBER',0x44:'PREVRANDAO',0x45:'GASLIMIT',
0x46:'CHAINID',0x47:'SELFBALANCE',0x48:'BASEFEE',0x49:'BLOBBASEFEE',0x50:'POP',0x51:'MLOAD',0x52:'MSTORE',
0x53:'MSTORE8',0x54:'SLOAD',0x55:'SSTORE',0x56:'JUMP',0x57:'JUMPI',0x58:'PC',0x59:'MSIZE',0x5a:'GAS',
0x5b:'JUMPDEST',0x5c:'TLOAD',0x5d:'TSTORE',0x5e:'MCOPY',0x5f:'PUSH0',0xf0:'CREATE',0xf1:'CALL',
0xf2:'CALLCODE',0xf3:'RETURN',0xf4:'DELEGATECALL',0xf5:'CREATE2',0xfa:'STATICCALL',0xfd:'REVERT',
0xfe:'INVALID',0xff:'SELFDESTRUCT'}

def disasm(code):
    out, pc, n = [], 0, len(code)
    while pc < n:
        op = code[pc]
        if 0x60 <= op <= 0x7f:
            k = op - 0x5f
            imm = code[pc+1:pc+1+k]
            out.append((pc, OPS.get(op, f'PUSH{k}'), imm, op))
            pc += 1 + k
        elif 0x80 <= op <= 0x8f:
            out.append((pc, f'DUP{op-0x7f}', b'', op)); pc += 1
        elif 0x90 <= op <= 0x9f:
            out.append((pc, f'SWAP{op-0x8f}', b'', op)); pc += 1
        elif 0xa0 <= op <= 0xa4:
            out.append((pc, f'LOG{op-0xa0}', b'', op)); pc += 1
        else:
            out.append((pc, OPS.get(op, f'OP_{op:02x}'), b'', op)); pc += 1
    return out

def u16(b): return int.from_bytes(b, 'big')
def u32(b): return int.from_bytes(b, 'big')

def characterize(code):
    ins = disasm(code)
    pc2i = {pc: i for i, (pc, _, _, _) in enumerate(ins)}
    jumpdests = {pc for pc, op, _, _ in ins if op == 'JUMPDEST'}
    push4 = [(pc, u32(imm)) for pc, op, imm, _ in ins if op.startswith('PUSH4') and len(imm) == 4]
    # prologue: first CALLDATALOAD/SHR sequence
    head = code[:16].hex()
    # locate the MOD table formula: ... DUP3 MOD ... SHL ... PUSH2 base ... ADD ... CODECOPY ... MLOAD ... JUMP
    formula = None
    for i, (pc, op, imm, _) in enumerate(ins):
        if op == 'MOD':
            window = ins[max(0, i-3):i+12]
            ops = [o for _, o, _, _ in window]
            if 'DUP3' in ops and 'SHL' in ops and 'CODECOPY' in ops:
                # find the PUSH2 base and PUSH1 divisor
                divisor = None; base = None; size = None; dst = None
                for j in range(max(0, i-4), min(len(ins), i+12)):
                    p, o, im, _ = ins[j]
                    if o == 'PUSH1' and im and j < i and ins[j+1][1] == 'DUP3': divisor = im[0]
                    if o == 'PUSH1' and im and j < i and ins[j+1][1] == 'SHL': shift = im[0]
                    if o == 'PUSH2' and im and base is None and j > i: base = u16(im)
                    if o == 'PUSH1' and im and j > i and ins[j+1][1] == 'CODECOPY' and size is None: size = im[0]
                    if o == 'PUSH1' and im and j > i and ins[j+1][1] == 'CODECOPY' and dst is None: dst = im[0]
                formula = {'mod_pc': pc, 'divisor': divisor, 'shift': shift, 'table_base': base,
                           'copy_size': size, 'copy_dst': dst, 'window_ops': ops}
                break
    table_entries = []
    if formula and formula['table_base'] is not None and formula['divisor']:
        b = formula['table_base']
        for k in range(formula['divisor']):
            table_entries.append(u16(code[b+2*k:b+2*k+2]))
    # XOR-chain compare sites: PUSH4 sel; DUP2; XOR; PUSH2 next; JUMPI
    xor_sites = []
    for i, (pc, op, imm, _) in enumerate(ins):
        if op == 'PUSH4' and len(imm) == 4 and i+4 < len(ins):
            seq = [ins[i+j][1] for j in range(1, 5)]
            if seq == ['DUP2', 'XOR', 'PUSH2', 'JUMPI']:
                xor_sites.append({'pc': pc, 'sel': imm.hex(), 'next': u16(ins[i+3][2])})
    # EQ-chain compare sites: PUSH4 sel; DUP1/DUP?; EQ; PUSH2 dst; JUMPI
    eq_sites = []
    for i, (pc, op, imm, _) in enumerate(ins):
        if op == 'PUSH4' and len(imm) == 4 and i+4 < len(ins):
            seq = [ins[i+j][1] for j in range(1, 5)]
            if seq[1] == 'EQ' and seq[2] == 'PUSH2' and seq[3] == 'JUMPI':
                eq_sites.append({'pc': pc, 'sel': imm.hex(), 'dst': u16(ins[i+3][2])})
    # CT/GT/EQ binary-search sites
    gt_sites = []
    for i, (pc, op, imm, _) in enumerate(ins):
        if op == 'PUSH4' and len(imm) == 4 and i+4 < len(ins):
            if ins[i+2][1] == 'GT' and ins[i+3][1] == 'PUSH2':
                gt_sites.append({'pc': pc, 'sel': imm.hex(), 'dst': u16(ins[i+3][2])})
    # PUSH2 targets that are JUMPDESTs, for offset-rule checking
    push2_targets = sorted({u16(imm) for pc, op, imm, _ in ins if op == 'PUSH2' and len(imm)==2})
    return {
        'size': len(code), 'head_hex': head,
        'jumpdests': len(jumpdests),
        'push4_sites': [{'pc': pc, 'imm': f'{v:08x}'} for pc, v in push4],
        'push4_distinct': sorted({f'{v:08x}' for _, v in push4}),
        'formula': formula,
        'table_entries': [f'{v:04x}' for v in table_entries],
        'table_entries_all_jumpdest': all(v in jumpdests for v in table_entries) if table_entries else None,
        'xor_sites': xor_sites, 'eq_sites': eq_sites, 'gt_sites': gt_sites,
        'push2_targets_jumpdest': [t for t in push2_targets if t in jumpdests],
    }

if __name__ == '__main__':
    code = open(sys.argv[1], 'rb').read()
    print(json.dumps(characterize(code), indent=1))
