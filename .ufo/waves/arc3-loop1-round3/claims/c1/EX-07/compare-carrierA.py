#!/usr/bin/env python3
"""EX-07 (arc3-loop1-round3, c1): carrier A (EX-03 CarrierA) cross-pin / cross-encoding comparison.

Carrier A = EX-03's `CarrierA` (source sha256 05b2cbb0…), solc 0.8.37 with the
optimizer enabled (--optimize --optimize-runs 200), runtime 1426 B / sha256
87d1bb03… (hex carrier ecd767… see manifest). Planted table: EX-03
planted-selectors.txt (sha256 d905412a…, K=9).

Compares the probe legs in this seat dir (legC-*) against the planted table and
against each other (payload, ids, decoded digests), and scans the carrier's
runtime bytes for non-dispatch PUSH4 constants (custom-error selectors) that the
probe must NOT report.

Usage: python3 compare-carrierA.py
"""
import json, glob, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
CARRIER = '/var/tmp/ex07/ex03/carrierA.runtime.hex'

SIGNATURES = {
    '01681a62': 'sweep(address)',
    '067b23c3': 'totalCredited()',
    '2e1a7d4d': 'withdraw(uint256)',
    '3f0d861a': 'rotate(address)',
    '5ce23950': 'isSolvent()',
    '75807250': 'creditOf(address)',
    '8da5cb5b': 'owner()',
    'c85e07b9': 'stamp()',
    'd0e30db0': 'deposit()',
}
ABI = json.load(open('/var/tmp/ex07/ex03/carrierA.abi.json'))
ABI_MUT = {}
for e in ABI:
    if e.get('type') == 'function':
        sig = e['name'] + '(' + ','.join(i['type'] for i in e['inputs']) + ')'
        ABI_MUT[e['name'] + '(' + ','.join(i['type'] for i in e['inputs']) + ')'] = e['stateMutability']


def load(path):
    d = json.load(open(path))
    return d.get('data', d)


def leg(path):
    d = load(path)
    nr = d['normalized_result']
    fns = [(x['selector'].replace('0x', ''), x['bytecode_offset'], x['dispatch'],
            x['inferred_state_mutability'], x['inferred_arguments']) for x in nr['functions']]
    return dict(file=os.path.basename(path), ev=d['evidence_id'], enc=d['parameters']['encoding'],
                path=d['parameters'].get('path'), subj=d['subject']['digest']['sha256'],
                bc=nr['bytecode']['sha256'], bc_bytes=nr['bytecode']['bytes'],
                art_bytes=nr['artifact']['bytes'], fns=sorted(fns),
                topkeys=sorted(d))


