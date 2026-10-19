#!/usr/bin/env python3
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
NAMES = {
    0x00: 'STOP', 0x01: 'ADD', 0x02: 'MUL', 0x03: 'SUB', 0x04: 'DIV',
    0x05: 'SDIV', 0x06: 'MOD', 0x10: 'LT', 0x11: 'GT', 0x14: 'EQ',
    0x15: 'ISZERO', 0x16: 'AND', 0x17: 'OR', 0x18: 'XOR', 0x1B: 'SHL',
    0x1C: 'SHR', 0x30: 'ADDRESS', 0x31: 'BALANCE', 0x32: 'ORIGIN',
    0x33: 'CALLER', 0x34: 'CALLVALUE', 0x35: 'CALLDATALOAD',
    0x36: 'CALLDATASIZE', 0x37: 'CALLDATACOPY', 0x38: 'CODESIZE',
    0x39: 'CODECOPY', 0x40: 'BLOCKHASH', 0x41: 'COINBASE',
    0x42: 'TIMESTAMP', 0x43: 'NUMBER', 0x44: 'PREVRANDAO',
    0x45: 'GASLIMIT', 0x46: 'CHAINID', 0x47: 'SELFBALANCE',
    0x48: 'BASEFEE', 0x50: 'POP', 0x51: 'MLOAD', 0x52: 'MSTORE',
    0x53: 'MSTORE8', 0x54: 'SLOAD', 0x55: 'SSTORE', 0x56: 'JUMP',
    0x57: 'JUMPI', 0x58: 'PC', 0x5A: 'GAS', 0x5B: 'JUMPDEST',
    0xF0: 'CREATE', 0xF1: 'CALL', 0xF3: 'RETURN', 0xFA: 'STATICCALL',
    0xFD: 'REVERT', 0xFE: 'INVALID', 0xFF: 'SELFDESTRUCT',
}
for opcode in range(0x60, 0x80):
    NAMES[opcode] = f'PUSH{opcode - 0x5F}'
for opcode in range(0x80, 0x90):
    NAMES[opcode] = f'DUP{opcode - 0x7F}'
for opcode in range(0x90, 0xA0):
    NAMES[opcode] = f'SWAP{opcode - 0x8F}'


def decode(data):
    instructions = []
    pc = 0
    while pc < len(data):
        start = pc
        opcode = data[pc]
        pc += 1
        width = opcode - 0x5F if 0x60 <= opcode <= 0x7F else 0
        immediate = data[pc:pc + width]
        pc += width
        instructions.append((start, NAMES.get(opcode, f'0x{opcode:02x}'), immediate))
    return instructions


def render(rows):
    return ' '.join(f'{pc:#x}:{name}' + (f' {imm.hex()}' if imm else '') for pc, name, imm in rows)


summaries = {}
for mode in ('no-fallback', 'payable-fallback'):
    directory = ROOT / mode
    data = (directory / 'runtime.bin').read_bytes()
    instructions = decode(data)
    methods = json.loads((directory / 'method-identifiers.json').read_text())
    selectors = {value.lower().removeprefix('0x') for value in methods.values()}
    rows = []
    for index, (pc, name, immediate) in enumerate(instructions):
        if name != 'PUSH4' or immediate.hex() not in selectors:
            continue
        if index + 3 >= len(instructions):
            continue
        compare = instructions[index + 1]
        destination = instructions[index + 2]
        branch = instructions[index + 3]
        if compare[1] not in ('EQ', 'SUB') or not destination[1].startswith('PUSH') or branch[1] != 'JUMPI':
            continue
        target = int.from_bytes(destination[2], 'big')
        rows.append((pc, immediate.hex(), compare[1], target))
    assert len(rows) == len(selectors) == 15
    assert {row[1] for row in rows} == selectors
    miss = [row for row in rows if row[2] == 'SUB']
    assert len(miss) == 1
    target = miss[0][3]
    target_index = next(i for i, row in enumerate(instructions) if row[0] == target)
    path = instructions[target_index:target_index + 18]
    summaries[mode] = {
        'bytes': len(data),
        'sha256': hashlib.sha256(data).hexdigest(),
        'selectors': selectors,
        'rows': rows,
        'miss': miss[0],
        'miss_path': path,
    }
    print(f'[{mode}] RUNTIME_BYTES={len(data)} SHA256={hashlib.sha256(data).hexdigest()}')
    print(f'COMPARE_ROWS={len(rows)} EQ={sum(row[2] == "EQ" for row in rows)} SUB={sum(row[2] == "SUB" for row in rows)} SELECTOR_SET={",".join(sorted(selectors))}')
    print(f'SUB_LEG_PC={miss[0][0]:#x} SELECTOR={miss[0][1]} MISMATCH_BRANCH_TARGET={target:#x}')
    print('MISMATCH_TARGET_PATH=' + render(path))
    print('DISPATCH_HEAD=' + render(instructions[:55]))

assert summaries['no-fallback']['selectors'] == summaries['payable-fallback']['selectors']
assert summaries['no-fallback']['miss'][3] == summaries['payable-fallback']['miss'][3] == 0x0E
print('SAME_15_SELECTOR_SET=True')
print('SUB_MISMATCH_TARGET_SHARED_PC=0x0e')
