#!/usr/bin/env python3
"""CR-3 — per-row view of gate-bearing but needleless units (the 'blank scope'
question behind the H3 floor). Reuses the frozen instrument's own units()/REA_GATE.
"""
import importlib.util
import json
import os
import sys

GATE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/c1-census-v10.py"
ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
spec = importlib.util.spec_from_file_location("census", GATE)
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)

files = sorted({s[0] for s in C.SCOPE})
fl = {}
for f in files:
    fl[f] = open(os.path.join(ROOT, f), encoding="utf-8",
                 errors="replace").read().splitlines()

rows = []
for (f, s, e, cls, ml, mr) in C.SCOPE:
    lines = fl[f]
    gb_total, gb_needleless, needleless_blocks = 0, [], []
    for (a, b, text) in C.units(lines):
        if b < s - 1 or a > e - 1:
            continue
        if not C.REA_GATE.search(text):
            continue
        gb_total += 1
        has_occ = bool(C.PIN.search(text)) or bool(C.VER.search(text)) or bool(C.PTR.search(text))
        if not has_occ:
            gb_needleless.append("%d-%d" % (a + 1, b + 1))
            needleless_blocks.append(text[:90])
    rows.append({"row": "%s:%d-%d" % (f, s, e), "class": cls,
                 "gate_units_intersecting": gb_total,
                 "gate_units_needleless": gb_needleless,
                 "sample_text": needleless_blocks[:2]})
print(json.dumps(rows, indent=1))
