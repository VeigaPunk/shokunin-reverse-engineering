#!/usr/bin/env python3
"""Classify a SquashFS v4 image by its metadata-block-length endianness.

Why this probe exists (seat R39AssimAvmCritic, round 39 wave 1): unblob 26.6.4
decides the `sasquatch-v4be` argument vector from one superblock equality
(`mkfs_time == bytes_used`, squashfs.py:48-49). The property that actually
separates AVM-BE from standard BE is stated in Freetz's format note
(S114 lane / S192 merged): everything is big-endian except the block-length
value at the start of each block.

Test: read the 2-byte metadata block header at `inode_table_start` and decode
it both ways. The 0x8000 bit is squashfs-tools' "stored uncompressed" flag, so
it is masked.

Two signals, strongest first:
  exact: len + inode_table_start + 2 == directory_table_start. Only holds when
         the inode table is a single metadata block, i.e. on small fixtures.
  plaus: masked length in (0, 8192] -- the metadata block payload has at most
         8192 bytes, so the correct endianness yields a plausible length and
         the wrong one usually yields a value far above 8192. This is a
         plausibility check, not an identity: compressed 8192-byte payloads can
         exceed 8192.

Usage: python3 -I -B probe-marker-vs-format.py IMAGE [IMAGE ...]
Prints one TSV row per image; exit 0 for every parsed image, 1 if any image is
not SquashFS v4.
"""
import struct
import sys

META_MAX = 8192


def field(b, off, fmt, be):
    size = struct.calcsize(fmt)
    return struct.unpack((">" if be else "<") + fmt, b[off:off + size])[0]


def classify(path):
    with open(path, "rb") as fh:
        b = fh.read()
    magic = b[0:4]
    if magic not in (b"sqsh", b"hsqs") or len(b) < 96:
        return {"path": path, "verdict": "not-squashfs-v4-magic"}
    be = magic == b"sqsh"
    major = field(b, 28, "H", be)
    if major != 4:
        return {"path": path, "verdict": f"version-{major}-not-4"}
    mkfs = field(b, 8, "I", be)
    bytes_used = field(b, 40, "Q", be)
    comp = field(b, 20, "H", be)
    itab = field(b, 64, "Q", be)
    dtab = field(b, 72, "Q", be)
    hdr = b[itab:itab + 2]
    len_le = struct.unpack("<H", hdr)[0] & 0x7FFF
    len_be = struct.unpack(">H", hdr)[0] & 0x7FFF
    exact_le = itab + 2 + len_le == dtab
    exact_be = itab + 2 + len_be == dtab
    plaus_le = 0 < len_le <= META_MAX
    plaus_be = 0 < len_be <= META_MAX
    if exact_le != exact_be:
        signal, length_endian = "exact", ("le" if exact_le else "be")
    elif plaus_le != plaus_be:
        signal, length_endian = "plausibility", ("le" if plaus_le else "be")
    elif plaus_le and plaus_be:
        signal, length_endian = "undecided", "ambiguous"
    else:
        signal, length_endian = "undecided", "implausible-both"
    marker = mkfs == bytes_used
    if not be:
        layout = "le"
    elif length_endian == "le":
        layout = "avm-be"
    elif length_endian == "be":
        layout = "standard-be"
    else:
        layout = "unresolved-be"
    # what unblob 26.6.4 does (squashfs.py:41-52), verbatim logic
    if be and major == 4:
        flag = "" if marker else "-be"
        ok = (marker and layout == "avm-be") or (not marker and layout == "standard-be")
        expect = "extract-ok" if ok else "expect-extractor-failure"
    else:
        flag, expect = "-le", "extract-ok"
    return {
        "path": path, "magic": magic.decode(), "major": major, "comp": comp,
        "mkfs_time": mkfs, "bytes_used": bytes_used,
        "marker": "yes" if marker else "no",
        "hdr_hex": hdr.hex(), "len_le": len_le, "len_be": len_be,
        "signal": signal, "length_endian": length_endian, "layout": layout,
        "unblob_v4be_flag": flag or "(none)", "unblob_expect": expect,
        "verdict": "ok",
    }


COLS = ["path", "magic", "major", "comp", "mkfs_time", "bytes_used", "marker",
        "hdr_hex", "len_le", "len_be", "signal", "length_endian", "layout",
        "unblob_v4be_flag", "unblob_expect", "verdict"]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: probe-marker-vs-format.py IMAGE [IMAGE ...]")
    print("\t".join(COLS))
    rc = 0
    for p in sys.argv[1:]:
        row = classify(p)
        if row["verdict"] != "ok":
            rc = 1
        print("\t".join(str(row.get(c, "")) for c in COLS))
    sys.exit(rc)
