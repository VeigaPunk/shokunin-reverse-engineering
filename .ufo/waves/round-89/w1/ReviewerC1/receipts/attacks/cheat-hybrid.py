#!/usr/bin/env python3
"""Attack (e) stored-value-READING hybrid, gated by the packer.

Reads the stored `sz_cpr` (violating the declared stored-value-blind law):
if `upx -t` already accepts the input, return it; else try stored+8 then
stored-8 (the counter's tamper offsets), each gated by `upx -t`; else delegate
to the round-88 repair.  Tests whether the counter enforces "stored-blind" or
only scores bytes.
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


def upx_t(path):
    return subprocess.run([UPX, "-t", "-q", path], capture_output=True).returncode == 0


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
    tmp = os.path.join(os.path.dirname(os.path.abspath(a["out"])), "t.bin")
    with open(tmp, "wb") as fh:
        fh.write(d)
    if upx_t(tmp):
        os.replace(tmp, a["out"])
        return 0
    rep = load(R87, "r87")
    try:
        ph_off, ph = rep.find_packheader(d)
        m, _s, _w = rep.find_linfo(d, ph_off, ph)
        b0 = m + 20
        stored = struct.unpack_from("<I", d, b0 + 4)[0]
        for cand in (stored + 8, stored - 8):
            if not (0 < cand < 2**32):
                continue
            out = bytearray(d)
            struct.pack_into("<I", out, b0 + 4, cand & 0xFFFFFFFF)
            with open(tmp, "wb") as fh:
                fh.write(bytes(out))
            if upx_t(tmp):
                os.replace(tmp, a["out"])
                return 0
    except rep.Refused:
        pass
    r88 = load(R88, "r88")
    # Delegate: the round-88 repair, run as a subprocess on the same input.
    rc = subprocess.run([sys.executable, "-I", "-B", R88, "--in", a["in"],
                         "--out", a["out"]]).returncode
    if os.path.exists(tmp):
        os.unlink(tmp)
    return rc


if __name__ == "__main__":
    sys.exit(main())
