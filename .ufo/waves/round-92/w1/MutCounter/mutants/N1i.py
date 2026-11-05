#!/usr/bin/env python3
"""N1i (MutCounter, isolation variant of N1): carrier-table repair that also passes the
intact input through byte-identical (identity), refusing only far and unknown cells."""
import importlib.util, os, sys
_H = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("mutlib", os.path.join(_H, "mutlib.py"))
M = importlib.util.module_from_spec(_s); _s.loader.exec_module(M)
NAME = "N1i"
src, dst = M.args()
data = M.read(src)
m = M.match(data)
if m and m[1] == "near":
    sys.exit(M.write(dst, m[3]))
if m and m[1] == "intact":
    sys.exit(M.write(dst, data))
sys.exit(M.refuse(NAME, "not a tampered cell"))
