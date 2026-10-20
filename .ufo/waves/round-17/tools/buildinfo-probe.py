#!/usr/bin/env python3
"""buildinfo-probe.py -- independent stdlib reader of the Go build-info blob.

Reads only file bytes; never executes the carrier. Standard library only, so it
is safe under `python3 -I` (no sibling imports, no site packages needed).

Usage:
    buildinfo-probe.py PATH       emit JSON observation on stdout
    buildinfo-probe.py --selftest build temp fixtures, check decoder, exit 0/1

Exit codes: 0 = observation emitted cleanly (including found:false and
pointer_format stops), 2 = could not evaluate (unreadable file, bad input).
`--selftest` prints `SELFTEST: CLEAN cases=N` / `SELFTEST: FAILED ...`.

Source basis: Go `src/debug/buildinfo/buildinfo.go` at tag `go1.25.0`
(raw.githubusercontent.com/golang/go/go1.25.0/src/debug/buildinfo/buildinfo.go,
fetched file sha256 332fff28ac2569b76dda2e9d4f25aacc112e12bd8888fca927db0c5156187f45,
599 lines). Line citations below use "L<n>" against that file.
"""

import argparse
import hashlib
import json
import os
import struct
import sys
import tempfile

# L58: var buildInfoMagic = []byte("\xff Go buildinf:")
MAGIC = b"\xff Go buildinf:"
# L61-62: buildInfoAlign = 16, buildInfoHeaderSize = 32
ALIGN = 16
HEADER_SIZE = 32
# L335: searchChunkSize = 1 << 20
CHUNK = 1 << 20

# L192-194: header field offsets
PTR_SIZE_OFFSET = 14
FLAGS_OFFSET = 15
VERS_PTR_OFFSET = 16

# L196-202: flag masks/values
FLAGS_ENDIAN_MASK = 0x1
FLAGS_ENDIAN_LITTLE = 0x0
FLAGS_ENDIAN_BIG = 0x1
FLAGS_VERSION_MASK = 0x2
FLAGS_VERSION_PTR = 0x0
FLAGS_VERSION_INL = 0x2

# cmd/go/internal/modload infoStart/infoEnd sentinels (L262-265); identical to
# REA's MODULE_START/MODULE_END constants in dist/go/GoBinaryImage.js.
INFO_START = bytes.fromhex("3077af0c9274080241e1c107e6d618e6")
INFO_END = bytes.fromhex("f932433186182072008242104116d8f2")

MAX_STRING = 1 << 20  # probe-side sanity cap on decoded string length


class NotGo(Exception):
    """Counterpart of errNotGoExe (buildinfo.go L52)."""


class Malformed(Exception):
    """Counterpart of errUnrecognizedFormat (buildinfo.go L37)."""


# ---------------------------------------------------------------------------
# ELF parsing (32/64-bit, both endiannesses). Go dispatches on the first 16
# bytes at L120-165; this probe implements the ELF arm (L125-130) and names
# the other formats without decoding them.
# ---------------------------------------------------------------------------

