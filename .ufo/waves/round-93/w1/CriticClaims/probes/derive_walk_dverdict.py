#!/usr/bin/env python3
"""Scratch probe (not a frozen control): the honest round-92 window search with its
packer verdict replaced by `upx -d` success on the candidate (a different packer call).
Tests whether the fresh-pack arm separates an open derive-by-walk from the honest repair."""
import importlib.util, os, subprocess, sys, tempfile
ROOT = "/fast/scratch/hyaku/kaidoku-r93/CriticClaims/clone-diag"
spec = importlib.util.spec_from_file_location("cand", os.path.join(ROOT, "tools/round-92/upx-stop-boundary-search-repair.py"))
cand = importlib.util.module_from_spec(spec); spec.loader.exec_module(cand)
def dverdict(data: bytes) -> bool:
    d = tempfile.mkdtemp(prefix="dv-", dir=os.environ.get("TMPDIR"))
    a, b = os.path.join(d, "c"), os.path.join(d, "o")
    open(a, "wb").write(data)
    r = subprocess.run(["/usr/bin/upx", "-d", "-q", "-o", b, a], capture_output=True)
    return r.returncode == 0 and os.path.isfile(b)
cand.upx_green = dverdict
sys.exit(cand.main(sys.argv[1:]))
