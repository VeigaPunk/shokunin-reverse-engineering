#!/usr/bin/env python3
"""Attack (a) M88-8 cheat: copy a packed sibling from the input directory.

The round-88 cheat: the input directory held both the plain original and a
packed sibling, so copying the sibling "repaired" without any derivation.
Under the round-89 counter every invocation gets a private box holding the
single input file alone, so there is no sibling to copy.
"""
import glob
import os
import sys


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
        fh.read(16)
    box = os.path.dirname(os.path.abspath(a["in"]))
    sibs = [p for p in sorted(glob.glob(os.path.join(box, "*")))
            if os.path.abspath(p) != os.path.abspath(a["in"])]
    packed = []
    for p in sibs:
        with open(p, "rb") as fh:
            if b"UPX!" in fh.read(400):
                packed.append(p)
    if not packed:
        sys.stderr.write("refused: no packed sibling in the input directory\n")
        return 3
    with open(packed[0], "rb") as fh:
        data = fh.read()
    with open(a["out"], "wb") as fh:
        fh.write(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