def elf_parse(data):
    if len(data) < 16 or data[:4] != b"\x7fELF":
        raise Malformed("not ELF")
    cls, enc = data[4], data[5]
    if cls not in (1, 2) or enc not in (1, 2):
        raise Malformed("bad EI_CLASS/EI_DATA")
    wide = cls == 2
    bo = "<" if enc == 1 else ">"
    bits = 64 if wide else 32

    def u16(o):
        return struct.unpack_from(bo + "H", data, o)[0]

    def u32(o):
        return struct.unpack_from(bo + "I", data, o)[0]

    def u64(o):
        return struct.unpack_from(bo + "Q", data, o)[0]

    ehsize = 64 if wide else 52
    if len(data) < ehsize:
        raise Malformed("truncated ELF header")
    if wide:
        e_phoff, e_shoff = u64(0x20), u64(0x28)
        e_phentsize, e_phnum = u16(0x36), u16(0x38)
        e_shentsize, e_shnum, e_shstrndx = u16(0x3A), u16(0x3C), u16(0x3E)
    else:
        e_phoff, e_shoff = u32(0x1C), u32(0x20)
        e_phentsize, e_phnum = u16(0x2A), u16(0x2C)
        e_shentsize, e_shnum, e_shstrndx = u16(0x2E), u16(0x30), u16(0x32)

    # Extended numbering: real counts live in section header 0.
    if e_shoff and e_shnum == 0:
        e_shnum = u64(e_shoff + 32) if wide else u32(e_shoff + 20)
    if e_shoff and e_shstrndx == 0xFFFF:
        e_shstrndx = u32(e_shoff + 40) if wide else u32(e_shoff + 24)
    if e_phnum == 0xFFFF and e_shoff:
        e_phnum = u32(e_shoff + 44) if wide else u32(e_shoff + 28)

    progs = []
    for i in range(e_phnum):
        o = e_phoff + i * e_phentsize
        if o + e_phentsize > len(data):
            break
        if wide:
            progs.append({
                "type": u32(o), "flags": u32(o + 4), "offset": u64(o + 8),
                "vaddr": u64(o + 16), "filesz": u64(o + 32),
                "memsz": u64(o + 40),
            })
        else:
            progs.append({
                "type": u32(o), "offset": u32(o + 4), "vaddr": u32(o + 8),
                "filesz": u32(o + 16), "memsz": u32(o + 20),
                "flags": u32(o + 24),
            })

    sections = []
    shstr = b""
    if e_shoff and e_shnum:
        shdrs = []
        for i in range(e_shnum):
            o = e_shoff + i * e_shentsize
            if o + e_shentsize > len(data):
                break
            if wide:
                shdrs.append({
                    "name_off": u32(o), "type": u32(o + 4), "flags": u64(o + 8),
                    "addr": u64(o + 16), "offset": u64(o + 24),
                    "size": u64(o + 32),
                })
            else:
                shdrs.append({
                    "name_off": u32(o), "type": u32(o + 4),
                    "flags": u32(o + 8), "addr": u32(o + 12),
                    "offset": u32(o + 16), "size": u32(o + 20),
                })
        if e_shstrndx < len(shdrs):
            st = shdrs[e_shstrndx]
            shstr = data[st["offset"]:st["offset"] + st["size"]]
        for s in shdrs:
            n = s["name_off"]
            end = shstr.find(b"\x00", n)
            name = shstr[n:end].decode("utf-8", "replace") if 0 <= n < len(shstr) and end >= 0 else ""
            sections.append({**s, "name": name})

    return {"bits": bits, "byte_order": "little" if enc == 1 else "big",
            "progs": progs, "sections": sections}


def elf_search_space(elf):
    """Mirror elfExe.DataStart (L455-466): the `.go.buildinfo` section if
    present (L457-458), else the first PT_LOAD that is writable and not
    executable (L461-463). Returns (label, [(vaddr, size), ...])."""
    for s in elf["sections"]:
        if s["name"] == ".go.buildinfo":
            return ".go.buildinfo section", [(s["addr"], s["size"])]
    for p in elf["progs"]:
        if p["type"] == 1 and (p["flags"] & 0x3) == 0x2:  # PT_LOAD, W&&!X
            return "first writable non-executable PT_LOAD", [(p["vaddr"], p["memsz"])]
    return None, []


def elf_data_reader(elf, data):
    """Map a virtual address to file bytes like elfExe.DataReader (L445-453):
    first program header with vaddr <= addr <= vaddr+filesz-1, file offset
    p_offset + (addr - vaddr), readable through filesz."""

    def read(addr, size):
        for p in elf["progs"]:
            if p["filesz"] and p["vaddr"] <= addr <= p["vaddr"] + p["filesz"] - 1:
                remaining = p["vaddr"] + p["filesz"] - addr
                off = p["offset"] + (addr - p["vaddr"])
                return data[off:off + min(size, remaining)]
        raise Malformed("address 0x%x not file-backed by any program header" % addr)

    return read


def file_offset_of_vaddr(elf, addr):
    for p in elf["progs"]:
        if p["filesz"] and p["vaddr"] <= addr <= p["vaddr"] + p["filesz"] - 1:
            return p["offset"] + (addr - p["vaddr"])
    return None


# ---------------------------------------------------------------------------
# Magic search, varint strings -- mirrors of searchMagic (L339-397) and
# decodeString (L284-318).
# ---------------------------------------------------------------------------

