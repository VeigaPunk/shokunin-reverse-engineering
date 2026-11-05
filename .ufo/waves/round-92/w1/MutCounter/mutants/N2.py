#!/usr/bin/env python3
"""N2 (MutCounter, literal): for a tampered (+/-7 window) cell writes the tampered input
with a 4-byte sentinel written at the file tail, outside the window (rc 0). Refuses otherwise."""
import importlib.util, os, sys
_H = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("mutlib", os.path.join(_H, "mutlib.py"))
M = importlib.util.module_from_spec(_s); _s.loader.exec_module(M)
NAME = "N2"
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
sys.exit(M.refuse(NAME, "not a tampered cell"))
