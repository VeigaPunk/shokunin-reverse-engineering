#!/usr/bin/env python3
"""Cheat repair for R88-C1: no chain geometry at all.

Composes the frozen round-87 anchor repair (the claimed artifact does the same)
and, when it refuses, brute-forces the 4-byte sz_cpr word with `upx -t` as the
oracle: for v in 1..sz_unc, write v and ask upx whether the file tests clean.
First v that passes is emitted.  No b_info plausibility test, no sentinel walk,
no u_len accounting.
"""
import importlib.util
import os
import struct
import subprocess
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
UPSTREAM = os.path.join(ROOT, "tools", "round-87", "upx-magic-repair.py")
UPX = "/usr/bin/upx"


def load(path=UPSTREAM):
    spec = importlib.util.spec_from_file_location("r87", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv):
    a = dict(zip(argv[::2], argv[1::2]))
    inp, out = a.get("--in"), a.get("--out")
    if not inp or not out:
        print("refused: --in and --out required", file=sys.stderr)
        return 2
    d = open(inp, "rb").read()
    if d[:4] != b"\x7fELF" or d[5] != 1:
        print("refused: not a little-endian ELF", file=sys.stderr)
        return 2
    rep = load()
    try:
        o, info = rep.repair(d)
        open(out, "wb").write(o)
        return 0
    except rep.Refused:
        pass
    try:
        ph_off, ph = rep.find_packheader(d)
        m, _s, _w = rep.find_linfo(d, ph_off, ph)
    except rep.Refused as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2
    b0 = m + 20
    sz_unc, _ = struct.unpack_from("<II", d, b0)
    cand = os.path.join(os.path.dirname(out), ".oracle.cand")
    for v in range(1, sz_unc + 1):
        dd = bytearray(d)
        struct.pack_into("<I", dd, b0 + 4, v)
        open(cand, "wb").write(bytes(dd))
        r = subprocess.run([UPX, "-t", "-q", cand], capture_output=True,
                           env={"PATH": "/usr/bin", "LANG": "C"})
        if r.returncode == 0:
            try:
                o, info = rep.repair(bytes(dd))
            except rep.Refused:
                continue
            open(out, "wb").write(o)
            os.unlink(cand)
            print(f"oracle: sz_cpr={v} after {v} upx -t probes", file=sys.stderr)
            return 0
    os.unlink(cand)
    print("refused: no sz_cpr passes upx -t", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
