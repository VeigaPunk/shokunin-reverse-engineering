#!/usr/bin/env python3
"""CriticC1 probe: UPX! occurrences vs structural PackHeader, pack determinism,
upx -t failure reasons per tamper."""
import hashlib, importlib.util, json, os, struct, subprocess, sys

S = "/fast/scratch/hyaku/kaidoku-r98/CriticC1"
UPX = "/usr/bin/upx"
os.makedirs(S + "/w/probe", exist_ok=True)
os.makedirs(S + "/cache", exist_ok=True)
spec = importlib.util.spec_from_file_location("bat", S + "/clone/tools/round-98/pe-upx-tamper-battery.py")
bat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bat)


def sha(b):
    return hashlib.sha256(b).hexdigest()


res, eff = {}, []
for name, src, pin in bat.CARRIERS:
    packed = os.path.join(S, "w", "base", name + ".upx")
    b = open(packed, "rb").read()
    occ = []
    i = b.find(b"UPX!")
    while i >= 0:
        occ.append(i)
        i = b.find(b"UPX!", i + 1)
    pj = os.path.join(S, "w", "probe", name + ".probe.out")
    p = subprocess.run([sys.executable, "-I", "-B", S + "/clone/tools/round-98/upx-pe-repair.py",
                        "--in", packed, "--out", pj, "--json"], capture_output=True, text=True)
    try:
        meta = json.loads(p.stdout)
    except Exception:
        meta = {"rc": p.returncode, "stderr": p.stderr[-160:]}
    pe = struct.unpack_from("<I", b, 0x3C)[0]
    opt = struct.unpack_from("<H", b, pe + 20)[0]
    st = pe + 24 + opt
    n = struct.unpack_from("<H", b, pe + 6)[0]
    secs = []
    for k in range(n):
        off = st + 40 * k
        secs.append([k, bytes(b[off:off + 8]).rstrip(b"\0").decode("latin1"),
                     struct.unpack_from("<I", b, off + 20)[0]])
    rp = os.path.join(S, "cache", name + ".upx")
    subprocess.run([UPX, "--best", "-q", "-o", rp, src], capture_output=True)
    rb = open(rp, "rb").read()
    res[name] = {"size": len(b), "pack_sha256": sha(b), "repack_sha_equal": sha(rb) == sha(b),
                 "repack_size": len(rb), "upx_bang_offsets": occ, "repair_json": meta,
                 "sections": secs}

for name, src, pin in bat.CARRIERS:
    pb = open(os.path.join(S, "w", "base", name + ".upx"), "rb").read()
    for kind in bat.TAMPERS:
        tp = os.path.join(S, "w", "probe", "%s.%s.tam" % (name, kind))
        open(tp, "wb").write(bat.tamper(pb, kind))
        r = subprocess.run([UPX, "-t", "-q", tp], capture_output=True, text=True)
        lines = [ln for ln in (r.stdout + r.stderr).strip().splitlines() if ln.strip()]
        eff.append({"carrier": name, "kind": kind, "rc": r.returncode,
                    "reason": lines[-1] if lines else ""})

json.dump({"carriers": res, "effective": eff}, open(S + "/out/probe1.json", "w"), indent=1)
for name, d in res.items():
    print(name, "size", d["size"], "repack_eq", d["repack_sha_equal"],
          "UPX!@", d["upx_bang_offsets"], "ph", d["repair_json"].get("packheader"),
          d["repair_json"].get("changes"))
for e in eff:
    print(e["carrier"], e["kind"], "rc", e["rc"], "|", e["reason"])
