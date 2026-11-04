#!/usr/bin/env python3
"""Cheat repair for R88-C1, v2: no chain geometry in the sz_cpr derivation.

Composes the frozen round-87 anchor repair (as the claimed artifact does).
When it refuses, locate block0 by the `u_file_size` redundancy scan (the
PackHeader's declared size appears in l_info.p_filesize; this is a plain byte
scan, not a chain walk and not the claimed geometry), then brute-force the
4-byte sz_cpr word with `upx -t` + `upx -d` as the oracle: first value that
tests clean and unpacks is emitted.  No b_info plausibility test, no sentinel
walk, no u_len accounting.
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


def block0_by_redundancy(d, ph_off, ph):
    want = struct.pack("<I", ph["u_file_size"])
    p = d.find(want, 12)
    while p != -1 and p < ph_off:
        m = p - 12
        if m >= 4 and m + 20 <= ph_off and d[m + 6] == ph["version"] \
                and d[m + 7] == ph["format"]:
            return m + 20
        p = d.find(want, p + 1)
    return None


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
    except rep.Refused as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2
    b0 = block0_by_redundancy(d, ph_off, ph)
    if b0 is None:
        print("refused: no l_info by redundancy", file=sys.stderr)
        return 2
    sz_unc, _ = struct.unpack_from("<II", d, b0)
    cand = os.path.join(os.path.dirname(out), ".oracle.cand")
    unpacked = os.path.join(os.path.dirname(out), ".oracle.un")
    env = {"PATH": "/usr/bin:/bin", "LANG": "C",
           "HOME": os.path.dirname(out), "TMPDIR": os.path.dirname(out)}
    probes = 0
    for v in range(1, sz_unc + 1):
        dd = bytearray(d)
        struct.pack_into("<I", dd, b0 + 4, v)
        open(cand, "wb").write(bytes(dd))
        probes += 1
        t = subprocess.run([UPX, "-t", "-q", cand], capture_output=True, env=env)
        if t.returncode != 0:
            continue
        u = subprocess.run([UPX, "-d", "-q", "-f", "-o", unpacked, cand],
                           capture_output=True, env=env)
        if u.returncode != 0:
            continue
        open(out, "wb").write(bytes(dd))
        for p in (cand, unpacked):
            if os.path.exists(p):
                os.unlink(p)
        print(f"oracle: sz_cpr={v} after {probes} upx probes", file=sys.stderr)
        return 0
    for p in (cand, unpacked):
        if os.path.exists(p):
            os.unlink(p)
    print(f"refused: no sz_cpr passes upx -t/-d ({probes} probes)", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
