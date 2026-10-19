#!/usr/bin/env python3
"""CR-1 r4 — identity re-derivation FROM THE WAVE COPIES (rule #14).

Reads only the landed artifacts under claims/c1/CR-1/{out,probe} and re-derives:
  (a) the independent byte-level dispatch census (bucket table + XOR chain);
  (b) the oracle set (Vyper's own method_identifiers);
  (c) the probe's recovered set from the sealed envelope.
Three-way agreement is asserted for every carrier; the three deliberate
injections are reported separately against their BASE oracle (they are expected
to differ by construction), and the two non-default optimizer forms (B: EQ+ISZERO,
C: byte-packed) are reported as 'unparsed by the Form-A census' — not as failures.

Exit code 0 iff every clean carrier agrees three ways.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vyrecon import vyper_dispatch

W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INJECTED = {'K8tampered': 'K8', 'K8-legbroken': 'K8', 'K8-partial': 'K8'}
# forms this seat's Form-A census cannot parse; verified by probe+oracle instead
ALT_FORM = {'K8.nooptimize', 'K8.Onone', 'K8.Ocodesize'}

def oracle(b):
    p = f'{W}/out/{b}.methodids.json'
    if not os.path.exists(p): return None
    return set(v.replace('0x', '') for v in json.load(open(p)).values())

def probe_set(b):
    for pin in ('6.4.0', '6.7.0'):
        p = f'{W}/probe/{b}.{pin}.json'
        if os.path.exists(p):
            j = json.load(open(p)); d = j.get('data', j)
            return set(x['selector'].replace('0x', '') for x in d['normalized_result']['functions'])
    return None

ok = []; inj = []; alt = []; bad = []
for f in sorted(os.listdir(f'{W}/out')):
    if not f.endswith('.runtime.hex'): continue
    b = f[:-len('.runtime.hex')]
    code = bytes.fromhex(open(f'{W}/out/{f}').read().strip().replace('0x', ''))
    sels, _, _, _ = vyper_dispatch(code)
    ps = probe_set(b)
    if b in INJECTED:
        base = oracle(INJECTED[b])
        inj.append((b, len(base), len(ps), sorted(base - ps), sorted(ps - base)))
        continue
    pl = oracle(b)
    if pl is None: continue
    if b in ALT_FORM:
        alt.append((b, len(pl), len(ps), ps == pl))
        continue
    if sels == pl and ps == pl: ok.append((b, len(sels)))
    else: bad.append((b, sorted(pl - sels), sorted(sels - pl), ps == pl))

print(f"three-way OK (census == oracle == probe): {len(ok)} carriers")
print(f"  " + " ".join(f"{b}(K={k})" for b, k in ok))
print(f"\ninjected variants vs their BASE oracle: {len(inj)}")
for b, kp, kn, miss, extra in inj:
    print(f"  INJ {b:16} base_K={kp} probe_K={kn} missing={miss} extra={extra}")
print(f"\nalt optimizer forms (unparsed by the Form-A census; probe==oracle asserted): {len(alt)}")
for b, kp, kn, agree in alt:
    print(f"  ALT {b:16} oracle_K={kp} probe_K={kn} probe==oracle={agree}")
print(f"\nFAILURES: {bad if bad else 'NONE'}")
sys.exit(1 if (bad or any(not a for _, _, _, a in alt)) else 0)
