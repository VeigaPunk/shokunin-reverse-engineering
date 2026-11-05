#!/usr/bin/env python3
"""ReviewerRepair parity harness: r98 vs r99 upx-pe-repair on battery cell classes + attacks."""
import hashlib, importlib.util, json, os, shutil, subprocess, sys

S = "/fast/scratch/hyaku/kaidoku-r99/ReviewerRepair"
R98 = S + "/clone/tools/round-98/upx-pe-repair.py"
R99 = S + "/clone/tools/round-99/upx-pe-repair.py"
UPX = "/usr/bin/upx"
W = S + "/exp"

spec = importlib.util.spec_from_file_location("bat", S + "/clone/tools/round-99/pe-upx-trunc-battery.py")
bat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bat)

def run(argv):
    p = subprocess.run(argv, capture_output=True, text=True, timeout=600)
    return p.returncode, p.stdout, p.stderr

def sha_b(b): return hashlib.sha256(b).hexdigest()

def snapshot(d):
    out = {}
    for root, dirs, files in os.walk(d):
        for f in files:
            p = os.path.join(root, f)
            out[os.path.relpath(p, d)] = os.path.getsize(p)
    return out

CELLS = W + "/cells"
os.makedirs(CELLS, exist_ok=True)
results = []

def probe(name, tag, data, expect="parity"):
    ip = os.path.join(CELLS, "%s.%s.in" % (name, tag))
    with open(ip, "wb") as fh: fh.write(data)
    o98, o99 = ip + ".r98.out", ip + ".r99.out"
    for p in (o98, o99):
        if os.path.exists(p): os.unlink(p)
    before = snapshot(CELLS)
    rc98, so98, se98 = run([sys.executable, "-I", "-B", R98, "--in", ip, "--out", o98])
    mid = snapshot(CELLS)
    rc99, so99, se99 = run([sys.executable, "-I", "-B", R99, "--in", ip, "--out", o99])
    after = snapshot(CELLS)
    b98 = open(o98, "rb").read() if os.path.exists(o98) else None
    b99 = open(o99, "rb").read() if os.path.exists(o99) else None
    trc, _, _ = run([UPX, "-t", "-q", ip])
    left98 = set(mid) - set(before) - {os.path.basename(o98)}
    left99 = set(after) - set(mid) - {os.path.basename(o99)}
    same_dec = (rc98 == rc99) if expect == "parity" else (rc98 == 0 and rc99 == 2 and "truncated" in se99)
    results.append({
        "cell": "%s.%s" % (name, tag), "size": len(data), "upx_t_rc": trc,
        "r98_rc": rc98, "r99_rc": rc99,
        "r98_sha": sha_b(b98) if b98 else None, "r99_sha": sha_b(b99) if b99 else None,
        "bytes_equal": (b98 == b99) if (b98 is not None and b99 is not None) else None,
        "same_decision": same_dec,
        "r98_msg": (so98 + se98).strip()[:100], "r99_msg": (so99 + se99).strip()[:100],
        "temp_left_98": sorted(left98), "temp_left_99": sorted(left99),
    })

# --- pins + packs ---
pins, packs = [], {}
os.makedirs(W + "/packs", exist_ok=True)
for name, srcp, pin in bat.CARRIERS:
    present = os.path.exists(srcp)
    ok = present and sha_b(open(srcp, "rb").read()) == pin
    pins.append({"carrier": name, "present": present, "pin_ok": ok})
    if not ok: continue
    os.makedirs(W + "/carriers", exist_ok=True)
    src = os.path.join(W, "carriers", name + ".orig")
    shutil.copyfile(srcp, src)
    pk = os.path.join(W, "packs", name + ".upx")
    rc, _, se = run([UPX, "--best", "-q", "-f", "-o", pk, src])
    if rc == 0 and os.path.exists(pk):
        with open(pk, "rb") as fh: packs[name] = fh.read()
    else:
        pins[-1]["pack_rc"] = rc; pins[-1]["pack_err"] = se.strip()[:120]