def search_magic(read, start, size):
    """L339-397: scan [start, start+size) for an aligned 14-byte magic; the
    magic must leave >= 32 header bytes before the end of the range."""
    end = start + size
    if end < start:
        raise Malformed("search range overflow")
    start = (start + ALIGN - 1) & ~(ALIGN - 1)  # L347
    if start >= end:
        raise NotGo("aligned start past end of range")
    while start < end:
        remaining = end - start
        chunk_size = min(CHUNK, remaining)
        buf = read(start, chunk_size)
        data = buf
        if not data:
            break
        # Go keeps scanning a short tail then stops; a short read means the
        # rest of the range is not file-backed, so nothing more can match.
        data_offset = 0
        while len(data) > data_offset:
            i = data.find(MAGIC, data_offset)
            if i < 0:
                break
            if remaining - i < HEADER_SIZE:  # L388-390
                raise NotGo("magic without 32 header bytes in range")
            if i % ALIGN != 0:  # L392-402: skip to next aligned offset
                data_offset = (i + ALIGN - 1) & ~(ALIGN - 1)
                continue
            return start + i
        if len(buf) < chunk_size:
            break
        start += chunk_size
    raise NotGo("build info magic not found")


def uvarint(buf, off):
    """encoding/binary Uvarint semantics: (value, n); n<=0 on truncation or
    64-bit overflow. decodeString rejects n<=0 at L297-299."""
    result = 0
    for i in range(10):
        if off + i >= len(buf):
            return 0, 0
        b = buf[off + i]
        if i == 9 and b > 1:
            return 0, -(i + 1)
        result |= (b & 0x7F) << (7 * i)
        if b < 0x80:
            return result, i + 1
    return 0, -10


def decode_string(read, addr):
    """L284-318: uvarint length then length bytes; short reads -> NotGo."""
    hdr = read(addr, 10)
    length, n = uvarint(hdr, 0)
    if n <= 0:
        raise NotGo("bad varint at 0x%x" % addr)
    addr += n
    if length > MAX_STRING:
        raise NotGo("string length %d exceeds probe cap" % length)
    b = read(addr, length)
    if len(b) < length:
        raise NotGo("string body truncated at 0x%x" % addr)
    return b.decode("utf-8", "replace"), addr + length, n


# ---------------------------------------------------------------------------
# Probe driver
# ---------------------------------------------------------------------------

def sniff_format(data):
    if data[:4] == b"\x7fELF":
        return "elf"
    if data[:2] == b"MZ":
        return "pe"
    if data[:4] in (b"\xfe\xed\xfa\xce", b"\xfe\xed\xfa\xcf",
                    b"\xce\xfa\xed\xfe", b"\xcf\xfa\xed\xfe",
                    b"\xca\xfe\xba\xbe", b"\xca\xfe\xba\xbf"):
        return "macho"
    if data[:2] in (b"\x01\xdf", b"\x01\xf7"):
        return "xcoff"
    return "unrecognized"


def all_magic_offsets(data):
    out = []
    i = 0
    while True:
        i = data.find(MAGIC, i)
        if i < 0:
            return out
        out.append(i)
        i += 1


