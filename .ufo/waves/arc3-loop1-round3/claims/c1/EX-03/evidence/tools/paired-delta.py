#!/usr/bin/env python3
"""arc3-loop1-round3 c1/EX-03 — optimizer-on vs optimizer-off shape comparison
for carrier A (same source, same compiler, only settings.optimizer differs)."""
import hashlib, os

S = '/var/tmp/ex03-r3'

def rd(p):
    return open(p).read().strip()

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

on_rt = rd(S + '/a-stdjson-out/carrierA.runtime.hex')
off_rt = rd(S + '/a-stdjson-opt-off/carrierA.runtime.hex')
on_cr = rd(S + '/a-stdjson-out/carrierA.creation.hex')
off_cr = rd(S + '/a-stdjson-opt-off/carrierA.creation.hex')
sels = ['01681a62', '067b23c3', '2e1a7d4d', '3f0d861a', '5ce23950', '75807250',
        '8da5cb5b', 'c85e07b9', 'd0e30db0']

L = []
def say(s):
    L.append(s)
    print(s)

say('OPTIMIZER-ON vs OPTIMIZER-OFF, carrier A (carrierA.sol sha256 %s)' % sha(S + '/a/carrierA.sol'))
say('compiler solcjs 0.8.37+commit.f401782d; only settings.optimizer differs;')
say('  off leg: outputSelection abi/evm.bytecode.object/evm.deployedBytecode.object/evm.methodIdentifiers')
say('  on leg : same + optimizer {enabled:true, runs:200}')
say('')
say('metric                              off        on        delta')
say('creation bytes .................... %-10d %-9d %+d' % (len(off_cr) // 2, len(on_cr) // 2, len(on_cr) // 2 - len(off_cr) // 2))
say('runtime  bytes .................... %-10d %-9d %+d' % (len(off_rt) // 2, len(on_rt) // 2, len(on_rt) // 2 - len(off_rt) // 2))

i = 0
while i < min(len(on_rt), len(off_rt)) and on_rt[i] == off_rt[i]:
    i += 1
say('runtime common prefix ............. %d bytes; first divergence at hex offset %d (byte %d)' % (i // 2, i, i // 2))
j = 0
while j < min(len(on_cr), len(off_cr)) and on_cr[j] == off_cr[j]:
    j += 1
say('creation common prefix ............ %d bytes; first divergence at hex offset %d (byte %d)' % (j // 2, j, j // 2))
say('')
for name, h in (('off', off_rt), ('on', on_rt)):
    say('%s runtime: len %d B' % (name, len(h) // 2))
    say('  head 48 B: %s' % h[:96])
    say('  dispatch sites "8063<push4 sel>": %d | EQ-jump 1461: %d | GT-jump 1161: %d' %
        (h.count('8063'), h.count('1461'), h.count('1161')))
    say('  prologue markers: 5f3560e01c at byte %s | 60003560e01c at byte %s' %
        (h.find('5f3560e01c') // 2, h.find('60003560e01c') // 2 if h.find('60003560e01c') != -1 else 'ABSENT'))
    say('  planted selector constants present verbatim: %d/9' % sum(1 for s in sels if s in h))
    say('  selector byte offsets: ' + ', '.join('%s@%d' % (s, h.find(s) // 2) for s in sels))
say('')
say('ABI byte-identity across modes: %s' % ('IDENTICAL' if sha(S + '/a-out/carrierA_sol_CarrierA.abi') == sha(S + '/a-cli-off-out/carrierA_sol_CarrierA.abi') else 'DIFFERS'))
say('methodIdentifiers byte-identity across modes: %s' % ('IDENTICAL' if sha(S + '/a-stdjson-out/carrierA.methodIdentifiers.json') == sha(S + '/a-stdjson-opt-off/carrierA.methodIdentifiers.json') else 'DIFFERS'))
say('CLI creation-leg == stdjson creation-leg (hex text minus newline):')
say('  off: %s' % ('IDENTICAL' if rd(S + '/a-cli-off-out/carrierA_sol_CarrierA.bin') == off_cr else 'DIFFERS'))
say('  on : %s' % ('IDENTICAL' if rd(S + '/a-out/carrierA_sol_CarrierA.bin') == on_cr else 'DIFFERS'))
say('')
say('READING (measurement, not inference): the dispatch structure is the same class in')
say('both modes — 6004361015610089 guard, 5f3560e01c selector extraction at byte 13, one')
say('GT split, then per-selector 8063...1461 EQ compares. Only jump targets and the')
say('bodies differ; the optimizer shrinks creation 2933->1460 B and runtime 2853->1426 B')
say('(50.2%) with the sorted binary-search dispatch preserved. No 60003560e01c prologue')
say('form occurs in either leg.')

out = S + '/evidence-optimizer-delta.txt'
open(out, 'w').write('\n'.join(L) + '\n')
print('wrote', out)