#!/usr/bin/env python3
"""upx-pe-repair.py - round-99 tool (R99-C2, coverage: truncated packed PE).

Successor of tools/round-98/upx-pe-repair.py (unchanged there).  Round 99 adds
the packer's own truncation test and a typed CLI envelope; the repair rule
below is the round-98 rule, byte for byte in its decisions.

Restores the two anti-unpack tampers that make UPX 5.2.0 refuse a UPX-packed
PE (win32/pe, win64/pep): an overwritten PackHeader `UPX!` magic and renamed
`UPX0`/`UPX1` section headers.  Grounded in the packer's own unpack gate,
UPX 5.2.0 `src/pefile.cpp` `PeFile::canUnpack0` (corpus/SOURCES.md S324):

  * the gate first tests `memcmp(isection[0].name, "UPX", 3) == 0`; only then
    does it look for a PackHeader, `fi->seek(isection[1].rawdataptr - 64)`
    and `readPackHeader(1024)` (fallback: from `isection[2].rawdataptr`);
  * a packed-looking file without both throws `CantUnpackException: file is
    (possibly) modified/hacked/protected`;
  * at pack time the sections are named `UPX0`, `UPX1` and `.rsrc` or `UPX2`.

PackHeader (UPX 5.2.0 `src/packhead.cpp`/`packhead.h`, S308/S309): 32 bytes,
magic(4) version format method level u_adler c_adler u_len c_len
u_file_size filter filter_cto n_mru checksum; the checksum byte is the sum of
bytes 4..30 mod 251 and EXCLUDES the magic, so it still validates a header
whose magic was overwritten.

Rule.  Parse the PE section table (>= 3 sections, as the gate requires).  In
the gate's two windows, find the offsets whose 32 bytes carry a PE format
byte (9 win32/pe, 36 win64/pep), a version byte 10..14 and a valid checksum,
with c_len < u_len and c_len <= file size.  Exactly one such offset must
exist, otherwise refuse.  Rewrite its magic to `UPX!` when it differs; rename
section 0 to `UPX0` and section 1 to `UPX1` when their names lack the `UPX`
prefix; rename section 2 when its name is neither `.rsrc` nor `UPX2*` to
`.rsrc` if the resource directory RVA lies inside it, else `UPX2`.  Nothing
else changes.  The anchor is located structurally, never by the tampered
value.

Truncation (round 99).  UPX 5.2.0 `PeFile::unpack0` computes
`overlay = file_size - ALIGN_UP(isection[n-1].rawdataptr + isection[n-1].size,
ih.filealign)` and `Packer::checkOverlay` throws `OverlayException: invalid
overlay size` when `(int) overlay < 0` (src/pefile.cpp 3041-3049, S324;
src/packer.cpp 431-433, S326).  The tool applies the same arithmetic to the
LAST section header and refuses `truncated` when the file is shorter than
that aligned end, and `filealign-zero` when FileAlignment is 0 (the packer's
`unexpected value in the PE header`).  A file longer than the end carries an
overlay, which the packer copies; it is not refused.

Usage: python3 -I -B upx-pe-repair.py --in <file> --out <file> [--json]
Exit: 0 repaired or already intact (--out written, atomically, through a
        mkstemp name in the --out directory);
      2 refused: not PE, too few sections, truncated, filealign-zero, zero or
        several PackHeader candidates, input-unreadable, output-is-directory,
        output-dir-missing, output-write-failed (--out not written, no
        temporary left).  No other exit status is intended.
"""
import argparse
import json
import os
import struct
import sys
import tempfile

PE_FORMATS = {9: "win32/pe", 36: "win64/pep"}
MAGIC = b"UPX!"
PH_LEN = 32


class Refuse(Exception):
    pass


