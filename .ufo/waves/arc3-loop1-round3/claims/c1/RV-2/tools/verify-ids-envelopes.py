#!/usr/bin/env python3
"""RV-2 r3: mechanically compare each of my re-run envelopes against the seat record
for the same absolute carrier path, and emit the id/envelope table."""
import json, pathlib

RS = pathlib.Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/claims/c1')
R3 = pathlib.Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round3/claims/c1')
EV = pathlib.Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round3/claims/c1/RV-2/evidence')

PAIRS = [
    ('r3-rv2token-hex-6.4.0.json', RS/'RV-2/probe-runtime-hex-6.4.0.json'),
    ('r3-rv2many-hex-6.4.0.json', RS/'RV-2/attack/probe-many.json'),
    ('r3-kdxtoken-hex-6.7.0.json', RS/'EX-06/evidence/run-hex-6.7.0.json'),
    ('my-legA-hex-6.4.0.json', R3/'EX-07/legA-hex-6.4.0.json'),
    ('my-legA-raw-6.4.0.json', R3/'EX-07/legA-raw-6.4.0.json'),
    ('my-legA-hex-6.5.0.json', R3/'EX-07/legA-hex-6.5.0.json'),
    ('my-legA-hex-6.7.0.json', R3/'EX-07/legA-hex-6.7.0.json'),
    ('my-ex06legA.json', R3/'EX-06/evidence/probe-carrier-A-hex-6.4.0.json'),
    ('my-optB-hex-6.4.0.json', R3/'EX-07/optB-hex-6.4.0.json'),
    ('my-optB-raw-6.4.0.json', R3/'EX-07/optB-raw-6.4.0.json'),
    ('my-optB-hex-6.7.0.json', R3/'EX-07/optB-hex-6.7.0.json'),
    ('my-ex05B-hex-6.4.0.json', R3/'EX-05/probe/probe-runtime-hex-6.4.0.json'),
    ('my-ex10-opt200-hex-6.4.0.json', R3/'EX-10/probe/probe-B-opt200-hex-6.4.0.json'),
    ('my-ex10-opt200-hex-6.7.0.json', R3/'EX-10/probe/probe-B-opt200-hex-6.7.0.json'),
    ('my-ex10-nopt-hex-6.4.0.json', R3/'EX-10/probe/probe-B-nopt-hex-6.4.0.json'),
    ('my-ex10-nopt-hex-6.7.0.json', R3/'EX-10/probe/probe-B-nopt-hex-6.7.0.json'),
    ('my-ex04-opt200.json', R3/'EX-04/evidence/probe/probe-opt200-hex-6.4.0.json'),
    ('my-ex04-noopt.json', R3/'EX-04/evidence/probe/probe-noopt-hex-6.4.0.json'),
    ('my-pl1-OptVault.json', R3/'PL-1/evidence/OptVault-6.4.0-hex.json'),
    ('my-pl1-MutMix.json', R3/'PL-1/evidence/MutMix-6.4.0-hex.json'),
    ('my-pl1-MutMixOpt.json', R3/'PL-1/evidence/MutMixOpt-6.4.0-hex.json'),
    ('my-cr2-CrVault.json', R3/'CR-2/evidence/probes/crv-on200-6.4.0.json'),
    ('my-cr2-CrWide.json', R3/'CR-2/evidence/probes/crw-on200-6.4.0.json'),
    ('my-sc1-rv2opt200.json', R3/'SC-1/evidence/probe-rv2-opt200-hex-6.4.0.json'),
    ('my-sc1-vaultopt200.json', R3/'SC-1/evidence/probe-vault-opt200-hex-6.4.0.json'),
    ('my-ex06-ex03carrierA.json', R3/'EX-06/evidence/probe-EX03carrierA-hex-6.4.0.json'),
    ('my-legC-hex-6.4.0.json', R3/'EX-07/legC-hex-6.4.0.json'),
    ('my-legC-raw-6.4.0.json', R3/'EX-07/legC-raw-6.4.0.json'),
    ('my-legC-hex-6.7.0.json', R3/'EX-07/legC-hex-6.7.0.json'),
]

def load(p):
    j = json.loads(pathlib.Path(p).read_text())
    if isinstance(j, dict) and 'data' in j and 'evidence_id' not in j:
        j = j['data']
    return j

ok = 0
for mine, theirs in PAIRS:
    a, b = load(EV/mine), load(theirs)
    id_match = a.get('evidence_id') == b.get('evidence_id')
    env_match = a == b
    path = a.get('subject', {}).get('local_path')
    n = len(a.get('raw_result', {}).get('functions', []))
    print(f"{'PASS' if (id_match and env_match) else 'FAIL'}  {mine:32s} n={n:2d} id_match={id_match} envelope_identical={env_match}  path={path}")
    ok += 1 if (id_match and env_match) else 0
print(f"\n{ok}/{len(PAIRS)} legs: id re-derived AND full envelope identical to the seat record")