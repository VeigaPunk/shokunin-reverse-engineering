#!/usr/bin/env python3
"""Scratch probe (not a frozen control): the honest round-92 repair with its window widened to 39.
Tests whether the battery's near (+/-7) and far (+/-40) arms separate window 16 from window 39."""
import importlib.util, os, sys
ROOT = "/fast/scratch/hyaku/kaidoku-r93/CriticClaims/clone-diag"
spec = importlib.util.spec_from_file_location("cand", os.path.join(ROOT, "tools/round-92/upx-stop-boundary-search-repair.py"))
cand = importlib.util.module_from_spec(spec); spec.loader.exec_module(cand)
cand.WINDOW = 39
sys.exit(cand.main(sys.argv[1:]))
