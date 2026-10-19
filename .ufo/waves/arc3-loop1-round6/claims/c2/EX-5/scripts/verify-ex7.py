"""Seat EX-5, arc3-loop1-round6: independent verification of EX-7's viaIR dispatch entry.

Re-derives every byte-level claim from EX-7's checked-in out/ bytes:
  - sha256 of all carrier files
  - selector set from the ABI via this seat's own keccak
  - dispatcher walk of viair-opt200 / viair-noopt / std-opt200
  - probe comparison against this seat's independent rea run
Outputs evidence/verify-ex7.json.
"""
import hashlib
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from disasm import dis  # noqa: E402
from keccak import keccak256  # noqa: E402

W = pathlib.Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round6/claims/c2/EX-7')
OUT = pathlib.Path('/var/tmp/ex05-r6/evidence')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(name):
    return (W / f'out/{name}/runtime.bin').read_bytes()


def abi_selectors(name):
    abi = json.loads((W / f'out/{name}/abi.json').read_text())
    sels = {}
    for item in abi:
        if item.get('type') != 'function':
            continue
        sig = item['name'] + '(' + ','.join(i['type'] for i in item.get('inputs', [])) + ')'
        sels[keccak256(sig.encode()).hex()[:8]] = sig
    return sels


def walk(code, sels, names):
    d = dis(code)
    push4 = [{'pc': pc, 'imm': imm, 'name': sels.get(imm)}
             for pc, op, name, imm, nxt in d if op == 0x63]
    eq, gt, sub = [], [], []
    by_pc = {o[0]: o for o in d}
    for i, (pc, op, name, imm, nxt) in enumerate(d):
        if op == 0x63:
            window = [o[2] for o in d[i + 1:i + 5]]
            # EQ chain leg: DUP1 PUSH4 sel EQ PUSH2 dst JUMPI
            if window[0] == 'EQ':
                tgt = d[i + 2] if i + 2 < len(d) else None
                eq.append({'push4_pc': pc, 'selector': imm, 'name': sels.get(imm),
                           'dst': int(tgt[3], 16) if tgt and tgt[2] == 'PUSH2' else None})
            elif window[0] == 'GT':
                tgt = d[i + 2] if i + 2 < len(d) else None
                gt.append({'push4_pc': pc, 'selector': imm, 'name': sels.get(imm),
                           'dst': int(tgt[3], 16) if tgt and tgt[2] == 'PUSH2' else None})
            elif window[0] == 'SUB':
                tgt = d[i + 2] if i + 2 < len(d) else None
                sub.append({'push4_pc': pc, 'selector': imm, 'name': sels.get(imm),
                            'dst': int(tgt[3], 16) if tgt and tgt[2] == 'PUSH2' else None})
    eq_pcs = [x['push4_pc'] for x in eq]
    gaps = sorted({b - a for a, b in zip(eq_pcs, eq_pcs[1:])})
    dst_jd = {x['dst']: code[x['dst']] == 0x5b for x in eq}
    return {
        'runtime_len': len(code),
        'runtime_sha256': hashlib.sha256(code).hexdigest(),
        'prologue_hex': code[:48].hex(),
        'push4_sites': push4,
        'non_selector_push4': [x for x in push4 if x['imm'] not in sels],
        'eq_legs': eq,
        'gt_legs': gt,
        'sub_legs': sub,
        'eq_pc_gaps': gaps,
        'eq_sorted_ascending': [x['selector'] for x in eq] == sorted(x['selector'] for x in eq),
        'all_eq_dst_jumpdests': all(dst_jd.values()),
        'eq_dst_jumpdest_map': dst_jd,
        'selector_count_in_abi': len(sels),
        'distinct_push4_selector_count': len({x['imm'] for x in push4 if x['imm'] in sels}),
    }


