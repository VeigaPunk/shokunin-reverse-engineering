#!/usr/bin/env python3
"""EX-08 seat: reconcile VaultB 6.7.0 envelopes against EX-04's frozen planted set
and EX-04's 6.4.0 envelope payload (cross-seat, cross-pin agreement).
Usage: reconcile-vaultb.py <evidence_dir> <ex04_evidence_dir>   -> JSON to stdout"""
import json, hashlib, sys, os

EV = sys.argv[1] if len(sys.argv) > 1 else '/var/tmp/ex08-r3/evidence'
X = sys.argv[2] if len(sys.argv) > 2 else '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence'

planted = json.load(open(f'{X}/planted-B-opt200.json'))
pl = {f['selector'].replace('0x', '') for f in planted['functions']}

def load(p):
    e = json.load(open(p)); nr = e['normalized_result']
    return e, {f['selector'].replace('0x', ''): f for f in nr['functions']}

ref_e, ref = load(f'{X}/probe/probe-opt200-hex-6.4.0.json')
ref_off = {s: f['bytecode_offset'] for s, f in ref.items()}

rows = []
for tag, path, binpath, cmp_off in [
    ('probe-VaultB-opt200-hex-6.7.0', f'{EV}/probe-VaultB-opt200-hex-6.7.0.json', f'{EV}/carrierB.runtime-opt200.bin', True),
    ('probe-VaultB-opt200-raw-6.7.0', f'{EV}/probe-VaultB-opt200-raw-6.7.0.json', f'{EV}/carrierB.runtime-opt200.bin', True),
    ('probe-VaultB-noopt-hex-6.7.0', f'{EV}/probe-VaultB-noopt-hex-6.7.0.json', f'{EV}/carrierB.runtime-noopt.bin', False),
    ('probe-VaultB-rerun-a-hex-6.7.0', f'{EV}/probe-VaultB-rerun-a-hex-6.7.0.json', f'{EV}/carrierB.runtime-opt200.bin', True),
]:
    e, fns = load(path)
    bsha = hashlib.sha256(open(binpath, 'rb').read()).hexdigest()
    offs = {s: f['bytecode_offset'] for s, f in fns.items()}
    rows.append(dict(
        tag=tag, evidence_id=e['evidence_id'], provider=e['provider']['version'],
        encoding=e['parameters']['encoding'], n=len(fns), planted_K=len(pl),
        missing=sorted(pl - set(fns)), extra=sorted(set(fns) - pl),
        bytecode_sha256=e['normalized_result']['bytecode']['sha256'],
        bytecode_equals_runtime_file=(e['normalized_result']['bytecode']['sha256'] == bsha),
        offsets_match_ex04_640=(offs == ref_off) if cmp_off else None,
        offsets=offs))

trap = load(f'{EV}/probe-VaultB-trap-raw-on-hexfile-6.7.0.json')[0]
hexsha = hashlib.sha256(open(f'{EV}/carrierB.runtime-opt200.hex', 'rb').read()).hexdigest()
trap_row = dict(tag='probe-VaultB-trap-raw-on-hexfile-6.7.0', evidence_id=trap['evidence_id'],
                n=len(trap['normalized_result']['functions']),
                bytecode_equals_hex_file=(trap['normalized_result']['bytecode']['sha256'] == hexsha),
                kind=trap['normalized_result']['bytecode']['kind'],
                discovery_completeness=trap['normalized_result']['discovery_completeness'])

print(json.dumps({'vaultb_6_7_0': rows, 'trap': trap_row}, indent=2))