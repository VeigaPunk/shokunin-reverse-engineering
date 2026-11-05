#!/usr/bin/env python3
"""Attack (b2) exhaustive packer oracle with the declared composition.

Composition identical in kind to the frozen repair: the r87 anchor path first,
the r88 l_info CANDIDATE locator for block 0 (no chain validation required).
The value itself is pure brute force: every candidate in [1, sz_unc0],
nearest the stored value first, accepted on the first `upx -t` pass.  No
sentinel walk, no u_len accounting, no chain geometry.
"""
import importlib.util
import os
import struct
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
R87 = os.path.join(LANE, "tools", "round-87", "upx-magic-repair.py")
R88 = os.path.join(LANE, "tools", "round-88", "upx-chain-repair.py")
UPX = "/usr/bin/upx"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


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
    rep = load(R87, "r87")
    r88 = load(R88, "r88")
    try:
        base, _info = rep.repair(d)  # anchor path: magic class + intact
    except rep.Refused:
        base = d
    try:
        ph_off, ph = rep.find_packheader(base)
    except rep.Refused as exc:
        sys.stderr.write(f"refused: {exc}\n")
        return 3
    tmp = os.path.join(os.path.dirname(os.path.abspath(a["out"])), "t.bin")
    for m in r88.l_info_candidates(base, ph_off, ph):
        b0 = m + 20
        if b0 + 12 > ph_off:
            continue
        sz_unc0, stored = struct.unpack_from("<II", base, b0)
        if sz_unc0 == 0:
            continue
        for cand in sorted(range(1, sz_unc0 + 1), key=lambda c: abs(c - stored)):
            out = bytearray(base)
            struct.pack_into("<I", out, b0 + 4, cand)
            with open(tmp, "wb") as fh:
                fh.write(bytes(out))
            r = subprocess.run([UPX, "-t", "-q", tmp], capture_output=True)
            if r.returncode == 0:
                os.replace(tmp, a["out"])
                return 0
            os.unlink(tmp)
    sys.stderr.write("refused: no candidate passes upx -t\n")
    return 3


if __name__ == "__main__":
    sys.exit(main())
