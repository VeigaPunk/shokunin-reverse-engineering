import importlib.util, json, os, sys
from pathlib import Path
repo = Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
spec = importlib.util.spec_from_file_location('eng', repo/'tools/round-50/c1-counter.py')
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
carriers = json.loads((repo/'tools/round-50/carriers.json').read_text())
freeze = '3663e6b21dccf4c4957f459301156664d8b151d6'
pins, sources = mod.prior_pins(str(repo), freeze, carriers)
print('prior_sources', sources)
print('prior_pin_count', len(pins))
for c in carriers['carriers']:
    p = c['sha256'].lower()
    print(c['id'], 'pin_in_prior=', p in pins, '=> carrier_fresh_ok =', (p not in pins))
print('prior_pin_candidates_present:', [(x, bool(mod.show(str(repo), freeze, x))) for x in mod.PRIOR_PIN_CANDIDATES])
print('prior_carrier_tables_present:', [(x, bool(mod.show(str(repo), freeze, x))) for x in mod.PRIOR_CARRIER_TABLES])
r42 = json.loads(mod.show(str(repo), freeze, 'tools/round-42/prior-pins.json'))
print('r42 prior pins count', len(r42.get('pins') or []))
r49 = json.loads(mod.show(str(repo), freeze, 'tools/round-49/carriers.json'))
print('r49 carriers pins', [c.get('sha256','')[:12] for c in r49.get('carriers') or []])
print('rea pkg found:', (mod.find_rea_pkg() or 'NONE'))
