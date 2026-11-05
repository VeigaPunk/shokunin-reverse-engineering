#!/usr/bin/env python3
"""CHEAT-C: candidate whose typed refusal exits 1 (a generic nonzero) instead of 2."""
import importlib.util, os, sys
CLONE = "/fast/scratch/hyaku/kaidoku-r91/CriticClaims/clone"
spec = importlib.util.spec_from_file_location("cand", os.path.join(CLONE, "tools/round-91/upx-stop-boundary-repair.py"))
cand = importlib.util.module_from_spec(spec); spec.loader.exec_module(cand)
rc = cand.main(sys.argv[1:])
sys.exit(1 if rc == 2 else rc)