def sections(b):
    if len(b) < 0x40 or b[:2] != b"MZ":
        raise Refuse("not-mz")
    pe = struct.unpack_from("<I", b, 0x3C)[0]
    if pe + 24 > len(b) or b[pe:pe + 4] != b"PE\0\0":
        raise Refuse("not-pe")
    n = struct.unpack_from("<H", b, pe + 6)[0]
    opt = struct.unpack_from("<H", b, pe + 20)[0]
    magic = struct.unpack_from("<H", b, pe + 24)[0]
    st = pe + 24 + opt
    if n < 3 or st + 40 * n > len(b):
        raise Refuse("sections")
    falign = struct.unpack_from("<I", b, pe + 24 + 36)[0]
    secs = []
    for k in range(n):
        o = st + 40 * k
        vsize, vaddr, rsize, rptr = struct.unpack_from("<IIII", b, o + 8)
        secs.append({"off": o, "name": bytes(b[o:o + 8]), "vaddr": vaddr,
                     "vsize": vsize, "rsize": rsize, "rptr": rptr})
    if falign == 0:
        raise Refuse("filealign-zero")
    last = secs[0]
    end = (last["rptr"] + last["rsize"] + falign - 1) // falign * falign
    if len(b) < end:
        raise Refuse("truncated: file %d bytes < aligned end of last section %d" % (len(b), end))
    # resource data directory (index 2)
    dd = pe + 24 + (96 if magic == 0x10B else 112)
    rsrc_rva = struct.unpack_from("<I", b, dd + 16)[0] if dd + 20 <= st else 0
    return secs, rsrc_rva


def ph_ok(b, i):
    if i < 0 or i + PH_LEN > len(b):
        return False
    h = b[i:i + PH_LEN]
    version, fmt = h[4], h[5]
    if fmt not in PE_FORMATS or not 10 <= version <= 14:
        return False
    if sum(h[4:31]) % 251 != h[31]:
        return False
    u_len, c_len = struct.unpack_from("<II", h, 16)
    return 0 < c_len < u_len and c_len <= len(b)


def find_packheader(b, secs):
    starts = (secs[1]["rptr"] - 64, secs[2]["rptr"])
    found = set()
    for s in starts:
        for i in range(max(0, s), max(0, s) + 1024):
            if ph_ok(b, i):
                found.add(i)
    if len(found) != 1:
        raise Refuse("packheader-candidates:%d" % len(found))
    return found.pop()


def repair(data):
    b = bytearray(data)
    secs, rsrc_rva = sections(b)
    i = find_packheader(b, secs)
    changes = []
    if bytes(b[i:i + 4]) != MAGIC:
        b[i:i + 4] = MAGIC
        changes.append("magic@%d" % i)
    for k, want in ((0, b"UPX0"), (1, b"UPX1")):
        if not secs[k]["name"].startswith(b"UPX"):
            o = secs[k]["off"]
            b[o:o + 8] = want.ljust(8, b"\0")
            changes.append("name%d" % k)
    s2 = secs[2]
    if not (s2["name"].rstrip(b"\0") == b".rsrc" or s2["name"].startswith(b"UPX2")):
        inside = s2["vaddr"] <= rsrc_rva < s2["vaddr"] + max(s2["vsize"], s2["rsize"])
        want = b".rsrc" if rsrc_rva and inside else b"UPX2"
        b[s2["off"]:s2["off"] + 8] = want.ljust(8, b"\0")
        changes.append("name2")
    return bytes(b), {"packheader": i, "format": PE_FORMATS[b[i + 5]], "changes": changes}


def refuse(msg, as_json):
    info = {"refused": msg}
    print(json.dumps(info) if as_json else "refused: %s" % msg, file=sys.stderr)
    return 2


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        with open(a.inp, "rb") as fh:
            data = fh.read()
    except OSError as e:
        return refuse("input-unreadable: %s" % e.strerror, a.json)
    if os.path.isdir(a.out):
        return refuse("output-is-directory", a.json)
    outdir = os.path.dirname(os.path.abspath(a.out))
    if not os.path.isdir(outdir):
        return refuse("output-dir-missing", a.json)
    try:
        out, info = repair(data)
    except (Refuse, struct.error) as e:
        return refuse(str(e) or type(e).__name__, a.json)
    tmp = None
    try:
        fd, tmp = tempfile.mkstemp(dir=outdir, prefix=os.path.basename(a.out) + ".tmp-")
        with os.fdopen(fd, "wb") as fh:
            fh.write(out)
            fh.flush()
            os.fsync(fh.fileno())
        os.chmod(tmp, 0o644)
        os.replace(tmp, a.out)
        tmp = None
    except OSError as e:
        return refuse("output-write-failed: %s" % e.strerror, a.json)
    finally:
        if tmp is not None and os.path.exists(tmp):
            os.unlink(tmp)
    info["intact"] = not info["changes"]
    print(json.dumps(info) if a.json else "ok %s" % (",".join(info["changes"]) or "intact"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
