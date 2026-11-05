#!/usr/bin/env python3
"""X1 (MutCounter, EXTRA beyond the six assigned counterfeits): on a tampered (+/-7 window)
cell exits 0 and writes the tampered input with a sentinel word outside the window. Intact
input passes through byte-identical; any other input is refused with a typed rc-2 refusal.
Purpose: the assigned six never reach the v2 `unsafe` gate (M4 lands in `other`); this one does."""
import importlib.util, os, sys
_H = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("mutlib", os.path.join(_H, "mutlib.py"))
M = importlib.util.module_from_spec(_s); _s.loader.exec_module(M)
NAME = "X1"
src, dst = M.args()
data = M.read(src)
m = M.match(data)
if m and m[1] == "near":
    sentinel = b"\xca\xfe\xba\xbe"
    if data[-4:] == sentinel:
        sentinel = b"\xde\xad\xbe\xef"
    out = bytearray(data)
    out[-4:] = sentinel
    sys.exit(M.write(dst, bytes(out)))
if m and m[1] == "intact":
    sys.exit(M.write(dst, data))
sys.exit(M.refuse(NAME, "unknown input"))
