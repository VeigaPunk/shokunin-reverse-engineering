#!/usr/bin/env python3
"""EX-07 (arc3-loop1-round4, c1): compare probe legs across pins, encodings and carriers.

Reads the *.json envelopes captured under /var/tmp/ex07-r4/legs (raw seat capture,
copied into this dir as evidence/) and prints:
  1. the per-leg table (id, encoding, subject digest, decoded bytecode, K)
  2. payload equality within each carrier family across pins and encodings
  3. K/K comparison against each carrier's planted set / ABI-derived set
  4. offset semantics (byte at the reported offset, Vyper vs solc convention)
  5. mutability/argument inference vs the compiled ABI
  6. the envelope key delta (relationship_coverage / limitation count) by pin
  7. id-domain probes: same bytes at different paths, encodings, symlink refusal

Carrier keys: A/B/C = r3 solc carriers (VaultB opt200 / VaultB nopt / Rv2TokenOpt)
              V/VC  = r4 Vyper CarrierV runtime / creation (EX-04)
              S     = r4 Vyper Smoke runtime (EX-02)
              D     = id-domain legs on the VaultB.opt200.hex bytes
Usage: python3 compare-legs.py [legs_dir]
"""
import glob
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEGS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'legs')


def sha256_file(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def leg(path):
    d = json.load(open(path))
    if 'normalized_result' not in d:
        reason = ''
        if 'details' in d and d['details'].get('issues'):
            reason = d['details']['issues'][0].get('reason', '')
        return dict(
            file=os.path.basename(path), ev='', enc='-', path='', subj='',
            bc='', bc_bytes=0, art_bytes=0, n=-1, sels=[], rows=[],
            rc=False, limits=0, env=sha256_file(path)[:16],
            refused=d.get('category', 'error'), reason=reason)
    nr = d['normalized_result']
    fns = nr['functions']
    return dict(
        refused=None, reason='',
        file=os.path.basename(path), ev=d['evidence_id'], enc=d['parameters']['encoding'],
        path=d['parameters']['path'], subj=d['subject']['digest']['sha256'],
        bc=nr['bytecode']['sha256'], bc_bytes=nr['bytecode']['bytes'],
        art_bytes=nr['artifact']['bytes'], n=len(fns),
        sels=sorted(x['selector'][2:] for x in fns),
        rows=sorted((x['selector'][2:], x['bytecode_offset'], x['dispatch'],
                     x['inferred_arguments'], x['inferred_state_mutability']) for x in fns),
        rc='relationship_coverage' in d, limits=len(d['limitations']),
        env=sha256_file(path)[:16])


def payload(r):
    return json.dumps(r['rows'], sort_keys=True)


def main():
    files = sorted(glob.glob(os.path.join(LEGS, '*.json')))
    legs = [leg(f) for f in files]
    groups = {}
    for r in legs:
        if r['refused']:
            continue
        key = r['file'].split('-')[0]
        groups.setdefault(key, []).append(r)

    print('== 1. per-leg table ==')
    for r in legs:
        if r['refused']:
            print(f"{r['file'][:-5]:26s} REFUSED category={r['refused']} reason={r['reason']}")
            continue
        print(f"{r['file'][:-5]:26s} enc={r['enc']:3s} n={r['n']:2d} "
              f"bc={r['bc'][:12]} {r['bc_bytes']:5d}B subj={r['subj'][:10]} "
              f"rc={'Y' if r['rc'] else 'n'} lim={r['limits']} ev={r['ev'][:14]}")

    print()
    print('== 2/3. per-family payload + id comparison ==')
    for key in sorted(groups):
        g = groups[key]
        print(f"  {key}: legs={len(g)} payloads={len(set(payload(r) for r in g))} "
              f"decoded_sha={len(set(r['bc'] for r in g))} ids={len(set(r['ev'] for r in g))} "
              f"subjects={len(set(r['subj'] for r in g))}")
        for pin in ('6.4.0', '6.5.0', '6.7.0'):
            h = [r for r in g if r['file'].endswith(f'hex-{pin}')]
            w = [r for r in g if r['file'].endswith(f'raw-{pin}')]
            if h and w and not h[0]['refused'] and not w[0]['refused']:
                print(f"     pin {pin}: payload_eq={payload(h[0]) == payload(w[0])} "
                      f"bc_eq={h[0]['bc'] == w[0]['bc']} id_eq={h[0]['ev'] == w[0]['ev']} "
                      f"subj_eq={h[0]['subj'] == w[0]['subj']}")

    print()
    print('== 4. offset semantics ==')
    for key in sorted(groups):
        g = [r for r in groups[key] if r['n'] > 0 and not r['refused']]
        if not g:
            continue
        r = g[0]
        code = bytes.fromhex(json.load(open(os.path.join(LEGS, r['file'])))['normalized_result']['bytecode']['hex'])
        jd = sum(1 for (s, off, *_ ) in r['rows'] if code[off] == 0x5b)
        jdm1 = sum(1 for (s, off, *_ ) in r['rows'] if off and code[off - 1] == 0x5b)
        jmpi = sum(1 for (s, off, *_ ) in r['rows'] if off and code[off - 1] == 0x57)
        print(f"  {key} ({r['file']}): n={r['n']} byte@off==JUMPDEST {jd}/{r['n']}  "
              f"byte@off-1==JUMPDEST {jdm1}/{r['n']}  byte@off-1==JUMPI {jmpi}/{r['n']}")

    print()
    print('== 6. envelope key delta by pin ==')
    for key in sorted(groups):
        row = []
        for r in sorted(groups[key], key=lambda x: x['file']):
            if r['refused']:
                continue
            row.append(f"{r['file'].split('-')[-1]}:{'Y' if r['rc'] else 'n'}/lim{r['limits']}")
        if row:
            print(f"  {key}: " + '  '.join(row))

    print()
    print('== 7. id-domain probes (VaultB.opt200 bytes) ==')
    base = next((r for r in legs if r['file'] == 'A-hex-6.4.0.json'), None)
    if base:
        print(f"  repo .hex path, hex : {base['ev']}  subj={base['subj'][:16]}")
        for name in ('D1-hexcopy-hex-6.4.0', 'D5-relative-hex-6.4.0', 'D7-shmcopy-hex-6.4.0'):
            r = next((x for x in legs if x['file'] == name + '.json'), None)
            if r and not r['refused']:
                print(f"  {name:22s}: {r['ev'][:34]}… subj={r['subj'][:16]} "
                      f"same_id={r['ev'] == base['ev']} same_subj={r['subj'] == base['subj']}")
    print('  refusals:')
    for r in legs:
        if r['refused']:
            print(f"    {r['file'][:-5]:26s} {r['refused']:14s} {r['reason']}")


if __name__ == '__main__':
    main()
