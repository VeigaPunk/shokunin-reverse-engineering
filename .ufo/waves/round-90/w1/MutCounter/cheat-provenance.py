#!/usr/bin/env python3
"""cheat-provenance.py - MutCounter's declared cheat repair (round 90, seat probe).

Not a repair.  It never derives a `sz_cpr` value: it re-packs each *pinned
carrier path* with the pinned packer and, when one candidate reproduces the
input except inside a single 4-byte `sz_cpr` window of the first `b_info`
segment, it returns the pristine packed bytes verbatim.

Shape of the probe (why it is a cheat and not a repair):
  * it needs the carrier files on disk to exist and be readable -- which is
    exactly what the counter's `carrier_blind` sandbox takes away;
  * it refuses (rc != 0) an input that is not a UPX image (N1) and an input
    whose differing bytes are not one `sz_cpr` window (N2), so the three
    `N*` controls are satisfied by construction and the *only* arms that can
    reject it are the provenance controls under test;
  * it returns the intact packed bytes, so `field_only`, `identity`,
    `test_ok`, `unpack_pin` and `rea_recover` all pass.

`--leak` writes a sibling of the input inside the invocation box, so the box
listing is not exactly ["in"]/["in", "out"]: the isolation control's probe.
"""

import argparse
import hashlib
import importlib.util
import os
import struct
import subprocess
import sys
import tempfile

PINNED = ("/usr/bin/jq", "/usr/bin/xxd", "/usr/lib/libz.so.1.3.2",
          "/usr/bin/docker-init")
ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
R87 = os.path.join(ROOT, "tools/round-87/upx-magic-repair.py")
R88 = os.path.join(ROOT, "tools/round-88/upx-chain-repair.py")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_MODS = None


def mods():
    global _MODS
    if _MODS is None:
        _MODS = (load(R87, "r87"), load(R88, "r88"))
    return _MODS


def layout(packed, rep=None, r88=None):
    """First-segment blocks of an *intact* packed image (the candidate)."""
    rep, r88 = (rep, r88) if rep is not None else mods()
    ph_off, ph = rep.find_packheader(packed)
    best = []
    for m in r88.l_info_candidates(packed, ph_off, ph):
        b0 = m + 20
        sz_unc0, _ = struct.unpack_from("<II", packed, b0)
        if sz_unc0 == 0:
            continue
        method = packed[b0 + 8]
        q, blocks = b0, []
        while q + 12 <= ph_off:
            su, sc = struct.unpack_from("<II", packed, q)
            if su == 0 or sc == 0 or sc > su or q + 12 + sc > ph_off \
                    or packed[q + 8] not in (method, ph["method"]):
                break
            blocks.append({"block": q, "sz_unc": su, "sz_cpr": sc})
            q += 12 + sc
        if len(blocks) > len(best):
            best = blocks
    return best


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--in", dest="src", required=True)
    ap.add_argument("--out", dest="dst", required=True)
    ap.add_argument("--upx", default="/usr/bin/upx")
    ap.add_argument("--leak", action="store_true")
    ap.add_argument("--scribble", action="store_true")
    args = ap.parse_args(argv)
    with open(args.src, "rb") as fh:
        data = fh.read()
    if args.leak:
        with open(os.path.join(os.path.dirname(os.path.abspath(args.src)),
                               "leak"), "wb") as fh:
            fh.write(b"cheat: scratch copy left in the box\n")
    if b"UPX!" not in data:
        print("cheat-provenance: not a UPX image (refused)")
        return 2
    tmp = tempfile.mkdtemp(prefix="cheat-")
    for i, path in enumerate(PINNED):
        out = os.path.join(tmp, f"p{i}")
        r = subprocess.run([args.upx, "--best", "-q", "-o", out,
                           os.path.realpath(path)],
                           capture_output=True, text=True)
        if r.returncode != 0 or not os.path.isfile(out):
            continue
        with open(out, "rb") as fh:
            cand = fh.read()
        if len(cand) != len(data):
            continue
        if cand == data:
            with open(args.dst, "wb") as fh:      # idempotent on an intact image
                fh.write(cand)
            print(f"cheat-provenance: {path} reproduces the input verbatim")
            return 0
        diffs = [i for i in range(len(cand)) if cand[i] != data[i]]
        try:
            blocks = layout(cand)
        except Exception:
            continue
        lo = min(diffs)
        for b in blocks:
            w = b["block"] + 4
            if w <= lo and max(diffs) < w + 4:
                value = struct.unpack_from("<I", data, w)[0]
                if 0 <= value <= b["sz_unc"]:
                    payload = cand
                    if args.scribble:
                        payload = bytearray(cand)
                        payload[8] ^= 0x01          # measured free byte (see docstring)
                        payload = bytes(payload)
                    with open(args.dst, "wb") as fh:   # provenance, no derivation
                        fh.write(payload)
                    print(f"cheat-provenance: {path} block@{b['block']} "
                          f"sz_cpr {b['sz_cpr']} -> {value} by re-pack")
                    return 0
    print("cheat-provenance: no pinned carrier reproduces this image")
    return 3


if __name__ == "__main__":
    sys.exit(main())
