#!/usr/bin/env python3
"""Attack (b) packer-as-oracle cheat.

Locates block 0 with the lane's r87 locator (loaded by path, exactly like the
frozen repair loads it), then brute-forces candidate `sz_cpr` values around
the stored one, accepting the first candidate the pinned packer's `upx -t`
accepts.  No chain geometry, no sentinel walk, no u_len accounting.
"""
import importlib.util
import os
import struct
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
R87 = os.path.join(LANE, "tools", "round-87", "upx-magic-repair.py")
UPX = "/usr/bin/upx"


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
    sz_unc, stored = struct.unpack_from("<II", d, b0)
    tmp = os.path.join(os.path.dirname(os.path.abspath(a["out"])), "t.bin")
    cands = [stored] + [stored + k for k in range(1, 33)] \
        + [stored - k for k in range(1, 33)]
    for cand in cands:
        if not (0 < cand <= sz_unc):
            continue
        out = bytearray(d)
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
