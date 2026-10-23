#!/usr/bin/env python3
"""R34 scratch-only GNU ELF symbol-version requirements reader (stdlib only).

Scope: static interpretation of already-built ELF64 little-endian x86_64/AArch64
images.  The only metadata interpreted is SHT_GNU_verneed (0x6ffffffe): the linked
SHT_STRTAB, the Elf64_Verneed chain, its Elf64_Vernaux chains, and the dependency
and version name strings those entries point at.

Non-goals: this is not exploitation, vulnerability, loader, ABI-correctness,
authenticity, signature or execution evidence.  It does not execute the input,
does not resolve symbols, does not read .gnu.version_d or .gnu.version, and does
not reconstruct synthetic ELF images.

API::

    result = parse(data: bytes) -> {"schema": 1, "needed": [{"file": str,
        "versions": [{"name": str, "flags": int, "other": int, "hash": int}]}]}

Canonical output: JSON with sort_keys=True, separators=(",", ":") and
ensure_ascii=True.  ``needed`` is sorted by ``file``; each ``versions`` list is
sorted by ``(name, other, flags, hash)`` (parent contract: file, name, other).

Rejections raise ElfError carrying one declared finding id.  ``--findings``
emits the full decision table with exact bounds and source anchors;
``--selftest`` runs text-built metadata-helper checks and, when ``--binaries``
is given, bounded outer checks against existing public ELF files (never against
the round's production read list).

vna_hash is emitted verbatim from the file.  This reader never recomputes or
compares a hash, never constrains names to GLIBC-like patterns, and decodes
name bytes losslessly as Latin-1.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import shutil
import struct
import subprocess
import sys

SCHEMA = 1
PROFILE = "r34-elf-verneed/1"
SCOPE = (
    "bounded structural decoding of declared GNU version-need metadata in existing ELF64 "
    "little-endian x86_64/AArch64 images; success never proves loader behavior, ABI "
    "correctness, authenticity or executability"
)

SHT_NULL = 0
SHT_STRTAB = 3
SHT_GNU_VERNEED = 0x6FFFFFFE

ELFCLASS64 = 2
ELFDATA2LSB = 1
EV_CURRENT = 1
ELFOSABI_NONE = 0
ELFOSABI_GNU = 3

ET_EXEC = 2
ET_DYN = 3
EM_X86_64 = 62
EM_AARCH64 = 183

ELF_HDR_SIZE = 64
SHDR_SIZE = 64
VERNEED_SIZE = 16
VERNAUX_SIZE = 16
VER_NEED_CURRENT = 1

LIMITS = {
    "max_input_bytes": 1 << 29,          # 536,870,912 bytes; CLI/file read cap.
    "max_verneed_entries": 1024,         # sh_info cap (real GNU output: single digits).
    "max_verneed_bytes": 1 << 16,        # 65,536 bytes for one .gnu.version_r.
    "max_aux_entries": 4096,             # sum of vn_cnt over all entries.
    "max_string_bytes": 1024,            # name length cap inside the linked strtab.
}

H_A = "/usr/include/elf.h (glibc 2.44+r50+g1848099f063e-1; sha256 c81533b751ce45e737d91c49a3a2ed5123b0dbc7006259a40ccb3904221847ca)"
R_A = "binutils-2_47 binutils/readelf.c (sourceware.org git hb=binutils-2_47; sha256 7e81eedf19b2b93663bb3f598f74b54c107bd699f551667eb1b3d0e33eddeeff)"
L_A = "LSB 5.0.0 LSB-Core-generic/symversion.html (sha256 982fe1208c76eda09d8619f3907783899e4e73b19c34f3e22314fb36cc8f7f91)"


def _row(fid, classification, stage, check, bound, kind, anchor):
    return {
        "id": fid,
        "classification": classification,
        "stage": stage,
        "check": check,
        "bound": bound,
        "bound_kind": kind,
        "anchor": anchor,
    }


# Precedence order: a single input is checked top-to-bottom; the last applicable row wins
# first.  Every id here has at least one literal raise site in this file (asserted by --selftest).
FINDINGS = [
    _row("error.malformed.elf_header_bounds", "malformed", "header",
         "input is long enough to hold Elf64_Ehdr", "len(data) >= 64", "format",
         H_A + ":81-97 (Elf64_Ehdr)"),
    _row("error.malformed.elf_magic", "malformed", "header",
         "ELF identification bytes", 'data[0:4] == b"\\x7fELF"', "format",
         H_A + ":103-114 (EI_MAG0..EI_MAG3)"),
    _row("error.unsupported.elf_class", "unsupported", "header",
         "64-bit image", "e_ident[EI_CLASS] == ELFCLASS64 (2)", "format",
         H_A + ":119-122"),
    _row("error.unsupported.elf_data", "unsupported", "header",
         "little-endian image", "e_ident[EI_DATA] == ELFDATA2LSB (1)", "format",
         H_A + ":125-127"),
    _row("error.malformed.ident_version", "malformed", "header",
         "identification version is current", "e_ident[EI_VERSION] == EV_CURRENT (1)", "format",
         H_A + ":131-132,378"),
    _row("error.unsupported.osabi", "unsupported", "header",
         "OS ABI is System V or GNU/Linux", "e_ident[EI_OSABI] in {0, 3}", "format",
         H_A + ":135-140"),
    _row("error.malformed.elf_version", "malformed", "header",
         "object version field is current", "e_version == EV_CURRENT (1)", "format",
         H_A + ":86,378"),
    _row("error.unsupported.elf_type", "unsupported", "header",
         "executable or shared object", "e_type in {ET_EXEC (2), ET_DYN (3)}", "format",
         H_A + ":160-161"),
    _row("error.unsupported.machine", "unsupported", "header",
         "x86_64 or AArch64", "e_machine in {EM_X86_64 (62), EM_AARCH64 (183)}", "format",
         H_A + ":219,317"),
    _row("error.malformed.ehsize", "malformed", "header",
         "ELF header size field is the ELF64 size", "e_ehsize == 64", "format",
         H_A + ":92,81-97"),
    _row("error.malformed.shentsize", "malformed", "header",
         "section header entry size is the ELF64 size", "e_shentsize == 64", "format",
         H_A + ":95,397-409 (Elf64_Shdr)"),
    _row("error.unsupported.no_section_table", "unsupported", "header",
         "section header table is present", "e_shoff != 0", "profile",
         H_A + ":87; " + R_A + ":14020 (dispatch is per section header)"),
    _row("error.unsupported.shnum_extended", "unsupported", "header",
         "plain section count (extended numbering not supported)", "e_shnum != 0", "profile",
         H_A + ":91 (e_shnum)"),
    _row("error.malformed.shoff_bounds", "malformed", "header",
         "section header table lies inside the file and after the ELF header",
         "64 <= e_shoff and e_shoff + e_shnum*64 <= len(data)", "format",
         H_A + ":87,91,397-409"),
    _row("error.malformed.sh0_type", "malformed", "sections",
         "section zero is the reserved null entry", "section[0].sh_type == SHT_NULL (0)", "format",
         H_A + ":430,397-409"),
    _row("error.malformed.verneed_bounds", "malformed", "verneed",
         "version-needs section lies inside the file", "sh_offset + sh_size <= len(data)", "format",
         H_A + ":397-409; " + R_A + ":14050-14056 (get_data)"),
    _row("error.unsupported.multiple_verneed", "unsupported", "verneed",
         "at most one SHT_GNU_verneed section is declared",
         "count(sh_type == SHT_GNU_verneed (0x6ffffffe)) <= 1", "profile",
         R_A + ":9089,14020 (readelf would print each section separately)"),
    _row("error.malformed.verneed_link", "malformed", "verneed",
         "sh_link names another existing section", "1 <= sh_link < e_shnum", "format",
         L_A + " (vn_file/vna_name are 'in the section header'); " + R_A + ":14061-14070"),
    _row("error.malformed.verneed_link_type", "malformed", "verneed",
         "linked section is a string table", "section[sh_link].sh_type == SHT_STRTAB (3)", "format",
         H_A + ":433 (SHT_STRTAB); " + L_A),
    _row("error.malformed.strtab_bounds", "malformed", "strtab",
         "linked string table lies inside the file", "link.sh_offset + link.sh_size <= len(data)", "format",
         H_A + ":397-409"),
    _row("error.malformed.verneed_count", "malformed", "verneed",
         "declared entry count matches the section body",
         "sh_info==0 => sh_size==0; sh_info>0 => sh_size>=16 and every entry fits", "format",
         R_A + ":14042-14058 (cnt < section->sh_info); " + L_A + " (vn_cnt)"),
    _row("error.unsupported.verneed_entries", "unsupported", "verneed",
         "declared entry count is within the profile bound", "sh_info <= 1024", "profile",
         "LIMITS.max_verneed_entries"),
    _row("error.unsupported.verneed_bytes", "unsupported", "verneed",
         "section body is within the profile bound", "sh_size <= 65536", "profile",
         "LIMITS.max_verneed_bytes"),
    _row("error.unsupported.verneed_revision", "unsupported", "entry",
         "structure revision is the defined current revision", "vn_version == 1", "format",
         L_A + " ('currently set to 1'); " + H_A + ":1140 (VER_NEED_CURRENT)"),
    _row("error.malformed.verneed_align", "malformed", "entry",
         "entry and aux offsets are naturally 4-byte aligned",
         "offset % 4 == 0 for each verneed, vn_aux target and vna_next target", "format",
         H_A + ":1128-1135,1157-1163 (Elf64_Half/Elf64_Word members)"),
    _row("error.malformed.verneed_next", "malformed", "entry",
         "vn_next forms one forward chain that exactly covers the declared entries",
         "last: vn_next==0; other: vn_next>=16, target>offset, target+16<=sh_size", "format",
         L_A + " (vn_next); " + R_A + ":14138-14151 (invalid/overflow checks)"),
    _row("error.malformed.verneed_aux", "malformed", "entry",
         "vn_aux is zero iff vn_cnt is zero; otherwise it points inside the body",
         "vn_cnt==0 => vn_aux==0; vn_cnt>0 => 16<=vn_aux and vn_aux+16<=sh_size", "format",
         L_A + " (vn_aux); " + R_A + ":14079-14087"),
    _row("error.unsupported.aux_entries", "unsupported", "aux",
         "auxiliary entry total is within the profile bound", "sum(vn_cnt) <= 4096", "profile",
         "LIMITS.max_aux_entries"),
    _row("error.malformed.aux_count", "malformed", "aux",
         "every declared auxiliary entry fits in the section body",
         "for each of vn_cnt entries: cursor+16 <= sh_size", "format",
         R_A + ":14096-14109; " + L_A + " (vn_cnt)"),
    _row("error.malformed.aux_next", "malformed", "aux",
         "vna_next forms one forward chain of exactly vn_cnt entries",
         "last: vna_next==0; other: vna_next>=16, target>cursor, target+16<=sh_size", "format",
         L_A + " (vna_next); " + R_A + ":14118-14134 (invalid/overflow checks)"),
    _row("error.malformed.strtab_offset", "malformed", "strings",
         "string offset lies inside the linked string table", "0 <= offset < link.sh_size", "format",
         L_A + " (vn_file/vna_name are section-relative offsets); " + R_A + ":14070,14111"),
    _row("error.malformed.string_unterminated", "malformed", "strings",
         "name is NUL-terminated inside the linked string table",
         "b'\\x00' exists in [offset, link.sh_size)", "format",
         "ELF string-table convention; " + L_A),
    _row("error.malformed.string_too_long", "malformed", "strings",
         "name length is within the profile bound", "end - start <= 1024", "profile",
         "LIMITS.max_string_bytes"),
    _row("error.malformed.verneed_overlap", "malformed", "coverage",
         "parsed 16-byte entry spans do not overlap", "16-byte spans are pairwise disjoint", "profile",
         H_A + ":1128-1135,1157-1163; GNU ld lays a verneed entry before its own aux chain"),
    _row("error.malformed.verneed_unreferenced", "malformed", "coverage",
         "bytes outside parsed spans are zero padding",
         "every byte not covered by a parsed span == 0x00", "profile",
         R_A + ":14142-14155 (readelf ignores unreferenced bytes); GNU ld emits exact size"),
    _row("error.io.read", "io", "io",
         "CLI input can be opened and read", "os.stat/os.open/read succeed", "profile",
         "CLI boundary; parse() takes bytes and performs no I/O"),
    _row("error.io.size", "io", "io",
         "CLI input stays inside the read cap", "file size <= 536870912 bytes", "profile",
         "LIMITS.max_input_bytes"),
]

FINDING_INDEX = {f["id"]: i for i, f in enumerate(FINDINGS)}
assert len(FINDING_INDEX) == len(FINDINGS)

EXIT_BY_CLASS = {"malformed": 12, "unsupported": 11, "io": 13}


def _classify(finding_id):
    for cls, prefix in (("malformed", "error.malformed."),
                        ("unsupported", "error.unsupported."),
                        ("io", "error.io.")):
        if finding_id.startswith(prefix):
            return cls
    raise ValueError("undeclared finding id: %r" % (finding_id,))


class ElfError(Exception):
    """A declared rejection.  ``finding_id`` is the machine-readable identity."""

    def __init__(self, finding_id, reason, **detail):
        super().__init__(finding_id + ": " + reason)
        self.finding_id = finding_id
        self.classification = _classify(finding_id)
        self.reason = reason
        self.detail = detail

    def as_dict(self):
        return {
            "schema": SCHEMA,
            "finding_id": self.finding_id,
            "classification": self.classification,
            "reason": self.reason,
            "detail": self.detail,
        }


def _fail(finding_id, reason, **detail):
    raise ElfError(finding_id, reason, **detail)


def _u16(b, off):
    return struct.unpack_from("<H", b, off)[0]


def _u32(b, off):
    return struct.unpack_from("<I", b, off)[0]


def _u64(b, off):
    return struct.unpack_from("<Q", b, off)[0]


def _cstring(b, base, size, off, field):
    """Decode one NUL-terminated name at ``off`` inside [base, base+size).

    Byte-preserving Latin-1 decode: no charset or pattern validation (parent directive).
    The scan is bounded by ``max_string_bytes`` so a huge unterminated region cannot be
    walked without limit.
    """
    if off >= size:
        _fail("error.malformed.strtab_offset", "string offset outside linked string table",
              field=field, offset=off, size=size)
    start = base + off
    limit = base + size
    scan = min(limit, start + LIMITS["max_string_bytes"] + 1)
    end = b.find(b"\x00", start, scan)
    if end < 0:
        if scan < limit:
            _fail("error.malformed.string_too_long", "string exceeds profile length bound",
                  field=field, offset=off, bound=LIMITS["max_string_bytes"])
        _fail("error.malformed.string_unterminated", "string is not NUL-terminated",
              field=field, offset=off, size=size)
    return b[start:end].decode("latin-1")


def _shdr(b, shoff, index):
    """Return (sh_type, sh_offset, sh_size, sh_link, sh_info) for one section header.

    Callers must have bounded the whole section table already.
    """
    off = shoff + index * SHDR_SIZE
    return (_u32(b, off + 4), _u64(b, off + 24), _u64(b, off + 32),
            _u32(b, off + 40), _u32(b, off + 44))


def _assemble(entries):
    """Sort and shape parsed entries into the canonical schema object."""
    needed = []
    for entry in entries:
        versions = sorted(
            (dict(v) for v in entry["versions"]),
            key=lambda v: (v["name"], v["other"], v["flags"], v["hash"]),
        )
        needed.append({"file": entry["file"], "versions": versions})
    needed.sort(key=lambda e: e["file"])  # stable: duplicate file names keep section order
    return {"schema": SCHEMA, "needed": needed}


def parse(data):
    """Parse ``data`` (bytes-like) and return the canonical version-needs object.

    Raises ElfError with a declared finding id for unsupported or malformed input.
    """
    if not isinstance(data, (bytes, bytearray, memoryview)):
        raise TypeError("parse() takes a bytes-like object")
    b = bytes(data)
    n = len(b)

    if n < ELF_HDR_SIZE:
        _fail("error.malformed.elf_header_bounds", "input shorter than an ELF64 header",
              need=ELF_HDR_SIZE, have=n)
    if b[0:4] != b"\x7fELF":
        _fail("error.malformed.elf_magic", "ELF identification bytes absent",
              have=b[0:4].hex())
    if b[4] != ELFCLASS64:
        _fail("error.unsupported.elf_class", "not ELFCLASS64", have=b[4])
    if b[5] != ELFDATA2LSB:
        _fail("error.unsupported.elf_data", "not ELFDATA2LSB", have=b[5])
    if b[6] != EV_CURRENT:
        _fail("error.malformed.ident_version", "EI_VERSION is not EV_CURRENT", have=b[6])
    if b[7] not in (ELFOSABI_NONE, ELFOSABI_GNU):
        _fail("error.unsupported.osabi", "OS ABI outside {SYSV, GNU/Linux}", have=b[7])

    e_type = _u16(b, 16)
    e_machine = _u16(b, 18)
    e_version = _u32(b, 20)
    e_shoff = _u64(b, 40)
    e_ehsize = _u16(b, 52)
    e_shentsize = _u16(b, 58)
    e_shnum = _u16(b, 60)

    if e_version != EV_CURRENT:
        _fail("error.malformed.elf_version", "e_version is not EV_CURRENT", have=e_version)
    if e_type not in (ET_EXEC, ET_DYN):
        _fail("error.unsupported.elf_type", "ELF type outside {ET_EXEC, ET_DYN}", have=e_type)
    if e_machine not in (EM_X86_64, EM_AARCH64):
        _fail("error.unsupported.machine", "machine outside {x86_64, AArch64}", have=e_machine)
    if e_ehsize != ELF_HDR_SIZE:
        _fail("error.malformed.ehsize", "e_ehsize is not 64", have=e_ehsize)
    if e_shentsize != SHDR_SIZE:
        _fail("error.malformed.shentsize", "e_shentsize is not 64", have=e_shentsize)
    if e_shoff == 0:
        _fail("error.unsupported.no_section_table", "no section header table offset")
    if e_shnum == 0:
        _fail("error.unsupported.shnum_extended", "extended section numbering is outside profile")
    if e_shoff < ELF_HDR_SIZE or e_shoff + e_shnum * SHDR_SIZE > n:
        _fail("error.malformed.shoff_bounds", "section header table outside file bounds",
              shoff=e_shoff, shnum=e_shnum, size=n)
    if _u32(b, e_shoff + 4) != SHT_NULL:
        _fail("error.malformed.sh0_type", "section zero is not SHT_NULL",
              have=_u32(b, e_shoff + 4))

    hits = []
    for i in range(e_shnum):
        if _u32(b, e_shoff + i * SHDR_SIZE + 4) == SHT_GNU_VERNEED:
            hits.append(i)
    if not hits:
        return _assemble([])
    if len(hits) > 1:
        _fail("error.unsupported.multiple_verneed", "multiple version-needs sections",
              indices=hits)

    index = hits[0]
    _, sh_offset, sh_size, sh_link, sh_info = _shdr(b, e_shoff, index)
    if sh_offset + sh_size > n:
        _fail("error.malformed.verneed_bounds", "version-needs section outside file bounds",
              offset=sh_offset, size=sh_size, file_size=n)
    if sh_link == 0 or sh_link >= e_shnum:
        _fail("error.malformed.verneed_link", "sh_link outside section table",
              link=sh_link, shnum=e_shnum)
    link_type, link_offset, link_size, _, _ = _shdr(b, e_shoff, sh_link)
    if link_type != SHT_STRTAB:
        _fail("error.malformed.verneed_link_type", "sh_link is not SHT_STRTAB",
              link=sh_link, have=link_type)
    if link_offset + link_size > n:
        _fail("error.malformed.strtab_bounds", "linked string table outside file bounds",
              offset=link_offset, size=link_size, file_size=n)

    if sh_info == 0:
        if sh_size != 0:
            _fail("error.malformed.verneed_count", "entries declared zero but section is not empty",
                  info=sh_info, size=sh_size)
        return _assemble([])
    if sh_size < VERNEED_SIZE:
        _fail("error.malformed.verneed_count", "section too small for one verneed entry",
              info=sh_info, size=sh_size)
    if sh_info > LIMITS["max_verneed_entries"]:
        _fail("error.unsupported.verneed_entries", "entry count above profile bound",
              info=sh_info, bound=LIMITS["max_verneed_entries"])
    if sh_size > LIMITS["max_verneed_bytes"]:
        _fail("error.unsupported.verneed_bytes", "section size above profile bound",
              size=sh_size, bound=LIMITS["max_verneed_bytes"])

    section = b[sh_offset:sh_offset + sh_size]
    entries = []
    spans = []
    off = 0
    total_aux = 0

    for i in range(sh_info):
        if off + VERNEED_SIZE > sh_size:
            _fail("error.malformed.verneed_count", "declared entry does not fit in section body",
                  index=i, offset=off, size=sh_size)
        if off % 4:
            _fail("error.malformed.verneed_align", "verneed offset is not 4-byte aligned",
                  index=i, offset=off)
        spans.append((off, "verneed"))

        vn_version = _u16(section, off)
        vn_cnt = _u16(section, off + 2)
        vn_file = _u32(section, off + 4)
        vn_aux = _u32(section, off + 8)
        vn_next = _u32(section, off + 12)

        if vn_version != VER_NEED_CURRENT:
            _fail("error.unsupported.verneed_revision", "vn_version is not 1",
                  index=i, have=vn_version)

        if i == sh_info - 1:
            if vn_next != 0:
                _fail("error.malformed.verneed_next", "last vn_next is not zero",
                      index=i, vn_next=vn_next)
            next_off = None
        else:
            if vn_next == 0:
                _fail("error.malformed.verneed_next", "non-last vn_next is zero",
                      index=i)
            next_off = off + vn_next
            if vn_next < VERNEED_SIZE or next_off <= off or next_off + VERNEED_SIZE > sh_size:
                _fail("error.malformed.verneed_next", "vn_next leaves the section body",
                      index=i, vn_next=vn_next, next=next_off, size=sh_size)
            if next_off % 4:
                _fail("error.malformed.verneed_align", "vn_next target is not 4-byte aligned",
                      index=i, next=next_off)

        if vn_cnt == 0:
            if vn_aux != 0:
                _fail("error.malformed.verneed_aux", "vn_aux is nonzero with zero entries",
                      index=i, vn_aux=vn_aux)
        else:
            if vn_aux == 0 or vn_aux < VERNEED_SIZE or vn_aux + VERNAUX_SIZE > sh_size:
                _fail("error.malformed.verneed_aux", "vn_aux does not point inside the body",
                      index=i, vn_aux=vn_aux, size=sh_size)

        total_aux += vn_cnt
        if total_aux > LIMITS["max_aux_entries"]:
            _fail("error.unsupported.aux_entries", "auxiliary entry total above profile bound",
                  total=total_aux, bound=LIMITS["max_aux_entries"])

        file_name = _cstring(b, link_offset, link_size, vn_file, "vn_file")

        versions = []
        cursor = off + vn_aux
        for j in range(vn_cnt):
            if cursor + VERNAUX_SIZE > sh_size:
                _fail("error.malformed.aux_count", "declared auxiliary entry does not fit",
                      index=i, aux_index=j, cursor=cursor, size=sh_size)
            if cursor % 4:
                _fail("error.malformed.verneed_align", "aux offset is not 4-byte aligned",
                      index=i, aux_index=j, offset=cursor)
            spans.append((cursor, "aux"))

            vna_hash = _u32(section, cursor)
            vna_flags = _u16(section, cursor + 4)
            vna_other = _u16(section, cursor + 6)
            vna_name = _u32(section, cursor + 8)
            vna_next = _u32(section, cursor + 12)

            if j == vn_cnt - 1:
                if vna_next != 0:
                    _fail("error.malformed.aux_next", "last vna_next is not zero",
                          index=i, aux_index=j, vna_next=vna_next)
                step = 0
            else:
                if vna_next == 0:
                    _fail("error.malformed.aux_next", "non-last vna_next is zero",
                          index=i, aux_index=j)
                target = cursor + vna_next
                if vna_next < VERNAUX_SIZE or target <= cursor or target + VERNAUX_SIZE > sh_size:
                    _fail("error.malformed.aux_next", "vna_next leaves the section body",
                          index=i, aux_index=j, vna_next=vna_next, target=target, size=sh_size)
                if target % 4:
                    _fail("error.malformed.verneed_align", "vna_next target is not 4-byte aligned",
                          index=i, aux_index=j, target=target)
                step = vna_next

            name = _cstring(b, link_offset, link_size, vna_name, "vna_name")
            versions.append({
                "name": name,
                "flags": vna_flags,
                "other": vna_other,
                "hash": vna_hash,
            })
            cursor += step

        entries.append({"file": file_name, "versions": versions})
        if next_off is not None:
            off = next_off

    coverage = bytearray(sh_size)
    for pos, kind in spans:
        for k in range(pos, pos + VERNEED_SIZE):
            if coverage[k]:
                _fail("error.malformed.verneed_overlap", "entry spans overlap",
                      offset=pos, kind=kind, byte=k)
            coverage[k] = 1
    for k in range(sh_size):
        if not coverage[k] and section[k] != 0:
            _fail("error.malformed.verneed_unreferenced", "nonzero byte outside parsed entries",
                  offset=k, byte=section[k])

    return _assemble(entries)


def dumps(obj):
    """Canonical JSON text (deterministic key order, compact separators, ASCII)."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def findings_document():
    """The frozen decision table, including declared bounds, limits and ignored fields."""
    return {
        "schema": "r34-elf-verneed-decisions/1",
        "profile": PROFILE,
        "scope": SCOPE,
        "accepts": {
            "ident": {"EI_CLASS": "ELFCLASS64 (2)", "EI_DATA": "ELFDATA2LSB (1)",
                      "EI_VERSION": "EV_CURRENT (1)", "EI_OSABI": [0, 3]},
            "types": {"ET_EXEC": 2, "ET_DYN": 3},
            "machines": {"EM_X86_64": 62, "EM_AARCH64": 183},
            "section_types": {"SHT_GNU_verneed": SHT_GNU_VERNEED, "linked SHT_STRTAB": SHT_STRTAB},
        },
        "limits": dict(LIMITS),
        "ignored": [
            "sh_entsize of SHT_GNU_verneed: GNU ld writes 0 (observed libz.so.1, libgcc_s.so.1) "
            "and readelf does not consult it (R:14042-14155 walks vn_next/vn_cnt).",
            "vna_flags, vna_other, vna_hash values: emitted verbatim; no flag whitelist, no hash "
            "recomputation, no index/versym cross-check.",
            "name bytes: decoded Latin-1 without charset or GLIBC-pattern validation.",
            "duplicate vn_file values: emitted as separate needed[] objects; the stable sort "
            "keeps section order. No merge or dedup is performed.",
            "vna_other: emitted raw as an unsigned 16-bit integer, including bit 15; readelf "
            "prints the same unmasked value.",
            "section names (for example .gnu.version_r): section type is authoritative, names are "
            "not required.",
            "program headers, .gnu.version, .gnu.version_d, dynamic entries: out of scope.",
        ],
        "precedence": [f["id"] for f in FINDINGS],
        "findings": FINDINGS,
    }


