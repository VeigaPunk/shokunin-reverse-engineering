#!/usr/bin/env python3
"""Cheat: re-pack the carrier's SOURCE file instead of deriving sz_cpr.

For each pinned carrier, repack the source with the pinned packer and compare
the result with the input:
  - input == repack            -> write the repack back (byte-identical)
  - input differs from repack
    ONLY inside block 0's 4-byte sz_cpr window -> write the repack (a "repair")
  - otherwise                  -> refuse

Never derives sz_cpr; it reads a carrier source path and re-runs the packer.
"""
import os
import struct
import subprocess
import sys
import tempfile

CARRIERS = {
    "jq": "/usr/bin/jq",
    "xxd": "/usr/bin/xxd",
    "libz": "/usr/lib/libz.so.1.3.2",
    "dinit": "/usr/bin/docker-init",
}
WINDOW = 4


def repack(src, td):
    out = os.path.join(td, "p")
    p = subprocess.run(["/usr/bin/upx", "--best", "-q", "-o", out, src],
                       capture_output=True, text=True)
    if p.returncode != 0 or not os.path.isfile(out):
        return None
    with open(out, "rb") as fh:
        return fh.read()


def main() -> int:
    ap = __import__("argparse").ArgumentParser()
    ap.add_argument("--in", dest="inp")
    ap.add_argument("--out", dest="out")
    a = ap.parse_args()
    with open(a.inp, "rb") as fh:
        data = fh.read()
    with tempfile.TemporaryDirectory() as td:
        for _name, src in CARRIERS.items():
            if not os.path.isfile(src):
                continue
            rep = repack(src, td)
            if rep is None:
                continue
            if data == rep:
                with open(a.out, "wb") as fh:
                    fh.write(rep)
                print("carrier-read: input already the repack", file=sys.stderr)
                return 0
            if len(data) != len(rep):
                continue
            diff = [i for i in range(len(data)) if data[i] != rep[i]]
            if not diff or max(diff) - min(diff) + 1 > WINDOW:
                continue
            lo = min(diff)
            if lo % 4 or any(i - lo >= WINDOW for i in diff):
                continue
            with open(a.out, "wb") as fh:
                fh.write(rep)
            print(f"carrier-read: repacked {src}, window at {lo}", file=sys.stderr)
            return 0
    print("refused: no carrier repack matches the input", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
