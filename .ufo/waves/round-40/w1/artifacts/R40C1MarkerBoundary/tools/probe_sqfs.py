#!/usr/bin/env python3
"""probe_sqfs.py — independent pure-stdlib SquashFS v4 layout probe (no sasquatch, no unblob).

Reports, per image:
  magic / compression / version / mkfs_time / bytes_used / marker (mkfs_time == bytes_used)
  the table offsets from the superblock
  the first metadata block-length header at inode_table_start decoded as LE and as BE
  an EXACT span walk: from inode_table_start step 2+len until dir_table_start (LE reading and
  BE reading); the same from dir_table_start to fragment_table_start.  A walk is "exact" when
  the running offset lands on the span end after at least one block, with no overshoot.

The exact walk works for tables spanning any number of metadata blocks, so it resolves the
block-length endianness on multi-block tables where a plausibility test cannot.

usage: probe_sqfs.py IMAGE...   (prints TSV to stdout)
exit 0 always; the verdict column states the finding.
"""
import struct
import sys

MASK = 0x8000


def sb(d):
    magic = d[0:4]
    e = "<" if magic == b"hsqs" else ">"
    f = e + "4sIIIIHHHHHHQQQQQQQQ"
    (magic, inodes, mkfs_time, block_size, fragments, compression, block_log,
     flags, no_ids, major, minor, root_inode, bytes_used, id_table_start,
     xattr_id_table_start, inode_table_start, dir_table_start,
     frag_table_start, lookup_table_start) = struct.unpack(f, d[:96])
    return dict(endian=e, magic=magic, inodes=inodes, mkfs_time=mkfs_time,
                block_size=block_size, fragments=fragments,
                compression=compression, major=major, minor=minor,
                bytes_used=bytes_used, id_table_start=id_table_start,
                inode_table_start=inode_table_start,
                dir_table_start=dir_table_start,
                frag_table_start=frag_table_start,
                lookup_table_start=lookup_table_start)


def walk(d, start, end, order):
    """Step metadata blocks from start to end reading the 2-byte length header in `order`."""
    pos, blocks, first = start, 0, None
    if start >= end:
        return None, 0, "empty-span"
    while pos < end:
        if pos + 2 > len(d):
            return first, blocks, "truncated"
        v = struct.unpack(order + "H", d[pos:pos + 2])[0]
        ln = v & 0x7FFF
        if first is None:
            first = ln
        blocks += 1
        if ln == 0 or pos + 2 + ln > end:
            return first, blocks, "overshoot"
        pos += 2 + ln
        if blocks > 100000:
            return first, blocks, "runaway"
    return first, blocks, "exact" if pos == end else "undershoot"


def probe(path):
    d = open(path, "rb").read()
    s = sb(d)
    marker = s["mkfs_time"] == s["bytes_used"]
    out = dict(path=path, size=len(d), magic=s["magic"].decode("latin-1"),
               comp=s["compression"], ver="%d.%d" % (s["major"], s["minor"]),
               mkfs_time=s["mkfs_time"], bytes_used=s["bytes_used"], marker=marker)
    out["inode_table_start"] = s["inode_table_start"]
    out["dir_table_start"] = s["dir_table_start"]
    out["frag_table_start"] = s["frag_table_start"]
    out["lookup_table_start"] = s["lookup_table_start"]
    if 0 <= s["inode_table_start"] < len(d) - 1:
        out["first_len_le"] = struct.unpack("<H", d[s["inode_table_start"]:s["inode_table_start"] + 2])[0] & 0x7FFF
        out["first_len_be"] = struct.unpack(">H", d[s["inode_table_start"]:s["inode_table_start"] + 2])[0] & 0x7FFF
    else:
        out["first_len_le"] = out["first_len_be"] = None
    # span ends: the next real table start (a -1 / out-of-file offset means "no such table",
    # so fall through to the next one; bytes_used closes the last metadata region).
    def nxt(start):
        cands = [v for v in (s["dir_table_start"], s["frag_table_start"],
                             s["lookup_table_start"], s["id_table_start"], s["bytes_used"])
                 if start < v <= len(d)]
        return min(cands) if cands else None
    inode_end = nxt(s["inode_table_start"])
    dir_end = nxt(s["dir_table_start"])
    for tag, a, b in (("inode", s["inode_table_start"], inode_end),
                      ("dir", s["dir_table_start"], dir_end)):
        for order, lab in (("<", "le"), (">", "be")):
            if b is None:
                out["%s_walk_%s" % (tag, lab)] = "0/no-span"
                continue
            _, n, rep = walk(d, a, b, order)
            out["%s_walk_%s" % (tag, lab)] = "%d/%s" % (n, rep)
    # verdict: which endianness makes BOTH spans exact, and at least one span longer than a block
    def ok(lab):
        vals = [out["inode_walk_" + lab], out["dir_walk_" + lab]]
        judged = [v for v in vals if not v.endswith("no-span")]
        return bool(judged) and all(v.endswith("exact") for v in judged)
    le_ok, be_ok = ok("le"), ok("be")
    multi = any(int(out[k].split("/")[0]) > 1 for k in ("inode_walk_le", "inode_walk_be", "dir_walk_le", "dir_walk_be"))
    layout = "le" if le_ok and not be_ok else "be" if be_ok and not le_ok else "ambiguous" if (le_ok and be_ok) else "neither"
    out["layout"] = layout
    out["multiblock"] = multi
    # AVM-layout is a property of the BE-magic form only: sqsh magic + LE block lengths.
    # (An hsqs image also shows "layout le"; that is ordinary LE SquashFS, not AVM.)
    out["avm_genuine"] = s["magic"] == b"sqsh" and marker and layout == "le"
    out["marker_only"] = s["magic"] == b"sqsh" and marker and layout == "be"
    return out


COLS = ["path", "size", "magic", "comp", "ver", "mkfs_time", "bytes_used", "marker",
        "inode_table_start", "dir_table_start", "frag_table_start", "lookup_table_start",
        "first_len_le", "first_len_be", "inode_walk_le", "inode_walk_be",
        "dir_walk_le", "dir_walk_be", "layout", "multiblock", "avm_genuine", "marker_only"]

if __name__ == "__main__":
    print("\t".join(COLS))
    for p in sys.argv[1:]:
        o = probe(p)
        print("\t".join(str(o.get(c)) for c in COLS))