# ---------------------------------------------------------------------------
# CLI


def _read_path(path):
    try:
        st = os.stat(path)
    except OSError as exc:
        _fail("error.io.read", "cannot stat input", path=path, errno=exc.errno,
              strerror=exc.strerror)
    if st.st_size > LIMITS["max_input_bytes"]:
        _fail("error.io.size", "input above read cap", path=path, size=st.st_size,
              bound=LIMITS["max_input_bytes"])
    try:
        with open(path, "rb") as handle:
            data = handle.read(LIMITS["max_input_bytes"] + 1)
    except OSError as exc:
        _fail("error.io.read", "cannot read input", path=path, errno=exc.errno,
              strerror=exc.strerror)
    if len(data) > LIMITS["max_input_bytes"]:
        _fail("error.io.size", "input above read cap", path=path, size=len(data),
              bound=LIMITS["max_input_bytes"])
    return data


_NEED_FILE_RE = re.compile(
    r"^\s*(?:0x)?[0-9a-f]+:\s+Version:\s+\d+\s+File:\s+(.+?)\s+Cnt:\s+\d+\s*$")
_NEED_AUX_RE = re.compile(
    r"^\s*(?:0x)?[0-9a-f]+:\s+Name:\s+(.+?)\s+Flags:\s+(.*?)\s+Version:\s+(\d+)\s*$")
