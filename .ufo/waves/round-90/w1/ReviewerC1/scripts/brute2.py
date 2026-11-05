#!/usr/bin/env python3
"""Round 2 of cheap arms: tarthe interior block (blocks[1]), which is what
the P1 battery actually tampers (stored_sz_cpr 1644/1658 jq etc.)."""
import hashlib, json, os, struct, subprocess, sys, tempfile, importlib.util
ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r90/ReviewerC1"
def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m); return m
rep = load(ROOT + "/tools/round-87/upx-magic-repair.py", "r87")
r88 = load(ROOT + "/tools/round-88/upx-chain-repair.py", "r88")
lay = json.load(open(S + "/work/run/lay.json"))

def upx_t(data):
    with tempfile.NamedTemporaryFile(suffix=".upx", delete=False) as fh:
        fh.write(data); p = fh.name
    r = subprocess.run(["/usr/bin/upx", "-t", "-q", p], capture_output=True)
    os.unlink(p)
    return r.returncode == 0

results = {"brute2": [], "first-successor2": []}
for name, v in lay.items():
    b1 = v["blocks"][1]
    for d in (-7, 7):
        val = b1["sz_cpr"] + d
        if not (0 < val <= b1["sz_unc"]): continue
        tid = "%s-%+d" % (name, d)
        rr = {"cell": tid}
        # brute force over 1..sz_unc on the interior block
        hits = None; tries = 0
        p, su = b1["block"], b1["sz_unc"]
        packed = open(S + "/work/run/%s/packed" % name, "rb").read()
        tt = bytearray(packed); struct.pack_into("<I", tt, p + 4, val)
        t = bytes(tt)
        for v in range(1, su + 1):
            if v == b1["sz_cpr"]: continue
            tries += 1
            t2 = bytearray(t); struct.pack_into("<I", t2, p + 4, v)
            if upx_t(bytes(t2)):
                hits = v
                rec = {"cell": tid, "pos": p, "derived": v, "tries": tries,
                       "valid_upx_t": True,
                       "identity": hashlib.sha256(bytes(t2)).hexdigest() == hashlib.sha256(packed).hexdigest()}
                break
        if hits is None:
            rec = {"cell": tid, "pos": p, "derived": None, "tries": tries, "valid_upx_t": False}
        results["brute2"].append(rec)
        json.dump(results, open(S + "/cheap-arms2.json", "w"), indent=1)
json.dump(results, open(S + "/cheap-arms2.json", "w"), indent=1)
print(json.dumps(results["brute2"], indent=1))
