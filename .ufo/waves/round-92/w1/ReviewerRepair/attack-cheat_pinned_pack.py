#!/usr/bin/env python3
"""cheat_pinned_pack.py - ReviewerRepair counterfeit for R92-C1 (ATTACK q1).

Writes the carrier's pristine packed bytes (rebuilt by packing the known
carrier with the pinned /usr/bin/upx --best in a scratch cache) when the tamper
delta is inside the declared +/-16 window, and refuses otherwise. It never
consults the packer's verdict (`upx -t`) to decide the cell: the decision is
carrier identification + a 4-byte delta comparison.

Scripted per the seat task as "the cheapest counterfeit that writes the
carrier's pinned packed bytes for each of the five carriers and refuses
otherwise". Cached packs live under $TMPDIR/cheatcache (scratch).
"""
import json
import os
import shutil
import subprocess
import sys
import hashlib
import tempfile

CARRIERS = [
    ("jq", "/usr/bin/jq"),
    ("xxd", "/usr/bin/xxd"),
    ("libz", "/usr/lib/libz.so.1.3.2"),
    ("dinit", "/usr/bin/docker-init"),
    ("xz", "/usr/bin/xz"),
]
WINDOW = 16


def clean_env():
    return {"PATH": os.environ.get("PATH") or "/usr/bin", "LANG": "C",
            "HOME": os.environ.get("TMPDIR", "/tmp"),
            "TMPDIR": os.environ.get("TMPDIR", "/tmp")}


def cache_dir():
    d = os.path.join(os.environ.get("TMPDIR", "/tmp"), "cheatcache", "packs")
    os.makedirs(d, exist_ok=True)
    return d


def pack_carrier(cid, src):
    """Pristine packed bytes for a carrier: deterministic fresh pack, cached."""
    cache = os.path.join(cache_dir(), cid)
    if os.path.isfile(cache):
        with open(cache, "rb") as fh:
            return fh.read()
    box = tempfile.mkdtemp(prefix="cheat-", dir=cache_dir())
    inp, outp = os.path.join(box, "in"), os.path.join(box, "packed")
    shutil.copyfile(src, inp)
    os.chmod(inp, 0o755)
    p = subprocess.run(["/usr/bin/upx", "--best", "-q", "-o", outp, inp],
                       capture_output=True, text=True, timeout=600,
                       env=clean_env())
    if p.returncode != 0 or not os.path.isfile(outp):
        raise RuntimeError(f"pack {cid} failed rc={p.returncode}: {p.stderr[-200:]}")
    with open(outp, "rb") as fh:
        data = fh.read()
    os.replace(outp, cache)
    shutil.rmtree(box, ignore_errors=True)
    return data


def reject(reason):
    print(json.dumps({"tool": "cheat_pinned_pack", "refused": reason}))
    return 2


def main():
    import struct
    argv = sys.argv[1:]
    src = argv[argv.index("--in") + 1]
    dst = argv[argv.index("--out") + 1]
    with open(src, "rb") as fh:
        t = fh.read()
    for cid, csrc in CARRIERS:
        pristine = pack_carrier(cid, csrc)
        if len(t) != len(pristine):
            continue
        if t == pristine:
            with open(dst, "wb") as fh:
                fh.write(t)
            print(json.dumps({"tool": "cheat_pinned_pack", "class": "intact"}))
            return 0
        diffs = [i for i, (a, b) in enumerate(zip(pristine, t)) if a != b]
        if not diffs or diffs[-1] - diffs[0] >= 4:
            continue
        w = diffs[0]
        try:
            stored, cur = struct.unpack_from("<II", pristine, w)[:0] or \
                (int.from_bytes(pristine[w:w + 4], "little"),
                 int.from_bytes(t[w:w + 4], "little"))
        except IndexError:
            continue
        if 0 < cur and abs(cur - stored) <= WINDOW and cur != stored:
            with open(dst, "wb") as fh:
                fh.write(pristine)
            print(json.dumps({"tool": "cheat_pinned_pack",
                              "class": "repaired", "carrier": cid,
                              "stored": stored, "value": cur}))
            return 0
        # delta outside the declared window -> typed refusal (rx 2, no output)
    return reject("no carrier matches (not one of the five, or delta out of window)")


if __name__ == "__main__":
    sys.exit(main())
