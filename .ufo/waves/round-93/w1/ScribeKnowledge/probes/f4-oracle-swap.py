#!/usr/bin/env python3
"""PROBE (unscored) F4: the round-92 repair with its packer verdict
`upx_green` replaced by an `upx -d` decompression oracle. This is NOT a
table forgery and NOT a carrier read: it derives the answer with a
different oracle. Used only to measure the fresh arm's mechanism floor."""
import importlib.util, os, subprocess, sys, tempfile
ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
spec = importlib.util.spec_from_file_location("cand", os.path.join(ROOT, "tools/round-92/upx-stop-boundary-search-repair.py"))
cand = importlib.util.module_from_spec(spec); spec.loader.exec_module(cand)
def decompresses(data):
    box = tempfile.mkdtemp(prefix="f4-")
    cand_p = os.path.join(box, "c"); out_p = os.path.join(box, "o")
    open(cand_p, "wb").write(data)
    r = subprocess.run(["/usr/bin/upx", "-d", "-q", "-o", out_p, cand_p], capture_output=True)
    return r.returncode == 0 and os.path.isfile(out_p)
cand.upx_green = decompresses
sys.exit(cand.main(sys.argv[1:]))
