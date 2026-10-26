#!/usr/bin/env python3
"""Probe the round-11 fixture for the AVM-BE SquashFS v4 layout (stdlib only).

Tests three sentences:
  S1  the 96-byte v4 superblock is big-endian and carries the AVM marker
      (mkfs_time == bytes_used);
  S2  every metadata block-length header decodes to its real payload size only
      as little-endian, and the payload ends exactly on the next structure
      (next table metadata block / table index); the big-endian decode does not;
  S3  unblob's chunk arithmetic on the superblock yields the padded chunk end.

Usage: python3 avm-fixture-probe.py IMAGE
"""
import lzma
import struct
import sys

SB = struct.Struct(">4sIIIIHHHHHHQQQQQQQQ")  # 96 bytes, AVM endian = big
FIELDS = (
    "s_magic", "inodes", "mkfs_time", "block_size", "fragments",
    "compression", "block_log", "flags", "no_ids", "s_major", "s_minor",
    "root_inode", "bytes_used", "id_table_start", "xattr_id_table_start",
    "inode_table_start", "directory_table_start", "fragment_table_start",
    "lookup_table_start",
)
PAD_SIZES = (4096, 1024)


def round_up(n, a):
    return a * -(-n // a)


def le16(b):
    return b[0] | (b[1] << 8)


def be16(b):
    return (b[0] << 8) | b[1]


def block(data, off):
    """Decode one metadata block header at `off` as LE; describe its payload."""
    hdr = data[off:off + 2]
    v_le = le16(hdr)
    v_be = be16(hdr)
    size = v_le & 0x7FFF
    stored = bool(v_le & 0x8000)
    payload = data[off + 2:off + 2 + size]
    rec = {
        "off": off, "hdr": hdr.hex(), "le": v_le, "be": v_be,
        "size": size, "stored": stored, "next": off + 2 + size,
        "payload_bytes": len(payload),
    }
    try:
        raw = payload if stored else lzma.decompress(payload)
        rec["raw_len"] = len(raw)
        rec["decode"] = "ok"
    except Exception as exc:  # noqa: BLE001 - probe records the failure
        rec["decode"] = f"fail:{type(exc).__name__}"
    be_size = v_be & 0x7FFF
    rec["be_size"] = be_size
    rec["be_stored"] = bool(v_be & 0x8000)
    return rec


def show(tag, rec, boundary):
    print(
        f"  {tag:24s} hdr@{rec['off']:3d} bytes={rec['hdr']} "
        f"LE={rec['le']:#06x} size={rec['size']:5d} "
        f"{'stored' if rec['stored'] else 'xz':6s} "
        f"raw={rec.get('raw_len', '-')} next={rec['next']:3d} "
        f"boundary={boundary} lands={rec['next'] == boundary} "
        f"decode={rec['decode']} | BE={rec['be']:#06x} "
        f"be_size={rec['be_size']} be_stored={rec['be_stored']}"
    )


def main(path):
    data = open(path, "rb").read()
    print(f"file={path} size={len(data)}")
    sb = dict(zip(FIELDS, SB.unpack_from(data, 0)))
    print("superblock (decoded big-endian):")
    for k in FIELDS:
        v = sb[k]
        print(f"  {k} = {v!r}" if isinstance(v, bytes) else f"  {k} = {v}")

    a1 = (sb["s_magic"] == b"sqsh" and sb["s_major"] == 4
          and sb["mkfs_time"] == sb["bytes_used"])
    print(f"S1 BE superblock + marker: magic={sb['s_magic']!r} "
          f"major={sb['s_major']} mkfs_time={sb['mkfs_time']} "
          f"bytes_used={sb['bytes_used']} -> {a1}")

    # Table metadata blocks are reached the way unsquashfs reaches them:
    # inode/directory start directly; fragment/id tables are index tables whose
    # BE u64 index points at the metadata block.
    frag_idx = struct.unpack_from(">Q", data, sb["fragment_table_start"])[0]
    id_idx = struct.unpack_from(">Q", data, sb["id_table_start"])[0]
    print(f"fragment index @{sb['fragment_table_start']} -> {frag_idx}; "
          f"id index @{sb['id_table_start']} -> {id_idx}")

    checks = [
        ("inode table", sb["inode_table_start"], sb["directory_table_start"]),
        ("directory table", sb["directory_table_start"], frag_idx),
        ("fragment table", frag_idx, sb["fragment_table_start"]),
        ("id table", id_idx, sb["id_table_start"]),
    ]
    ok = 0
    for tag, off, boundary in checks:
        rec = block(data, off)
        show(tag, rec, boundary)
        if rec["next"] == boundary and rec["decode"] == "ok":
            ok += 1
    print(f"S2 LE metadata headers land on every boundary: {ok}/{len(checks)} "
          f"-> {ok == len(checks)}")

    end_of_data = (0 + sb["bytes_used"]) & 0xFFFFFFFF
    end_offset = None
    print("S3 unblob _SquashFSBase.calculate_chunk arithmetic:")
    for pad in sorted(PAD_SIZES, reverse=True):
        size = round_up(sb["bytes_used"], pad)
        pad_len = size - sb["bytes_used"]
        tail = data[end_of_data:end_of_data + pad_len]
        zero = len(tail) == pad_len and tail == b"\x00" * pad_len
        print(f"  pad={pad} round_up={size} pad_len={pad_len} zero_tail={zero}")
        if zero:
            end_offset = size
            break
    if end_offset is None:
        end_offset = sb["bytes_used"]
    print(f"  chunk=0x0-0x{end_offset:x} bytes_used=0x{sb['bytes_used']:x}; "
          f"no block-length validation in the handler")


if __name__ == "__main__":
    main(sys.argv[1])
