#!/usr/bin/env python3
"""EX-8 (arc3-loop1-round6, c2): a deliberately SHAPE-BLIND census — the r1/r3
solc recipe PUSH4 sel ; (DUPn) ; EQ ; PUSH2 dst ; JUMPI — run against the six
Vyper forms and the three EX-7 solc legs. Measures the false-honest-stop hazard."""
import sys, json
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else '/var/tmp/ex08-r6')
from walker import dis

def eqonly(code):
    d = dis(code); by = {o[0]: o for o in d}; sels = set()
    for pc, nm, imm, nx in d:
        if nm != 'PUSH4': continue
        j = pc + 5
        if j in by and by[j][1] in ('DUP1','DUP2','DUP3'): j += 1
        if j in by and by[j][1]=='EQ' and (j+1) in by and by[j+1][1]=='PUSH2' and (j+4) in by and by[j+4][1]=='JUMPI':
            sels.add(imm)
    return sorted(sels)

EX7 = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round6/claims/c2/EX-7'
targets = [('ex7-viair-opt200', f'{EX7}/out/viair-opt200/runtime.bin'),
           ('ex7-viair-noopt',  f'{EX7}/out/viair-noopt/runtime.bin'),
           ('ex7-std-opt200',   f'{EX7}/out/std-opt200/runtime.bin')] + [
           (f'vy-{t}', f'out/{t}/runtime.bin') for t in
           ['default','Ocodesize','Onone','nooptimize','paris-default','paris-codesize']]
out = {}
for tag, path in targets:
    code = open(path,'rb').read(); s = eqonly(code)
    out[tag] = dict(n=len(s), selectors=s)
    print(f'{tag:22s} eqonly={len(s):2d}')
json.dump(out, sys.stdout, indent=1); print()