_FLAG_TOKENS = {"BASE": 0x1, "WEAK": 0x2, "INFO": 0x4}


def _flags_from_text(text):
    text = text.strip()
    if text == "none":
        return 0
    if not text or "unknown" in text.lower() or "0x" in text:
        return None
    value = 0
    for token in text.split("|"):
        token = token.strip()
        if token not in _FLAG_TOKENS:
            return None
        value |= _FLAG_TOKENS[token]
    return value


def _readelf_manifest(path):
    """Independent oracle for selftest: readelf's version-needs (file, name, other, flags).

    Hash is not printed by readelf; the reader's hash field is therefore not oracle-checked.
    """
    exe = shutil.which("readelf")
    if not exe:
        return None, "readelf not found"
    env = dict(os.environ, LC_ALL="C")
    try:
        proc = subprocess.run([exe, "-V", "--wide", path], capture_output=True, text=True,
                              timeout=30, env=env, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        return None, "readelf failed: %s" % (exc,)
    if proc.returncode != 0:
        return None, "readelf exit %d" % proc.returncode
    rows = []
    current = None
    in_needs = False
    unparsed = 0
    for line in proc.stdout.splitlines():
        if line.startswith("Version needs section"):
            in_needs = True
            current = None
            continue
        if line.startswith("Version ") and " section" in line:
            in_needs = False
            continue
        if not in_needs:
            continue
        if not line.strip() or line.lstrip().startswith("Addr:"):
            continue
        match = _NEED_FILE_RE.match(line)
        if match:
            current = match.group(1).strip()
            continue
        match = _NEED_AUX_RE.match(line)
        if match and current is not None:
            rows.append((current, match.group(1).strip(), int(match.group(3)),
                         _flags_from_text(match.group(2))))
            continue
        unparsed += 1
    note = "ok" if not unparsed else "unparsed=%d" % unparsed
    return rows, note


def _selftest(binaries, use_oracle=True):
    checks = []

    def check(name, condition, detail=""):
        checks.append((name, bool(condition), detail))

    def expect(name, finding_id, fn):
        try:
            fn()
        except ElfError as exc:
            check(name, exc.finding_id == finding_id,
                  "want %s got %s" % (finding_id, exc.finding_id))
        else:
            check(name, False, "no ElfError; want %s" % finding_id)

    # 1. Declared table integrity.
    ids = [f["id"] for f in FINDINGS]
    check("findings.unique", len(ids) == len(set(ids)))
    for row in FINDINGS:
        check("findings.prefix." + row["id"],
              row["id"].startswith("error." + row["classification"] + "."))
        check("findings.fields." + row["id"],
              all(isinstance(row.get(k), str) and row[k]
                  for k in ("stage", "check", "bound", "anchor"))
              and row.get("bound_kind") in ("format", "profile"))
        check("findings.exit." + row["id"],
              row["classification"] in EXIT_BY_CLASS)
    source = open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(source)
    raised = set()
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "_fail" and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)):
            raised.add(node.args[0].value)
    check("findings.code-coverage", raised == set(ids),
          "unraised=%s undeclared=%s" % (sorted(set(ids) - raised), sorted(raised - set(ids))))

    # 2. String helper on text-built string-table bytes (no ELF image constructed).
    table = b"libc.so.6\x00GLIBC_2.34\x00"
    check("cstring.first", _cstring(table, 0, len(table), 0, "t") == "libc.so.6")
    check("cstring.second", _cstring(table, 0, len(table), 10, "t") == "GLIBC_2.34")
    check("cstring.empty-decodes", _cstring(b"\x00x\x00", 0, 3, 0, "t") == "")
    check("cstring.latin1-decode", _cstring(b"\xff\x00", 0, 2, 0, "t") == "\xff")
    check("cstring.max-length",
          _cstring(b"a" * 1024 + b"\x00", 0, 1025, 0, "t") == "a" * 1024)
    expect("cstring.offset", "error.malformed.strtab_offset",
           lambda: _cstring(table, 0, len(table), len(table), "t"))
    expect("cstring.unterminated", "error.malformed.string_unterminated",
           lambda: _cstring(b"abc", 0, 3, 0, "t"))
    expect("cstring.too-long", "error.malformed.string_too_long",
           lambda: _cstring(b"a" * 1100, 0, 1100, 0, "t"))
    expect("cstring.cap-boundary-unterminated", "error.malformed.string_unterminated",
           lambda: _cstring(b"a" * 1025, 0, 1025, 0, "t"))

    # 3. Canonical shaping and ordering on text-built metadata records.
    raw = [
        {"file": "b.so", "versions": [
            {"name": "B2", "flags": 0, "other": 5, "hash": 9},
            {"name": "B1", "flags": 2, "other": 7, "hash": 1},
        ]},
        {"file": "a.so", "versions": [
            {"name": "A", "flags": 0, "other": 1, "hash": 0},
            {"name": "A", "flags": 0, "other": 0, "hash": 0},
        ]},
    ]
    shaped = _assemble(raw)
    expected = {"schema": 1, "needed": [
        {"file": "a.so", "versions": [
            {"name": "A", "flags": 0, "other": 0, "hash": 0},
            {"name": "A", "flags": 0, "other": 1, "hash": 0},
        ]},
        {"file": "b.so", "versions": [
            {"name": "B1", "flags": 2, "other": 7, "hash": 1},
            {"name": "B2", "flags": 0, "other": 5, "hash": 9},
        ]},
    ]}
    check("assemble.sort", shaped == expected)
    check("assemble.canonical", dumps(shaped) == (
        '{"needed":[{"file":"a.so","versions":[{"flags":0,"hash":0,"name":"A","other":0},'
        '{"flags":0,"hash":0,"name":"A","other":1}]},{"file":"b.so","versions":'
        '[{"flags":2,"hash":1,"name":"B1","other":7},{"flags":0,"hash":9,"name":"B2",'
        '"other":5}]}],"schema":1}'))
    check("assemble.roundtrip", json.loads(dumps(shaped)) == shaped)

    # 4. Negative prefixes (empty/short/non-ELF blobs only; no ELF image is constructed).
    expect("parse.empty", "error.malformed.elf_header_bounds", lambda: parse(b""))
    expect("parse.short", "error.malformed.elf_header_bounds", lambda: parse(b"\x7fELF"))
    expect("parse.magic", "error.malformed.elf_magic",
           lambda: parse(b"NOT-AN-ELF" + bytes(55)))

    # 5. Optional outer checks on explicitly supplied existing ELF files.
    outer = []
    for path in binaries:
        try:
            data = _read_path(path)
            obj = parse(data)
        except ElfError as exc:
            check("outer.parse." + path, False, exc.finding_id)
            continue
        files = obj["needed"]
        versions = [v for e in files for v in e["versions"]]
        ordered = all(
            e["file"] <= f["file"] for e, f in zip(files, files[1:])
        )
        inner = all(
            [(v["name"], v["other"], v["flags"], v["hash"]) for v in e["versions"]]
            == sorted((v["name"], v["other"], v["flags"], v["hash"]) for v in e["versions"])
            for e in files
        )
        check("outer.sorted." + path, ordered and inner)
        check("outer.schema." + path,
              obj.get("schema") == 1 and isinstance(files, list)
              and all(isinstance(v["hash"], int) and isinstance(v["flags"], int)
                      and isinstance(v["other"], int) for v in versions))
        oracle_note = "skipped"
        if use_oracle:
            manifest, note = _readelf_manifest(path)
            if manifest is None:
                oracle_note = "skipped(" + note + ")"
            else:
                want = sorted((f, n, o) for f, n, o, _ in manifest)
                got = sorted((e["file"], v["name"], v["other"])
                             for e in files for v in e["versions"])
                flags_checked = sum(1 for row in manifest if row[3] is not None)
                check("outer.oracle." + path, got == want,
                      "readelf rows=%d reader rows=%d note=%s"
                      % (len(want), len(got), note))
                oracle_note = "readelf triples=%d flags_checked=%d" % (len(want), flags_checked)
        outer.append({"path": path, "files": len(files), "versions": len(versions),
                      "oracle": oracle_note})

    failed = [c for c in checks if not c[1]]
    for name, ok, detail in checks:
        print(("PASS " if ok else "FAIL ") + name + ("" if ok or not detail else " :: " + detail))
    for row in outer:
        print("outer %(path)s files=%(files)d versions=%(versions)d oracle=%(oracle)s" % row)
    print("reader-selftest: %s checks=%d binaries=%d"
          % ("PASS" if not failed else "FAIL", len(checks), len(binaries)))
    return 0 if not failed else 1


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="reader.py",
        description="Decode GNU ELF symbol-version requirements (SHT_GNU_verneed) from an "
                    "existing ELF64 LE x86_64/AArch64 image.")
    parser.add_argument("path", nargs="?", help="ELF file to read; JSON goes to stdout")
    parser.add_argument("--findings", action="store_true", help="emit the decision table JSON")
    parser.add_argument("--selftest", action="store_true", help="run internal and outer checks")
    parser.add_argument("--binaries", nargs="+", default=None,
                        metavar="PATH", help="existing public ELF files for selftest outer checks")
    parser.add_argument("--no-oracle", action="store_true",
                        help="do not compare selftest outer checks against readelf")
    args = parser.parse_args(argv)

    if args.findings:
        if args.path:
            parser.error("PATH is not accepted with --findings")
        sys.stdout.write(dumps(findings_document()) + "\n")
        return 0
    if args.selftest:
        if args.path:
            parser.error("PATH is not accepted with --selftest")
        return _selftest(args.binaries or [], use_oracle=not args.no_oracle)
    if args.binaries is not None:
        parser.error("--binaries is only accepted with --selftest")
    if not args.path:
        parser.error("PATH is required unless --findings or --selftest is given")

    try:
        obj = parse(_read_path(args.path))
    except ElfError as exc:
        sys.stdout.write(dumps(exc.as_dict()) + "\n")
        return EXIT_BY_CLASS[exc.classification]
    sys.stdout.write(dumps(obj) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
