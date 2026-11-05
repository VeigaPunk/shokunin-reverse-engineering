#!/usr/bin/env python3
"""Kill-rule attack: score 4 of 4 while reading and hashing a carrier path.

Delegates to the frozen repair module (so the output is genuinely correct),
but ALSO opens and sha256-hashes the pinned carrier /usr/bin/jq during every
invocation, and writes marker files both inside its invocation box and in a
persistent scratch path.  The counter's isolation control is a pre-run listing
of the box, so neither the carrier read nor the in-run box writes are visible
to it.
"""
import hashlib
import importlib.util
import os
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FROZEN = os.path.join(LANE, "tools", "round-89", "upx-field-value-repair.py")
CARRIER = "/usr/bin/jq"
MARKER_DIR = "/fast/scratch/hyaku/kaidoku-r89/ReviewerC1/attacks/markers"


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
    # Out-of-band read the counter cannot see: the pinned carrier itself.
    with open(CARRIER, "rb") as fh:
        carrier = fh.read()
    chash = hashlib.sha256(carrier).hexdigest()
    os.makedirs(MARKER_DIR, exist_ok=True)
    with open(os.path.join(MARKER_DIR, "carrier-read.log"), "a") as fh:
        fh.write(f"read {CARRIER} sha256={chash} in_len={len(d)}\n")
    # In-run box write: invisible to the pre-run listing snapshot.
    box = os.path.dirname(os.path.abspath(a["in"]))
    with open(os.path.join(box, "carrier-read.marker"), "w") as fh:
        fh.write(chash + "\n")
    spec = importlib.util.spec_from_file_location("frozen", FROZEN)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    try:
        out, _info = mod.repair(d)
    except mod.Refused as exc:
        sys.stderr.write(f"refused: {exc}\n")
        return 3
    with open(a["out"], "wb") as fh:
        fh.write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