def main():
    OUT.mkdir(exist_ok=True)
    res = {}
    probes = {
        'viair-opt200': json.loads((pathlib.Path('/var/tmp/ex05-r6/probe/EX7-viair-opt200.hex.6.4.0.json')).read_text()),
    }
    # EX-7's own 6.4.0 envelope for byte comparison of the decoded payload
    own = json.loads((W / 'probe/probe-viair-opt200-hex-6.4.0.json').read_text())
    own = own.get('data', own)

    for name in ['viair-opt200', 'viair-noopt', 'std-opt200']:
        code = load(name)
        sels = abi_selectors(name)
        w = walk(code, sels, names={})
        # probe match (only the independently re-probed leg)
        if name == 'viair-opt200':
            p = probes[name]
            pd = p.get('data', p)
            nr = pd['normalized_result']
            w['independent_probe_6.4.0'] = {
                'evidence_id': pd['evidence_id'],
                'functions': len(nr['functions']),
                'dispatch_values': sorted({f['dispatch'] for f in nr['functions']}),
                'selectors': sorted(f['selector'].removeprefix('0x') for f in nr['functions']),
                'offsets': {f['selector'].removeprefix('0x'): f['bytecode_offset'] for f in nr['functions']},
                'mutability': {f['selector'].removeprefix('0x'): f['inferred_state_mutability'] for f in nr['functions']},
                'decoded_sha256': nr['bytecode']['sha256'],
                'selector_set_equals_my_abi_derivation': set(f['selector'].removeprefix('0x') for f in nr['functions']) == set(sels),
            }
            w['own_envelope_decoded_sha256'] = own.get('data', own)['normalized_result']['bytecode']['sha256']
        # creation embedding
        cr = (W / f'out/{name}/creation.bin').read_bytes()
        w['creation_len'] = len(cr)
        w['creation_sha256'] = hashlib.sha256(cr).hexdigest()
        w['runtime_embedded_at'] = cr.find(code)
        # offset rule from the independent probe
        if name == 'viair-opt200':
            offs = w['independent_probe_6.4.0']['offsets']
            by_sel = {x['selector']: x for x in w['eq_legs'] + w['sub_legs']}
            w['offset_rule'] = {}
            for s, off in offs.items():
                leg = by_sel.get(s)
                w['offset_rule'][s] = {
                    'reported': off,
                    'push4_pc': leg['push4_pc'] if leg else None,
                    'dst': leg['dst'] if leg else None,
                    'equals_dst': bool(leg and off == leg['dst']),
                    'delta_from_push4': off - leg['push4_pc'] if leg else None,
                    'is_jumpdest': code[off] == 0x5b,
                }
        res[name] = w

    # CBOR trailer decode of viair-opt200
    code = load('viair-opt200')
    tail = code[-64:]
    res['viair-opt200']['trailer_tail_hex'] = tail.hex()
    i = tail.find(bytes.fromhex('a2'))
    res['viair-opt200']['cbor_start'] = i
    # trap evidence: raw-on-hex and creation probe envelopes
    for tag, path in [('raw_on_hex_6.4.0', W / 'probe/probe-viair-opt200-hexasraw-TRAP-6.4.0.json'),
                      ('creation_6.4.0', W / 'probe/probe-viair-opt200-creation-6.4.0.json')]:
        j = json.loads(path.read_text())
        d = j.get('data', j)
        res['viair-opt200'][tag] = {
            'functions': len(d['normalized_result']['functions']),
            'decoded_sha256': d['normalized_result']['bytecode']['sha256'],
            'subject_file_sha256': j['subject']['digest']['sha256'],
            'evidence_id': d['evidence_id'],
        }
    # shipped file digests (runtime.hex text sha)
    res['file_sha256'] = {}
    for name in ['viair-opt200', 'viair-noopt', 'std-opt200']:
        for ext in ['runtime.bin', 'runtime.hex', 'creation.bin', 'creation.hex', 'abi.json', 'method-identifiers.json']:
            p = W / f'out/{name}/{ext}'
            res['file_sha256'][f'{name}/{ext}'] = sha(p)
    (OUT / 'verify-ex7.json').write_text(json.dumps(res, indent=1) + '\n')

    print('name  len  sha  push4  sel  dup  eq  gt  sub  gaps  asc  all_dst_jd  embed@')
    for name in ['viair-opt200', 'viair-noopt', 'std-opt200']:
        w = res[name]
        eqs = [x['selector'] for x in w['eq_legs']]
        print(name, w['runtime_len'], w['runtime_sha256'][:16], len(w['push4_sites']),
              len(set(eqs)), len(eqs) - len(set(eqs)), len(w['eq_legs']), len(w['gt_legs']),
              len(w['sub_legs']), w['eq_pc_gaps'], w['eq_sorted_ascending'],
              w['all_eq_dst_jumpdests'], w['runtime_embedded_at'])
    print('independent viair-opt200 probe:', res['viair-opt200']['independent_probe_6.4.0'])
    print('offset rule equal_dst count:', sum(1 for v in res['viair-opt200']['offset_rule'].values() if v['equals_dst']),
          '/', len(res['viair-opt200']['offset_rule']))
    print('sub legs:', res['viair-opt200']['sub_legs'])
    print('non-selector PUSH4 viair:', res['viair-opt200']['non_selector_push4'])
    print('non-selector PUSH4 std:', res['std-opt200']['non_selector_push4'])
    print('creation embed:', {n: (res[n]['creation_len'], res[n]['runtime_embedded_at']) for n in ['viair-opt200', 'viair-noopt', 'std-opt200']})
    print('traps:', {k: (res['viair-opt200'][k]['functions'], res['viair-opt200'][k]['decoded_sha256'][:16]) for k in ['raw_on_hex_6.4.0', 'creation_6.4.0']})


if __name__ == '__main__':
    main()
