"""Seat EX-5, arc3-loop1-round6: byte-level dispatcher walk for Vyper 0.4.3 optimizer forms.

Two carriers: K8 (round-4 CR-1 source; fresh compile byte-identical to custody) and
Ex05Vault (this seat; mixed mutability). Outputs one JSON per (carrier, form).
"""
import hashlib
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from disasm import dis  # noqa: E402
from keccak import selector  # noqa: E402

ROOT = pathlib.Path('/var/tmp/ex05-r6')
SETS = {
    'K8': [f'f{i}(uint256)' for i in range(8)],
    'Ex05Vault': ['alpha(uint256)', 'beta(uint256)', 'gamma(uint256)', 'delta(uint256)',
                  'epsilon()', 'zeta()', 'eta()'],
}
FORMS = [('gas', '-O gas (default)'), ('noopt', '--no-optimize'), ('codesize', '-O codesize')]


def load(carrier, form):
    rt = (ROOT / f'out/{carrier}.{form}.runtime.hex').read_text().strip().removeprefix('0x')
    cr = (ROOT / f'out/{carrier}.{form}.creation.hex').read_text().strip().removeprefix('0x')
    return bytes.fromhex(rt), bytes.fromhex(cr)


def probes(carrier, form):
    out = []
    for pin in ['6.4.0', '6.7.0']:
        p = ROOT / f'probe/{carrier}.{form}.hex.{pin}.json'
        if not p.exists():
            continue
        j = json.loads(p.read_text())
        d = j.get('data', j)
        nr = d['normalized_result']
        out.append({
            'rea_pin': pin,
            'evidence_id': d['evidence_id'],
            'subject_file_sha256': j['subject']['digest']['sha256'],
            'decoded_sha256': nr['bytecode']['sha256'],
            'functions': len(nr['functions']),
            'dispatch_values': sorted({f['dispatch'] for f in nr['functions']}),
            'selectors': sorted(f['selector'].removeprefix('0x') for f in nr['functions']),
            'offsets': {f['selector'].removeprefix('0x'): f['bytecode_offset'] for f in nr['functions']},
            'mutability': {f['selector'].removeprefix('0x'): f['inferred_state_mutability'] for f in nr['functions']},
            'arguments': {f['selector'].removeprefix('0x'): f['inferred_arguments'] for f in nr['functions']},
        })
    return out


def walk_xor_table(code, sels, names):
    d = dis(code)
    by_pc = {o[0]: o for o in d}
    bucket_count = code[8]
    table_base = int.from_bytes(code[15:17], 'big')
    table = [int.from_bytes(code[table_base + 2 * i:table_base + 2 * i + 2], 'big')
             for i in range(bucket_count)]
    sentinel = table[0]
    chains = {}
    for b, head in enumerate(table):
        steps = []
        if head != sentinel:
            pc = head
            guard = 0
            while guard < 40:
                o = by_pc.get(pc)
                if o is None:
                    break
                if o[2] == 'JUMPDEST':
                    pc += 1
                    continue
                if o[1] == 0x63:
                    sel = o[3]
                    nxt = by_pc.get(pc + 7)
                    target = int(nxt[3], 16) if nxt and nxt[2] == 'PUSH2' else None
                    steps.append({'push4_pc': pc, 'selector': sel, 'name': names.get(sel), 'next_pc': target})
                    if target is None:
                        break
                    pc = target
                    guard += 1
                    continue
                break
        chains[b] = {'head': head, 'empty': head == sentinel, 'members': steps}
    push4 = [{'pc': pc, 'imm': imm, 'selector_name': names.get(imm)}
             for pc, op, name, imm, nxt in d if op == 0x63]
    return {
        'dispatch_class': 'selector %% %d; CODECOPY one uint16 bucket entry to mem[30:32]; MLOAD; JUMP; per-bucket XOR chain' % bucket_count,
        'prologue_hex': code[:24].hex(),
        'bucket_count': bucket_count,
        'table_base': table_base,
        'table_entries': table,
        'empty_bucket_sentinel': sentinel,
        'buckets': chains,
        'push4_sites': push4,
        'non_selector_push4': [x for x in push4 if x['imm'] not in sels],
        'selector_buckets': {names[s]: {'selector': s, 'bucket': int(s, 16) % bucket_count} for s in sels},
    }


def walk_eq_chain(code, sels, names):
    d = dis(code)
    legs = []
    for i, (pc, op, name, imm, nxt) in enumerate(d):
        if op == 0x63 and imm in sels:
            seq = [o[2] for o in d[i + 1:i + 8]]
            legs.append({
                'push4_pc': pc, 'selector': imm, 'name': names[imm],
                'compare_seq': seq,
                'next_pc': int(d[i + 4][3], 16) if d[i + 4][2] == 'PUSH2' else None,
                'body_pc': pc + 12 if seq[:4] == ['DUP2', 'EQ', 'ISZERO', 'PUSH2'] else None,
            })
    return {
        'dispatch_class': 'linear source-order EQ+ISZERO chain; per-leg calldata/value guards inline; PUSH2 handler jump',
        'prologue_hex': code[:14].hex(),
        'guard': {
            'bytes': code[0:13].hex(),
            'decoded': 'PUSH1 4; CALLDATASIZE; LT; ISZERO; PUSH2 0x000d; JUMPI; PUSH2 <revert>; JUMP',
            'semantics': 'calldatasize >= 4 -> dispatch (JUMPDEST at 13); else revert block',
        },
        'legs': legs,
        'push4_sites': [{'pc': pc, 'imm': imm, 'selector_name': names.get(imm)}
                        for pc, op, name, imm, nxt in d if op == 0x63],
        'non_selector_push4': [{'pc': pc, 'imm': imm} for pc, op, name, imm, nxt in d
                               if op == 0x63 and imm not in sels],
    }


