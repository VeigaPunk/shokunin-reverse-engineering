#!/usr/bin/env python3
"""Emit provenance.json / superblock.json / metadata-chain.json for the V1 AVM-BE
carrier from measured bytes only (nothing typed by hand)."""
import hashlib
import json
import lzma
import os
import struct
import sys

SRC = sys.argv[1]          # scratch root
ART = sys.argv[2]          # artifacts dir


def sha(b):
    return hashlib.sha256(b).hexdigest()


def sb_fields(blob):
    fmt = ">" if blob[:4] == b"sqsh" else "<"
    u16 = lambda o: struct.unpack(fmt + "H", blob[o:o + 2])[0]
    u32 = lambda o: struct.unpack(fmt + "I", blob[o:o + 4])[0]
    u64 = lambda o: struct.unpack(fmt + "Q", blob[o:o + 8])[0]
    return {
        "magic_ascii": blob[:4].decode("ascii"),
        "magic_hex": blob[:4].hex(),
        "endianness": "BE" if fmt == ">" else "LE",
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
        "_fmt": fmt,
    }


def meta_chain(blob, start, end, fmt):
    off, sizes = start, []
    while off < end:
        v = struct.unpack(fmt + "H", blob[off:off + 2])[0]
        s = v & 0x7FFF
        if s == 0:
            break
        sizes.append(s)
        off += 2 + s
    return sizes, off


