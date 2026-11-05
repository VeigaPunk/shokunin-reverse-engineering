#!/usr/bin/env python3
"""Attack (b-full) exhaustive packer oracle, composed with the r87 anchor.

No chain geometry anywhere: the r87 anchor path is applied exactly as the
frozen repair composes it (magic class + intact passthrough), and the field
value itself is found by trying EVERY candidate in [1, sz_unc0], nearest to
the stored value first, accepting the first the pinned packer's `upx -t`
accepts.  This is the calibration experiment: if this meets the whole frozen
predicate (including the r88 and r87 regression arms), the counter certifies
the outcome, not the derivation law.
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
    # Declared composition: the r87 anchor path first, exactly like the frozen
    # repair; on refusal the derivation (here: the oracle) runs on the input.
    try:
        base, _info = rep.repair(d)
    except rep.Refused:
        base = d
    try:
        ph_off, ph = rep.find_packheader(base)
        m, _s, _w = rep.find_linfo(base, ph_off, ph)
    except rep.Refused as exc:
        sys.stderr.write(f"refused: {exc}\n")
        return 3
    b0 = m + 20
    sz_unc0, stored = struct.unpack_from("<II", base, b0)
    tmp = os.path.join(os.path.dirname(os.path.abspath(a["out"])), "t.bin")
    cands = sorted(range(1, sz_unc0 + 1), key=lambda c: abs(c - stored))
    for cand in cands:
        out = bytearray(base)
        struct.pack_into("<I", out, b0 + 4, cand)
        with open(tmp, "wb") as fh:
            fh.write(bytes(out))
        r = subprocess.run([UPX, "-t", "-q", tmp], capture_output=True)
        if r.returncode == 0:
            os.replace(tmp, a["out"])
            return 0
        os.unlink(tmp)
    sys.stderr.write("refused: no candidate in [1, sz_unc0] passes upx -t\n")
    return 3


if __name__ == "__main__":
    sys.exit(main())
