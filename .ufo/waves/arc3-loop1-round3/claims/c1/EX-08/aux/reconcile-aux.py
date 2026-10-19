#!/usr/bin/env python3
"""EX-08 seat: reconcile the seat-side auxiliary carrier (HarborBound + twins)
envelopes against the frozen planted-K.json (pre-probe). -> JSON to stdout"""
import json, hashlib, os, sys

EV = sys.argv[1] if len(sys.argv) > 1 else '/var/tmp/ex08-r3/evidence'
planted = json.load(open(f'{EV}/planted-K.json'))
targets = {
    'CarrierB': ('HarborBound', f'{EV}/CarrierB.runtime.bin'),
    'CarrierBNoOpt': ('HarborBoundNoOpt', f'{EV}/CarrierBNoOpt.runtime.bin'),
    'HarborLib': ('HarborLib', f'{EV}/HarborLib.runtime.bin'),
}
files = sorted(f for f in os.listdir(EV) if f.startswith('probe-CarrierB') or f.startswith('probe-HarborLib'))
rows = []
for f in files:
    if not f.endswith('.json'):
        continue
    env = json.load(open(f'{EV}/{f}'))
    which = 'HarborLib' if 'HarborLib' in f else ('CarrierBNoOpt' if 'NoOpt' in f else 'CarrierB')
    key, binp = targets[which]
    b = open(binp, 'rb').read()
    bsha = hashlib.sha256(b).hexdigest()
    pl = {x['selector'][2:] for x in planted[key]['functions']}
    fns = env['normalized_result']['functions']
    got = {x['selector'][2:] for x in fns}
    jd = [(x['selector'], x['bytecode_offset'], b[x['bytecode_offset']]) for x in fns]
    rows.append(dict(
        file=f, evidence_id=env['evidence_id'], provider=env['provider']['version'],
        n=len(fns), planted_K=len(pl), missing=sorted(pl - got), extra=sorted(got - pl),
        subject_sha256=env['subject']['digest']['sha256'],
        subject_is_runtime_file=(env['subject']['digest']['sha256'] == bsha),
        bytecode_sha256=env['normalized_result']['bytecode']['sha256'],
        bytecode_is_runtime_file=(env['normalized_result']['bytecode']['sha256'] == bsha),
        all_offsets_jumpdest=all(x[2] == 0x5b for x in jd),
        offsets={x['selector']: x['bytecode_offset'] for x in fns},
        mutability={x['selector']: x['inferred_state_mutability'] for x in fns}))
print(json.dumps(rows, indent=2))