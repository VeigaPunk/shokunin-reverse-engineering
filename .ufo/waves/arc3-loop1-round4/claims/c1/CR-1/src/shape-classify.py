#!/usr/bin/env python3
"""CR-1 r4 — Vyper dispatch-shape classifier (Form A / B / C) + probe agreement.
Form A: 2-byte CODECOPY bucket table + `PUSH4 sel DUP2 XOR PUSH2 next JUMPI` chain (default -O gas).
Form B: `PUSH4 sel DUP2 EQ ISZERO PUSH2 body JUMPI` linear (--no-optimize / -O none).
Form C: byte-packed table, no PUSH4 immediates (-O codesize).
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vyrecon import vyper_dispatch
from disasm import dis

W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def classify(code):
    d = dis(code); by = {o[0]: (o[1], o[2]) for o in d}
    xor = eq = 0
    for off, n, imm, nx in d:
        if n != 'PUSH4': continue
        j = nx
        for _ in range(3):
            t = by.get(j)
            if not t: break
            if t[0] == '0x18': xor += 1; j += 1; continue
            if t[0] == 'EQ': eq += 1; j += 1; continue
            if t[0] in ('DUP2', 'ISZERO'): j += 1; continue
            break
    p4 = sum(1 for _, n, _, _ in d if n == 'PUSH4')
    if p4 and xor: return 'A'
    if p4 and eq: return 'B'
    if not p4: return 'C'
    return '?'

rows = []
for f in sorted(os.listdir(f'{W}/out')):
    if not f.endswith('.runtime.hex'): continue
    b = f[:-len('.runtime.hex')]
    code = bytes.fromhex(open(f'{W}/out/{f}').read().strip().replace('0x', ''))
    sels, legs, tbl, ent = vyper_dispatch(code)
    mp = f'{W}/out/{b}.methodids.json'
    pl = set(v.replace('0x', '') for v in json.load(open(mp)).values()) if os.path.exists(mp) else None
    pp = f'{W}/probe/{b}.6.4.0.json'
    pn = None
    if os.path.exists(pp):
        j = json.load(open(pp)); dd = j.get('data', j)
        pn = set(x['selector'].replace('0x', '') for x in dd['normalized_result']['functions'])
    rows.append((b, len(code), classify(code), len(sels), len(pl) if pl else None, len(pn) if pn else None,
                 (sels == pl) if pl else None, (pn == pl) if (pl and pn) else None))
print(f"{'carrier':16} {'B':>5} {'form':>4} {'census':>6} {'oracle':>6} {'probe':>6} {'census==oracle':>14} {'probe==oracle':>13}")
for r in rows:
    b, n, form, kc, kp, kn, co, po = r
    print(f"{b:16} {n:>5} {form:>4} {kc:>6} {kp if kp is not None else '-':>6} {kn if kn is not None else '-':>6} {str(co):>14} {str(po):>13}")
