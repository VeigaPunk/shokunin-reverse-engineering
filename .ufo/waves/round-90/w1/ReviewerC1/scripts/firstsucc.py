#!/usr/bin/env python3
"""First-plausible-successor arm, interior block (the one the battery tampers)."""
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

results = []
for name, v in lay.items():
    b1 = v["blocks"][1]
    ph_off = v["ph_off"]
    for d in (-7, 7):
        val = b1["sz_cpr"] + d
        if not (0 < val <= b1["sz_unc"]): continue
        tid = "%s-%+d" % (name, d)
        packed = open(S + "/work/run/%s/packed" % name, "rb").read()
        t = bytearray(packed); struct.pack_into("<I", t, b1["block"] + 4, val)
        t = bytes(t)
        p, su, sc_stored = b1["block"], b1["sz_unc"], b1["sz_cpr"]
        method = packed[b1["block"] + 8]
        rec = {"cell": tid, "pos": p, "stored": sc_stored}
        hits = None
        for s in range(p + 13, ph_off - 12):
            su2, sc2 = struct.unpack_from("<II", t, s)
            if not (0 < sc2 <= su2) or s + 12 + sc2 > ph_off or t[s+8] not in (method, 14):
                continue
            derived = s - (p + 12)
            if not (0 < derived <= su) or derived == sc_stored: continue
            t2 = bytearray(t); struct.pack_into("<I", t2, p + 4, derived)
            hits = derived
            rec.update({"successor": s, "derived": derived,
                        "valid_upx_t": upx_t(bytes(t2)),
                        "identity": hashlib.sha256(bytes(t2)).hexdigest() == hashlib.sha256(packed).hexdigest()})
            break
        if hits is None:
            rec.update({"successor": None, "derived": None, "valid_upx_t": False})
        results.append(rec)
        json.dump(results, open(S + "/cheap-arms3.json", "w"), indent=1)
print(json.dumps(results, indent=1))