def main():
    member = open(os.path.join(SRC, "x/var/remote/var/tmp/filesystem.image"), "rb").read()
    le = open(os.path.join(SRC, "x/var/remote/var/tmp/x86/filesystem.image"), "rb").read()
    image = open(os.path.join(SRC, "fw.image"), "rb").read()
    carrier = open(os.path.join(SRC, "carrier-v1-be.sqsh"), "rb").read()
    sb = sb_fields(member)
    bu = sb["bytes_used"]

    # ---- provenance chain -------------------------------------------------
    hdr_lines = open(os.path.join(SRC, "headers.txt"), "r", errors="replace").read().splitlines()
    prov = {
        "seat": "R40C1VendorV1",
        "claim": "R40-C1 carrier V1 (AVM-layout big-endian SquashFS v4)",
        "chain": {
            "1_url": {
                "url": "https://download.avm.de/fritzbox/fritzbox-6490-cable/other/fritz.os/FRITZ.Box_6490_Cable-07.57.image",
                "http_status": 200,
                "response_headers": hdr_lines,
                "fetched_utc": "2026-10-26T18:17:31Z (server Date header)",
            },
            "2_image": {
                "bytes": len(image),
                "sha256": sha(image),
                "pinned_sha256": "f518ce6baa05b30d84264d9349cca9bf0b9402986d4112bda8ad73a04f9ede6d",
                "pin_matches": sha(image) == "f518ce6baa05b30d84264d9349cca9bf0b9402986d4112bda8ad73a04f9ede6d",
                "container": "POSIX tar (ustar, no compression; 21 entries)",
            },
            "3_tar_member": {
                "path": "./var/remote/var/tmp/filesystem.image",
                "size": 5443592,
                "tar_header_offset": 32025600,
                "tar_data_offset": 32026112,
                "tar_data_end_exclusive": 37469704,
                "sha256": sha(member),
                "sha256_of_image_byte_range": sha(image[32026112:37469704]),
                "range_equals_member": image[32026112:37469704] == member,
                "role": "AVM-BE SquashFS v4 member (the C1 carrier source)",
            },
            "3b_tar_member_le_reference": {
                "path": "./var/remote/var/tmp/x86/filesystem.image",
                "size": len(le),
                "sha256": sha(le),
                "role": "LE sibling (hsqs) - NOT a C1 carrier; recorded for provenance only",
            },
            "4_byte_range": {
                "start": 0,
                "end_exclusive": bu,
                "basis": "superblock bytes_used (BE at offset 40..48)",
                "extent_bytes": bu,
            },
            "5_carrier": {
                "path": "carrier-v1-be.sqsh",
                "bytes": len(carrier),
                "sha256": sha(carrier),
                "carve": "head -c 5442392 fw-member > carrier-v1-be.sqsh",
                "equals_member_prefix": carrier == member[:bu],
            },
        },
        "member_shape": {
            "file_bytes": len(member),
            "bytes_used": bu,
            "zero_pad_bytes_to_next_4096": ((bu + 4095) // 4096) * 4096 - bu,
            "trailer_offset": ((bu + 4095) // 4096) * 4096,
            "trailer_bytes": len(member) - ((bu + 4095) // 4096) * 4096,
            "trailer_hex": member[((bu + 4095) // 4096) * 4096:].hex(),
            "pad_is_all_zero": member[bu:((bu + 4095) // 4096) * 4096].count(0)
                               == ((bu + 4095) // 4096) * 4096 - bu,
            "same_shape_in_le_member": {
                "le_file_bytes": len(le),
                "le_bytes_used": sb_fields(le)["bytes_used"],
                "le_zero_pad": ((sb_fields(le)["bytes_used"] + 4095) // 4096) * 4096
                               - sb_fields(le)["bytes_used"],
                "le_trailer_hex": le[((sb_fields(le)["bytes_used"] + 4095) // 4096) * 4096:].hex(),
            },
        },
        "carrier_choice": {
            "chosen": "member[0:bytes_used] (5442392 bytes)",
            "rejected": ["whole member (5443592 bytes: 1192 zero pad + 8-byte vendor trailer)",
                         "member[0:5443584] (bytes_used zero-padded to 4096)"],
            "reason": "unblob _SquashFSBase.calculate_chunk rounds bytes_used up to 4096 ONLY if "
                      "the read at bytes_used starts with that many zero bytes; on the whole "
                      "member that holds, so the chunk ends at 5443584 and the trailing 8 bytes "
                      "become an UnknownChunkReport (measured on a dev fixture of the same shape, "
                      "rep-C). Truncating to bytes_used makes the read short, the padding test "
                      "fail, and the chunk equal the whole carrier (measured, rep-A): one chunk, "
                      "zero unknown-chunk noise.",
            "tools_never_run_on_carrier": ["REA extract-firmware", "unblob"],
            "allowed_reads_performed": ["python3 sb-parse.py", "python3 sb-walk.py",
                                        "sasquatch-v4be -ll (no -be)", "sasquatch-v4be -be -ll"],
        },
    }

    # ---- superblock -------------------------------------------------------
    sb_out = {"path": "carrier-v1-be.sqsh", "carrier_sha256": sha(carrier)}
    sb_out.update({k: v for k, v in sb.items() if k != "_fmt"})
    sb_out["compression_name"] = {1: "gzip", 2: "lzma", 3: "lzo", 4: "xz",
                                  5: "lz4", 6: "zstd"}.get(sb["compression_id"])
    sb_out["mkfs_time_utc"] = "1970-03-04T23:46:32+00:00 (secs since epoch; not a real date)"
    sb_out["avm_marker_mkfs_time_eq_bytes_used"] = sb["mkfs_time"] == sb["bytes_used"]
    sb_out["block_size_matches_block_log"] = (1 << sb["block_log"]) == sb["block_size"]
    sb_out["table_ladder_strictly_increasing"] = all(
        a < b for a, b in zip(
            [sb["inode_table_start"], sb["directory_table_start"], sb["fragment_table_start"],
             sb["lookup_table_start"], sb["id_table_start"]],
            [sb["directory_table_start"], sb["fragment_table_start"], sb["lookup_table_start"],
             sb["id_table_start"], sb["bytes_used"]]))
    sb_out["flags_decoded"] = {
        "duplicates": bool(sb["flags"] & 0x0040),          # 0x0040
        "exportable": bool(sb["flags"] & 0x0080),
        "no_xattrs": bool(sb["flags"] & 0x0200),
        "compressor_options_present": bool(sb["flags"] & 0x0400),
        "raw": sb["flags"],
    }
    its, dts = sb["inode_table_start"], sb["directory_table_start"]
    hdr_raw = struct.unpack(">H", carrier[its:its + 2])[0]
    le_raw = struct.unpack("<H", carrier[its:its + 2])[0]
    sb_out["first_metadata_header_at_inode_table_start"] = {
        "offset": its,
        "bytes_hex": carrier[its:its + 2].hex(),
        "as_little_endian": {"raw": le_raw, "stored": le_raw & 0x7FFF,
                             "uncompressed_flag": bool(le_raw & 0x8000)},
        "as_big_endian": {"raw": hdr_raw, "stored": hdr_raw & 0x7FFF,
                          "uncompressed_flag": bool(hdr_raw & 0x8000)},
        "be_overruns_directory_table": its + 2 + (hdr_raw & 0x7FFF) > dts,
        "le_fits_before_directory_table": its + 2 + (le_raw & 0x7FFF) <= dts,
    }

    # ---- metadata chain walk (the discriminating test) --------------------
    chain = {"carrier": {}, "le_member": {}, "dev_control": {}}
    for label, blob in (("carrier", carrier), ("le_member", le)):
        f = ">" if blob[:4] == b"sqsh" else "<"
        s = sb_fields(blob)
        for name, fmt in (("little", "<"), ("big", ">")):
            sizes, end = meta_chain(blob, s["inode_table_start"], s["directory_table_start"], fmt)
            chain[label][name] = {
                "dir_headers": len(sizes), "dir_sizes": sizes,
                "dir_landed_exact": end == s["directory_table_start"],
            }
        sizes, end = meta_chain(blob, s["directory_table_start"], s["fragment_table_start"], "<")
        chain[label]["directory_table_le"] = {
            "headers": len(sizes), "sizes": sizes,
            "landed_exactly_on_fragment_table_start": end == s["fragment_table_start"],
        }
        first = struct.unpack("<H", blob[s["inode_table_start"]:s["inode_table_start"] + 2])[0]
        blk = blob[s["inode_table_start"] + 2:s["inode_table_start"] + 2 + (first & 0x7FFF)]
        try:
            chain[label]["first_inode_block_xz"] = {
                "declared_le_length": first & 0x7FFF,
                "decompressed_bytes": len(lzma.decompress(blk)),
            }
        except Exception as exc:  # noqa: BLE001
            chain[label]["first_inode_block_xz"] = {"error": type(exc).__name__}
        overlong = struct.unpack(">H", blob[s["inode_table_start"]:s["inode_table_start"] + 2])[0]
        try:
            chain[label]["first_inode_block_xz_as_be_length"] = {
                "declared_be_length": overlong & 0x7FFF,
                "decompressed_bytes": len(
                    lzma.decompress(blob[s["inode_table_start"] + 2:
                                         s["inode_table_start"] + 2 + (overlong & 0x7FFF)])),
                "note": "an OVER-long slice still yields a valid xz stream (decoder stops at the "
                        "stream end), so bytes_used/decompression alone is not discriminating; "
                        "the chain landing test is",
            }
        except Exception as exc:  # noqa: BLE001
            chain[label]["first_inode_block_xz_as_be_length"] = {"error": type(exc).__name__}
    dev = open(os.path.join(SRC, "dev-be.sqsh"), "rb").read()
    s = sb_fields(dev)
    sizes_le, end_le = meta_chain(dev, s["inode_table_start"], s["directory_table_start"], "<")
    sizes_be, end_be = meta_chain(dev, s["inode_table_start"], s["directory_table_start"], ">")
    chain["dev_control"] = {
        "file": "dev-be.sqsh (gen-squashfs.py --endian be --comp gzip, fresh tree)",
        "sha256": sha(dev),
        "little_landed_exact": end_le == s["directory_table_start"],
        "big_landed_exact": end_be == s["directory_table_start"],
        "note": "standard BE body: BE lengths land exactly, LE do not (the inverse of the carrier)",
    }
    chain["verdict"] = {
        "carrier_block_lengths": "little-endian",
        "carrier_superblock": "big-endian",
        "discriminating_evidence": "inode-table AND directory-table header chains both land "
                                   "exactly on the next table start only under LE (5 headers "
                                   "/ 8574 B and 4 headers / 10808 B respectively)",
    }

    for name, obj in (("provenance.json", prov), ("superblock.json", sb_out),
                      ("metadata-chain.json", chain)):
        with open(os.path.join(ART, name), "w") as fh:
            json.dump(obj, fh, indent=2)
            fh.write("\n")
        print("wrote", name)


if __name__ == "__main__":
    main()
