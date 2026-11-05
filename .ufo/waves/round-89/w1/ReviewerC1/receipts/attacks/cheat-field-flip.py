#!/usr/bin/env python3
"""Attack: does `field_only` really bind the changed byte to the window?

Runs the frozen repair, then flips ONE extra byte in the packed file's
`e_ident[EI_PAD]` region (byte 9) — a byte the packer's `upx -t` and
`upx -d`-identity do not depend on.  If `field_only` were absent, the case
would still pass `test_ok` and `identity`; the arm is what catches it.
"""
import importlib.util
import os
import struct
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FROZEN = os.path.join(LANE, "tools", "round-89", "upx-field-value-repair.py")


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
    spec = importlib.util.spec_from_file_location("frozen", FROZEN)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    try:
        out, _info = mod.repair(d)
    except mod.Refused as exc:
        sys.stderr.write(f"refused: {exc}\n")
        return 3
    out = bytearray(out)
    out[9] ^= 0x01  # e_ident[EI_PAD]: outside block 0's sz_cpr window
    with open(a["out"], "wb") as fh:
        fh.write(bytes(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
