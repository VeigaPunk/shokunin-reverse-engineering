#!/usr/bin/env python3
"""EX-6 (arc3-loop1-round6) independent EVM byte walker.

Linear sweep with PUSH immediates skipped. Reports the dispatcher facts this
seat is adjudicating: guard form, PUSH4 sites with their following compare
opcode, EQ-chain stride, SUB legs, JUMPDEST set, and the offset convention
(PUSH2 dst vs push4_pc+10). No code from the seat under verification is used.
"""
import json, sys

NAMES = {
    0x00: 'STOP', 0x01: 'ADD', 0x02: 'MUL', 0x03: 'SUB', 0x04: 'DIV', 0x05: 'SDIV',
    0x06: 'MOD', 0x07: 'SMOD', 0x08: 'ADDMOD', 0x09: 'MULMOD', 0x0a: 'EXP', 0x0b: 'SIGNEXTEND',
    0x10: 'LT', 0x11: 'GT', 0x12: 'SLT', 0x13: 'SGT', 0x14: 'EQ', 0x15: 'ISZERO',
    0x16: 'AND', 0x17: 'OR', 0x18: 'XOR', 0x19: 'NOT', 0x1a: 'BYTE', 0x1b: 'SHL', 0x1c: 'SHR', 0x1d: 'SAR',
    0x20: 'KECCAK256', 0x30: 'ADDRESS', 0x31: 'BALANCE', 0x32: 'ORIGIN', 0x33: 'CALLER',
    0x34: 'CALLVALUE', 0x35: 'CALLDATALOAD', 0x36: 'CALLDATASIZE', 0x37: 'CALLDATACOPY',
    0x38: 'CODESIZE', 0x39: 'CODECOPY', 0x3a: 'GASPRICE', 0x3b: 'EXTCODESIZE', 0x3c: 'EXTCODECOPY',
    0x3d: 'RETURNDATASIZE', 0x3e: 'RETURNDATACOPY', 0x3f: 'EXTCODEHASH',
    0x40: 'BLOCKHASH', 0x41: 'COINBASE', 0x42: 'TIMESTAMP', 0x43: 'NUMBER', 0x44: 'PREVRANDAO',
    0x45: 'GASLIMIT', 0x46: 'CHAINID', 0x47: 'SELFBALANCE', 0x48: 'BASEFEE', 0x49: 'BLOBBASEFEE',
    0x50: 'POP', 0x51: 'MLOAD', 0x52: 'MSTORE', 0x53: 'MSTORE8', 0x54: 'SLOAD', 0x55: 'SSTORE',
    0x56: 'JUMP', 0x57: 'JUMPI', 0x58: 'PC', 0x59: 'MSIZE', 0x5a: 'GAS', 0x5b: 'JUMPDEST',
    0x5c: 'TLOAD', 0x5d: 'TSTORE', 0x5e: 'MCOPY', 0x5f: 'PUSH0',
    0xf0: 'CREATE', 0xf1: 'CALL', 0xf2: 'CALLCODE', 0xf3: 'RETURN', 0xf4: 'DELEGATECALL',
    0xf5: 'CREATE2', 0xfa: 'STATICCALL', 0xfd: 'REVERT', 0xfe: 'INVALID', 0xff: 'SELFDESTRUCT',
}
for i in range(1, 33):
    NAMES[0x5f + i] = f'PUSH{i}'
for i in range(1, 17):
    NAMES[0x7f + i] = f'DUP{i}'
for i in range(1, 17):
    NAMES[0x8f + i] = f'SWAP{i}'
for i in range(5):
    NAMES[0xa0 + i] = f'LOG{i}'


def decode(code):
    """Linear sweep; returns list of (pc, op, imm_bytes, size)."""
    out, pc, n = [], 0, len(code)
    while pc < n:
        op = code[pc]
        if 0x60 <= op <= 0x7f:
            k = op - 0x5f
            imm = code[pc + 1:pc + 1 + k]
            out.append((pc, op, imm, 1 + k))
            pc += 1 + k
        else:
            out.append((pc, op, b'', 1))
            pc += 1
    return out


