import collections
import hashlib
import pathlib
import sys

SCRATCH = pathlib.Path('/var/tmp/kaidoku-ex4-r7')
NAMES = {'gas': 'gas.runtime.hex', 'noopt': 'noopt.runtime.hex', 'codesize': 'codesize.runtime.hex'}
BASE = {
    0x00: 'STOP', 0x01: 'ADD', 0x02: 'MUL', 0x03: 'SUB', 0x04: 'DIV',
    0x05: 'SDIV', 0x06: 'MOD', 0x08: 'ADDMOD', 0x09: 'MULMOD',
    0x0a: 'EXP', 0x10: 'LT', 0x11: 'GT', 0x12: 'SLT', 0x13: 'SGT',
    0x14: 'EQ', 0x15: 'ISZERO', 0x16: 'AND', 0x17: 'OR', 0x18: 'XOR',
    0x19: 'NOT', 0x1a: 'BYTE', 0x1b: 'SHL', 0x1c: 'SHR', 0x1d: 'SAR',
    0x20: 'SHA3', 0x30: 'ADDRESS', 0x31: 'BALANCE', 0x32: 'ORIGIN',
    0x33: 'CALLER', 0x34: 'CALLVALUE', 0x35: 'CALLDATALOAD',
    0x36: 'CALLDATASIZE', 0x37: 'CALLDATACOPY', 0x38: 'CODESIZE',
    0x39: 'CODECOPY', 0x3a: 'GASPRICE', 0x3d: 'RETURNDATASIZE',
    0x40: 'BLOCKHASH', 0x41: 'COINBASE', 0x42: 'TIMESTAMP',
    0x43: 'NUMBER', 0x44: 'PREVRANDAO', 0x45: 'GASLIMIT', 0x46: 'CHAINID',
    0x47: 'SELFBALANCE', 0x48: 'BASEFEE', 0x50: 'POP', 0x51: 'MLOAD',
    0x52: 'MSTORE', 0x53: 'MSTORE8', 0x54: 'SLOAD', 0x55: 'SSTORE',
    0x56: 'JUMP', 0x57: 'JUMPI', 0x58: 'PC', 0x59: 'MSIZE', 0x5a: 'GAS',
    0x5b: 'JUMPDEST', 0x5f: 'PUSH0', 0xf0: 'CREATE', 0xf1: 'CALL',
    0xf2: 'CALLCODE', 0xf3: 'RETURN', 0xf4: 'DELEGATECALL', 0xf5: 'CREATE2',
    0xfa: 'STATICCALL', 0xfd: 'REVERT', 0xfe: 'INVALID', 0xff: 'SELFDESTRUCT',
}


def decode(code):
    rows = []
    pc = 0
    while pc < len(code):
        start = pc
        op = code[pc]
        pc += 1
        if 0x60 <= op <= 0x7f:
            n = op - 0x5f
            imm = code[pc:pc+n]
            pc += n
            name = f'PUSH{n}'
            value = int.from_bytes(imm, 'big')
            arg = f'0x{value:0{n*2}x}'
        elif 0x80 <= op <= 0x8f:
            name, arg = f'DUP{op-0x7f}', ''
        elif 0x90 <= op <= 0x9f:
            name, arg = f'SWAP{op-0x8f}', ''
        elif 0xa0 <= op <= 0xa4:
            name, arg = f'LOG{op-0xa0}', ''
        else:
            name, arg = BASE.get(op, f'OP_{op:02x}'), ''
        rows.append((start, name, arg))
    return rows


for form, filename in NAMES.items():
    path = SCRATCH / filename
    code = bytes.fromhex(path.read_text().strip().removeprefix('0x'))
    rows = decode(code)
    counts = collections.Counter(name for _, name, _ in rows)
    push4 = [(pc, arg) for pc, name, arg in rows if name == 'PUSH4']
    print(f'[{form}] bytes={len(code)} sha256={hashlib.sha256(code).hexdigest()}')
    print('counts=' + ', '.join(f'{k}:{counts[k]}' for k in ('PUSH4', 'EQ', 'XOR', 'MOD', 'CODECOPY', 'JUMPI', 'JUMPDEST') if counts[k]))
    print('PUSH4=' + (', '.join(f'{pc:#x}:{arg}' for pc, arg in push4) if push4 else 'none'))
    if form == 'gas':
        print('prologue=' + ' '.join(f'{pc:#x}:{name}{(" " + arg) if arg else ""}' for pc, name, arg in rows[:18]))
    elif form == 'noopt':
        print('dispatcher-comparisons=')
        for i, (pc, name, arg) in enumerate(rows):
            if name == 'PUSH4':
                print('  ' + ' '.join(f'{p:#x}:{n}{(" " + a) if a else ""}' for p, n, a in rows[i:i+6]))
    else:
        print('selector-lookup-prefix=' + ' '.join(f'{pc:#x}:{name}{(" " + arg) if arg else ""}' for pc, name, arg in rows[:52]))
        print('codecopy-contexts=')
        for i, (pc, name, arg) in enumerate(rows):
            if name == 'CODECOPY':
                print('  ' + ' '.join(f'{p:#x}:{n}{(" " + a) if a else ""}' for p, n, a in rows[max(0,i-8):i+5]))
        print(f'tail_27_bytes_at_0x12b={code[0x12b:0x12b+27].hex()}')
    print('')
