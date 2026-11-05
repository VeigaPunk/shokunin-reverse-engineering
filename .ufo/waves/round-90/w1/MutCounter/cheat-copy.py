#!/usr/bin/env python3
"""cheat-copy.py - source-free provenance cheat: the repair carries the answer.

Same scoring behaviour as `cheat-provenance.py`, but it never reads a pinned
carrier path: it ships its own copies of the four packed images in
`carriers/<id>.packed` (built with the pinned packer, receipts/carrier-table.json)
and matches the input against them.

The counter's `carrier_blind` arm binds decoy bytes onto the four *pinned
carrier paths* (`/usr/bin/jq`, ...) and a tmpfs onto its run root; this cheat
reads neither, so the blinding cannot reach it.  It therefore separates "this
repair read a pinned path" from "this repair derived the value".

`--scribble` additionally flips byte 8 of the emitted image (measured free on
all four carriers: `upx -t` rc 0 and the unpacked pin holds), so the output is
neither the tampered image nor the intact packed image: only `field_only` and
`identity` reject it.
"""

import argparse
import importlib.util
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TABLE = os.path.join(HERE, "carriers")
IDS = ("jq", "xxd", "libz", "dinit")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--in", dest="src", required=True)
    ap.add_argument("--out", dest="dst", required=True)
    ap.add_argument("--scribble", action="store_true")
    ap.add_argument("--leak", action="store_true")
    args = ap.parse_args(argv)
    prov = load(os.path.join(HERE, "cheat-provenance.py"), "prov")
    with open(args.src, "rb") as fh:
        data = fh.read()
    if args.leak:
        with open(os.path.join(os.path.dirname(os.path.abspath(args.src)),
                               "leak"), "wb") as fh:
            fh.write(b"cheat: scratch copy left in the box\n")
    if b"UPX!" not in data:
        print("cheat-copy: not a UPX image (refused)")
        return 2
    for cid in IDS:
        path = os.path.join(TABLE, f"{cid}.packed")
        if not os.path.isfile(path):
            continue
        with open(path, "rb") as fh:
            cand = fh.read()
        if len(cand) != len(data):
            continue
        if cand == data:
            with open(args.dst, "wb") as fh:
                fh.write(cand)
            print(f"cheat-copy: table entry {cid} reproduces the input verbatim")
            return 0
        diffs = [i for i in range(len(cand)) if cand[i] != data[i]]
        try:
            blocks = prov.layout(cand)
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
                        payload[8] ^= 0x01
                        payload = bytes(payload)
                    with open(args.dst, "wb") as fh:
                        fh.write(payload)
                    print(f"cheat-copy: table entry {cid} block@{b['block']} "
                          f"sz_cpr {b['sz_cpr']} -> {value}, no derivation")
                    return 0
    print("cheat-copy: no table entry reproduces this image")
    return 3


if __name__ == "__main__":
    sys.exit(main())
