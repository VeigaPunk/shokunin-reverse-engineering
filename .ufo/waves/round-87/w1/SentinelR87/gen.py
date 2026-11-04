#!/usr/bin/env python3
"""SentinelR87 hostile-input generator for upx-magic-repair.py (round 87)."""
import os, random, struct, sys

MAGIC = b"UPX!"
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
UFS = 0x00ABCDEF  # u_file_size used by crafted PackHeaders


def ph(ufs=UFS, version=14, fmt=22):
    h = bytearray(MAGIC + bytes([version, fmt, 14, 10]) +
                  struct.pack("<IIIII", 1, 2, 64, 64, ufs) + bytes(4))
    h[31] = sum(h[4:31]) % 251
    return bytes(h)


def elf():
    return b"\x7fELF\x02\x01\x01" + b"\0" * 57


def linfo(ufs=UFS):
    # l_checksum, l_magic, l_lsize, l_version, l_format ; p_progid, p_filesize, p_blocksize
    return struct.pack("<I", 0) + MAGIC + struct.pack("<HBB", 3000, 14, 22) + \
        struct.pack("<III", 0, ufs, ufs)


def binfo(unc, cpr, meth=14):
    return struct.pack("<IIBBBB", unc, cpr, meth, 0, 0, 0)


def w(name, data):
    with open(os.path.join(OUT, name), "wb") as fh:
        fh.write(data)


w("A-empty", b"")
w("B-4bytes", b"\x7fELF")
w("C-zeros-64M", b"\0" * (64 << 20))
w("D-elf-random-1M", elf() + random.Random(87).randbytes(1 << 20))
w("D2-elf-zeros-64M", elf() + b"\0" * ((64 << 20) - 64))
# E: chains whose b_info points at itself (sz_cpr 0) or past the end (0xffffffff)
w("E1-selfchain-cpr0", elf() + linfo() + binfo(100, 0) + b"\0" * 12 + ph() + b"\0" * 4)
w("E2-chain-cprmax", elf() + linfo() + binfo(0xFFFFFFFF, 0xFFFFFFFF) + b"\0" * 12 + ph() + b"\0" * 4)
# E3: a chain that loops by reusing its own header bytes as next block (impossible: q strictly grows)
w("E3-selfchain-cpr1", elf() + linfo() + (binfo(2, 1) + b"\x02") * 4 + b"\0" * 12 + ph() + b"\0" * 4)
# F: PackHeader u_file_size occurs K times, each a matching l_info followed by one
# plausible b_info and a breaker, no sentinel anywhere -> every candidate re-runs the
# resume scan to ph_off: O(K * n).
for k in (250, 500, 1000, 2000):
    rec = linfo() + binfo(2, 1) + b"\x01" + b"\xff" * 8
    w(f"F-ufs-x{k}", elf() + rec * k + ph() + b"\0" * 4)
# G: one l_info, first walk stops after 1 block (breaker), then M chained 13-byte
# blocks with no sentinel -> resume scan walks each suffix: O(M^2).
for m in (1000, 2000, 4000, 8000):
    body = linfo() + binfo(2, 1) + b"\x01" + b"\xff" * 8 + (binfo(2, 1) + b"\x01") * m + b"\xff" * 12
    w(f"G-quadchain-m{m}", elf() + body + ph() + b"\0" * 4)
# H: G + F combined at small scale (K candidates each re-walking M^2)
body = (linfo() + binfo(2, 1) + b"\x01" + b"\xff" * 8) * 20 + (binfo(2, 1) + b"\x01") * 2000 + b"\xff" * 12
w("H-combined-k20-m2000", elf() + body + ph() + b"\0" * 4)
# I: crafted non-UPX ELF that satisfies all three anchors (false repair, tamper zero)
good = elf() + linfo() + binfo(100, 8) + b"A" * 8 + struct.pack("<II", 0, 0) + b"\0" * 4 + ph() + b"\0" * 4
w("I-crafted-nonupx-tampered", good.replace(MAGIC, b"\0\0\0\0"))
# J: valid PackHeader, u_file_size never occurs -> refuse fast on large file
w("J-ph-only-32M", elf() + b"\x11" * (32 << 20) + ph() + b"\0" * 4)
print("ok", sorted(os.listdir(OUT)))
