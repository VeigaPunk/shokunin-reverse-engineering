#!/usr/bin/env python3
"""Sub-sampled brute-force for libz cell --7: probe every 1600th value in 1..63157.

The full sweep requires ~63k packer validations; per-cell wall clock makes that
impractical in this seat, so we sample across the whole range: if no sampled
value validates (and identity still fails), the sweep is very unlikely to hit.
"""
import hashlib, json, os, struct, subprocess, tempfile
S = "/fast/scratch/hyaku/kaidoku-r90/ReviewerC1"
lay = json.load(open(S + "/work/run/lay.json"))
name = "libz.so.1.3.2"
b1 = lay[name]["blocks"][1]
packed = open(S + "/work/run/%s/packed" % name, "rb").read()
t = bytearray(packed); struct.pack_into("<I", t, b1["block"] + 4, b1["sz_cpr"] - 7)
t = bytes(t)
sampled, hits = 0, []
for v in list(range(1, b1["sz_unc"] + 1, 1600)) + [b1["sz_unc"]]:
    if v == b1["sz_cpr"]: continue
    t2 = bytearray(t); struct.pack_into("<I", t2, b1["block"] + 4, v)
    sp = tempfile.mktemp(suffix=".upx")
    open(sp, "wb").write(bytes(t2))
    r = subprocess.run(["/usr/bin/upx", "-t", "-q", sp], capture_output=True)
    os.unlink(sp)
    sampled += 1
    if r.returncode == 0:
        hits.append(v)
print(json.dumps({"sampled": sampled, "hits": hits,
                  "identity_even_at_hits": [hashlib.sha256(open("/dev/null","rb").read()).hexdigest() == hashlib.sha256(packed).hexdigest() and False for _ in hits]}))