# --- battery cell classes, parity expectations ---
for name, pb in packs.items():
    probe(name, "intact", pb)
    for kind in bat.TAMPERS:
        probe(name, kind, bat.tamper(pb, kind))
    dec = bat.decoy(pb)
    if dec is not None:
        probe(name, "decoy", dec)
    ov = os.urandom(1 + int.from_bytes(os.urandom(2), "little") % 4096)
    probe(name, "ov-intact", pb + ov)
    probe(name, "ov-both", bat.tamper(pb, "both") + ov)
    for base_tag, base in (("intact", pb), ("both", bat.tamper(pb, "both"))):
        for cut_tag, at in sorted(bat.cuts(pb).items()):
            probe(name, "trunc-%s-%s" % (base_tag, cut_tag), base[:at], expect="trunc")

# --- attack probes on first PE32 and first PE32+ pack ---
def pe_off(b): return int.from_bytes(b[0x3C:0x40], "little")

probes_done = []
for name, pb in packs.items():
    pe = pe_off(pb)
    magic = int.from_bytes(pb[pe+24:pe+26], "little")
    key = "pe32" if magic == 0x10B else "pe32+"
    if key in probes_done: continue
    probes_done.append(key)
    st, n, falign, secs = bat.pe_layout(pb)
    b = bytearray(pb)
    b[pe+6:pe+8] = (n + 1).to_bytes(2, "little")          # n sections > file holds
    probe(name, "atk-nsec-plus1", bytes(b))
    b = bytearray(pb); b[pe+24+36:pe+24+40] = b"\0\0\0\0"  # FileAlignment = 0
    probe(name, "atk-falign-zero", bytes(b))
    b = bytearray(pb); b[pe+24+36:pe+24+40] = (3).to_bytes(4, "little")  # non-pow2 falign
    probe(name, "atk-falign-3", bytes(b))
    b = bytearray(pb); b[pe+24+36:pe+24+40] = (0xFFFFFFFF).to_bytes(4, "little")
    probe(name, "atk-falign-FFFFFFFF", bytes(b))
    b = bytearray(pb)                                       # 2^32 wrap on last section raw end
    off = st + 40 * (n - 1) + 20
    b[off:off+4] = (0xFFFFFE00).to_bytes(4, "little")
    probe(name, "atk-wrap-rptr", bytes(b))
    b = bytearray(pb)                                       # huge SizeOfRawData on last section
    off = st + 40 * (n - 1) + 16
    b[off:off+4] = (0xFFFFFF00).to_bytes(4, "little")
    probe(name, "atk-huge-rsize", bytes(b))
    b = bytearray(pb)                                       # sections in non-raw order (swap 2 and 3)
    if n >= 4:
        h2 = bytes(b[st+40:st+80]); h3 = bytes(b[st+80:st+120])
        b[st+40:st+80] = h3; b[st+80:st+120] = h2
        probe(name, "atk-swap-sec23", bytes(b))

# --- CLI / error envelope ---
ED = W + "/err"; shutil.rmtree(ED, ignore_errors=True); os.makedirs(ED)
some = os.path.join(W, "packs", "t32.upx")
if not os.path.exists(some) and packs:
    some = os.path.join(W, "packs", list(packs)[0] + ".upx")
def cli(tag, argv):
    rc, so, se = run(argv)
    after = sorted(os.listdir(ED))
    results.append({"cell": "cli." + tag, "r98_rc": None, "r99_rc": None,
                    "upx_t_rc": None, "same_decision": None, "bytes_equal": None,
                    "rc": rc, "stdout": so.strip()[:100], "stderr": se.strip()[:160],
                    "traceback": "Traceback" in (so + se), "dir_after": after})

