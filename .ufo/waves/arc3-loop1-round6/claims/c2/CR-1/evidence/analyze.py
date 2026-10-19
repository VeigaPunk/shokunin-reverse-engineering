"""Form-specific dispatch analyzer for the Vyper 0.4.3 optimizer variants.

Seat CR-1, arc3-loop1-round6. Reads pinned runtime carriers (read-only) and
emits a JSON/text characterization derived from the bytes alone.
"""
import hashlib
import json
import sys

from disasm import NAMES, load, sweep


def u16(code, off):
    return int.from_bytes(code[off:off + 2], 'big')


def u32(code, off):
    return int.from_bytes(code[off:off + 4], 'big')


def op_at(code, pc):
    op = code[pc]
    if op == 0x5f:
        return op, b''
    if 0x60 <= op <= 0x7f:
        return op, code[pc + 1:pc + 1 + op - 0x5f]
    return op, b''


def push_sites(code, want):
    return [(pc, int.from_bytes(imm, 'big')) for pc, op, imm in sweep(code) if op == want]


def opcode_counts(code):
    counts = {}
    for _, op, _ in sweep(code):
        nm = NAMES.get(op, f'0x{op:02x}')
        counts[nm] = counts.get(nm, 0) + 1
    return counts


def form_a(code):
    """5f3560e01c|60003560e01c header, u16 table at base, XOR chain."""
    out = {}
    # header: PUSH1 2 PUSH1 N DUP3 MOD PUSH1 1 SHL PUSH2 base ADD PUSH1 0x1e CODECOPY
    i = code.find(bytes.fromhex('6002'))
    assert i >= 0
    n = code[i + 3]
    # locate pattern 6001 1b 61 xx xx 01 601e 39
    j = code.find(bytes.fromhex('60011b'), i)
    assert j == i + 6, (i, j, code[i:i + 20].hex())
    assert code[j + 3] == 0x61, code[j + 3:j + 10].hex()
    base = u16(code, j + 4)
    assert code[j + 6] == 0x01 and code[j + 8] == 0x1e and code[j + 9] == 0x39
    table = [u16(code, base + 2 * k) for k in range(n)]
    out.update({
        'form': 'A',
        'prologue_hex': code[:5].hex(),
        'bucket_count': n,
        'table_base': base,
        'entry_size': 2,
        'table': table,
        'table_all_jumpdests': all(t in [pc for pc, op, _ in sweep(code) if op == 0x5b]
                                   for t in table),
        'empty_sentinel': sorted({t for t in table if table.count(t) > 1}),
        'distinct_targets': sorted(set(table)),
        'push4_sites': [{'pc': pc, 'sel': f'{s:08x}'} for pc, s in push_sites(code, 0x63)],
        'compare_ops': {k: opcode_counts(code).get(k, 0) for k in ('XOR', 'EQ', 'GT', 'ISZERO')},
    })
    return out


def form_b(code):
    out = {}
    p4 = push_sites(code, 0x63)
    out.update({'form': 'B', 'push4_count': len(p4)})
    sites = []
    for pc, sel in p4:
        ops_after = {q: (o, im) for q, o, im in sweep(code) if q > pc}
        qs = sorted(q for q in ops_after if q <= pc + 14)
        seq = [f'{NAMES.get(ops_after[q][0], hex(ops_after[q][0]))}'
               f'{(" 0x" + ops_after[q][1].hex()) if ops_after[q][1] else ""}'
               for q in qs]
        sites.append({'pc': pc, 'sel': f'{sel:08x}', 'seq_after_push4': seq,
                      'body_pc': pc + 12, 'body_byte': f'0x{code[pc + 12]:02x}'})
    out['sites'] = sites
    out['strides'] = [b - a for a, b in zip([s['pc'] for s in sites],
                                            [s['pc'] for s in sites][1:])]
    out['eq_count'] = opcode_counts(code).get('EQ', 0)
    out['xor_count'] = opcode_counts(code).get('XOR', 0)
    out['push2_count'] = len(push_sites(code, 0x61))
    return out


def form_c(code):
    out = {}
    # header CODECOPY: 6005 61<off> 601b 39  -> 5 bytes = [u16 mult][u16 base][u8 n]
    i = code.find(bytes.fromhex('600561'))
    assert i == 5, code[:24].hex()
    off = u16(code, i + 3)
    hdr = code[off:off + 5]
    mult = u16(hdr, 0)
    base = u16(hdr, 2)
    n = hdr[4]
    entries = []
    for k in range(n):
        e = code[base + 7 * k:base + 7 * k + 7]
        sel = int.from_bytes(e[0:4], 'big')
        dst = int.from_bytes(e[4:6], 'big')
        flags = e[6]
        idx = ((mult * sel) >> 24) % n
        entries.append({'index': k, 'sel': f'{sel:08x}', 'dst': dst,
                       'dst_is_jumpdest': dst in [pc for pc, op, _ in sweep(code)
                                                  if op == 0x5b],
                       'guard_byte': f'0x{flags:02x}',
                       'calldata_minus4': (flags & 0xfe),
                       'payable_bit': flags & 1,
                       'hash_index': idx, 'hash_hits_entry': idx == k})
    out.update({'form': 'C', 'header': {'at': off, 'mult': mult, 'base': base,
                                        'count': n},
                'entry_stride': 7, 'table_end': base + 7 * n, 'code_len': len(code),
                'entries': entries,
                'hash_distinct': len({e['hash_index'] for e in entries}) == n,
                'push4_count': len(push_sites(code, 0x63)),
                'compare_ops': {k: opcode_counts(code).get(k, 0)
                                for k in ('XOR', 'EQ', 'GT', 'ISZERO')}})
    return out


def analyze(path):
    code = load(path)
    counts = opcode_counts(code)
    jumpdests = [pc for pc, op, _ in sweep(code) if op == 0x5b]
    if code[:5] == bytes.fromhex('5f3560e01c') and code.find(bytes.fromhex('600260'), 0, 20) == 5:
        detail = form_a(code)
    elif code[:6] == bytes.fromhex('60003560e01c') and code.find(bytes.fromhex('600260'), 0, 20) == 6:
        detail = form_a(code)
        detail['note'] = 'no-PUSH0 prologue (paris/london hardfork)'
    elif code.find(bytes.fromhex('600561')) == 5:
        detail = form_c(code)
    elif code.find(bytes.fromhex('6004361015')) == 0:
        detail = form_b(code)
    else:
        detail = {'form': 'unknown'}
    return {
        'path': path,
        'bytes': len(code),
        'sha256': hashlib.sha256(code).hexdigest(),
        'hex_file_sha256': hashlib.sha256(open(path, 'rb').read()).hexdigest(),
        'jumpdest_count': len(jumpdests),
        'jumpdests': jumpdests,
        'prologue_hex': code[:8].hex(),
        'opcodes': {k: counts.get(k, 0) for k in
                    ('PUSH0', 'PUSH1', 'PUSH2', 'PUSH4', 'XOR', 'EQ', 'GT',
                     'ISZERO', 'MOD', 'SHL', 'SHR', 'CODECOPY', 'MLOAD', 'JUMP',
                     'JUMPI', 'JUMPDEST')},
        'detail': detail,
    }


if __name__ == '__main__':
    for p in sys.argv[1:]:
        print(json.dumps(analyze(p), indent=1))
