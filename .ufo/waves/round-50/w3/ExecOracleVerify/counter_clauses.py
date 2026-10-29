#!/usr/bin/env python3
"""Run the FROZEN counter's own parsers and layout probe over the c6430
bytes and the frozen c6430 tables.

This exercises, with the counter's own code and without any REA run:
  * `parse_oracle`      -> the counter's `oracle_ok` clause
  * `parse_nonregular`  -> the counter's `nonregular_ok` clause
  * `layout_probe`      -> the counter's `layout_ok` clause (LE hsqs v4.0 xz,
                            mkfs_time == bytes_used, tables inside bytes_used)
  * `carve_ok` logic    -> bytes_used == ext.length == file size of the carve
  * the counter's `rederive_oracle` on the carved bytes -> `oracle_rederived_ok`

Exit 0 = the frozen counter's own clauses accept the bytes and tables.
"""
import importlib.util
import json
import os
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
SCRATCH = os.path.dirname(os.path.abspath(__file__))
COUNTER = os.path.join(LANE, 'tools/round-50/c1-counter.py')
ORACLE = os.path.join(LANE, 'tools/round-50/oracle/c6430.oracle.tsv')
NONREG = os.path.join(LANE, 'tools/round-50/oracle/c6430.nonregular.tsv')
CARRIER = os.path.join(SCRATCH, 'carrier.bin')
OUT = os.path.join(SCRATCH, 'counter_clauses.json')

spec = importlib.util.spec_from_file_location('r50_c1_counter', COUNTER)
mod = importlib.util.module_from_spec(spec)
sys.modules['r50_c1_counter'] = mod
spec.loader.exec_module(mod)

res = {}

oracle_rows, oerr = mod.parse_oracle(open(ORACLE, 'rb').read())
res['parse_oracle'] = {'error': oerr, 'rows': len(oracle_rows)}

nonreg_rows, nerr = mod.parse_nonregular(open(NONREG, 'rb').read())
res['parse_nonregular'] = {'error': nerr, 'rows': len(nonreg_rows)}

raw = open(CARRIER, 'rb').read()
lay = mod.layout_probe(raw)
res['layout_probe'] = lay

# the counter's carve_ok branch for an external carrier (carriers.json 'length')
res['carve_ok'] = {'length': 23861507, 'bytes_used': lay.get('bytes_used'),
                    'size': lay.get('size'),
                    'ok': lay.get('bytes_used') == lay.get('size') == 23861507}

# the counter's own oracle re-derivation (its `oracle_rederived_ok` clause)
derived = mod.rederive_oracle(raw, SCRATCH, 'c6430-verify')
want, got = set(oracle_rows), set(derived)
res['oracle_rederived_ok'] = {
    'frozen_rows': len(want), 'derived_rows': len(got),
    'frozen_only': sorted(want - got)[:5], 'derived_only': sorted(got - want)[:5],
    'ok': want == got}

ok = (oerr is None and nerr is None and bool(lay.get('ok'))
      and res['carve_ok']['ok'] and res['oracle_rederived_ok']['ok'])
res['verdict'] = 'PASS' if ok else 'FAIL'
with open(OUT, 'w', encoding='utf-8') as fh:
    json.dump(res, fh, indent=1, sort_keys=True)
print(json.dumps(res, indent=1, sort_keys=True))
sys.exit(0 if ok else 1)
