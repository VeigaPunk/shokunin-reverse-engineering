"""Boundary-true linear disassembler for EVM runtime bytes (seat CR-1, arc3-r6).

Usage: python3 disasm.py <hexfile> [--json out.json] [--limit N]
Reports: size, sha256, boundary-true PUSH1/PUSH2/PUSH4 sites, JUMPDESTs,
and a disassembly listing (optionally truncated).
"""
import hashlib
import json
import sys

NAMES = {
    0x00: 'STOP', 0x01: 'ADD', 0x02: 'MUL', 0x03: 'SUB', 0x04: 'DIV',
    0x05: 'SDIV', 0x06: 'MOD', 0x07: 'SMOD', 0x08: 'ADDMOD', 0x09: 'MULMOD',
    0x0a: 'EXP', 0x0b: 'SIGNEXTEND', 0x10: 'LT', 0x11: 'GT', 0x12: 'SLT',
    0x13: 'SGT', 0x14: 'EQ', 0x15: 'ISZERO', 0x16: 'AND', 0x17: 'OR',
    0x18: 'XOR', 0x19: 'NOT', 0x1a: 'BYTE', 0x1b: 'SHL', 0x1c: 'SHR',
    0x1d: 'SAR', 0x20: 'SHA3', 0x30: 'ADDRESS', 0x31: 'BALANCE',
    0x32: 'ORIGIN', 0x33: 'CALLER', 0x34: 'CALLVALUE', 0x35: 'CALLDATALOAD',
    0x36: 'CALLDATASIZE', 0x37: 'CALLDATACOPY', 0x38: 'CODESIZE',
    0x39: 'CODECOPY', 0x3a: 'GASPRICE', 0x3b: 'EXTCODESIZE',
    0x3c: 'EXTCODECOPY', 0x3d: 'RETURNDATASIZE', 0x3e: 'RETURNDATACOPY',
    0x3f: 'EXTCODEHASH', 0x40: 'BLOCKHASH', 0x41: 'COINBASE',
    0x42: 'TIMESTAMP', 0x43: 'NUMBER', 0x44: 'PREVRANDAO', 0x45: 'GASLIMIT',
    0x46: 'CHAINID', 0x47: 'SELFBALANCE', 0x48: 'BASEFEE', 0x49: 'BLOBHASH',
    0x4a: 'BLOBBASEFEE', 0x50: 'POP', 0x51: 'MLOAD', 0x52: 'MSTORE',
    0x53: 'MSTORE8', 0x54: 'SLOAD', 0x55: 'SSTORE', 0x56: 'JUMP', 0x57: 'JUMPI',
    0x58: 'PC', 0x59: 'MSIZE', 0x5a: 'GAS', 0x5b: 'JUMPDEST', 0x5c: 'TLOAD',
    0x5d: 'TSTORE', 0x5e: 'MCOPY', 0x5f: 'PUSH0', 0xf0: 'CREATE',
    0xf1: 'CALL', 0xf2: 'CALLCODE', 0xf3: 'RETURN', 0xf4: 'DELEGATECALL',
    0xf5: 'CREATE2', 0xfa: 'STATICCALL', 0xfd: 'REVERT', 0xfe: 'INVALID',
    0xff: 'SELFDESTRUCT',
}
for i in range(1, 33):
    NAMES[0x5f + i] = f'PUSH{i}'
for i in range(1, 17):
    NAMES[0x7f + i] = f'DUP{i}'
    NAMES[0x8f + i] = f'SWAP{i}'
for i in range(5):
    NAMES[0xa0 + i] = f'LOG{i}'


def load(path):
    t = open(path).read().strip()
    if t.startswith('0x'):
        t = t[2:]
    return bytes.fromhex(t)


def sweep(code):
    """Boundary-true sweep: pcs of every instruction start + decoded ops."""
    ops = []
    pc = 0
    n = len(code)
    while pc < n:
        op = code[pc]
        if op == 0x5f:
            ops.append((pc, op, b''))
            pc += 1
        elif 0x60 <= op <= 0x7f:
            k = op - 0x5f
            imm = code[pc + 1:pc + 1 + k]
            ops.append((pc, op, imm))
            pc += 1 + k
        else:
            ops.append((pc, op, b''))
            pc += 1
    return ops


def name(op, imm):
    nm = NAMES.get(op, f'0x{op:02x}')
    if imm:
        return f'{nm} 0x{imm.hex()}'
    return nm


def census(path, limit=None, out_json=None):
    code = load(path)
    ops = sweep(code)
    jumpdests = [pc for pc, op, _ in ops if op == 0x5b]
    push4 = [(pc, int.from_bytes(imm, 'big')) for pc, op, imm in ops if op == 0x63]
    push2 = [int.from_bytes(imm, 'big') for pc, op, imm in ops if op == 0x61]
    push1 = [int.from_bytes(imm, 'big') for pc, op, imm in ops if op == 0x60]
    res = {
        'path': path,
        'bytes': len(code),
        'sha256': hashlib.sha256(code).hexdigest(),
        'hex_sha256': hashlib.sha256(open(path, 'rb').read()).hexdigest(),
        'jumpdests': jumpdests,
        'push4_sites': [{'pc': pc, 'imm': f'{imm:08x}'} for pc, imm in push4],
        'push4_count': len(push4),
        'push2_count': len(push2),
        'push1_count': len(push1),
        'op_histogram': {},
    }
    for _, op, _ in ops:
        nm = NAMES.get(op, f'0x{op:02x}')
        res['op_histogram'][nm] = res['op_histogram'].get(nm, 0) + 1
    listing = [f'{pc:5d} 0x{code[pc]:02x} {name(op, imm)}' for pc, op, imm in ops]
    if limit:
        listing = listing[:limit]
    if out_json:
        json.dump(res, open(out_json, 'w'), indent=1)
    return res, listing


if __name__ == '__main__':
    path = sys.argv[1]
    lim = None
    out = None
    if '--limit' in sys.argv:
        lim = int(sys.argv[sys.argv.index('--limit') + 1])
    if '--json' in sys.argv:
        out = sys.argv[sys.argv.index('--json') + 1]
    res, listing = census(path, lim, out)
    print(json.dumps({k: v for k, v in res.items() if k != 'op_histogram'}, indent=1))
    print('---')
    print('\n'.join(listing))
