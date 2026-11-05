#!/usr/bin/env python3
"""CriticC1 variant probe (not frozen, not in the battery).
 V1 layout: t32.exe with the DOS stub grown by N bytes (e_lfanew += N, all
    PointerToRawData += N, SizeOfHeaders += N), packed with UPX 5.2.0 --best.
    Tests whether the PackHeader stays at UPX1.rawptr-64 (structural) or at 992.
 V2 decoy: the battery's t32 pack with the real magic zeroed and a checksum-valid
    PackHeader-looking record placed at 960 (adjacent to the real one at 992).
Reference for unpack equivalence is ALWAYS upx -d of the untampered pack of the
same input. Scores real candidate, f1 fixed-offset, f7 lazy anchor."""
import hashlib, os, struct, subprocess, sys

S = "/fast/scratch/hyaku/kaidoku-r98/CriticC1"
UPX = "/usr/bin/upx"
SRC = "/home/vgpnk/.local/share/kaidoku-pwnenv/lib/python3.11/site-packages/pip/_vendor/distlib/t32.exe"
W = os.path.join(S, "w", "variants")
os.makedirs(W, exist_ok=True)
CMDS = {"real": S + "/clone/tools/round-98/upx-pe-repair.py",
        "f1_fixed_offset": S + "/f1_fixed_offset.py",
        "f7_lazy_anchor": S + "/f7_lazy_anchor.py"}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def run(args):
    return subprocess.run(args, capture_output=True, text=True)


def unp(src, out):
    if os.path.exists(out):
        os.unlink(out)
    r = run([UPX, "-d", "-q", "-o", out, src])
    return sha(out) if r.returncode == 0 and os.path.exists(out) else None


def grow_stub(data, add):
    b = bytearray(data)
    pe = struct.unpack_from("<I", b, 0x3C)[0]
    opt = pe + 24
    soh = struct.unpack_from("<I", b, opt + 60)[0]
    n = struct.unpack_from("<H", b, pe + 6)[0]
    st = opt + struct.unpack_from("<H", b, pe + 20)[0]
    b[0x40:0x40] = b"\0" * add
    struct.pack_into("<I", b, 0x3C, pe + add)
    pe2, opt2, st2 = pe + add, opt + add, st + add
    struct.pack_into("<I", b, opt2 + 60, soh + add)
    for k in range(n):
        off = st2 + 40 * k
        raw = struct.unpack_from("<I", b, off + 20)[0]
        if raw:
            struct.pack_into("<I", b, off + 20, raw + add)
    return bytes(b)


def rawptr1(b):
    pe = struct.unpack_from("<I", b, 0x3C)[0]
    st = pe + 24 + struct.unpack_from("<H", b, pe + 20)[0]
    return struct.unpack_from("<I", b, st + 60)[0]


def score(tag, packed, ref):
    p = os.path.join(W, tag + ".packed")
    open(p, "wb").write(packed)
    occ, i = [], packed.find(b"UPX!")
    while i >= 0:
        occ.append(i)
        i = packed.find(b"UPX!", i + 1)
    print(tag, "| UPX!@", occ, "| UPX1 rawptr-64", rawptr1(packed) - 64, "| ref", ref is not None)
    for label, cmd in CMDS.items():
        out = os.path.join(W, "%s.%s.out" % (tag, label))
        if os.path.exists(out):
            os.unlink(out)
        rc = run([sys.executable, "-I", "-B", cmd, "--in", p, "--out", out]).returncode
        wrote = os.path.exists(out)
        tt = run([UPX, "-t", "-q", out]).returncode if wrote else None
        eq = bool(wrote and tt == 0 and ref is not None and unp(out, out + ".unp") == ref)
        print("   %-16s repair_rc=%s wrote=%s upx_t_rc=%s unpack_equiv=%s" % (label, rc, wrote, tt, eq))


for add in (0x400, 0x800, 0x1000):
    tag = "V1stub%x" % add
    vin = os.path.join(W, tag + ".exe")
    open(vin, "wb").write(grow_stub(open(SRC, "rb").read(), add))
    vpk = os.path.join(W, tag + ".upx")
    r = run([UPX, "--best", "-q", "-o", vpk, vin])
    if r.returncode != 0:
        print(tag, "pack rc", r.returncode, (r.stdout + r.stderr).strip()[-160:])
        continue
    pb = open(vpk, "rb").read()
    ref = unp(vpk, os.path.join(W, tag + ".ref"))
    tb = bytearray(pb)
    i = tb.find(b"UPX!")
    if i >= 0:
        tb[i:i + 4] = b"\0\0\0\0"
    print(tag, "packed size", len(pb), "untampered upx -t rc", run([UPX, "-t", "-q", vpk]).returncode)
    score(tag + "_magic", bytes(tb), ref)

# V2 decoy on the battery's t32 pack (magic zeroed; decoy record at 960)
base = open(S + "/w/base/t32.upx", "rb").read()
ref2 = unp(S + "/w/base/t32.upx", os.path.join(W, "t32base.ref"))
d = bytearray(base)
d[992:996] = b"\0\0\0\0"
rec = bytearray(32)
rec[4] = 13
rec[5] = 9
struct.pack_into("<I", rec, 16, 0x2000)
struct.pack_into("<I", rec, 20, 0x1000)
rec[31] = sum(rec[4:31]) % 251
d[960:992] = rec
score("V2decoy", bytes(d), ref2)