def walk(code):
    ins = decode(code)
    jumpdests = {pc for pc, op, _, _ in ins if op == 0x5b}
    push4 = []
    for idx, (pc, op, imm, size) in enumerate(ins):
        if op == 0x63:  # PUSH4
            nxt = ins[idx + 1] if idx + 1 < len(ins) else (None, None, b'', 1)
            after = ins[idx + 2] if idx + 2 < len(ins) else (None, None, b'', 1)
            entry = {'pc': pc, 'imm': imm.hex(), 'next_op': NAMES.get(nxt[1], hex(nxt[1])),
                     'next_pc': nxt[0]}
            if nxt[1] == 0x14 and nxt[0] + 1 + 1 + 0 == 0:  # unreachable branch guard
                pass
            # For EQ legs: EQ at nxt[0], then PUSH2 at nxt[0]+1
            if nxt[1] == 0x14:
                p2 = ins[idx + 2]
                if p2[1] == 0x61:
                    entry['eq_dst'] = int.from_bytes(p2[2], 'big')
                    entry['eq_dst_pc'] = p2[0]
                    entry['eq_dst_is_jumpdest'] = entry['eq_dst'] in jumpdests
                j = ins[idx + 3] if idx + 3 < len(ins) else (None, None, b'', 1)
                entry['after_push2'] = NAMES.get(j[1], hex(j[1]))
            if nxt[1] == 0x03 and after[1] == 0x61:  # SUB PUSH2 ...
                entry['sub_dst'] = int.from_bytes(after[2], 'big')
                entry['sub_dst_pc'] = after[0]
                entry['sub_dst_is_jumpdest'] = entry['sub_dst'] in jumpdests
                j = ins[idx + 3] if idx + 3 < len(ins) else (None, None, b'', 1)
                entry['sub_after'] = NAMES.get(j[1], hex(j[1]))
            push4.append(entry)

    # Guard: look in first 40 bytes for PUSH1 04 CALLDATASIZE LT [ISZERO] PUSHn dst JUMPI
    guard = None
    for i in range(min(len(ins) - 4, 20)):
        seq = ins[i:i + 7]
        ops = [s[1] for s in seq]
        if ops[0] == 0x60 and seq[0][2] == b'\x04' and ops[1] == 0x36 and ops[2] == 0x10:
            if ops[3] == 0x15:
                jd = seq[4]
                guard = {'form': 'PUSH1 04 CALLDATASIZE LT ISZERO PUSHn dst JUMPI',
                         'pcs': [seq[0][0], seq[1][0], seq[2][0], seq[3][0], seq[4][0], seq[5][0]],
                         'dst_op': NAMES.get(seq[4][1]), 'dst': int.from_bytes(seq[4][2], 'big')}
                break
            elif seq[3][1] == 0x61:
                guard = {'form': 'PUSH1 04 CALLDATASIZE LT PUSH2 dst JUMPI',
                         'pcs': [seq[0][0], seq[1][0], seq[2][0], seq[3][0], seq[4][0]],
                         'dst_op': NAMES.get(seq[3][1]), 'dst': int.from_bytes(seq[3][2], 'big')}
                break

    eq_legs = [p for p in push4 if p['next_op'] == 'EQ' and 'eq_dst' in p]
    sub_legs = [p for p in push4 if p['next_op'] == 'SUB' and 'sub_dst' in p]
    others = [p for p in push4 if p['next_op'] not in ('EQ', 'SUB')]
    eq_pcs = [p['pc'] for p in eq_legs[:1] + eq_legs[1:]]
    gaps = sorted({eq_legs[i + 1]['pc'] - eq_legs[i]['pc'] for i in range(len(eq_legs) - 1)})
    imms = [p['imm'] for p in eq_legs]
    return {
        'len': len(code),
        'n_jumpdests': len(jumpdests),
        'guard': guard,
        'push4_total': len(push4),
        'push4_non_selector': [p for p in others],
        'eq_count': len(eq_legs),
        'eq_selectors': imms,
        'eq_selectors_sorted_ascending': imms == sorted(imms),
        'eq_pc_gaps': gaps,
        'eq_dsts': [p['eq_dst'] for p in eq_legs],
        'eq_dsts_all_jumpdest': all(p['eq_dst_is_jumpdest'] for p in eq_legs),
        'sub_legs': sub_legs,
        'sub_is_final_push4': bool(sub_legs and sub_legs[0]['pc'] == push4[-1]['pc']),
        'offset_rule': {
            'eq_legs_dst_eq_jumpdest': sum(1 for p in eq_legs if p['eq_dst_is_jumpdest']),
            'sub_leg_push4_pc_plus_10': [p['pc'] + 10 for p in sub_legs],
        },
    }


if __name__ == '__main__':
    path = sys.argv[1]
    code = open(path, 'rb').read()
    print(json.dumps(walk(code), indent=1, sort_keys=True))
