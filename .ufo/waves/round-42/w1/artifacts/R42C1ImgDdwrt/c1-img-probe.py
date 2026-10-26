#!/usr/bin/env python3
"""Oracle probe for a candidate carrier: superblock, reader matrix, magic-isolation.

Reads a published candidate image with the two non-sasquatch readers only
(unsquashfs -s / -lls, 7z l). No REA, no unblob, no sasquatch are invoked.

For each (image, offset):
  * parse the SquashFS v3 superblock from bytes
  * carve [offset, offset+bytes_used) into --work
  * unsquashfs -s / -lls and `7z l -slt` on the carve  (as published magic)
  * copy the carve with bytes 0..3 replaced by the standard v3 magic for that
    byte order (hsqs / sqsh) and repeat both readers: isolates "magic gate" from
    "block codec" as the cause of a reader failure.

Usage: c1-img-probe.py --work DIR image:offset [image:offset ...]
Writes JSON to stdout.
"""
import argparse
import hashlib
import json
import os
import shutil
import struct
import subprocess

UNBLOB_HANDLER = "/home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py"

MAGIC_VARIANT = {
    b"hsqs": ("v3/std-L", "LE", b"hsqs"),
    b"sqsh": ("v3/std-B", "BE", b"sqsh"),
    b"hsqt": ("v3/ddwrt-L", "LE", b"hsqs"),
    b"tqsh": ("v3/ddwrt-B", "BE", b"sqsh"),
    b"shsq": ("v3/broadcom-L", "LE", b"hsqs"),
    b"qshs": ("v3/broadcom-B", "BE", b"sqsh"),
    b"zlqs": ("v3/nonstandard-L", "LE", b"hsqs"),
    b"sqlz": ("v3/nonstandard-B", "BE", b"sqsh"),
}

V3_KEYS = ["inodes", "bytes_used_2", "uid_start_2", "guid_start_2", "inode_table_start_2",
           "directory_table_start_2", "s_major", "s_minor", "block_size_1", "block_log",
           "flags", "no_uids", "no_guids", "mkfs_time", "root_inode", "block_size",
           "fragments", "fragment_table_start_2", "bytes_used", "uid_start", "guid_start",
           "inode_table_start", "directory_table_start", "fragment_table_start",
           "lookup_table_start"]
V3_FMT = "6I4H3B I Q I I I Q Q Q Q Q Q Q"


def parse_v3(buf, off):
    b = buf[off:off + 119]
    magic = b[0:4]
    variant, order, std = MAGIC_VARIANT.get(magic, ("unknown", "?", b"hsqs"))
    vals = struct.unpack((">" if order == "BE" else "<") + V3_FMT, b[4:119])
    d = dict(zip(V3_KEYS, vals))
    d.update(magic_bytes=magic.decode("latin-1"), variant=variant, struct_endian=order,
             standard_magic_for_order=std.decode())
    return d


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def sevenzip_counts(out):
    files = dirs = links = other = 0
    mode = None
    rows = []
    for line in out.splitlines():
        if line.startswith("Path = "):
            if mode is not None:
                rows.append(mode)
            mode = None
        elif line.startswith("Mode = "):
            mode = line[7:].strip()
    if mode is not None:
        rows.append(mode)
    for m in rows:
        if m.startswith("d"):
            dirs += 1
        elif m.startswith("l"):
            links += 1
        elif m.startswith("-"):
            files += 1
        else:
            other += 1
    return dict(entries=len(rows), files=files, dirs=dirs, symlinks=links, other=other)


def reader_matrix(path):
    rc_s, so_s, se_s = run(["unsquashfs", "-s", path])
    rc_l, so_l, se_l = run(["unsquashfs", "-lls", path])
    rc_7, so_7, se_7 = run(["7z", "l", "-ba", "-slt", path])
    sqfs_lls = [l for l in so_l.splitlines() if l]
    return {
        "unsquashfs_s": {"rc": rc_s,
                         "lines": [l for l in (so_s + se_s).splitlines() if l][:6]},
        "unsquashfs_lls": {"rc": rc_l, "entry_lines": len(sqfs_lls),
                           "stderr": [l for l in se_l.splitlines() if l][:4],
                           "sample": sqfs_lls[:3]},
        "7z": {"rc": rc_7, "counts": sevenzip_counts(so_7),
               "stderr": [l for l in se_7.splitlines() if l][:3]},
    }


def probe(image, off, workdir):
    data = open(image, "rb").read()
    sb = parse_v3(data, off)
    used = sb["bytes_used"]
    rec = {"image": image, "image_bytes": len(data), "image_sha256": hashlib.sha256(data).hexdigest(),
           "superblock_offset": off, "superblock": sb}
    if used > len(data) - off:
        rec["error"] = "bytes_used exceeds image tail"
        return rec
    carve = os.path.join(workdir, os.path.basename(image) + f".{off}.sqfs")
    blob = data[off:off + used]
    open(carve, "wb").write(blob)
    rec["carve"] = carve
    rec["carve_bytes"] = used
    rec["carve_sha256"] = hashlib.sha256(blob).hexdigest()
    rec["as_published"] = reader_matrix(carve)

    patched = os.path.join(workdir, os.path.basename(image) + f".{off}.stdmagic.sqfs")
    pb = bytearray(blob)
    pb[0:4] = sb["standard_magic_for_order"].encode("latin-1")
    open(patched, "wb").write(pb)
    rec["std_magic_copy"] = {"path": patched, "magic": sb["standard_magic_for_order"],
                             "sha256": hashlib.sha256(pb).hexdigest(),
                             "readers": reader_matrix(patched)}
    return rec


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("targets", nargs="+")
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    out = []
    for t in a.targets:
        img, off = t.rsplit(":", 1)
        out.append(probe(img, int(off, 0), a.work))
    print(json.dumps(out, indent=1))
