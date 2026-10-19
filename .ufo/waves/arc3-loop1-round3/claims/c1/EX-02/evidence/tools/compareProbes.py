#!/usr/bin/env python3
# arc3-loop1-round3 c1/EX-02 — mechanical comparison of every probe leg's
# function set against the planted set, plus the non-dispatch trap check.
# Run: python3 compareProbes.py (paths below are the landed artifact paths).
import json, hashlib

REPO = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round3/claims/c1/EX-02'
EV = REPO + '/evidence'

planted = {}
for l in open(REPO + '/planted-A.txt'):
    l = l.strip()
    if l.startswith('0x'):
        sel, rest = l.split(' ', 1)
        planted[sel[2:]] = rest

runtime = bytes.fromhex(open(EV + '/carrierA.runtime.hex').read().strip())
abi = json.load(open(EV + '/carrierA.abi.json'))

def abi_sig_mut(fn_sel):
    # map selector -> (sig, abi mutability) via canonical type join
    for e in abi:
        if e['type'] != 'function':
            continue
        sig = e['name'] + '(' + ','.join(i['type'] for i in e['inputs']) + ')'
        from shutil import which
        # selector computed by the caller; here just return by sig lookup table
    return None

# build sig -> mutability from abi for the display column
sig_mut = {}
for e in abi:
    if e['type'] == 'function':
        sig_mut[e['name'] + '(' + ','.join(i['type'] for i in e['inputs']) + ')'] = e['stateMutability']

TRAPS = {'30cd7471', '4e487b71', '6508d58f', '1d0c41', '461bcd'}
LEGS = [
    ('hex 6.4.0', EV + '/probe-carrierA-hex-6.4.0.json'),
    ('bin raw 6.4.0', EV + '/probe-carrierA-bin-raw-6.4.0.json'),
    ('hex 6.7.0', EV + '/probe-carrierA-hex-6.7.0.json'),
    ('raw-on-hexfile 6.4.0 [input-shape trap]', EV + '/probe-carrierA-rawonhexfile-6.4.0.json'),
]

out = []
out.append('probe-vs-planted-A — arc3-loop1-round3 c1/EX-02 (carrierA, solc 0.8.37, optimizer runs=200)')
out.append('planted source: planted-A.txt (%d selectors, recorded before the first probe envelope)' % len(planted))
out.append('decoded runtime sha256: ' + hashlib.sha256(runtime).hexdigest() + ' (%d B)' % len(runtime))
out.append('')

for label, path in LEGS:
    d = json.load(open(path))
    nr = d['normalized_result']
    fns = nr.get('functions', [])
    by_sel = {x['selector'][2:].lower(): x for x in fns}
    missing = sorted(set(planted) - set(by_sel))
    extra = sorted(set(by_sel) - set(planted))
    traps_hit = sorted(set(by_sel) & TRAPS)
    out.append('=' * 78)
    out.append('LEG: ' + label)
    out.append('  evidence_id: ' + d['evidence_id'])
    out.append('  subject.file.sha256: ' + d['subject']['digest']['sha256'])
    out.append('  decoded bytecode.sha256: %s (%d B), kind=%s' % (nr['bytecode']['sha256'], nr['bytecode']['bytes'], nr['bytecode']['kind']))
    out.append('  functions=%d  missing=%s  extra=%s' % (len(fns), missing, extra))
    out.append('  non-dispatch trap constants reported as functions: %s' % (traps_hit if traps_hit else 'none'))
    out.append('  K/K verdict: %s' % ('K/K (set-equal, zero extras)' if not missing and not extra and len(fns) == len(planted) else 'MISMATCH'))
    if fns:
        out.append('  per-function (planted order by selector):')
        for s in sorted(planted):
            x = by_sel.get(s)
            if not x:
                out.append('    %s ABSENT  (%s)' % (s, planted[s]))
                continue
            off = x['bytecode_offset']
            byte = '0x%02x' % runtime[off] if 0 <= off < len(runtime) else 'n/a'
            sig = planted[s].split(' [')[0]
            am = sig_mut.get(sig, '?')
            pm = x['inferred_state_mutability']
            note = '' if am == pm else '  <-- mutability differs (ABI says %s)' % am
            out.append('    %s off=%-4d byte@off=%s dispatch=%s args=%-9s probe_mut=%-10s abi_mut=%s%s' % (s, off, byte, x['dispatch'], "'" + x['inferred_arguments'] + "'", pm, am, note))
    out.append('')

out.append('cross-leg decoded-bytecode digest agreement:')
digests = {}
for label, path in LEGS:
    d = json.load(open(path))
    nr = d['normalized_result']
    digests.setdefault(nr['bytecode']['sha256'], []).append(label + ' (%d B)' % nr['bytecode']['bytes'])
for dg, legs in digests.items():
    out.append('  %s  <- %s' % (dg, '; '.join(legs)))

text = '\n'.join(out) + '\n'
open(EV + '/probe-vs-planted-A.txt', 'w').write(text)
print(text)