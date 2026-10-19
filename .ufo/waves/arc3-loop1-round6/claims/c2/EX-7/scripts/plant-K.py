#!/usr/bin/env python3
"""EX-7 pre-compile planted-K derivation (derivation 1 of 2: pure-Python keccak).

Parses the external function signatures out of ViaIrVault.sol, derives
Keccak-256 selectors, checks ERC-20 absence, writes planted-K.json.
Run BEFORE compiling (pre-compile/pre-probe discipline).
"""
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from keccak import keccak256, selector  # noqa: E402

ROOT = Path('/var/tmp/ex07-r6')
SRC = (ROOT / 'src' / 'ViaIrVault.sol').read_text()

# strip comments, then take the parameter lists of external function decls
body = re.sub(r'///[^\n]*|/\*.*?\*/', '', SRC, flags=re.S)
sigs = []
for m in re.finditer(r'function\s+(\w+)\s*\(([^)]*)\)\s*external\s+(?:payable\s+|view\s+|pure\s+)*returns\b|function\s+(\w+)\s*\(([^)]*)\)\s*external', body):
    name = m.group(1) or m.group(3)
    params = (m.group(2) or m.group(4) or '').strip()
    types = []
    if params:
        for p in params.split(','):
            t = p.strip().split()[0]
            # data locations in params (calldata/memory) do not appear here; mappings are private
            types.append(t)
    sigs.append(f"{name}({','.join(types)})")

sigs = sorted(set(sigs))
rows = []
for sig in sigs:
    h = keccak256(sig.encode())
    rows.append({'sig': sig, 'selector': h.hex()[:8], 'keccak256_full': h.hex()})

erc20 = ['transfer(address,uint256)', 'transferFrom(address,address,uint256)',
         'balanceOf(address)', 'approve(address,uint256)', 'allowance(address,address)',
         'totalSupply()', 'name()', 'symbol()', 'decimals()']
erc20_sels = {s: selector(s) for s in erc20}
planted = {r['selector'] for r in rows}
collisions = sorted(planted & set(erc20_sels.values()))

out = {
    'recorded_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z',
    'stage': 'pre-compile/pre-probe',
    'source_file': 'src/ViaIrVault.sol',
    'derivation': 'pure-Python keccak-f[1600] (keccak.py, selftest PASS 8/8 known vectors)',
    'K': len(rows),
    'functions': rows,
    'receive_entry': 'receive() payable present in source (no selector; recorded separately)',
    'erc20_absence': {'checked': erc20_sels, 'collisions_with_planted': collisions},
}
(ROOT / 'evidence' / 'planted-K.json').write_text(json.dumps(out, indent=2) + '\n')
print(f"K={len(rows)} collisions={collisions}")
for r in rows:
    print(r['selector'], r['sig'])
