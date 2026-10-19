#!/usr/bin/env python3
"""EX-09 (arc3-loop1-round4, c1 controls) — verification harness.

Reconciles, for every captured envelope:
  * the recovered selector set vs the planted K (Vyper ABI-derived, pre-probe);
  * the decoded bytecode sha256 vs the carrier file's own sha256;
  * the reported bytecode_offset semantics on the byte level;
  * the `inferred_state_mutability` payload vs the compiled ABI's stateMutability.
Never invokes the probe: reads only sealed envelopes + carriers.
"""
import json, pathlib, sys, collections

ROOT = pathlib.Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round4/claims/c1/EX-09')
PROBE = ROOT / "probe"
CARR = ROOT / 'carriers'

def sha256(p):
    import hashlib
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

def load(name):
    return json.load(open(PROBE / name))

def is_err(d):
    return 'code' in d and 'normalized_result' not in d

report = {'selectors': {}, 'errors': {}, 'offset_semantics': {}, 'mutability': {}}

# ---------- 1. Vyper runtime legs: K/K against planted ----------
planted = json.load(open(ROOT / 'planted' / 'planted-K.json'))
K = set(planted['selectors'])
runtime_legs = ['vy-runtime-hex-6.4.0.json', 'vy-runtime-raw-6.4.0.json',
                'vy-runtime-hex-6.7.0.json', 'vy-runtime-raw-6.7.0.json',
                'vy-runtime-0xhex-6.4.0.json']
print('== Vyper runtime legs (K=%d planted) ==' % len(K))
for leg in runtime_legs:
    d = load(leg)
    nr = d['normalized_result']
    got = {f['selector'][2:] for f in nr['functions']}
    dec = nr['bytecode']['sha256']
    ok = got == K
    print(f'  {leg:30s} n={len(got)} set_equal={ok} missing={sorted(K-got)} extra={sorted(got-K)}')
    print(f'      decoded sha256={dec[:16]}… file sha256={sha256(CARR/"Ex09Vault.runtime.bin")[:16]}… equal={dec==sha256(CARR/"Ex09Vault.runtime.bin")}')
    report['selectors'][leg] = {'n': len(got), 'set_equal': ok,
                                'missing': sorted(K - got), 'extra': sorted(got - K),
                                'evidence_id': d['evidence_id'], 'decoded_sha256': dec}

# ---------- 2. Vyper creation legs: parsed-empty ----------
print('\n== Vyper creation/initcode legs ==')
for leg in ['vy-creation-hex-6.4.0.json', 'vy-creation-raw-6.4.0.json',
            'vy-creation-hex-6.7.0.json', 'vy-creation-raw-6.7.0.json',
            'vy-creation-0xhex-6.4.0.json']:
    d = load(leg); nr = d['normalized_result']
    print(f'  {leg:30s} n={len(nr["functions"])} decoded_bytes={nr["bytecode"]["bytes"]} '
          f'sha={nr["bytecode"]["sha256"][:16]}… completeness={nr["discovery_completeness"]}')
    report['selectors'][leg] = {'n': len(nr['functions']), 'evidence_id': d['evidence_id'],
                                'decoded_sha256': nr['bytecode']['sha256'],
                                'discovery_completeness': nr['discovery_completeness']}

# ---------- 3. solc creation control ----------
print('\n== solc 0.8.37 creation control (prior-round carrier) ==')
for leg in ['solc-creation-hex-6.4.0.json', 'solc-creation-raw-6.4.0.json']:
    d = load(leg); nr = d['normalized_result']
    print(f'  {leg:30s} n={len(nr["functions"])} bytes={nr["bytecode"]["bytes"]} sha={nr["bytecode"]["sha256"][:16]}…')
    report['selectors'][leg] = {'n': len(nr['functions']), 'evidence_id': d['evidence_id']}

# ---------- 4. offset semantics on the byte level ----------
print('\n== reported bytecode_offset semantics (Vyper runtime) ==')
rt = (CARR / 'Ex09Vault.runtime.bin').read_bytes()
d = load('vy-runtime-hex-6.4.0.json')
for f in d['normalized_result']['functions']:
    sel = f['selector'][2:]; off = f['bytecode_offset']
    b = bytes.fromhex(sel)
    site = rt.find(b'\x63' + b)
    at = rt[off]
    print(f'  {sel} off={off:4d} byte_at_off=0x{at:02x} is_jumpdest={at==0x5b} '
          f'push4_pc={site} off-(pc+9)={off-(site+9)}')
    report['offset_semantics'][sel] = {'offset': off, 'byte_at_offset': at,
                                       'is_jumpdest': at == 0x5b,
                                       'push4_pc': site, 'delta_from_pc_plus_9': off - (site + 9)}

# ---------- 5. mutability divergence vs the compiled ABI ----------
print('\n== inferred_state_mutability vs compiled ABI ==')
abi = {e['name']: e.get('stateMutability') for e in json.load(open(ROOT / 'vyper' / 'Ex09Vault.abi.json'))
       if e.get('type') == 'function'}
for f in d['normalized_result']['functions']:
    sel = f['selector'][2:]
    sig = next(e['signature'] for e in planted['entries'] if e['selector'] == sel)
    name = sig.split('(')[0]
    print(f'  {sel} {sig:24s} abi={abi.get(name):11s} inferred={f["inferred_state_mutability"]:9s} '
          f'{"MATCH" if abi.get(name)==f["inferred_state_mutability"] else "DIVERGES"}')
    report['mutability'][sel] = {'signature': sig, 'abi': abi.get(name),
                                 'inferred': f['inferred_state_mutability']}

# ---------- 6. error envelope census ----------
print('\n== typed error envelopes ==')
for p in sorted(PROBE.glob('*.json')):
    d = json.load(open(p))
    if is_err(d):
        det = d.get('details') or {}
        iss = (det.get('issues') or [{}])[0]
        print(f'  {p.name:34s} code={d["code"]:16s} reason={iss.get("reason",""):14s} {iss.get("message","")[:60]}')
        report['errors'][p.name] = {'code': d['code'], 'category': d.get('category'),
                                    'reason': iss.get('reason'), 'message': iss.get('message')}

json.dump(report, open('/var/tmp/ex09-r4/verify-sealed.json', 'w'), indent=1)
print('\nwrote /var/tmp/ex09-r4/verify-sealed.json')
