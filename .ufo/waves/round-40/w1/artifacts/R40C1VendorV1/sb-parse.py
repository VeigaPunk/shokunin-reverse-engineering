#!/usr/bin/env python3
"""Independent pure-stdlib SquashFS v4 superblock parser + metadata block-length
endianness probe.  Reads ONLY bytes; imports nothing from unblob/sasquatch.

Superblock v4 layout (little-endian fields unless the magic says BE):
  0  u32 magic          'hsqs' = LE, 'sqsh' = BE
  4  u32 inode_count
  8  u32 mkfs_time
 12  u32 block_size
 16  u32 fragment_count
 20  u16 compression
 22  u16 block_log
 24  u16 flags
 26  u16 id_count
 28  u16 version_major
 30  u16 version_minor
 32  u64 root_inode_ref
 40  u64 bytes_used
 48  u64 id_table_start
 56  u64 xattr_id_table_start
 64  u64 inode_table_start
 72  u64 directory_table_start
 80  u64 fragment_table_start
 88  u64 lookup_table_start
(sum = 96 bytes of superblock; first metadata/data byte at 96)
"""
import json
import struct
import sys

MAGICS = {b"hsqs": ("little", "<", "LE"), b"sqsh": ("big", ">", "BE")}
COMPRESSIONS = {
    1: "gzip", 2: "lzma", 3: "lzo", 4: "xz", 5: "lz4", 6: "zstd",
}


def decode_header(blob, off, endian):
    """Return (value_masked, raw16, size_field_ok) for a 2-byte metadata
    block-length header at `off`. Bit 15 set means the block is uncompressed;
    the low 15 bits are the on-disk stored size."""
    raw = blob[off:off + 2]
    if len(raw) < 2:
        return None
    v = struct.unpack(endian + "H", raw)[0]
    return {"raw": v, "stored": v & 0x7FFF, "uncompressed_flag": bool(v & 0x8000)}


def main(path):
    with open(path, "rb") as fh:
        blob = fh.read()
    out = {"path": path, "file_size": len(blob)}

    magic = blob[:4]
    if magic not in MAGICS:
        out["error"] = "unknown magic %r" % (magic,)
        print(json.dumps(out, indent=2))
        return 2
    endian, endian_fmt, endian_name = MAGICS[magic]
    out["magic_ascii"] = magic.decode("ascii")
    out["magic_hex"] = magic.hex()
    out["endianness"] = endian_name

    u16 = lambda o: struct.unpack(endian_fmt + "H", blob[o:o + 2])[0]
    u32 = lambda o: struct.unpack(endian_fmt + "I", blob[o:o + 4])[0]
    u64 = lambda o: struct.unpack(endian_fmt + "Q", blob[o:o + 8])[0]

    sb = {
        "inode_count": u32(4),
        "mkfs_time": u32(8),
        "block_size": u32(12),
        "fragment_count": u32(16),
        "compression_id": u16(20),
        "block_log": u16(22),
        "flags": u16(24),
        "id_count": u16(26),
        "s_major": u16(28),
        "s_minor": u16(30),
        "root_inode_ref": u64(32),
        "bytes_used": u64(40),
        "id_table_start": u64(48),
        "xattr_id_table_start": u64(56),
        "inode_table_start": u64(64),
        "directory_table_start": u64(72),
        "fragment_table_start": u64(80),
        "lookup_table_start": u64(88),
    }
    sb["flags_decoded"] = {
        "uncompressed_inodes": bool(sb["flags"] & 0x0001),
        "uncompressed_data": bool(sb["flags"] & 0x0002),
        "check": bool(sb["flags"] & 0x0004),
        "uncompressed_fragments": bool(sb["flags"] & 0x0008),
        "no_fragments": bool(sb["flags"] & 0x0010),
        "always_fragments": bool(sb["flags"] & 0x0020),
        "duplicates": bool(sb["flags"] & 0x0040),
        "exportable": bool(sb["flags"] & 0x0080),
        "uncompressed_xattrs": bool(sb["flags"] & 0x0100),
        "no_xattrs": bool(sb["flags"] & 0x0200),
        "compressor_options": bool(sb["flags"] & 0x0400),
    }
    sb["u64_minus_one_fields"] = sorted(
        k for k, v in sb.items() if v == 0xFFFFFFFFFFFFFFFF)
    sb["compression_name"] = COMPRESSIONS.get(sb["compression_id"], "unknown")
    sb["mkfs_time_utc"] = None
    try:
        import datetime
        sb["mkfs_time_utc"] = datetime.datetime.fromtimestamp(
            sb["mkfs_time"], datetime.timezone.utc).isoformat()
    except Exception:
        pass
    # AVM marker: the vendor sets mkfs_time equal to bytes_used.
    sb["avm_marker_mkfs_time_eq_bytes_used"] = sb["mkfs_time"] == sb["bytes_used"]
    # Root inode ref = (block offset within inode table) << 16 | inode offset.
    sb["root_inode_block"] = sb["root_inode_ref"] >> 16
    sb["root_inode_offset"] = sb["root_inode_ref"] & 0xFFFF
    out["superblock"] = sb

    # Byte range accounting: what lives past bytes_used?
    tail = len(blob) - sb["bytes_used"]
    out["tail"] = {
        "bytes_past_bytes_used": tail,
        "bytes_used": sb["bytes_used"],
        "file_size": len(blob),
    }
    if tail > 0:
        past = blob[sb["bytes_used"]:]
        out["tail"]["first_64_hex"] = past[:64].hex()
        out["tail"]["all_zero"] = past.count(0) == len(past)
        out["tail"]["sha256"] = __import__("hashlib").sha256(past).hexdigest()
        out["tail"]["distinct_byte_values"] = sorted(set(past))[:16]
    elif tail < 0:
        out["tail"]["note"] = "bytes_used exceeds file size"

    # Metadata block-length header at inode_table_start, decoded both ways.
    its = sb["inode_table_start"]
    probes = {}
    for name, e in (("little", "<"), ("big", ">")):
        probes[name] = decode_header(blob, its, e)
    out["metadata_header_at_inode_table_start"] = {
        "offset": its,
        "bytes_hex": blob[its:its + 2].hex(),
        "as_little_endian": probes["little"],
        "as_big_endian": probes["big"],
    }
    # Plausibility: the stored size must fit before the next table, and the
    # following header must also decode to a sane size.
    nxt = sb["directory_table_start"]
    plaus = {}
    for name, e in (("little", "<"), ("big", ">")):
        h0 = decode_header(blob, its, e)
        h1 = decode_header(blob, its + 2 + h0["stored"], e)
        ok = (h0["stored"] > 0 and its + 2 + h0["stored"] <= nxt
              and h1 is not None)
        plaus[name] = {
            "first_stored": h0["stored"],
            "second_header_stored": None if h1 is None else h1["stored"],
            "first_block_end": its + 2 + h0["stored"],
            "fits_before_directory_table": its + 2 + h0["stored"] <= nxt,
            "second_header_available": h1 is not None,
            "plausible": bool(ok),
        }
    out["metadata_header_plausibility"] = plaus
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
