#!/usr/bin/env python3
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
runtime = path.read_bytes()
trailer_length = int.from_bytes(runtime[-2:], 'big')
code_end = len(runtime) - 2 - trailer_length
if trailer_length > len(runtime) - 2 or code_end <= 0:
    raise ValueError('invalid terminal length suffix')
code = runtime[:code_end]
opnames = {
    0x00: 'STOP', 0x01: 'ADD', 0x02: 'MUL', 0x03: 'SUB', 0x04: 'DIV',
    0x10: 'LT', 0x11: 'GT', 0x12: 'SLT', 0x13: 'SGT', 0x14: 'EQ',
    0x15: 'ISZERO', 0x16: 'AND', 0x17: 'OR', 0x18: 'XOR', 0x19: 'NOT',
    0x1a: 'BYTE', 0x1b: 'SHL', 0x1c: 'SHR', 0x20: 'KECCAK256',
    0x33: 'CALLER', 0x34: 'CALLVALUE', 0x35: 'CALLDATALOAD',
    0x36: 'CALLDATASIZE', 0x37: 'CALLDATACOPY', 0x38: 'CODESIZE',
    0x39: 'CODECOPY', 0x3d: 'RETURNDATASIZE', 0x50: 'POP',
    0x51: 'MLOAD', 0x52: 'MSTORE', 0x54: 'SLOAD', 0x55: 'SSTORE',
    0x56: 'JUMP', 0x57: 'JUMPI', 0x5b: 'JUMPDEST', 0x5f: 'PUSH0',
    0xf3: 'RETURN', 0xfd: 'REVERT', 0xfe: 'INVALID', 0xff: 'SELFDESTRUCT',
}
rows = []
pc = 0
while pc < len(code):
    start = pc
    op = code[pc]
    pc += 1
    if 0x60 <= op <= 0x7f:
        n = op - 0x5f
        immediate = code[pc:pc + n]
        pc += n
        name = f'PUSH{n}'
        arg = '0x' + immediate.hex()
    else:
        if 0x80 <= op <= 0x8f:
            name = f'DUP{op - 0x7f}'
        elif 0x90 <= op <= 0x9f:
            name = f'SWAP{op - 0x8f}'
        else:
            name = opnames.get(op, f'OP_{op:02x}')
        arg = ''
    rows.append((start, name, arg))

push4 = [row for row in rows if row[1] == 'PUSH4']
print(f'runtime_bytes={len(runtime)}')
print(f'code_bytes_before_terminal_metadata={code_end}')
print(f'terminal_metadata_bytes={trailer_length}')
print('opcode_boundary_push4=' + json.dumps([{'pc': pc, 'immediate': arg} for pc, _, arg in push4]))
print('early_dispatch_ops=')
for pc, name, arg in rows:
    if pc > 320:
        break
    print(f'{pc:04x}: {name}' + (f' {arg}' if arg else ''))
