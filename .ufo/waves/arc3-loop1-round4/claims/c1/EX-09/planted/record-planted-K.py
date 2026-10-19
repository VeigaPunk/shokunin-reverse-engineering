#!/usr/bin/env python3
"""EX-09 (arc3-loop1-round4, c1 controls) — record the planted selector set for
Ex09Vault BEFORE any probe. Two independent keccak-256 implementations must agree:
  impl A: EX-05/keccak_ref.py  (pure-Python reference)
  impl B: EX-04/evidence/keccak256.py (separate pure-Python implementation)
Selector set is derived from Vyper's own ABI (Ex09Vault.abi.json), i.e. from the
compiler's declared interface, not from any tool output.
"""
import importlib.util, json, sys, datetime

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

BASE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round4/claims/c1'
A = load(f'{BASE}/EX-05/keccak_ref.py', 'ka').keccak256
B = load(f'{BASE}/EX-04/evidence/keccak256.py', 'kb').keccak256

def canon(t):
    if t.startswith('tuple('):
        inner = t[6:-1]
        return '(' + ','.join(canon(x) for x in inner.split(',')) + ')'
    return t

def sig(fn):
    return f"{fn['name']}({','.join(canon(i['type']) for i in fn['inputs'])})"

abi = json.load(open(sys.argv[1]))
entries = []
for e in abi:
    if e.get('type') == 'function':
        s = sig(e)
        ha, hb = A(s.encode()), B(s.encode())
        assert ha == hb, f'impl disagreement on {s}: {ha.hex()} vs {hb.hex()}'
        entries.append({'signature': s, 'selector': ha[:4].hex(),
                        'keccak256': ha.hex(), 'stateMutability': e.get('stateMutability')})
entries.sort(key=lambda x: x['selector'])
out = {
    'seat': 'EX-09', 'chain': 'c1', 'wave': 'arc3-loop1-round4',
    'carrier': 'Ex09Vault (Vyper 0.4.3+commit.bff19ea2)',
    'recorded_utc': datetime.datetime.now(datetime.UTC).isoformat().replace('+00:00', 'Z'),
    'K': len(entries),
    'impls': ['EX-05/keccak_ref.py', 'EX-04/evidence/keccak256.py'],
    'impls_agree': True,
    'selectors': [e['selector'] for e in entries],
    'entries': entries,
    'non_selector_entries': [e.get('type') for e in abi if e.get('type') in ('fallback', 'constructor', 'event')],
}
json.dump(out, open(sys.argv[2], 'w'), indent=1)
print(json.dumps({'K': out['K'], 'selectors': out['selectors']}))
for e in entries: print(' ', e['selector'], e['signature'], e['stateMutability'])
