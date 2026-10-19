#!/usr/bin/env python3
"""RV-2 arc3-loop1-round3 reviewer check #2: the additional wave carriers."""
import hashlib, json, pathlib, re, sys

OUT = pathlib.Path('/var/tmp/rv2-r3/out')

def s(*xs): return set(xs)

EXPECTED = {
    'ex04-opt200': s('07bf89ab','0bf6cc08','0db02622','2f54bf6e','42cde4e8','59bf77df','797af627','960bfe04','a8c162fb','d0e30db0','d9caa3d2'),
    'ex04-noopt': s('07bf89ab','0bf6cc08','0db02622','2f54bf6e','42cde4e8','59bf77df','797af627','960bfe04','a8c162fb','d0e30db0','d9caa3d2'),
    'pl1-OptVault': s('16c38b3c','2e1a7d4d','5c975abb','75807250','d0e30db0'),
    'pl1-MutMix': s('0f991d72','18178358','1b9265b8','56076947','6206a233','d6d21dfd'),
    'pl1-MutMixOpt': s('0f991d72','18178358','1b9265b8','56076947','6206a233','d6d21dfd'),
    'cr2-CrVault': s('16f0115b','18178358','2e1a7d4d','42cde4e8','8da5cb5b','960bfe04','ed88c68e'),
    'cr2-CrWide': s('09a6c1bb','17018a84','2ae1431c','2cf962cf','3c9d377d','50cd4df2','604f7523','68dd531a','741a0c1e','86b714e2','8b2138bc','920f5c73','aa66aa63','aec6165d','bc35450a','c0cc8c65','c27fc305','c3642756','ce4b01e5','d7531d91','d9e5b125','e7025593'),
    'sc1-rv2opt200': s('095ea7b3','18160ddd','23b872dd','70a08231','a9059cbb'),
    'sc1-vaultopt200': s('13af4035','27e235e3','2e1a7d4d','5ce2a6a0','5fd2b883','6392a51f','7d882097','8da5cb5b','b16a867c','d0e30db0'),
    'ex06-ex03carrierA': s('01681a62','067b23c3','2e1a7d4d','3f0d861a','5ce23950','75807250','8da5cb5b','c85e07b9','d0e30db0'),
}

LEGS = {
    'my-ex04-opt200.json': ('ex04-opt200', '/dev/shm/ex04-r3/out/carrierB.runtime-opt200.hex', 'hex'),
    'my-ex04-noopt.json': ('ex04-noopt', '/dev/shm/ex04-r3/out/carrierB.runtime-noopt.hex', 'hex'),
    'my-pl1-OptVault.json': ('pl1-OptVault', '/var/tmp/pl1-r3/out/OptVault.runtime.hex', 'hex'),
    'my-pl1-MutMix.json': ('pl1-MutMix', '/var/tmp/pl1-r3/out/MutMix.runtime.hex', 'hex'),
    'my-pl1-MutMixOpt.json': ('pl1-MutMixOpt', '/var/tmp/pl1-r3/out/MutMixOpt.runtime.hex', 'hex'),
    'my-cr2-CrVault.json': ('cr2-CrVault', '/var/tmp/cr2r3/work/crv-on200.CrVault.runtime.hex', 'hex'),
    'my-cr2-CrWide.json': ('cr2-CrWide', '/var/tmp/cr2r3/work/crw-on200.CrWide.runtime.hex', 'hex'),
    'my-sc1-rv2opt200.json': ('sc1-rv2opt200', '/var/tmp/sc1-r3/out/Rv2Token.opt200.runtime.hex', 'hex'),
    'my-sc1-vaultopt200.json': ('sc1-vaultopt200', '/var/tmp/sc1-r3/out/VaultCourt.opt200.runtime.hex', 'hex'),
    'my-ex06-ex03carrierA.json': ('ex06-ex03carrierA', '/var/tmp/ex06-r3/work/ex03/carrierA.runtime.hex', 'hex'),
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
    rb = raw_bytes(cpath, enc)
    offs = [f['bytecodeOffset'] for f in fns]
    ok_offsets = all(rb[o] == 0x5b for o in offs)
    bad = [o for o in offs if rb[o] != 0x5b]
    bc = j['normalized_result']['bytecode']
    ok_digest = bc['sha256'] == hashlib.sha256(rb).hexdigest() and bc['bytes'] == len(rb)
    # dispatch shape sniff
    n_eq = len(re.findall(rb'\x14\x60(.)\x57', rb))
    n_gt = len(re.findall(rb'\x11\x61(..)\x57', rb))
    prologue = '5f3560e01c' if b'\x5f\x35\x60\xe0\x1c' in rb else ('60003560e01c' if b'\x60\x00\x35\x60\xe0\x1c' in rb else '?')
    ok = sels == exp and disp == ['abi'] and ok_offsets and ok_digest
    fails += 0 if ok else 1
    print(f"{'PASS' if ok else 'FAIL'} {leg:28s} K={len(sels)}/{len(exp)} "
          f"set={'OK' if sels==exp else 'MISMATCH'} dispatch={disp} "
          f"offsets={'jumpdest' if ok_offsets else 'bad'+str(bad)} digest={'OK' if ok_digest else 'BAD'} "
          f"| prologue={prologue} EQ-sites={n_eq} GT-sites={n_gt}")

print(f"\n{fails} failures out of {len(LEGS)} legs")
sys.exit(1 if fails else 0)