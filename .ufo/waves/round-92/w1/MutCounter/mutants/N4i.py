#!/usr/bin/env python3
"""N4i (MutCounter, isolation variant of N4): repairs near and far cells to pristine and
passes the intact input through byte-identical; refuses unknown inputs only."""
import importlib.util, os, sys
_H = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("mutlib", os.path.join(_H, "mutlib.py"))
M = importlib.util.module_from_spec(_s); _s.loader.exec_module(M)
NAME = "N4i"
src, dst = M.args()
data = M.read(src)
m = M.match(data)
if m and m[1] in ("near", "far"):
    sys.exit(M.write(dst, m[3]))
if m and m[1] == "intact":
    sys.exit(M.write(dst, data))
sys.exit(M.refuse(NAME, "unknown input"))
