"""Minimal EVM disassembler for seat EX-5 arc3-loop1-round6 (opcode-boundary walk)."""

PUSH1_32 = list(range(0x60, 0x80))
NAMES = {
    0x00: 'STOP', 0x01: 'ADD', 0x02: 'MUL', 0x03: 'SUB', 0x04: 'DIV', 0x06: 'MOD',
    0x07: 'SMOD', 0x0a: 'EXP', 0x0b: 'SIGNEXTEND', 0x10: 'LT', 0x11: 'GT',
    0x12: 'SLT', 0x13: 'SGT', 0x14: 'EQ', 0x15: 'ISZERO', 0x16: 'AND', 0x17: 'OR',
    0x18: 'XOR', 0x19: 'NOT', 0x1a: 'BYTE', 0x1b: 'SHL', 0x1c: 'SHR', 0x1d: 'SAR',
    0x20: 'KECCAK256', 0x30: 'ADDRESS', 0x31: 'BALANCE', 0x33: 'CALLER', 0x34: 'CALLVALUE',
    0x35: 'CALLDATALOAD', 0x36: 'CALLDATASIZE', 0x37: 'CALLDATACOPY', 0x38: 'CODESIZE',
    0x39: 'CODECOPY', 0x3b: 'EXTCODESIZE', 0x3d: 'RETURNDATASIZE', 0x3e: 'RETURNDATACOPY',
    0x40: 'BLOCKHASH', 0x41: 'COINBASE', 0x42: 'TIMESTAMP', 0x43: 'NUMBER',
    0x44: 'PREVRANDAO', 0x45: 'GASLIMIT', 0x46: 'CHAINID', 0x47: 'SELFBALANCE',
    0x48: 'BASEFEE', 0x50: 'POP', 0x51: 'MLOAD', 0x52: 'MSTORE', 0x53: 'MSTORE8',
    0x54: 'SLOAD', 0x55: 'SSTORE', 0x56: 'JUMP', 0x57: 'JUMPI', 0x58: 'PC',
    0x59: 'MSIZE', 0x5a: 'GAS', 0x5b: 'JUMPDEST', 0x5e: 'MCOPY', 0x5f: 'PUSH0',
    0xf0: 'CREATE', 0xf1: 'CALL', 0xf3: 'RETURN', 0xf4: 'DELEGATECALL', 0xf5: 'CREATE2',
    0xfa: 'STATICCALL', 0xfd: 'REVERT', 0xfe: 'INVALID', 0xff: 'SELFDESTRUCT',
}
for i in range(16):
    NAMES[0x80 + i] = f'DUP{i + 1}'
    NAMES[0x90 + i] = f'SWAP{i + 1}'
    NAMES[0xa0 + i] = f'LOG{i}'
for i in range(0x60, 0x80):
    NAMES[i] = f'PUSH{i - 0x5f}'


def dis(code: bytes):
    """Return list of (pc, opcode, name, imm_hex, next_pc)."""
    out = []
    i = 0
    while i < len(code):
        op = code[i]
        if 0x60 <= op <= 0x7f:
            n = op - 0x5f
            imm = code[i + 1:i + 1 + n]
            out.append((i, op, NAMES[op], imm.hex(), i + 1 + n))
            i += 1 + n
        else:
            out.append((i, op, NAMES.get(op, f'OP_{op:02x}'), '', i + 1))
            i += 1
    return out


def main(path, lo=0, hi=None):
    lo, hi = int(lo), (None if hi is None else int(hi))
    h = open(path).read().strip()
    if h.startswith('0x'):
        h = h[2:]
    code = bytes.fromhex(h)
    hi = len(code) if hi is None else hi
    for pc, op, name, imm, nxt in dis(code):
        if lo <= pc < hi:
            print(f'{pc:5} {name:10} {imm[:24]:24} -> {nxt}')


if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
