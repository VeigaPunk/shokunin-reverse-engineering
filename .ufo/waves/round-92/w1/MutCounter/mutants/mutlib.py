"""Shared helpers for the MutCounter mutants (scratch only; never in the lane).

A mutant is a repair/refusal command run as `python3 -I -B <mutant> --in IN --out OUT`
by the frozen counters. `match()` identifies the carrier of an input by comparing it
to the pinned packed images in `pinned/`, which is the carrier-table oracle that the
mutants model. It never reads the frozen counters' own pristine bytes at runtime.
"""
import argparse
import json
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
CLASS = "T7-chain-stop-boundary"
with open(os.path.join(HERE, "pinned", "table.json"), encoding="utf-8") as _fh:
    TABLE = json.load(_fh)


def args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", required=True)
    ap.add_argument("--out", dest="dst", required=True)
    a = ap.parse_args()
    return a.src, a.dst


def read(path):
    with open(path, "rb") as fh:
        return fh.read()


def write(path, data):
    with open(path, "wb") as fh:
        fh.write(data)
    return 0


def refuse(name, why):
    """Typed refusal (rc 2, JSON last line with a `refused` key); no output file."""
    print(json.dumps({"tool": name, "class": CLASS, "refused": why}))
    return 2


def pinned(cid):
    with open(os.path.join(HERE, "pinned", cid + ".bin"), "rb") as fh:
        return fh.read()


def match(data):
    """Identify the carrier by pinned-image comparison.

    Returns None, or (cid, kind, delta, P) where kind is:
      intact - data == pinned packed image of cid;
      near   - differs from P only inside the last-block sz_cpr window, delta +/-7;
      far    - differs only inside that window, delta +/-40;
      other  - differs only inside that window, any other delta.
    """
    for cid, ent in TABLE.items():
        P = pinned(cid)
        if len(P) != len(data):
            continue
        diff = [i for i, (a, b) in enumerate(zip(data, P)) if a != b]
        if not diff:
            return cid, "intact", 0, P
        w = ent["window"]
        if all(w <= i < w + 4 for i in diff):
            delta = struct.unpack_from("<I", data, w)[0] - ent["pristine"]
            kind = "near" if abs(delta) == 7 else "far" if abs(delta) == 40 else "other"
            return cid, kind, delta, P
    return None


def window(cid):
    return TABLE[cid]["window"]
