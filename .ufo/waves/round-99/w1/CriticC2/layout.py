#!/usr/bin/env python3
"""Measure carrier layouts (scratch analysis for CriticC2). Reads frozen battery module read-only."""
import importlib.util
import json
import os
import shutil
import struct
import subprocess
import sys

S = "/fast/scratch/hyaku/kaidoku-r99/CriticC2"
CLONE = S + "/clone"
WORK = S + "/work"
os.makedirs(WORK, exist_ok=True)
spec = importlib.util.spec_from_file_location("battery", CLONE + "/tools/round-99/pe-upx-trunc-battery.py")
bat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bat)


def info(b):
    pe = struct.unpack_from("<I", b, 0x3C)[0]
    n = struct.unpack_from("<H", b, pe + 6)[0]
    opt = struct.unpack_from("<H", b, pe + 20)[0]
    falign = struct.unpack_from("<I", b, pe + 24 + 36)[0]
    st = pe + 24 + opt
    secs = []
    for k in range(n):
        o = st + 40 * k
        name = bytes(b[o:o + 8]).rstrip(b"\0").decode("latin1")
        vsize, vaddr, rsize, rptr = struct.unpack_from("<IIII", b, o + 8)
        secs.append((name, rptr, rsize, vaddr, vsize))
    return falign, secs


def align_up(v, a):
    return (v + a - 1) // a * a


rows = []
for name, src, pin in bat.CARRIERS:
    if not os.path.exists(src) or bat.sha(src) != pin:
        rows.append({"name": name, "error": "pin/exists"})
        continue
    orig = os.path.join(WORK, name + ".orig")
    shutil.copyfile(src, orig)
    packed = os.path.join(WORK, name + ".upx")
    p = subprocess.run(["/usr/bin/upx", "--best", "-q", "-f", "-o", packed, orig], capture_output=True, text=True)
    if p.returncode != 0:
        rows.append({"name": name, "error": "pack rc %d" % p.returncode})
        continue
    b = open(packed, "rb").read()
    falign, secs = info(b)
    last_name, lrptr, lrsize, _, _ = secs[-1]
    end_raw = lrptr + lrsize
    end = align_up(end_raw, falign)
    upxpos = b.find(b"UPX!")
    rptr1, rsize1 = secs[1][1], secs[1][2]
    rows.append({
        "name": name, "len": len(b), "falign": falign, "sections": [(s[0], s[1], s[2]) for s in secs],
        "last_raw_end": end_raw, "aligned_end": end, "last_raw_end_aligned": end_raw == end,
        "len_mod_falign": len(b) % falign, "len_eq_aligned_end": len(b) == end,
        "upx_pos": upxpos, "end_minus_upxpos": end - upxpos,
        "upx1_mid": rptr1 + rsize1 // 2, "cut_end_m1": end - 1,
        "upx1_sec_start": rptr1, "upx1_sec_end": rptr1 + rsize1,
        "mid_mod_falign": (rptr1 + rsize1 // 2) % falign,
        "decoy_applicable": bat.decoy(b) is not None,
        "sha": bat.sha(packed),
    })
    print(name, "len", len(b), "falign", falign, "lastend", end_raw, "aligned", end, "upxpos", upxpos, flush=True)

json.dump(rows, open(S + "/layout.json", "w"), indent=1)
print(json.dumps(rows, indent=1))
