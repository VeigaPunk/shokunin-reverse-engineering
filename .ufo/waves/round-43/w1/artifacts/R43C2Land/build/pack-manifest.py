#!/usr/bin/env python3
"""pack-manifest — the landing manifest for the R43-C2 pack.

Seat R43C2Land, round 43 wave 1.  Stdlib only, TMPDIR-honouring.

Emits one line per copy: its lane-relative path, its byte count, its sha256,
the map entry that names it, the host path the SOURCES row names, and whether
the copy is a firmware image (it must not be: the claim forbids third-party
firmware among the copies).

Usage: pack-manifest.py --pack <dir> --lane <lane root> --out <tsv>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tarfile

# Magic numbers that would mark a third-party firmware image.
FIRMWARE_MAGICS = {
    b"hsqs": "squashfs", b"sqsh": "squashfs", b"shsq": "squashfs",
    b"\x45\x3d\xcd\x28": "cramfs", b"\x28\xcd\x3d\x45": "cramfs",
    b"\x85\x19\x01\x28": "jffs2", b"\x27\x05\x19\x56": "ubifs",
    b"\x31\x18\x10\x06": "ubi", b"\xd0\x0d\xfe\xed": "dtb",
    b"\x1f\x8b": "gzip", b"BZh": "bzip2", b"\xfd7zXZ": "xz",
    b"\x04\x22\x4d\x18": "lz4", b"\x28\xb5\x2f\xfd": "zstd",
    b"7z\xbc\xaf\x27\x1c": "7zip", b"\x89PNG": "png", b"\xff\xd8\xff": "jpeg",
    b"PK\x03\x04": "zip", b"ustar": "tar",
}


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def magic_of(path: str) -> str:
    with open(path, "rb") as fh:
        head = fh.read(64)
    for magic, name in FIRMWARE_MAGICS.items():
        if head.startswith(magic):
            return name
    return "-"


def inner_magics(path: str) -> list[str]:
    """For an archive, the magics of its members (first bytes of each)."""
    out = []
    try:
        with tarfile.open(path, "r:") as tar:
            for m in tar.getmembers():
                if not m.isreg():
                    continue
                fh = tar.extractfile(m)
                if fh is None:
                    continue
                head = fh.read(16)
                for magic, name in FIRMWARE_MAGICS.items():
                    if head.startswith(magic):
                        out.append("%s:%s" % (m.name, name))
                        break
    except tarfile.TarError:
        pass
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", required=True)
    ap.add_argument("--lane", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)

    pack = os.path.abspath(args.pack)
    with open(os.path.join(pack, "corpus", "evidence", "local-sources.json"),
              "r", encoding="utf-8") as fh:
        doc = json.load(fh)

    by_copy = {}
    for host, entry in doc["sources"].items():
        by_copy[entry["copy"]] = (host, entry)

    rows = ["copy\tbytes\tsha256\tkind\thost_path\touter_magic\tinner_magic\tin_lane"]
    bad = 0
    for copy_rel in sorted(by_copy):
        host, entry = by_copy[copy_rel]
        abs_path = os.path.join(pack, copy_rel)
        in_lane = os.path.isfile(os.path.join(os.path.abspath(args.lane), copy_rel))
        if not os.path.isfile(abs_path):
            # the copy is not part of this pack: it already lives in the lane
            # (row S126, the round-41 closure), so it is measured in place
            if not in_lane:
                rows.append("%s\tMISSING\t%s\t%s\t%s\t-\t-\tno" %
                            (copy_rel, entry["sha256"], entry.get("kind", "file"), host))
                rows.append("# MISSING %s" % copy_rel)
                bad += 1
                continue
            abs_path = os.path.join(os.path.abspath(args.lane), copy_rel)
        size = os.path.getsize(abs_path)
        digest = sha256_file(abs_path)
        outer = magic_of(abs_path)
        inner = ",".join(inner_magics(abs_path)) or "-"
        rows.append("%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s" %
                    (copy_rel, size, digest, entry.get("kind", "file"), host,
                     outer, inner, "yes" if in_lane else "no"))
        if digest != entry["sha256"]:
            rows.append("# MISMATCH %s" % copy_rel)
            bad += 1
        if size > 5 * 1024 * 1024:
            rows.append("# OVER-BOUND %s" % copy_rel)
            bad += 1

    out = "\n".join(rows) + "\n"
    out += "copies: %d, findings: %d\n" % (len(by_copy), bad)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(out)
    sys.stdout.write(out)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
