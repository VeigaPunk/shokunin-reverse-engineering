#!/usr/bin/env python3
"""EX-7 dispatcher walk — fixed compare-site pattern + per-offset decode."""
import hashlib
import json
import sys

PUSHN = {0x60 + i: i + 1 for i in range(32)}
JUMPDEST = 0x5B
PLANTED = {'deposit': 'd0e30db0', 'digestOf': '6901eb1e', 'mark': 'ee02438e',
           'marked': '1c8e5adb', 'pause': '8456cb59', 'readBalance': '78d20574',
           'readFee': '90ab171e', 'readOwner': '9389acb5', 'readPaused': '8e943bce',
           'readTotal': '5ff1f6ee', 'scale': '6e69f38c', 'setFee': '69fe0e2d',
           'sweep': '01681a62', 'unpause': '3f4ba83a', 'withdraw': '2e1a7d4d'}
SEL2NAME = {v: k for k, v in PLANTED.items()}
PLANTED_HEX = set(PLANTED.values())


def sweep(code):
    pc = 0
    out = []
    while pc < len(code):
        op = code[pc]
        if op in PUSHN:
            ln = PUSHN[op]
            out.append((pc, op, code[pc + 1:pc + 1 + ln]))
            pc += 1 + ln
        else:
            out.append((pc, op, None))
            pc += 1
    return out


def main(tag, hexfile, probefile):
    code = bytes.fromhex(open(hexfile).read().strip())
    env = json.load(open(probefile))
    fns = env['normalized_result']['functions']
    ops = sweep(code)
    report = {'tag': tag, 'runtime_len': len(code),
              'runtime_sha256': hashlib.sha256(code).hexdigest()}

    # compare sites: [PUSH4 imm] [EQ|GT] [PUSH2 dst] [JUMPI] — optional DUP1 before
    sites = []
    for i, (pc, op, imm) in enumerate(ops):
        if op == 0x63 and i + 3 < len(ops):
            c1 = ops[i + 1]
            c2 = ops[i + 2]
            c3 = ops[i + 3]
            if c1[1] in (0x14, 0x11) and c2[1] == 0x61 and c3[1] == 0x57:
                dst = int.from_bytes(c2[2], 'big')
                sites.append({'pc': pc, 'imm': imm.hex(), 'cmp': 'EQ' if c1[1] == 0x14 else 'GT',
                              'dst': dst, 'dst_is_jumpdest': code[dst] == JUMPDEST,
                              'dup1_before': ops[i - 1][1] == 0x80})
    eq = [s for s in sites if s['cmp'] == 'EQ']
    gt = [s for s in sites if s['cmp'] == 'GT']
    report['compare_sites'] = {
        'count': len(sites), 'eq': len(eq), 'gt': len(gt),
        'eq_imms_in_order': [s['imm'] for s in eq],
        'eq_sorted_ascending': [s['imm'] for s in eq] == sorted(s['imm'] for s in eq),
        'eq_first_pc': eq[0]['pc'] if eq else None, 'eq_last_pc': eq[-1]['pc'] if eq else None,
        'eq_strictly_contiguous': None,
        'all_dst_jumpdests': all(s['dst_is_jumpdest'] for s in sites),
        'gt_sites': [{'pc': s['pc'], 'imm': s['imm']} for s in gt],
    }
    if len(eq) > 1:
        gaps = [eq[k + 1]['pc'] - eq[k]['pc'] for k in range(len(eq) - 1)]
        report['compare_sites']['eq_pc_gaps'] = gaps
        report['compare_sites']['eq_strictly_contiguous'] = len(set(gaps)) == 1

    # per-offset decode
    push2_targets = {int.from_bytes(imm, 'big') for _, op, imm in ops if op == 0x61}
    rows = []
    for fn in sorted(fns, key=lambda f: f['bytecode_offset']):
        off = fn['bytecode_offset']
        sel = fn['selector'].removeprefix('0x')
        site = next((s for s in sites if s['imm'] == sel), None)
        rows.append({'selector': sel, 'name': SEL2NAME[sel], 'offset': off,
                     'byte_hex': f"{code[off]:02x}", 'is_jumpdest': code[off] == JUMPDEST,
                     'is_push2_target': off in push2_targets,
                     'eq_site_pc': site['pc'] if site else None,
                     'eq_dst': site['dst'] if site else None,
                     'offset_minus_site_pc': off - site['pc'] if site else None,
                     'offset_minus_dst': off - site['dst'] if site else None,
                     'ctx': code[max(0, off - 4):off + 5].hex()})
    report['offset_rows'] = rows
    report['offset_summary'] = {
        'jumpdest': sum(1 for r in rows if r['is_jumpdest']),
        'push2_target': sum(1 for r in rows if r['is_push2_target']),
        'dist_rules': sorted({r['offset_minus_site_pc'] for r in rows if r['offset_minus_site_pc'] is not None}),
        'non_jumpdest_rows': [{k: r[k] for k in ('selector', 'offset', 'byte_hex', 'ctx', 'eq_dst', 'offset_minus_dst')} for r in rows if not r['is_jumpdest']],
    }

    # dispatcher head ops (first 60) + guard structure
    report['head_ops'] = ' '.join(
        f"{op:02x}" if imm is None else f"{op:02x}<{imm.hex()}>" for _, op, imm in ops[:60])

    # PUSH4 non-selector census
    non_sel = [{'pc': pc, 'imm': imm.hex()} for pc, op, imm in ops
               if op == 0x63 and imm.hex() not in PLANTED_HEX]
    report['push4_non_selector'] = non_sel
    print(json.dumps(report, indent=1))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
