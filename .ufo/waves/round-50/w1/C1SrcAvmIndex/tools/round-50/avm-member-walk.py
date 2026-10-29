#!/usr/bin/env python3
"""Draft (C1SrcAvmIndex, round 50 wave 1): walk the tar members of a public AVM
FRITZ!OS image over HTTP Range reads and report, for every `*filesystem.image`
member, the SquashFS superblock fields the round-50 C1 carrier clause reads.

Stdlib only (`python3 -I -B`). Reads 512-byte tar headers and 96-byte superblock
prefixes; never downloads a whole image. Output: JSON on stdout.

Superblock fields (SquashFS 4.0, the same offsets for both byte orders):
  magic at 0 (`hsqs` = little-endian, `sqsh` = big-endian),
  mkfs_time at 8, compression id at 20, major/minor at 28/30, bytes_used at 40.
The AVM marker is `mkfs_time == bytes_used`. A genuine round-50 carrier needs
endian LE, major 4, minor 0, compression 4 and the marker; the big-endian
rootfs of the same cable images also satisfies the marker, so the marker alone
does not select the LE carrier.

Usage:
  python3 -I -B avm-member-walk.py <path-under-download.avm.de/fritzbox/> [...]
"""
import datetime
import json
import struct
import sys
import urllib.request

BASE = "https://download.avm.de/fritzbox/"
UA = "kaidoku-round50-avm-member-walk/draft"


def rng(url, start, length):
    req = urllib.request.Request(
        url, headers={"Range": f"bytes={start}-{start + length - 1}", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status, r.read()


def octal(field):
    text = field.rstrip(b"\x00 ").decode() or "0"
    return int(text, 8)


def padded(size):
    return ((size + 511) // 512) * 512


def superblock(url, data_off, size, status):
    _, sb = rng(url, data_off, 96)
    magic = sb[0:4]
    if magic == b"hsqs":
        e = "<"
    elif magic == b"sqsh":
        e = ">"
    else:
        return {"magic": magic.decode("latin1"), "http": status}
    major, minor = struct.unpack_from(e + "HH", sb, 28)
    mkfs_time = struct.unpack_from(e + "I", sb, 8)[0]
    comp = struct.unpack_from(e + "H", sb, 20)[0]
    bytes_used = struct.unpack_from(e + "Q", sb, 40)[0]
    return {
        "magic": magic.decode("latin1"), "endian": "LE" if e == "<" else "BE",
        "major": major, "minor": minor, "compression_id": comp,
        "mkfs_time": mkfs_time, "bytes_used": bytes_used,
        "mkfs_eq_bytes_used": mkfs_time == bytes_used, "http": status,
    }


def walk(path):
    url = BASE + path
    off = 0
    pending = None
    members = []
    while len(members) < 400:
        status, hdr = rng(url, off, 512)
        if len(hdr) < 512 or hdr == b"\x00" * 512:
            break
        name = hdr[0:100].split(b"\x00")[0].decode("utf-8", "replace")
        size = octal(hdr[124:136])
        typ = chr(hdr[156]) if hdr[156] else "0"
        if typ == "L":  # GNU long name: the payload is the next member's name
            _, payload = rng(url, off + 512, padded(size))
            pending = payload[:size].split(b"\x00")[0].decode("utf-8", "replace")
            off += 512 + padded(size)
            continue
        full = pending or name
        pending = None
        rec = {"name": full, "typeflag": typ, "size": size,
               "data_offset": off + 512, "http": status}
        if full.endswith("filesystem.image") and size > 96:
            rec["superblock"] = superblock(url, off + 512, size, status)
        members.append(rec)
        off += 512 + padded(size)
    return members


def main(paths):
    out = {}
    for p in paths:
        utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        out[p] = {"utc": utc, "members": walk(p)}
    json.dump(out, sys.stdout, indent=1)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
