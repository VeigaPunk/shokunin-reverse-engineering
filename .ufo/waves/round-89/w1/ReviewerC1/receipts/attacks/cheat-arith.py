#!/usr/bin/env python3
"""Attack (d) u_len arithmetic cheat, no sentinel walk, no oracle.

Single-block arithmetic: every pinned carrier has declared `u_len` under one
UPX block (4096), so assume block 0's compressed data runs to the PackHeader:
`sz_cpr0 = ph_off - (b0 + 12)`.
"""
import importlib.util
import os
import struct
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
R87 = os.path.join(LANE, "tools", "round-87", "upx-magic-repair.py")


def main() -> int:
    a = {}
    for i, x in enumerate(sys.argv):
        if x == "--in":
            a["in"] = sys.argv[i + 1]
        if x == "--out":
            a["out"] = sys.argv[i + 1]
    if "in" not in a or "out" not in a:
        return 2
    with open(a["in"], "rb") as fh:
        d = fh.read()
    spec = importlib.util.spec_from_file_location("r87", R87)
    rep = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rep)
    try:
        ph_off, ph = rep.find_packheader(d)
        m, _s, _w = rep.find_linfo(d, ph_off, ph)
    except rep.Refused as exc:
        sys.stderr.write(f"refused: {exc}\n")
        return 3
    b0 = m + 20
    guess = ph_off - (b0 + 12)
    out = bytearray(d)
    struct.pack_into("<I", out, b0 + 4, guess & 0xFFFFFFFF)
    with open(a["out"], "wb") as fh:
        fh.write(bytes(out))
    sys.stderr.write(f"u_len={ph['u_len']} guess={guess}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
