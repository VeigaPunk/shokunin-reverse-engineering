#!/usr/bin/env python3
"""C1Frontier (round-50 w1): verify two members of the L1's 'v3 sqsh comp 0'
AVM-hosted group by HTTP Range superblock reads only (<=1 KiB per request,
no extraction). Prints a receipt per request: url, Range, status,
Content-Range, length, sha256, UTC. Parses each fetched superblock under the
v4 field map (both endiannesses) plus, once grounded, a v3 map supplied in
V3_MAP below. No response body is written to disk."""
import hashlib
import json
import struct
import sys
import time
import urllib.error
import urllib.request

TARGETS = [
    ("fritzbox-3272",
     "https://download.avm.de/fritzbox/fritzbox-3272/deutschland/fritz.os/FRITZ.Box_3272.126.06.89.image"),
    ("fritzbox-7412",
     "https://download.avm.de/fritzbox/fritzbox-7412/deutschland/fritz.os/FRITZ.Box_7412.137.06.88.image"),
]

V4_FMT = "IIIIIHHHHHHQQQQQQQQ"
V4_FIELDS = ("magic", "inodes", "mkfs_time", "block_size", "fragments",
             "compression", "block_log", "flags", "no_ids", "s_major",
             "s_minor", "root_inode", "bytes_used", "id_table_start",
             "xattr_id_table_start", "inode_table_start",
             "directory_table_start", "fragment_table_start",
             "export_table_start")

# Grounded in plougher/squashfs-tools 4.6.1 squashfs_compat.h,
# struct squashfs_super_block_3 (packed; bit offsets in SQUASHFS_SWAP_SUPER_BLOCK_3
# divided by 8). v3 has NO compression field; offset 20 is inode_table_start_2.
# Parsed fields end at directory_table_start (byte 95) because the fetch is 96 B.
V3_FIELDS = (
    ("s_magic", 0, "I"), ("inodes", 4, "I"), ("bytes_used_2", 8, "I"),
    ("uid_start_2", 12, "I"), ("guid_start_2", 16, "I"),
    ("inode_table_start_2", 20, "I"),
    ("directory_table_start_2", 24, "I"), ("s_major", 28, "H"),
    ("s_minor", 30, "H"), ("block_size_1", 32, "H"), ("block_log", 34, "H"),
    ("flags", 36, "B"), ("no_uids", 37, "B"), ("no_guids", 38, "B"),
    ("mkfs_time", 39, "i"), ("root_inode", 43, "Q"), ("block_size", 51, "I"),
    ("fragments", 55, "I"), ("fragment_table_start_2", 59, "I"),
    ("bytes_used", 63, "Q"), ("uid_start", 71, "Q"), ("guid_start", 79, "Q"),
    ("inode_table_start", 87, "Q"), ("directory_table_start", 95, "Q"),
)


def fetch(url, start, end):
    req = urllib.request.Request(url)
    req.add_header("Range", "bytes=%d-%d" % (start, end))
    t0 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
            return {
                "url": url, "range": "bytes=%d-%d" % (start, end),
                "status": r.status,
                "content_range": r.headers.get("Content-Range"),
                "len": len(body),
                "sha256": hashlib.sha256(body).hexdigest(),
                "utc": t0, "body": body,
            }
    except urllib.error.HTTPError as e:
        return {"url": url, "range": "bytes=%d-%d" % (start, end),
                "status": e.code, "content_range": None, "len": 0,
                "sha256": None, "utc": t0, "body": b"", "error": str(e)[:100]}
    except Exception as e:  # noqa: BLE001 - receipt keeps the failure
        return {"url": url, "range": "bytes=%d-%d" % (start, end),
                "status": None, "content_range": None, "len": 0,
                "sha256": None, "utc": t0, "body": b"", "error": str(e)[:100]}


def parse_sb(sb):
    views = {}
    views["hex_sb96"] = sb.hex()
    for tag, e in (("v4map_be", ">"), ("v4map_le", "<")):
        vals = dict(zip(V4_FIELDS, struct.unpack_from(e + V4_FMT, sb, 0)))
        views[tag] = vals
    for tag, e in (("v3map_be", ">"), ("v3map_le", "<")):
        vals = {}
        for name, off, fmt in V3_FIELDS:
            if off + struct.calcsize(fmt) <= len(sb):
                vals[name] = struct.unpack_from(e + fmt, sb, off)[0]
        views[tag] = vals
    views["magic_bytes"] = sb[:4].hex()
    views["sha256_sb"] = hashlib.sha256(sb).hexdigest()
    return views


def probe(url):
    receipts = []
    off = 0
    member = None
    for _ in range(40):
        r = fetch(url, off, off + 511)
        body = r.get("body", b"")
        r.pop("body", None)
        if r.get("status") not in (200, 206):
            r["note"] = "tar-header fetch failed; walk stopped"
            receipts.append(r)
            break
        name = body[:100].split(b"\0")[0].decode("utf-8", "replace")
        try:
            size = int(body[124:135].split(b"\0")[0] or b"0", 8)
        except ValueError:
            size = -1
        r["tar_member"] = {"name": name, "size": size,
                           "typeflag": chr(body[156]) if len(body) > 156 else "?"}
        receipts.append(r)
        if name.endswith("filesystem.image"):
            member = off
            break
        if size < 0:
            r["note"] = "unparsable size; walk stopped"
            break
        off += 512 + ((size + 511) // 512) * 512
    out = {"url": url, "receipts": receipts}
    if member is None:
        out["result"] = "filesystem.image member not reached"
        return out
    data_off = member + 512
    sb_r = fetch(url, data_off, data_off + 95)
    out["superblock_request"] = {k: v for k, v in sb_r.items() if k != "body"}
    if sb_r.get("status") in (200, 206) and len(sb_r.get("body", b"")) >= 48:
        out["superblock"] = parse_sb(sb_r["body"])
    return out


def main():
    for label, url in TARGETS:
        res = probe(url)
        res["model"] = label
        print(json.dumps(res, indent=1, default=str), flush=True)


if __name__ == "__main__":
    main()