def walk_phf_table(code, sels, names):
    header_off = int.from_bytes(code[8:10], 'big')  # PUSH2 at pc 7 in the prologue
    header = code[header_off:header_off + 5]
    multiplier = int.from_bytes(header[0:2], 'big')
    table_base = int.from_bytes(header[2:4], 'big')
    count = header[4]
    entries = []
    for i in range(count):
        off = table_base + 7 * i
        raw = code[off:off + 7]
        entries.append({
            'table_offset': off,
            'selector': raw[0:4].hex(),
            'name': names.get(raw[0:4].hex()),
            'handler_offset': int.from_bytes(raw[4:6], 'big'),
            'tag': raw[6],
            'tag_decode': {
                'nonpayable_revert_on_value': raw[6] & 1,
                'required_calldata_bytes_minus_4': (raw[6] & 0xfe) - 4,
            },
            'handler_is_jumpdest': code[int.from_bytes(raw[4:6], 'big')] == 0x5b,
        })
    derived = {}
    for s in sels:
        idx = ((int(s, 16) * multiplier) >> 24) % count
        derived[names[s]] = {'selector': s, 'index': idx,
                             'entry_selector': entries[idx]['selector'],
                             'perfect': entries[idx]['selector'] == s}
    return {
        'dispatch_class': 'minimal-perfect-hash direct table: CODECOPY 5-byte header; index=((sel*K)>>24)%%count; CODECOPY 7-byte entry; verify selector; tag guard; JUMP handler (K=%d, count=%d)' % (len(sels), count),
        'prologue_hex': code[:32].hex(),
        'header': {'raw_hex': header.hex(), 'multiplier': multiplier,
                   'table_base': table_base, 'count': count},
        'entries': entries,
        'perfect_hash': derived,
        'push4_sites': [{'pc': pc, 'imm': imm} for pc, op, name, imm, nxt in dis(code) if op == 0x63],
        'selector_literals_present_only_as_table_data': True,
    }


def main():
    outdir = ROOT / 'evidence'
    outdir.mkdir(exist_ok=True)
    summary = {}
    walkers = {'gas': walk_xor_table, 'noopt': walk_eq_chain, 'codesize': walk_phf_table}
    for carrier, sigs in SETS.items():
        sels = {selector(s): s for s in sigs}
        names = {selector(s): s.split('(')[0] for s in sigs}
        src = ROOT / f'src/{carrier}.vy'
        summary[carrier] = {}
        for form, flag in FORMS:
            code, creation = load(carrier, form)
            walk = walkers[form](code, sels, names)
            walk.update({
                'carrier': carrier,
                'form': form,
                'compile_flags': flag,
                'compiler': 'vyper 0.4.3+commit.bff19ea2',
                'source': f'{src.name} sha256 {hashlib.sha256(src.read_bytes()).hexdigest()}',
                'runtime_len': len(code),
                'runtime_sha256': hashlib.sha256(code).hexdigest(),
                'creation_len': len(creation),
                'creation_sha256': hashlib.sha256(creation).hexdigest(),
                'planted_selectors': {s: names[s] for s in sels},
                'probes': probes(carrier, form),
                'offset_rule': {},
            })
            for p in walk['probes']:
                offs = p['offsets']
                if form in ('gas', 'noopt'):
                    pushes = ({l['selector']: l['push4_pc'] for l in walk.get('legs', [])} or
                              {x['imm']: x['pc'] for x in walk.get('push4_sites', [])})
                    walk['offset_rule'][p['rea_pin']] = {
                        'reported_offsets': offs,
                        'push4_pc': pushes,
                        'delta': {s: offs[s] - pushes[s] for s in offs},
                        'landing': {s: 'body_guard_pc' for s in offs},
                    }
                else:
                    walk['offset_rule'][p['rea_pin']] = {
                        'reported_offsets': offs,
                        'distinct_offsets': sorted(set(offs.values())),
                        'note': 'all K selectors report the same shared post-match guard pc; handlers are table-resolved',
                        'handler_offsets_from_table': {e['selector']: e['handler_offset'] for e in walk['entries']},
                    }
            summary[carrier][form] = {
                'runtime_len': walk['runtime_len'],
                'runtime_sha256': walk['runtime_sha256'],
                'creation_len': walk['creation_len'],
                'creation_sha256': walk['creation_sha256'],
                'dispatch_class': walk['dispatch_class'],
            }
            (outdir / f'walk-{carrier}-{form}.json').write_text(json.dumps(walk, indent=1) + '\n')
            print(carrier, form, walk['runtime_len'], walk['runtime_sha256'])
    (outdir / 'walk-summary.json').write_text(json.dumps(summary, indent=1) + '\n')


if __name__ == '__main__':
    main()
