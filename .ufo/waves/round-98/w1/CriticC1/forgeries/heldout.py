#!/usr/bin/env python3
"""CriticC1 held-out probe: carriers NOT in the frozen battery.
Packs each held-out PE with UPX 5.2.0 --best, tampers magic/names/both, and scores
the real candidate and forgeries (f1 fixed-offset with refuse guard, f7 lazy anchor,
f2 size cache with an empty cache) on unpack-equivalence against the reference.
Also reports whether the held-out pack's UPX! offsets are exactly one, and the
UPX1 rawdataptr-64 anchor."""
import hashlib, importlib.util, json, os, struct, subprocess, sys

S = "/fast/scratch/hyaku/kaidoku-r98/CriticC1"
UPX = "/usr/bin/upx"
HELD = [
    ("setup_cli32", "/home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages/setuptools/cli-32.exe"),
    ("setup_cli64", "/home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages/setuptools/cli-64.exe"),
    ("setup_gui32", "/home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages/setuptools/gui-32.exe"),
    ("setup_gui64", "/home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages/setuptools/gui-64.exe"),
    ("setup_cli", "/home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages/setuptools/cli.exe"),
    ("fastlist86", "/home/vgpnk/.local/share/fnm/node-versions/v22.20.0/installation/lib/node_modules/pnpm/dist/vendor/fastlist-0.3.0-x86.exe"),
]
spec = importlib.util.spec_from_file_location("bat", S + "/clone/tools/round-98/pe-upx-tamper-battery.py")
bat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bat)
W = os.path.join(S, "w", "heldout")
os.makedirs(W, exist_ok=True)
CMDS = {
    "real": S + "/clone/tools/round-98/upx-pe-repair.py",
    "f1_fixed_offset": S + "/f1_fixed_offset.py",
    "f7_lazy_anchor": S + "/f7_lazy_anchor.py",
    "f3_names_only": S + "/f3_names_only.py",
    "f4_magic_only": S + "/f4_magic_only.py",
}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def run(args):
    return subprocess.run(args, capture_output=True, text=True).returncode


def unp(src, out):
    if os.path.exists(out):
        os.unlink(out)
    return sha(out) if run([UPX, "-d", "-q", "-o", out, src]) == 0 and os.path.exists(out) else None


res = []
for name, src in HELD:
    orig = os.path.join(W, name + ".exe")
    open(orig, "wb").write(open(src, "rb").read())
    packed = os.path.join(W, name + ".upx")
    if run([UPX, "--best", "-q", "-o", packed, orig]) != 0:
        res.append({"carrier": name, "error": "pack failed"})
        continue
    pb = open(packed, "rb").read()
    ref = unp(packed, os.path.join(W, name + ".ref"))
    occ = []
    i = pb.find(b"UPX!")
    while i >= 0:
        occ.append(i)
        i = pb.find(b"UPX!", i + 1)
    pe = struct.unpack_from("<I", pb, 0x3C)[0]
    st = pe + 24 + struct.unpack_from("<H", pb, pe + 20)[0]
    rawptr1 = struct.unpack_from("<I", pb, st + 40 + 20)[0]
    entry = {"carrier": name, "size": len(pb), "upx_bang": occ, "rawptr1_minus64": rawptr1 - 64,
             "ref_ok": ref is not None, "cells": {}}
    for kind in bat.TAMPERS:
        tp = os.path.join(W, "%s.%s.tam" % (name, kind))
        open(tp, "wb").write(bat.tamper(pb, kind))
        eff = run([UPX, "-t", "-q", tp]) != 0
        entry["cells"][kind] = {"effective": eff}
        for label, cmd in CMDS.items():
            out = os.path.join(W, "%s.%s.%s" % (name, kind, label))
            if os.path.exists(out):
                os.unlink(out)
            rc = run([sys.executable, "-I", "-B", cmd, "--in", tp, "--out", out])
            ok = False
            if rc == 0 and os.path.exists(out) and run([UPX, "-t", "-q", out]) == 0:
                ok = unp(out, out + ".unp") == ref
            entry["cells"][kind][label] = {"rc": rc, "recovered": ok}
    # refused arm on the unpacked original
    for label, cmd in CMDS.items():
        out = os.path.join(W, "%s.refuse.%s" % (name, label))
        if os.path.exists(out):
            os.unlink(out)
        rc = run([sys.executable, "-I", "-B", cmd, "--in", orig, "--out", out])
        entry.setdefault("refuse", {})[label] = {"rc": rc, "wrote": os.path.exists(out)}
    res.append(entry)
json.dump(res, open(S + "/out/heldout.json", "w"), indent=1)
for e in res:
    if "error" in e:
        print(e)
        continue
    print(e["carrier"], "size", e["size"], "UPX!@", e["upx_bang"], "rawptr1-64", e["rawptr1_minus64"], "ref_ok", e["ref_ok"])
    for kind in bat.TAMPERS:
        c = e["cells"][kind]
        print("  ", kind, "eff", c["effective"], {k: c[k]["recovered"] for k in CMDS})
    print("   refuse", {k: (v["rc"], v["wrote"]) for k, v in e["refuse"].items()})
