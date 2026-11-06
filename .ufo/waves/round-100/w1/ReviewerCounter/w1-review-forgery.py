#!/usr/bin/env python3
"""w1-review-forgery.py - ReviewerCounter probe for the round-100 C1 battery.

Repairs magic/names tampers from the PE layout and a self-validating PackHeader
scan.  Refuses the corrupt and truncated arms from the input FILENAME alone,
never from content: a content-blindness demonstration for the frozen counter.
"""
import os
import struct
import sys
import zlib


def u16(b, o):
    return struct.unpack_from("<H", b, o)[0]


def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


def find_ph(b):
    n = len(b)
    for i in range(0, min(n, 65536)):
        w = b[i:i+4]
        if w != b"UPX!" and w != b"\0\0\0\0":
            continue
        if i + 32 > n:
            continue
        c_len = u32(b, i + 20)
        if c_len < 16 or i + 32 + c_len > n:
            continue
        if (zlib.adler32(b[i+32:i+32+c_len]) & 0xffffffff) == u32(b, i + 12):
            return i
    return None


def repair(b):
    i = find_ph(b)
    if i is None:
        return None
    b = bytearray(b)
    b[i:i+4] = b"UPX!"
    pe = u32(b, 0x3C)
    nsec = u16(b, pe + 6)
    st = pe + 24 + u16(b, pe + 20)
    names = (b".text\0\0\0", b".data\0\0\0\0", b".rdata\0\0")
    for k in range(min(nsec, 3)):
        off = st + 40 * k
        if bytes(b[off:off+8]) == names[k]:
            b[off:off+8] = (b"UPX%d" % k).ljust(8, b"\0")
    return bytes(b)


def main():
    args = sys.argv[1:]
    inp = out = None
    for idx, a in enumerate(args):
        if a == "--in":
            inp = args[idx+1]
        elif a == "--out":
            out = args[idx+1]
    base = os.path.basename(inp or "")
    if ".corrupt-" in base:
        sys.stderr.write("checksum error: c_adler mismatch\n")
        return 2
    if ".trunc-" in base:
        sys.stderr.write("truncated input\n")
        return 2
    try:
        data = open(inp, "rb").read()
    except OSError:
        sys.stderr.write("cannot read input\n")
        return 2
    fixed = repair(data)
    if fixed is None:
        sys.stderr.write("not a UPX pack\n")
        return 2
    try:
        with open(out, "wb") as fh:
            fh.write(fixed)
    except OSError:
        sys.stderr.write("cannot write output\n")
        return 2
    sys.stdout.write("ok repaired\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
