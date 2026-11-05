#!/usr/bin/env python3
"""mkvariants.py - ExecGeomIndep: build the four sz_cpr inputs of one packed file.

Uses derive-szcpr.py's own locator (locate()) on the INTACT packed file to
find block 0, then writes:
  intact   - byte-identical copy
  zero     - sz_cpr := 0
  minus8   - sz_cpr := true - 8
  fff0     - sz_cpr := 0xFFFFFFF0
Usage: mkvariants.py PACKED OUTDIR
"""
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import derive_szcpr as ds  # noqa: E402


def main(argv):
    packed, outdir = argv[1], argv[2]
    with open(packed, "rb") as fh:
        d = fh.read()
    loc = ds.locate(d)
    b0, true_cpr = loc["block0"], loc["stored_sz_cpr"]
    os.makedirs(outdir, exist_ok=True)
    made = {}
    for name, value in (("intact", None), ("zero", 0),
                        ("minus8", true_cpr - 8), ("fff0", 0xFFFFFFF0)):
        data = d if value is None else d[:b0 + 4] + struct.pack("<I", value) + d[b0 + 8:]
        p = os.path.join(outdir, name)
        with open(p, "wb") as fh:
            fh.write(data)
        made[name] = {"path": p, "sz_cpr_written": value if value is not None
                      else true_cpr}
    print(json.dumps({"packed": packed, "block0": b0, "true_sz_cpr": true_cpr,
                      "variants": made}, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
