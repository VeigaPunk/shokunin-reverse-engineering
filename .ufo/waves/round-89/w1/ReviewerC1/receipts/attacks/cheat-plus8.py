#!/usr/bin/env python3
"""Attack (c) blind arithmetic cheat: write `stored + 8`.

The counter's class tamper is `stored - 8` (or `stored + 8` when the stored
value is <= 8), so on every carrier whose true first-block `sz_cpr` exceeds 8
the blind `stored + 8` IS the true value.  No derivation, no oracle.
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
    out = bytearray(d)
    stored = struct.unpack_from("<I", d, b0 + 4)[0]
    struct.pack_into("<I", out, b0 + 4, (stored + 8) & 0xFFFFFFFF)
    with open(a["out"], "wb") as fh:
        fh.write(bytes(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