def keccak4(sig):
    # pure-python keccak-256 (reference-derived sponge), returns first 4 bytes hex
    RC = [0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
          0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
          0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
          0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
          0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
          0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008]
    R = [[0, 36, 3, 41, 18], [1, 44, 10, 45, 2], [62, 6, 43, 15, 61],
         [28, 55, 25, 21, 56], [27, 20, 39, 8, 14]]
    M = (1 << 64) - 1

    def rol(x, n):
        return ((x << n) | (x >> (64 - n))) & M

    rate = 136
    data = bytearray(sig.encode())
    padlen = rate - (len(data) % rate)
    data += b'\x01' + b'\x00' * (padlen - 2) + b'\x80'
    S = [[0] * 5 for _ in range(5)]
    for off in range(0, len(data), rate):
        blk = data[off:off + rate]
        for i in range(rate // 8):
            lane = int.from_bytes(blk[i * 8:i * 8 + 8], 'little')
            x, y = i % 5, i // 5
            S[x][y] ^= lane
        for rnd in range(24):
            C = [S[x][0] ^ S[x][1] ^ S[x][2] ^ S[x][3] ^ S[x][4] for x in range(5)]
            D = [C[(x - 1) % 5] ^ rol(C[(x + 1) % 5], 1) for x in range(5)]
            for x in range(5):
                for y in range(5):
                    S[x][y] ^= D[x]
            B = [[0] * 5 for _ in range(5)]
            for x in range(5):
                for y in range(5):
                    B[y][(2 * x + 3 * y) % 5] = rol(S[x][y], R[x][y])
            for x in range(5):
                for y in range(5):
                    S[x][y] = B[x][y] ^ ((~B[(x + 1) % 5][y]) & B[(x + 2) % 5][y])
            S[0][0] ^= RC[rnd]
    out = b''.join(int.to_bytes(S[x][y], 8, 'little') for y in range(5) for x in range(5))
    return out[:4].hex()


def main():
    # self-test of keccak4 against known ERC-20 vectors
    assert keccak4('transfer(address,uint256)') == 'a9059cbb', keccak4('transfer(address,uint256)')
    assert keccak4('stamp()') == 'c85e07b9', keccak4('stamp()')
    print('keccak4 self-test vs known vectors: PASS (a9059cbb, c85e07b9)')

    planted_raw = open('/var/tmp/ex07/ex03/planted-selectors.txt').read().strip().split('\n')
    planted = {}
    for line in planted_raw:
        if line.startswith('0x'):
            sel, sig = line.split()[0][2:], line.split()[1]
            planted[sel] = sig
    print(f"planted from EX-03 table: K={len(planted)}")
    # independent keccak re-derivation of every planted selector
    for sel, sig in planted.items():
        assert keccak4(sig) == sel, (sig, sel, keccak4(sig))
    print('independent keccak-256 re-derivation of all 9 planted selectors: PASS')

    rows = [leg(p) for p in sorted(glob.glob(os.path.join(HERE, 'legC-*.json')))]
    allok = True
    for r in rows:
        got = [f[0] for f in r['fns']]
        missing = sorted(set(planted) - set(got)); extra = sorted(set(got) - set(planted))
        if missing or extra:
            allok = False
        print(f"\n{r['file']:30s} enc={r['enc']:3s} ev={r['ev']}")
        print(f"    path={r['path']}")
        print(f"    subject={r['subj'][:16]}… artifact={r['art_bytes']}B decoded={r['bc'][:16]}… {r['bc_bytes']}B n={len(got)}")
        print(f"    missing={missing} extra={extra}")
        for sel, off, disp, mut, args in r['fns']:
            abi_mut = ABI_MUT.get(planted.get(sel, SIGNATURES.get(sel, '')))
            flag = '' if abi_mut is None or mut == abi_mut else f'  <-- mutability differs from ABI ({abi_mut})'
            print(f"    {sel} {planted.get(sel, SIGNATURES.get(sel,'?')):<34s} off={off:4d} dispatch={disp} mut={mut} args={args!r}{flag}")

    print('\n== cross-check ==')
    ids = {r['file']: r['ev'] for r in rows}
    print('distinct ev ids:', len(set(ids.values())), 'of', len(ids))
    print('rerun stability 6.7.0 hex:', ids['legC-hex-6.7.0.json'] == ids['legC-hex-6.7.0-rerun.json'])
    print('rerun stability 6.4.0 raw:', ids['legC-raw-6.4.0.json'] == ids['legC-raw-6.4.0-rerun.json'])
    for pin in ('6.4.0', '6.5.0', '6.7.0'):
        h = [r for r in rows if r['file'] == f'legC-hex-{pin}.json'][0]
        rr = [r for r in rows if r['file'] == f'legC-raw-{pin}.json'][0]
        print(f'pin {pin}: hex==raw payload {h["fns"] == rr["fns"]}; decoded sha equal {h["bc"] == rr["bc"]}')
    print('distinct payloads across all legs:', len(set(json.dumps(r['fns']) for r in rows)))
    print('distinct decoded digests across all legs:', len(set(r['bc'] for r in rows)))
    print("schema: relationship_coverage present in", {r['file']: ('relationship_coverage' in r['topkeys']) for r in rows})

    # non-dispatch PUSH4 constants in the carrier (custom errors) must not be reported
    hx = open(CARRIER).read().strip()
    body = bytes.fromhex(hx)
    sel_bytes = {bytes.fromhex(s) for s in planted}
    sites = []
    for i, b in enumerate(body):
        if b == 0x63 and i + 4 < len(body):
            imm = body[i + 1:i + 5]
            if imm not in sel_bytes:
                sites.append((i, imm.hex()))
    errsigs = ['NotOwner()', 'Insufficient(uint256,uint256)']
    print('\n== non-dispatch PUSH4 constants (naive linear scan; includes data bytes) ==')
    for pc, imm in sites:
        tag = ''
        for es in errsigs:
            if imm == keccak4(es):
                tag = f'  <- custom error selector keccak({es})'
        print(f'    PUSH4 {imm} @ {pc}{tag}')
    reported = {f[0] for r in rows for f in r['fns']}
    leaked = sorted(imm for _, imm in sites if imm in reported)
    print('custom-error/non-selector constants reported by the probe:', leaked or '[] (none)')

    print('\nVERDICT:', 'planted K=9 recovered on every leg, zero missing / zero extra' if allok else 'MISMATCH')


if __name__ == '__main__':
    main()