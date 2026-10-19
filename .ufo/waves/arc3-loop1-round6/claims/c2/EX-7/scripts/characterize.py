#!/usr/bin/env python3
"""EX-7 byte-level characterization of the three ViaIrVault runtimes.

For each leg:
  1. opcode-boundary linear sweep (PUSHn-aware) -> PUSH4 immediate census
     classified selector / non-selector
  2. reported probe offsets: byte at offset, is it JUMPDEST (0x5b), is it a
     PUSH2 dispatch target, is it push4_pc+11 (r4 Vyper rule)
  3. compare-site walk: locate every `PUSH4 <imm> <EQ|GT> PUSH2 <dst> JUMPI`
     site, group by class, list dst, note sortedness
  4. CBOR trailer decode (solc metadata)
"""
import json
import sys

PUSH = 0x60
PUSHN = {0x60 + i: i + 1 for i in range(32)}
JUMPDEST = 0x5B
PLANTED = {'deposit': 'd0e30db0', 'digestOf': '6901eb1e', 'mark': 'ee02438e',
           'marked': '1c8e5adb', 'pause': '8456cb59', 'readBalance': '78d20574',
           'readFee': '90ab171e', 'readOwner': '9389acb5', 'readPaused': '8e943bce',
           'readTotal': '5ff1f6ee', 'scale': '6e69f38c', 'setFee': '69fe0e2d',
           'sweep': '01681a62', 'unpause': '3f4ba83a', 'withdraw': '2e1a7d4d'}
SEL2NAME = {v: k for k, v in PLANTED.items()}
PLANTED_HEX = set(PLANTED.values())


def sweep(code: bytes):
    """linear sweep honoring PUSHn immediates; yield (pc, op, imm_or_None)."""
    pc = 0
    out = []
    n = len(code)
    while pc < n:
        op = code[pc]
        if op in PUSHN:
            ln = PUSHN[op]
            imm = code[pc + 1:pc + 1 + ln]
            out.append((pc, op, imm))
            pc += 1 + ln
        else:
            out.append((pc, op, None))
            pc += 1
    return out


def push4_census(code):
    rows = []
    for pc, op, imm in sweep(code):
        if op == 0x63:  # PUSH4
            h = imm.hex()
            rows.append((pc, h, SEL2NAME.get(h, '')))
    return rows


def byte_at(code, off):
    return code[off] if 0 <= off < len(code) else None


def main(tag, hexfile, probefile):
    code = bytes.fromhex(open(hexfile).read().strip())
    env = json.load(open(probefile))
    nr = env['normalized_result']
    fns = nr['functions']
    report = {'tag': tag, 'runtime_len': len(code), 'runtime_sha256': __import__('hashlib').sha256(code).hexdigest()}

    # 1. PUSH4 census
    c4 = push4_census(code)
    sel_hits = [r for r in c4 if r[1] in PLANTED_HEX]
    non_sel = [r for r in c4 if r[1] not in PLANTED_HEX]
    dup_sel = sorted({r[1] for r in sel_hits if [x[1] for x in sel_hits].count(r[1]) > 1})
    report['push4_census'] = {
        'total_push4_sites': len(c4),
        'selector_sites': len(sel_hits),
        'distinct_selectors': len({r[1] for r in sel_hits}),
        'duplicated_selectors': dup_sel,
        'non_selector_immediates': [{'pc': pc, 'imm': h} for pc, h, _ in non_sel],
    }

    # 2. offsets
    push2_targets = set()
    for pc, op, imm in sweep(code):
        if op == 0x61:  # PUSH2
            push2_targets.add(int.from_bytes(imm, 'big'))
    off_rows = []
    for fn in sorted(fns, key=lambda f: f['bytecode_offset']):
        off = fn['bytecode_offset']
        sel = fn['selector'].removeprefix('0x')
        # find the compare site whose selector is this: pc of PUSH4 with this imm
        site = next((pc for pc, h, _ in c4 if h == sel), None)
        off_rows.append({
            'selector': sel, 'name': SEL2NAME[sel], 'offset': off,
            'byte_at_offset': hex(byte_at(code, off)),
            'is_jumpdest': byte_at(code, off) == JUMPDEST,
            'is_push2_target': off in push2_targets,
            'eq_push4_pc': site,
            'offset_minus_push4pc': off - site if site is not None else None,
        })
    report['offsets'] = off_rows

    # 3. compare-site walk: PUSH4 imm (EQ=0x14|GT=0x11) PUSH2 dst JUMPI(0x57)
    ops = sweep(code)
    sites = []
    for i, (pc, op, imm) in enumerate(ops):
        if op == 0x63 and i + 4 < len(ops):
            op1, op2, op3, op4 = ops[i + 1][1], ops[i + 2][1], ops[i + 3][1], ops[i + 4][1]
            imm2 = ops[i + 3][2] if op2 == 0x61 or op2 == 0x63 else None
            # pattern A: PUSH4 sel EQ PUSH2 dst JUMPI
            if op1 == 0x14 and op2 == 0x61 and op4 == 0x57:
                dst = int.from_bytes(ops[i + 3][2], 'big')
                sites.append({'pc': pc, 'imm': imm.hex(), 'cmp': 'EQ', 'dst': dst,
                              'named': SEL2NAME.get(imm.hex(), '')})
            # pattern B: PUSH4 sel GT PUSH2 dst JUMPI
            elif op1 == 0x11 and op2 == 0x61 and op4 == 0x57:
                dst = int.from_bytes(ops[i + 3][2], 'big')
                sites.append({'pc': pc, 'imm': imm.hex(), 'cmp': 'GT', 'dst': dst,
                              'named': SEL2NAME.get(imm.hex(), '')})
    report['compare_sites'] = {
        'count': len(sites),
        'cmp_mix': sorted({s['cmp'] for s in sites}),
        'eq_order': [s['imm'] for s in sites if s['cmp'] == 'EQ'],
        'gt_imms': [s['imm'] for s in sites if s['cmp'] == 'GT'],
        'eq_sorted_ascending': [s['imm'] for s in sites if s['cmp'] == 'EQ'] ==
            sorted(s['imm'] for s in sites if s['cmp'] == 'EQ'),
        'dst_all_jumpdests': all(byte_at(code, s['dst']) == JUMPDEST for s in sites),
    }

    # 4. CBOR trailer (solc metadata): scan tail for 0xa2 0x65 'ipfs'... or a1/a2 begin-map
    tail = code[-200:]
    idx = tail.find(b'\xa2\x65ipfs')
    if idx == -1:
        idx = tail.find(b'\xa1\x65ipfs')
    report['cbor'] = {'ipfs_marker_at_tail_offset': (idx + (len(code) - 200)) if idx != -1 else None}

    print(json.dumps(report, indent=1))
    return report


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
