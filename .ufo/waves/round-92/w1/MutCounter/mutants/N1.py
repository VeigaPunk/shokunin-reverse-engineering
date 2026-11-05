#!/usr/bin/env python3
"""N1 (MutCounter, literal): carrier-table repair. Writes the pinned packed image of the
carrier for a tampered (+/-7 window) cell; refuses everything else (intact included)."""
import importlib.util, os, sys
_H = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("mutlib", os.path.join(_H, "mutlib.py"))
M = importlib.util.module_from_spec(_s); _s.loader.exec_module(M)
NAME = "N1"
src, dst = M.args()
m = M.match(M.read(src))
if m and m[1] == "near":
    sys.exit(M.write(dst, m[3]))
sys.exit(M.refuse(NAME, "not a tampered cell"))
