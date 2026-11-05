#!/usr/bin/env python3
"""N4 (MutCounter, literal): carrier-table repair that also repairs the far (+/-40) cells
to pristine; refuses intact and unknown inputs."""
import importlib.util, os, sys
_H = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("mutlib", os.path.join(_H, "mutlib.py"))
M = importlib.util.module_from_spec(_s); _s.loader.exec_module(M)
NAME = "N4"
src, dst = M.args()
m = M.match(M.read(src))
if m and m[1] in ("near", "far"):
    sys.exit(M.write(dst, m[3]))
sys.exit(M.refuse(NAME, "not a tampered cell"))
