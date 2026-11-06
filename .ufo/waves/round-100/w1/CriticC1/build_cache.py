#!/usr/bin/env python3
"""build_cache.py - CriticC1 scratch tool: build the pristine-pack cache that
forgery crit-f1-cache.py consults.  Packs the 10 pinned carriers with the
battery's exact command, locates the PackHeader structurally, keys the cache
by sha256 of header field bytes [i+4, i+32) (magic-independent), and stores
the pristine bytes.  Scratch only; never committed to the lane.
"""
import hashlib
import json
import os
import struct
import subprocess

UPX = "/usr/bin/upx"
CACHE = "/fast/scratch/hyaku/kaidoku-r100/CriticC1/cache"
WORK = "/fast/scratch/hyaku/kaidoku-r100/CriticC1/cache-build"
DL = "/home/vgpnk/.local/share/kaidoku-pwnenv/lib/python3.11/site-packages/pip/_vendor/distlib"
OGL = "/usr/lib/python3.14/site-packages/OpenGL/DLLS"
CARRIERS = [
    ("t32", DL + "/t32.exe", "6b4195e640a85ac32eb6f9628822a622057df1e459df7c17a12f97aeabc9415b"),
    ("t64", DL + "/t64.exe", "81a618f21cb87db9076134e70388b6e9cb7c2106739011b6a51772d22cae06b7"),
    ("w32", DL + "/w32.exe", "47872cc77f8e18cf642f868f23340a468e537e64521d9a3a416c8b84384d064b"),
    ("w64", DL + "/w64.exe", "7a319ffaba23a017d7b1e18ba726ba6c54c53d6446db55f92af53c279894f8ad"),
    ("winhello", "/opt/ghidra/docs/GhidraClass/ExerciseFiles/WinhelloCPP/WinHelloCPP.exe",
     "7a98a934de5f578c3a547af873221b221d037bafa87ceee71dd4f089dd228202"),
    ("fastlist64", "/home/vgpnk/.local/share/fnm/node-versions/v22.20.0/installation/lib/"
     "node_modules/pnpm/dist/vendor/fastlist-0.3.0-x64.exe",
     "d1a71f9ac1728082c1b276392725c3e010b98714888579b99152e401abedbf11"),
    ("freeglut32dll", OGL + "/freeglut32.vc14.dll",
     "c9c00a4ea9b9fecdcae81f6facaf27e349714d56fe7640ce9c37ed38841a0b87"),
    ("gle64dll", OGL + "/gle64.vc9.dll",
     "b427510af633a6298481e738942f3268daedf44d6c01af74620579034bede9ce"),
    ("llio32dll", "/opt/ghidra/GPL/DMG/data/os/win_x86_32/llio_i386.dll",
     "e855478acf0d36f846befb48bfd239b7ef46e568e2408091591adec274ed0879"),
    ("sevenzip64dll", "/opt/ghidra/Ghidra/Features/FileFormats/data/sevenzipnativelibs/"
     "Windows-amd64/lib7-Zip-JBinding.dll",
     "c769642c8a489e8fc078b8387fb9865ac5c5482ce22301a40d00145fa1304b27"),
]


def sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def pe_secs(b):
    pe = struct.unpack_from("<I", b, 0x3C)[0]
    n = struct.unpack_from("<H", b, pe + 6)[0]
    opt = struct.unpack_from("<H", b, pe + 20)[0]
    st = pe + 24 + opt
    return [struct.unpack_from("<II", b, st + 40 * k + 16) for k in range(n)]  # (rsize, rptr)


def ph_ok(b, i):
    if i < 0 or i + 32 > len(b):
        return False
    h = b[i:i + 32]
    version, fmt = h[4], h[5]
    if fmt not in (9, 36) or not 10 <= version <= 14:
        return False
    if sum(h[4:31]) % 251 != h[31]:
        return False
    u_len, c_len = struct.unpack_from("<II", h, 16)
    return 0 < c_len < u_len and c_len <= len(b)


def find_ph(b):
    secs = pe_secs(b)
    starts = (secs[1][1] - 64, secs[2][1])
    found = set()
    for s in starts:
        for i in range(max(0, s), max(0, s) + 1024):
            if ph_ok(b, i):
                found.add(i)
    assert len(found) == 1, found
    return found.pop()


os.makedirs(CACHE, exist_ok=True)
os.makedirs(WORK, exist_ok=True)
rows = []
for name, srcp, pin in CARRIERS:
    assert sha(srcp) == pin, ("pin mismatch", name)
    packed = os.path.join(WORK, name + ".upx")
    r = subprocess.run([UPX, "--best", "-q", "-f", "-o", packed, srcp], capture_output=True)
    assert r.returncode == 0, (name, r.stderr[-300:])
    with open(packed, "rb") as fh:
        b = fh.read()
    i = find_ph(b)
    key = hashlib.sha256(b[i + 4:i + 32]).hexdigest()
    u_len, c_len = struct.unpack_from("<II", b, i + 16)
    with open(os.path.join(CACHE, key), "wb") as fh:
        fh.write(b)
    rows.append({"name": name, "key": key, "method": b[i + 6], "level": b[i + 7],
                 "u_adler": "%08x" % struct.unpack_from("<I", b, i + 8)[0],
                 "c_adler": "%08x" % struct.unpack_from("<I", b, i + 12)[0],
                 "u_len": u_len, "c_len": c_len, "size": len(b), "ph": i})
keys = [r["key"] for r in rows]
assert len(set(keys)) == len(keys), "key collision"
with open(os.path.join(WORK, "rows.json"), "w") as fh:
    json.dump(rows, fh, indent=1)
for r in rows:
    print("%-14s method=%d level=%d c_len=%d u_len=%d size=%d ph=%d key=%s"
          % (r["name"], r["method"], r["level"], r["c_len"], r["u_len"], r["size"], r["ph"], r["key"][:12]))
print("cache files:", len(os.listdir(CACHE)))