inp = os.path.join(ED, "in.upx"); shutil.copyfile(some, inp)
cli("missing-in-r99", [sys.executable, "-I", "-B", R99, "--in", ED + "/no-such", "--out", ED + "/o1"])
cli("missing-in-r98", [sys.executable, "-I", "-B", R98, "--in", ED + "/no-such", "--out", ED + "/o1b"])
cli("missing-outdir-r99", [sys.executable, "-I", "-B", R99, "--in", inp, "--out", ED + "/nodir/o2"])
cli("missing-outdir-r98", [sys.executable, "-I", "-B", R98, "--in", inp, "--out", ED + "/nodir/o2b"])
od = os.path.join(ED, "is-a-dir"); os.makedirs(od)
cli("out-is-dir-r99", [sys.executable, "-I", "-B", R99, "--in", inp, "--out", od])
cli("out-is-dir-r98", [sys.executable, "-I", "-B", R98, "--in", inp, "--out", od])
ro = os.path.join(ED, "ro"); os.makedirs(ro); os.chmod(ro, 0o500)
cli("readonly-outdir-r99", [sys.executable, "-I", "-B", R99, "--in", inp, "--out", ro + "/o3"])
cli("readonly-outdir-r98", [sys.executable, "-I", "-B", R98, "--in", inp, "--out", ro + "/o3b"])
os.chmod(ro, 0o700)
din = os.path.join(ED, "dir-in"); os.makedirs(din)
cli("in-is-dir-r99", [sys.executable, "-I", "-B", R99, "--in", din, "--out", ED + "/o4"])
cli("in-is-dir-r98", [sys.executable, "-I", "-B", R98, "--in", din, "--out", ED + "/o4b"])
# in == out in-place, both tools
pl = os.path.join(ED, "place1.upx"); shutil.copyfile(some, pl)
tb = bat.tamper(open(some, "rb").read(), "both")
with open(pl, "wb") as fh: fh.write(tb)
cli("inplace-r98", [sys.executable, "-I", "-B", R98, "--in", pl, "--out", pl])
sha_place_r98 = sha_b(open(pl, "rb").read()) if os.path.exists(pl) else None
with open(pl, "wb") as fh: fh.write(tb)
cli("inplace-r99", [sys.executable, "-I", "-B", R99, "--in", pl, "--out", pl])
sha_place_r99 = sha_b(open(pl, "rb").read()) if os.path.exists(pl) else None
results.append({"cell": "cli.inplace-compare", "r98_sha": sha_place_r98, "r99_sha": sha_place_r99,
                "bytes_equal": sha_place_r98 == sha_place_r99})
# --json parity on a repaired cell
jd = os.path.join(ED, "j.in"); open(jd, "wb").write(tb)
rcj98 = run([sys.executable, "-I", "-B", R98, "--json", "--in", jd, "--out", ED + "/j98.out"])
rcj99 = run([sys.executable, "-I", "-B", R99, "--json", "--in", jd, "--out", ED + "/j99.out"])
results.append({"cell": "cli.json-parity", "r98_rc": rcj98[0], "r99_rc": rcj99[0],
                "r98_stdout": rcj98[1].strip(), "r99_stdout": rcj99[1].strip(),
                "bytes_equal": open(ED+"/j98.out","rb").read() == open(ED+"/j99.out","rb").read()
                if os.path.exists(ED+"/j98.out") and os.path.exists(ED+"/j99.out") else None})

receipt = {"pins": pins, "n_cells": len(results), "results": results}
with open(W + "/parity-receipt.json", "w") as fh:
    json.dump(receipt, fh, indent=1)
# compact console summary
par_bad = [r for r in results if r.get("same_decision") is False or r.get("bytes_equal") is False
           or r.get("temp_left_98") or r.get("temp_left_99")]
print(json.dumps({"pins": [(p["carrier"], p["pin_ok"]) for p in pins],
                  "n_cells": len(results),
                  "parity_or_temp_violations": [r["cell"] for r in par_bad]}))
for r in results:
    if r["cell"].startswith(("cli.", "atk.")) or r.get("same_decision") is False or r.get("bytes_equal") is False:
        print(json.dumps(r))
