#!/usr/bin/env python3
"""validate_committed.py - run the committed repair and validate its output
with the packer itself, per carrier.  Produces committed_validation.json."""
import hashlib
import json
import os
import shutil
import subprocess
import sys

S = os.environ.get("GEOMX_WORK") or os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(os.path.abspath(__file__))
TOOL = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-88/upx-chain-repair.py"
NAMES = ["jq", "xxd", "libz.so.1.3.2", "docker-init"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def run(cmd):
    p = subprocess.run(cmd, capture_output=True)
    return {"cmd": cmd, "exit": p.returncode,
            "stdout": p.stdout.decode("utf-8", "replace").strip(),
            "stderr": p.stderr.decode("utf-8", "replace").strip()}


out = {}
for n in NAMES:
    w = os.path.join(S, "work", n)
    tam = os.path.join(w, n + ".tampered")
    rep = os.path.join(w, n + ".committed2")
    r = run([sys.executable, "-I", "-B", TOOL, "--in", tam, "--out", rep, "--json"])
    rec = {"repair_exit": r["exit"], "repair_stderr": r["stderr"]}
    if r["exit"] == 0:
        info = json.loads(r["stdout"])
        rec["class"] = info.get("class")
        rec["derived_sz_cpr"] = (info.get("geometry") or {}).get("derived_sz_cpr")
        rec["upstream_sha256"] = info.get("upstream_sha256")
        rec["output_sha256"] = sha(rep)
        rec["output_byte_identical_to_packed"] = sha(rep) == sha(os.path.join(S, "pack", n + ".packed"))
        t = run(["/usr/bin/upx", "-t", rep])
        rec["upx_t_exit"] = t["exit"]
        rec["upx_t_stderr"] = t["stderr"].splitlines()[-1:] if t["stderr"] else []
        if t["exit"] == 0:
            d = os.path.join(w, n + ".committed2.d")
            shutil.copyfile(rep, d)
            u = run(["/usr/bin/upx", "-d", "-o", d + ".out", d])
            rec["upx_d_exit"] = u["exit"]
            if u["exit"] == 0:
                rec["restored_sha256"] = sha(d + ".out")
                rec["restored_matches_carrier"] = rec["restored_sha256"] == sha(os.path.join(S, "pack", n + ".orig"))
    out[n] = rec
    print(n, json.dumps({k: rec[k] for k in rec if k not in ("repair_stderr",)}, sort_keys=True))
json.dump(out, open(os.path.join(OUT, "committed_validation.json"), "w"), indent=1, sort_keys=True)
