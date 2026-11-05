#!/usr/bin/env python3
"""CHEAT-C (round-91 CriticClaims, reproduced): the candidate's rc-2 typed refusal exits 1 instead."""
import importlib.util, os, sys
ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
spec = importlib.util.spec_from_file_location("cand", os.path.join(ROOT, "tools/round-91/upx-stop-boundary-repair.py"))
cand = importlib.util.module_from_spec(spec); spec.loader.exec_module(cand)
rc = cand.main(sys.argv[1:])
sys.exit(1 if rc == 2 else rc)
