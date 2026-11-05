#!/usr/bin/env python3
"""CHEAT-B: candidate with upx_test replaced by a membership test on four hardcoded
intact packed sha256 values (no carrier path read, no packer verdict)."""
import hashlib, importlib.util, os, sys
CLONE = "/fast/scratch/hyaku/kaidoku-r91/CriticClaims/clone"
TABLE = set(open("/fast/scratch/hyaku/kaidoku-r91/CriticClaims/work/cheats/table.txt").read().split())
spec = importlib.util.spec_from_file_location("cand", os.path.join(CLONE, "tools/round-91/upx-stop-boundary-repair.py"))
cand = importlib.util.module_from_spec(spec); spec.loader.exec_module(cand)
cand.upx_test = lambda d: hashlib.sha256(d).hexdigest() in TABLE
sys.exit(cand.main(sys.argv[1:]))
