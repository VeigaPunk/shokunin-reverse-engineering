#!/usr/bin/env python3
"""control-cheat-repack.py - declared red control for the round-90 counter.

The cheapest provenance cheat a scored repair can run: read the *pinned carrier
path* (the unpacked original), pack it again with the packer, and return the
result -- no derivation at all, because `upx --best` is deterministic.  It is
scored twice by the counter: unblinded it must reproduce the intact packed bytes
(the control is live), and inside the carrier-blind sandbox it must fail (the
control is killed).  QUALITY 168/170.

Not a repair.  Never scores a case the counter counts as recovered; the counter
requires `carrier_blind` true for `met`.
"""

import argparse
import os
import subprocess
import sys
import tempfile

PINNED = ("/usr/bin/jq", "/usr/bin/xxd", "/usr/lib/libz.so.1.3.2",
          "/usr/bin/docker-init")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--in", dest="src", required=True)
    ap.add_argument("--out", dest="dst", required=True)
    ap.add_argument("--upx", default="/usr/bin/upx")
    args = ap.parse_args(argv)
    want = os.path.getsize(args.src)
    tmp = tempfile.mkdtemp(prefix="cheat-")
    for i, path in enumerate(PINNED):
        out = os.path.join(tmp, f"p{i}")
        r = subprocess.run([args.upx, "--best", "-q", "-o", out, path],
                           capture_output=True, text=True)
        if r.returncode != 0 or not os.path.isfile(out):
            continue
        if os.path.getsize(out) == want:
            with open(out, "rb") as fh:
                data = fh.read()
            with open(args.dst, "wb") as fh:
                fh.write(data)
            print("cheat-repack: matched a pinned carrier")
            return 0
    print("cheat-repack: no pinned carrier reproduces this size")
    return 2


if __name__ == "__main__":
    sys.exit(main())
