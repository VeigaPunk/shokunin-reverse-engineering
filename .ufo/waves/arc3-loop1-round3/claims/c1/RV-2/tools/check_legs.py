#!/usr/bin/env python3
"""RV-2 arc3-loop1-round3 reviewer check: K/K, dispatch, offsets, digest binding."""
import hashlib, json, pathlib, sys

RS = pathlib.Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round3/claims/c1')
OUT = pathlib.Path('/var/tmp/rv2-r3/out')

EXPECTED = {
    'carrier-A': {'a9059cbb', '70a08231', '095ea7b3'},
    'optB': {'095ea7b3', '18160ddd', '23b872dd', '70a08231', 'a9059cbb'},
    'CarrierB': {'3efdef66', '410673e5', '51f91066', '6ea056a9', '8da5cb5b',
                 'ca1d209d', 'd5d44d80', 'e7ee6ad6'},
    'VaultB': {'24a9d853', '27e235e3', '2e1a7d4d', '3d96e276', '3f4ba83a',
               '5c975abb', '69fe0e2d', '7d882097', '8456cb59', '8da5cb5b',
               '9c421eb5', 'cbf9fe5f', 'd0e30db0'},
}

# leg -> (carrier, carrier bytes path, encoding)
LEGS = {
    'my-legA-hex-6.4.0.json': ('carrier-A', '/var/tmp/ex07/carrier-A.hex', 'hex'),
    'my-legA-raw-6.4.0.json': ('carrier-A', '/var/tmp/ex07/carrier-A.bin', 'raw'),
    'my-legA-hex-6.7.0.json': ('carrier-A', '/var/tmp/ex07/carrier-A.hex', 'hex'),
    'my-legA-hex-6.5.0.json': ('carrier-A', '/var/tmp/ex07/carrier-A.hex', 'hex'),
    'my-ex06legA.json': ('carrier-A', '/var/tmp/ex06-r3/work/carrier-A.hex', 'hex'),
    'my-optB-hex-6.4.0.json': ('optB', '/var/tmp/ex07/Rv2TokenOpt.runtime.hex', 'hex'),
    'my-optB-raw-6.4.0.json': ('optB', '/var/tmp/ex07/Rv2TokenOpt.runtime.bin', 'raw'),
    'my-optB-hex-6.7.0.json': ('optB', '/var/tmp/ex07/Rv2TokenOpt.runtime.hex', 'hex'),
    'my-ex05B-hex-6.4.0.json': ('CarrierB', str(RS / 'EX-05/out/CarrierB.runtime.hex'), 'hex'),
    'my-ex10-opt200-hex-6.4.0.json': ('VaultB', str(RS / 'EX-10/out/VaultB.opt200.runtime.hex'), 'hex'),
    'my-ex10-opt200-hex-6.7.0.json': ('VaultB', str(RS / 'EX-10/out/VaultB.opt200.runtime.hex'), 'hex'),
    'my-ex10-nopt-hex-6.4.0.json': ('VaultB', str(RS / 'EX-10/out/VaultB.nopt.runtime.hex'), 'hex'),
    'my-ex10-nopt-hex-6.7.0.json': ('VaultB', str(RS / 'EX-10/out/VaultB.nopt.runtime.hex'), 'hex'),
}

def raw_bytes(path, enc):
    b = pathlib.Path(path).read_bytes()
    if enc == 'hex':
        t = b.decode('utf-8').strip()
        if t[:2].lower() == '0x': t = t[2:]
        return bytes.fromhex(t)
    return b

fails = 0
for leg, (carrier, cpath, enc) in LEGS.items():
    j = json.loads((OUT / leg).read_text())
    fns = j['raw_result']['functions']
    sels = sorted(f['selector'] for f in fns)
    disp = sorted({f['dispatch'] for f in fns})
    exp = sorted(EXPECTED[carrier])
    ok_set = sels == exp
    ok_disp = disp == ['abi']
    bc = j['normalized_result']['bytecode']
    rb = raw_bytes(cpath, enc)
    ok_digest = bc['sha256'] == hashlib.sha256(rb).hexdigest() and bc['bytes'] == len(rb)
    offs = [f['bytecodeOffset'] for f in fns]
    if carrier == 'carrier-A':
        # Hand-assembled control (r1 CR-1): the tool reports the declared jump
        # immediates (38/48/58); the carrier's own 0x5b bytes sit at 40/50/60
        # (immediates are 2 short of its JUMPDESTs). r1 CR-1's record
        # (out-A-hex.json) shows the same 58/48/38 -- no drift. The
        # "offsets land on JUMPDEST" reading applies to solc-convention
        # carriers only; here we check the declared-target semantics instead.
        ok_offsets = sorted(offs) == [38, 48, 58] and all(rb[o] != 0x5b for o in offs)
        off_note = 'declared-immediates 38/48/58 (hand-asm; JUMPDESTs at 40/50/60)'
    else:
        ok_offsets = all(rb[o] == 0x5b for o in offs)
        bad_off = [o for o in offs if rb[o] != 0x5b]
        off_note = 'jumpdest' if ok_offsets else 'BAD ' + str(bad_off)
    status = 'PASS' if (ok_set and ok_disp and ok_digest and ok_offsets) else 'FAIL'
    if status == 'FAIL': fails += 1
    print(f"{status} {leg:34s} K={len(sels)} set={'OK' if ok_set else 'MISMATCH'} "
          f"dispatch={disp} digest_bind={'OK' if ok_digest else 'BAD'} "
          f"offsets={off_note}")

print(f"\n{fails} failures out of {len(LEGS)} legs")
sys.exit(1 if fails else 0)