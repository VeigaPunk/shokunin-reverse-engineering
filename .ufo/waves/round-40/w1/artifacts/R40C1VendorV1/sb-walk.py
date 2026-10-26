#!/usr/bin/env python3
"""Byte-level proof that the AVM-BE member's metadata block-length headers are
LITTLE-endian while the superblock is BIG-endian.

Method (pure stdlib, no sasquatch/unblob code):
  1. Walk the 2-byte block-length header chain from inode_table_start to
     directory_table_start under each candidate byte order.  The chain can only
     land exactly on directory_table_start for the true byte order.
  2. Decompress the first block with lzma (SquashFS xz metadata blocks are
     whole xz streams) using each candidate length; only the true length is a
     valid xz stream that yields the fixed 8192-byte metadata block size.
"""
import json
import lzma
import struct
import sys

META_BLOCK = 8192  # SQUASHFS_METADATA_SIZE


def blocks(blob, start, end, fmt):
    """Yield (offset, stored, uncompressed_flag) while the chain stays inside
    [start, end); return (chain, landed_exactly)."""
    off, out = start, []
    while off < end:
        raw = blob[off:off + 2]
        if len(raw) < 2:
            return out, False
        v = struct.unpack(fmt + "H", raw)[0]
        stored = v & 0x7FFF
        if stored == 0:
            return out, False
        off += 2 + stored
        out.append({"offset": off - 2 - stored, "raw": v,
                    "stored": stored, "uncompressed_flag": bool(v & 0x8000)})
        if len(out) > 100000:
            return out, False
    return out, off == end


def first_block_decompress(blob, off, stored, flag):
    data = blob[off + 2:off + 2 + stored]
    if flag:
        return {"mode": "stored-uncompressed", "bytes": len(data)}
    try:
        d = lzma.decompress(data)
        return {"mode": "xz", "decompressed_bytes": len(d),
                "matches_metadata_block_size": len(d) == META_BLOCK}
    except Exception as exc:  # noqa: BLE001 - report, do not crash
        return {"mode": "xz", "error": type(exc).__name__, "detail": str(exc)}


def main(path):
    blob = open(path, "rb").read()
    magic = blob[:4]
    fmt = ">" if magic == b"sqsh" else "<"
    u16 = lambda o: struct.unpack(fmt + "H", blob[o:o + 2])[0]
    u64 = lambda o: struct.unpack(fmt + "Q", blob[o:o + 8])[0]
    its, dts = u64(64), u64(72)
    out = {
        "path": path,
        "superblock_endianness": "BE" if fmt == ">" else "LE",
        "inode_table_start": its,
        "directory_table_start": dts,
        "inode_table_span": dts - its,
    }
    for name, f in (("little", "<"), ("big", ">")):
        chain, exact = blocks(blob, its, dts, f)
        first = chain[0] if chain else None
        entry = {
            "headers": len(chain),
            "nonzero_headers": sum(1 for c in chain if c["raw"]),
            "landed_exactly_on_directory_table_start": exact,
            "first_block": first,
        }
        if first:
            entry["first_block_decompress"] = first_block_decompress(
                blob, first["offset"], first["stored"],
                first["uncompressed_flag"])
        out[name] = entry
    out["verdict_block_lengths"] = (
        "little-endian" if out["little"]["landed_exactly_on_directory_table_start"]
        else "big-endian" if out["big"]["landed_exactly_on_directory_table_start"]
        else "undetermined")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
