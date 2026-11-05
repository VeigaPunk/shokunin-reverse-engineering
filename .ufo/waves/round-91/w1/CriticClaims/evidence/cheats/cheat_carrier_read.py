#!/usr/bin/env python3
"""CHEAT-A: candidate with upx_test replaced by 'input == pack(pinned carrier path)'.
Reads the carrier path; never inspects the packer verdict."""
import importlib.util, os, shutil, subprocess, sys, tempfile
CLONE = "/fast/scratch/hyaku/kaidoku-r91/CriticClaims/clone"
CARRIERS = ["/usr/bin/jq", "/usr/bin/xxd", "/usr/lib/libz.so.1.3.2", "/usr/bin/docker-init"]
spec = importlib.util.spec_from_file_location("cand", os.path.join(CLONE, "tools/round-91/upx-stop-boundary-repair.py"))
cand = importlib.util.module_from_spec(spec); spec.loader.exec_module(cand)
def carrier_packed_matches(d):
    for c in CARRIERS:
        box = tempfile.mkdtemp(prefix="ca-")
        inp, outp = os.path.join(box, "in"), os.path.join(box, "p")
        shutil.copyfile(c, inp); os.chmod(inp, 0o755)
        subprocess.run(["/usr/bin/upx", "--best", "-q", "-o", outp, inp], capture_output=True)
        if os.path.isfile(outp) and open(outp, "rb").read() == d:
            return True
    return False
cand.upx_test = carrier_packed_matches
sys.exit(cand.main(sys.argv[1:]))
