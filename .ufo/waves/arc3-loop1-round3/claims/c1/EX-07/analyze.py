#!/usr/bin/env python3
"""EX-07 (arc3-loop1-round3, c1): compare probe legs across pins and encodings.

Reads the legA-*.json (hand-assembled carrier A, r1 CR-1 control) and optB-*.json
(Rv2TokenOpt: Rv2Token.sol compiled here with solc 0.8.37 --optimize runs=200)
envelopes, and prints: per-leg payload, planted-K comparison (optB), cross-pin /
cross-encoding equality, and ev_ id grouping.

Usage: python3 analyze.py   (run from the seat dir)
"""
import json, glob, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load(path):
    d = json.load(open(path))
    return d.get('data', d)


def leginfo(path):
    d = load(path)
    nr = d['normalized_result']
    fns = [(x['selector'].replace('0x', ''), x['bytecode_offset'], x['dispatch'],
            x['inferred_state_mutability'], x['inferred_arguments']) for x in nr['functions']]
    return dict(file=os.path.basename(path), ev=d['evidence_id'],
                enc=d['parameters']['encoding'],
                path=d['parameters'].get('path'),
                subj=d['subject']['digest']['sha256'],
                art_bytes=nr['artifact']['bytes'], bc_bytes=nr['bytecode']['bytes'],
                bc=nr['bytecode']['sha256'], ok=len(fns),
                fns=sorted(fns), topkeys=sorted(d))


def main():
    print('== LEG A: hand-assembled control carrier-A (3 dispatched selectors + decoys deadbeef/ffffffff) ==')
    print('   expected selectors {095ea7b3, 70a08231, a9059cbb} — derived from the carrier hex bytes (static property)')
    rowsA = [leginfo(p) for p in sorted(glob.glob(os.path.join(HERE, 'legA-*.json')))]
    for r in rowsA:
        print(f"{r['file']:30s} enc={r['enc']:3s} ev={r['ev']}")
        print(f"    path={r['path']} subj={r['subj'][:12]}… art={r['art_bytes']}B bc={r['bc'][:12]}… {r['bc_bytes']}B n={r['ok']}")
        any_reveal = 'relationship_coverage' in r['topkeys']
        print(f"    fns={[f[0] for f in r['fns']]} offsets={[f[1] for f in r['fns']]} "
              f"mut={sorted(set(f[3] for f in r['fns']))} relationship_coverage={'yes' if any_reveal else 'no'}")

    print()
    print('== LEG B: Rv2TokenOpt (Rv2Token.sol + solc 0.8.37 optimizer enabled, runs=200) ==')
    planted = json.load(open(os.path.join(HERE, 'Rv2TokenOpt.planted-K.json')))
    K = sorted(s.replace('0x', '') for s in planted['selectors'])
    print(f"   planted K={planted['K']} selectors={K} (recorded {planted['recorded_utc']}, "
          f"oracle_match={planted['oracle_set_match']})")
    rowsB = [leginfo(p) for p in sorted(glob.glob(os.path.join(HERE, 'optB-*.json')))]
    verdict_ok = True
    for r in rowsB:
        got = sorted(f[0] for f in r['fns'])
        missing = sorted(set(K) - set(got)); extra = sorted(set(got) - set(K))
        if missing or extra:
            verdict_ok = False
        print(f"{r['file']:30s} enc={r['enc']:3s} ev={r['ev']}")
        print(f"    path={r['path']} subj={r['subj'][:12]}… art={r['art_bytes']}B bc={r['bc'][:12]}… {r['bc_bytes']}B n={r['ok']}")
        print(f"    fns={got} offsets={[f[1] for f in r['fns']]} missing={missing} extra={extra}")

    print()
    print('== cross-check ==')
    idsA = {r['file']: r['ev'] for r in rowsA}
    idsB = {r['file']: r['ev'] for r in rowsB}
    print('leg A distinct ev ids:', len(set(idsA.values())), 'of', len(idsA))
    print('leg B distinct ev ids:', len(set(idsB.values())), 'of', len(idsB))
    print('leg A rerun stability 6.4.0/6.7.0:',
          idsA['legA-hex-6.4.0.json'] == idsA['legA-hex-6.4.0-rerun.json'],
          idsA['legA-hex-6.7.0.json'] == idsA['legA-hex-6.7.0-rerun.json'])
    print('leg B rerun stability 6.7.0:', idsB['optB-hex-6.7.0.json'] == idsB['optB-hex-6.7.0-rerun.json'])
    # encodings equal within pin, and bytecode digest across all legs of a carrier
    for tag, rows, pins in (('A', rowsA, ('6.4.0', '6.5.0', '6.7.0')), ('B', rowsB, ('6.4.0', '6.5.0', '6.7.0'))):
        for pin in pins:
            h = [r for r in rows if r['file'] == f'leg{tag}-hex-{pin}.json']
            if not h:
                h = [r for r in rows if r['file'] == f'optB-hex-{pin}.json']
            rr = [r for r in rows if r['file'] == f'leg{tag}-raw-{pin}.json']
            if not rr:
                rr = [r for r in rows if r['file'] == f'optB-raw-{pin}.json']
            if h and rr:
                print(f'leg {tag} pin {pin}: hex==raw payload {h[0]["fns"] == rr[0]["fns"]}; '
                      f'bytecode sha equal {h[0]["bc"] == rr[0]["bc"]}')
        bcs = set(r['bc'] for r in rows)
        print(f'leg {tag}: distinct decoded bytecode sha256 across all legs = {len(bcs)}')
        payloads = set(json.dumps(r['fns']) for r in rows)
        print(f'leg {tag}: distinct function payloads across all legs = {len(payloads)}')
    print()
    print('VERDICT leg B:', 'K/K on every leg, zero missing / zero extra' if verdict_ok else 'MISMATCH')
    print('VERDICT leg A:', '3/3 expected selectors, decoys absent, on every leg',
          all(sorted(f[0] for f in r['fns']) == ['095ea7b3', '70a08231', 'a9059cbb'] for r in rowsA))


if __name__ == '__main__':
    main()