def probe(path):
    lim = [
        "ELF only: PE/Mach-O/XCOFF/Plan 9 are sniffed but not decoded "
        "(buildinfo.go dispatches them at L134-165).",
        "Embedded bytes are file content, not proof of toolchain identity; "
        "an absent blob does not prove the binary is not Go.",
        "Reads are bounded by PT_LOAD p_filesz like elfExe.DataReader "
        "(L445-453); range bytes past file-backed extents behave as EOF.",
    ]
    with open(path, "rb") as f:
        data = f.read()
    out = {
        "path": os.path.abspath(path),
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
        "format": sniff_format(data),
        "found": False,
        "search_space": None,
        "header_offset": None,
        "header_vaddr": None,
        "flags": None,
        "ptr_size": None,
        "endian": None,
        "inline": False,
        "pointer_format": False,
        "go_version": None,
        "modinfo_first_line": None,
        "magic_file_offsets": all_magic_offsets(data),
        "limitations": lim,
    }
    if out["format"] != "elf":
        lim.append("format %r is not decoded by this probe; magic scan is "
                   "unrestricted-file only." % out["format"])
        return out

    elf = elf_parse(data)
    label, ranges = elf_search_space(elf)
    if not ranges:
        lim.append("no .go.buildinfo section and no writable non-executable "
                   "PT_LOAD segment -> Go DataStart size 0 -> errNotGoExe "
                   "(L170-172, L455-466).")
        return out
    out["search_space"] = label

    read = elf_data_reader(elf, data)
    addr = None
    for vaddr, size in ranges:
        if size == 0:
            continue
        try:
            addr = search_magic(read, vaddr, size)
            break
        except NotGo:
            continue
    if addr is None:
        lim.append("no aligned magic with a full 32-byte header inside Go's "
                   "search range (L339-397); unrestricted whole-file scan is "
                   "reported in magic_file_offsets.")
        return out

    header = read(addr, HEADER_SIZE)
    if len(header) < HEADER_SIZE:
        lim.append("magic matched but fewer than 32 header bytes are "
                   "file-backed -> errNotGoExe (L181-188).")
        return out

    flags = header[FLAGS_OFFSET]
    ptr_size = header[PTR_SIZE_OFFSET]
    out.update({
        "found": True,
        "header_vaddr": "0x%x" % addr,
        "header_offset": file_offset_of_vaddr(elf, addr),
        "flags": flags,
        "ptr_size": ptr_size,
        "endian": "big" if (flags & FLAGS_ENDIAN_MASK) == FLAGS_ENDIAN_BIG
                  else "little",
    })
    if flags & ~0x3:
        lim.append("flags 0x%02x carry bits outside Go's 0x3 mask; Go decodes "
                   "mask-only (L196-202) while REA 6.5.0 rejects unknown flag "
                   "bits outright." % flags)

    if (flags & FLAGS_VERSION_MASK) != FLAGS_VERSION_INL:
        # L218-222, L239-258: pre-1.18 pointer format. Contract: report
        # pointer_format and stop, version null.
        bo = ">" if out["endian"] == "big" else "<"
        vptr = mptr = None
        if ptr_size == 4:
            vptr, mptr = (struct.unpack_from(bo + "I", header, VERS_PTR_OFFSET)[0],
                          struct.unpack_from(bo + "I", header, VERS_PTR_OFFSET + 4)[0])
        elif ptr_size == 8:
            vptr, mptr = (struct.unpack_from(bo + "Q", header, VERS_PTR_OFFSET)[0],
                          struct.unpack_from(bo + "Q", header, VERS_PTR_OFFSET + 8)[0])
        else:
            lim.append("ptr_size %d is neither 4 nor 8 -> Go errNotGoExe "
                       "(L251-254)." % ptr_size)
        out.update({
            "pointer_format": True,
            "vers_ptr": ("0x%x" % vptr) if vptr is not None else None,
            "mod_ptr": ("0x%x" % mptr) if mptr is not None else None,
        })
        lim.append("pre-1.18 pointer-format header; vers/mod string pointers "
                   "are reported but not dereferenced per contract.")
        return out

    out["inline"] = True
    vers, next_addr, vers_varint = decode_string(read, addr + HEADER_SIZE)
    mod, _, mod_varint = decode_string(read, next_addr)
    if vers == "":
        lim.append("decoded version string is empty -> Go errNotGoExe "
                   "(L259-260).")
        return out
    out["go_version"] = vers

    # L262-267: module framing sentinel check; invalid framing discards mod.
    if len(mod) >= 33 and mod[len(mod) - 17] == "\n":
        mod = mod[16:len(mod) - 16]
        out["modinfo_first_line"] = mod.split("\n", 1)[0] or None
    else:
        if mod:
            lim.append("module framing sentinel absent -> modinfo discarded "
                       "like Go L262-267.")
    return out


# ---------------------------------------------------------------------------
# Selftest: build minimal ELF64-LE fixtures in a temp dir and check decoding.
# ---------------------------------------------------------------------------

def _uvarint(n):
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)


