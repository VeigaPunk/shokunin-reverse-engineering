#!/usr/bin/env python3
"""N3 (MutCounter, literal): for a tampered (+/-7 window) cell rewrites the four-byte
window to (tampered value XOR 1), which is not the pristine value, and exits 0. Refuses otherwise."""
import importlib.util, os, struct, sys
_H = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("mutlib", os.path.join(_H, "mutlib.py"))
M = importlib.util.module_from_spec(_s); _s.loader.exec_module(M)
NAME = "N3"
src, dst = M.args()
data = M.read(src)
m = M.match(data)
if m and m[1] == "near":
    w = M.window(m[0])
    out = bytearray(data)
    val = struct.unpack_from("<I", data, w)[0]
    struct.pack_into("<I", out, w, val ^ 1)
    sys.exit(M.write(dst, bytes(out)))
sys.exit(M.refuse(NAME, "not a tampered cell"))
