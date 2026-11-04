#!/usr/bin/env python3
"""Generate the 7 rule wrappers, build packed+tampered fixtures, run the probe."""
import json
import os
import shutil
import struct
import subprocess
import sys

S = "/fast/scratch/hyaku/kaidoku-r88/ReviewerC1"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, S)
import vcommon as V  # noqa: E402

RULES = ["R1-first-plausible", "R2-ulen-no-sentinel", "R3-sentinel-only-smallest",
         "R4-pblocksize", "R5-clen-12n", "R6-global-scanfill", "R7-oracle"]

# 1. wrappers
os.makedirs(os.path.join(S, "rules"), exist_ok=True)
for r in RULES:
    with open(os.path.join(S, "rules", f"{r}.py"), "w") as fh:
        fh.write("#!/usr/bin/env python3\n"
                 "import sys\n"
                 f"sys.path.insert(0, {S!r})\n"
                 "import vcommon as V\n"
                 f"raise SystemExit(V.main({r!r}))\n")

# 2. fixtures
rep = V.load_r87()
fix = os.path.join(S, "fix")
os.makedirs(fix, exist_ok=True)
CARRIERS = [("jq", "/usr/bin/jq"), ("xxd", "/usr/bin/xxd"),
            ("libz", "/usr/lib/libz.so.1.3.2"), ("dinit", "/usr/bin/docker-init")]
manifest = {}
for cid, src in CARRIERS:
    d = os.path.join(fix, cid)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    orig = os.path.join(d, "orig")
    shutil.copy2(src, orig)
    packed = os.path.join(d, "packed")
    r = subprocess.run(["upx", "--best", "-q", "-o", packed, orig],
                       capture_output=True, text=True)
    assert r.returncode == 0, (cid, r.stderr)
    pb = open(packed, "rb").read()
    ph_off, ph = rep.find_packheader(pb)
    m, _s, _w = rep.find_linfo(pb, ph_off, ph)
    b0 = m + 20
    sz_unc0, sz_cpr0 = struct.unpack_from("<II", pb, b0)
    tb = bytearray(pb)
    tb[b0 + 4:b0 + 8] = b"\0\0\0\0"
    tampered = os.path.join(d, "tampered")
    open(tampered, "wb").write(bytes(tb))
    pt = subprocess.run(["upx", "-t", "-q", tampered], capture_output=True, text=True)
    manifest[cid] = {
        "b0": b0, "l_magic": m, "sz_unc0": sz_unc0, "true_sz_cpr": sz_cpr0,
        "p_blocksize": struct.unpack_from("<I", pb, m + 16)[0],
        "ph": ph, "ph_off": ph_off, "packed_len": len(pb),
        "pre_upx_t_rc": pt.returncode, "pre_tail": (pt.stdout + pt.stderr).strip()[-120:],
    }
    print(cid, json.dumps(manifest[cid]))
json.dump(manifest, open(os.path.join(S, "manifest.json"), "w"), indent=1)

# 3. probe: derived value per rule vs true
print("\n=== probe: derived sz_cpr vs true ===")
for cid, _src in CARRIERS:
    dd = os.path.join(fix, cid)
    tampered = os.path.join(dd, "tampered")
    true = manifest[cid]["true_sz_cpr"]
    row = {"carrier": cid, "true": true}
    for r in RULES:
        outp = os.path.join(dd, f"out-{r}")
        pr = subprocess.run([sys.executable, "-I", "-B",
                             os.path.join(S, "rules", f"{r}.py"),
                             "--in", tampered, "--out", outp, "--json"],
                            capture_output=True, text=True)
        info = {}
        try:
            info = json.loads(pr.stdout or "{}")
        except json.JSONDecodeError:
            pass
        row[r] = info.get("geometry", {}).get("derived_sz_cpr",
                                             info.get("geometry", {}).get("p_blocksize")) \
            if pr.returncode == 0 else f"refused:{(pr.stderr or '').strip()[-60:]}"
        row[f"{r}_match"] = (row[r] == true) if isinstance(row[r], int) else False
    print(json.dumps(row))