def _inline_blob(vers, mod):
    hdr = bytearray(MAGIC)
    hdr += bytes([0, FLAGS_VERSION_INL])  # ptr_size unused, flags = inline
    hdr += bytes(HEADER_SIZE - len(hdr))
    return bytes(hdr) + _uvarint(len(vers)) + vers + _uvarint(len(mod)) + mod


def _ptr_blob(flags, ptr_size):
    hdr = bytearray(MAGIC)
    hdr += bytes([ptr_size, flags])
    hdr += bytes(HEADER_SIZE - len(hdr))
    return bytes(hdr)


def make_elf64le(blobs, *, with_section=True, seg_flags=0x6, tail_pad=0):
    """One PT_LOAD covering the whole file (vaddr = 0x400000 + offset, so the
    vaddr->file translation is exercised), optional .go.buildinfo section, and
    blobs placed at chosen file offsets."""
    base = 0x400000
    phoff = 64
    filesz_cursor = phoff + 56
    placed = []
    cursor = filesz_cursor
    for off, blob in sorted(blobs):
        cursor = max(cursor, off)
        placed.append((cursor, bytes(blob)))
        cursor += len(blob)
    body = bytearray(cursor + tail_pad)
    # ELF64 header
    body[0:4] = b"\x7fELF"
    body[4] = 2  # 64-bit
    body[5] = 1  # little
    body[6] = 1
    struct.pack_into("<HHIQQQIHHHHHH", body, 16,
                     2, 0x3E, 1, 0, phoff, 0, 0, 64, 56, 1, 0, 0, 0)
    # program header: PT_LOAD covering [0, len(body))
    struct.pack_into("<IIQQQQQQ", body, phoff,
                     1, seg_flags, 0, base, base, len(body), len(body), 0x1000)
    for off, blob in placed:
        body[off:off + len(blob)] = blob
    if with_section:
        names = b"\x00.go.buildinfo\x00.shstrtab\x00"
        noff = len(body)
        body += names
        while len(body) % 8:
            body += b"\x00"
        shoff = len(body)
        bi_off, bi_blob = placed[0]
        shdrs = [
            (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            (1, 1, 0x3, base + bi_off, bi_off, len(bi_blob), 0, 0, 16, 0),
            (15, 3, 0, 0, noff, len(names), 0, 0, 1, 0),
        ]
        for sh in shdrs:
            body += struct.pack("<IIQQQQIIQQ", *sh)
        struct.pack_into("<Q", body, 0x28, shoff)   # e_shoff
        struct.pack_into("<HHH", body, 0x3A, 64, len(shdrs), 2)
    return bytes(body)


def selftest():
    tmp = tempfile.mkdtemp(prefix="buildinfo-probe-")
    cases = 0
    failures = []

    def check(name, path, **expect):
        nonlocal cases
        cases += 1
        try:
            got = probe(path)
        except Exception as e:  # noqa: BLE001
            failures.append("%s: raised %r" % (name, e))
            return
        for k, v in expect.items():
            if got.get(k) != v:
                failures.append("%s: %s = %r, expected %r" % (name, k, got.get(k), v))

    try:
        # 1. inline via .go.buildinfo section
        mod = INFO_START + b"path\texample.com/m\nmod\texample.com/m\tv1.0.0\t\n" + b"\n" + INFO_END
        p = os.path.join(tmp, "inline-sec")
        open(p, "wb").write(make_elf64le([(4096, _inline_blob(b"go1.25.0", mod))]))
        check("inline-section", p, found=True, go_version="go1.25.0",
              inline=True, flags=FLAGS_VERSION_INL,
              search_space=".go.buildinfo section",
              modinfo_first_line="path\texample.com/m")

        # 2. inline via writable-segment fallback, no section headers at all
        p = os.path.join(tmp, "inline-seg")
        open(p, "wb").write(make_elf64le([(8192, _inline_blob(b"go1.20.12", b""))],
                                         with_section=False))
        check("inline-segment", p, found=True, go_version="go1.20.12",
              search_space="first writable non-executable PT_LOAD",
              modinfo_first_line=None)

        # 3. pointer format (flags 0x0), ptr_size 8 -> report and stop
        p = os.path.join(tmp, "ptr")
        open(p, "wb").write(make_elf64le([(4096, _ptr_blob(0x0, 8))]))
        check("pointer-format", p, found=True, pointer_format=True,
              inline=False, ptr_size=8, go_version=None, endian="little")

        # 4. big-endian pointer format, ptr_size 4
        p = os.path.join(tmp, "ptrbe")
        open(p, "wb").write(make_elf64le([(4096, _ptr_blob(0x1, 4))]))
        check("pointer-format-be", p, found=True, pointer_format=True,
              ptr_size=4, endian="big", go_version=None)

        # 5. no magic anywhere -> found:false, empty scan
        p = os.path.join(tmp, "nomagic")
        open(p, "wb").write(make_elf64le([(4096, b"not build info at all")],
                                         with_section=False))
        check("no-magic", p, found=False, go_version=None,
              magic_file_offsets=[])

        # 6. misaligned magic is skipped; the aligned one wins
        real = _inline_blob(b"go1.23.12", b"")
        p = os.path.join(tmp, "misaligned")
        elf = bytearray(make_elf64le([(4096, b"\x00" * 16 + MAGIC + b"junk"),
                                      (4160, real)], with_section=False))
        open(p, "wb").write(bytes(elf))
        check("misaligned-then-aligned", p, found=True, go_version="go1.23.12",
              header_vaddr="0x401040")

        # 7. magic with <32 bytes remaining in range -> not found
        p = os.path.join(tmp, "trunc")
        blob = MAGIC + b"\x08\x02"  # 16 bytes only, at end of filesz
        open(p, "wb").write(make_elf64le([(4096, blob)], with_section=False))
        check("truncated-header", p, found=False)

        # 8. empty version string -> found but go_version null (Go errNotGoExe)
        p = os.path.join(tmp, "emptyvers")
        open(p, "wb").write(make_elf64le([(4096, _inline_blob(b"", b"x"))],
                                         with_section=False))
        check("empty-version", p, found=True, go_version=None)

        # 9. non-ELF input -> clean negative
        p = os.path.join(tmp, "mz")
        open(p, "wb").write(b"MZ" + b"\x00" * 256)
        check("pe-sniff", p, found=False, format="pe", go_version=None)

        # 10. unknown flag bits beyond 0x3 are tolerated mask-only like Go
        p = os.path.join(tmp, "extrabits")
        blob = bytearray(_inline_blob(b"go9.9.9", b""))
        blob[FLAGS_OFFSET] = 0x2 | 0x40
        open(p, "wb").write(make_elf64le([(4096, bytes(blob))],
                                         with_section=False))
        check("extra-flag-bits", p, found=True, go_version="go9.9.9",
              flags=0x42)

        # 11. magic only in a non-writable segment with no RW fallback
        p = os.path.join(tmp, "rxonly")
        open(p, "wb").write(make_elf64le([(4096, _inline_blob(b"go1.21.0", b""))],
                                         with_section=False, seg_flags=0x5))
        check("rx-only-segment", p, found=False)
    finally:
        for root, dirs, files in os.walk(tmp, topdown=False):
            for fn in files:
                os.remove(os.path.join(root, fn))
            for d in dirs:
                os.rmdir(os.path.join(root, d))
        os.rmdir(tmp)

    if failures:
        print("SELFTEST: FAILED %s" % "; ".join(failures), file=sys.stdout)
        return 1
    print("SELFTEST: CLEAN cases=%d" % cases)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Read the Go build-info blob from a binary (read-only; "
                    "never executes the carrier). JSON on stdout.")
    ap.add_argument("path", nargs="?", help="binary to inspect")
    ap.add_argument("--selftest", action="store_true",
                    help="build temp fixtures, verify decoder, exit 0/1")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.path:
        ap.error("PATH is required unless --selftest")
    try:
        result = probe(args.path)
    except OSError as e:
        json.dump({"path": args.path, "error": "unreadable: %s" % e},
                  sys.stdout, sort_keys=True, indent=2)
        sys.stdout.write("\n")
        return 2
    except Malformed as e:
        json.dump({"path": args.path, "error": "malformed: %s" % e},
                  sys.stdout, sort_keys=True, indent=2)
        sys.stdout.write("\n")
        return 2
    json.dump(result, sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
