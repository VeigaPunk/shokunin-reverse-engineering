#!/usr/bin/env python3
"""N5 (MutCounter, literal): repairs near cells to pristine, refuses far cells, and for the
intact input writes output with one byte changed (last byte XOR 1, rc 0)."""
import importlib.util, os, sys
_H = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("mutlib", os.path.join(_H, "mutlib.py"))
M = importlib.util.module_from_spec(_s); _s.loader.exec_module(M)
NAME = "N5"
src, dst = M.args()
data = M.read(src)
m = M.match(data)
if m and m[1] == "near":
    sys.exit(M.write(dst, m[3]))
if m and m[1] == "intact":
    out = bytearray(data)
    out[-1] ^= 0x01
    sys.exit(M.write(dst, bytes(out)))
sys.exit(M.refuse(NAME, "not a tampered cell"))
