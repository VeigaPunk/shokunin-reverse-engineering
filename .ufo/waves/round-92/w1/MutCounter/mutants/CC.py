#!/usr/bin/env python3
"""Harness cross-check: CHEAT-C reproduced in the clone (rc 2 typed refusal exits 1).
Expected pre label under v2: typed 0."""
import importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
spec = importlib.util.spec_from_file_location("cand", os.path.join(ROOT, "tools/round-91/upx-stop-boundary-repair.py"))
cand = importlib.util.module_from_spec(spec); spec.loader.exec_module(cand)
rc = cand.main(sys.argv[1:])
sys.exit(1 if rc == 2 else rc)
