#!/usr/bin/env python3
"""R33 selftest fixture recipe generator (scratch only; deliberately separate from the parser).

This module builds synthetic PE32+ byte strings and pins an independently expected finding id for each
case. It imports nothing from `chpe_profile.py` and uses none of the parser's decision functions, so the
fixture recipe can be frozen before production scoring and cannot silently track parser changes.

Contents: `Image` (minimal PE32+ serializer), `LAYOUTS` (two different memory layouts), `canonical`
(well-formed ARM64X-shaped image), mutators, and `CASES` = (case name, builder, expected finding id).
"""

import struct


def _align(x, a):
    return (x + a - 1) // a * a


class Image:
    """Minimal PE32+ model serialised by `build`; fields are mutated directly by selftest cases."""

    def __init__(self, L):
        self.L = L
        self.machine = 0xAA64
        self.magic = 0x20B
        self.image_base = L["ib"]
        self.ndirs = 16
        self.dirs = {}
        self.sections = []

    def add(self, name, va, chars, vsize=None):
        self.sections.append({"name": name, "va": va, "chars": chars, "data": bytearray(), "vsize": vsize,
                              "rsize": None})

    def sec(self, name):
        return next(s for s in self.sections if s["name"] == name)

    def write(self, rva, blob):
        for s in self.sections:
            if s["va"] <= rva < s["va"] + 0x1000:
                o = rva - s["va"]
                if len(s["data"]) < o + len(blob):
                    s["data"].extend(b"\0" * (o + len(blob) - len(s["data"])))
                s["data"][o:o + len(blob)] = blob
                return
        raise ValueError("builder: rva %#x has no section" % rva)

    def set_map(self, entries, rva=None):
        L = self.L
        rva = L["map"] if rva is None else rva
        self.write(rva, b"".join(struct.pack("<II", s, n) for s, n in entries))
        self.write(L["meta"] + 4, struct.pack("<II", rva, len(entries)))

    def build(self):
        fa = 0x200
        nsec = len(self.sections)
        pe = 0x80
        opt_size = 112 + 8 * self.ndirs
        soh = _align(pe + 24 + opt_size + 40 * nsec, fa)
        out = bytearray(soh)
        out[0:2] = b"MZ"
        struct.pack_into("<I", out, 0x3C, pe)
        out[pe:pe + 4] = b"PE\0\0"
        struct.pack_into("<HHIIIHH", out, pe + 4, self.machine, nsec, 0, 0, 0, opt_size, 0x2022)
        o = pe + 24
        struct.pack_into("<H", out, o, self.magic)
        struct.pack_into("<Q", out, o + 24, self.image_base)
        struct.pack_into("<II", out, o + 32, 0x1000, fa)
        size_image = min(_align(max(s["va"] + max(s["vsize"] or 0, len(s["data"])) for s in self.sections),
                                0x1000), 0xFFFFF000)
        struct.pack_into("<II", out, o + 56, size_image, soh)
        struct.pack_into("<HH", out, o + 68, 3, 0x160)
        struct.pack_into("<I", out, o + 108, self.ndirs)
        for i, (rva, size) in self.dirs.items():
            if i < self.ndirs:
                struct.pack_into("<II", out, o + 112 + 8 * i, rva, size)
        so = o + opt_size
        ptr = soh
        for i, s in enumerate(self.sections):
            data = bytes(s["data"])
            rsize = s["rsize"] if s["rsize"] is not None else _align(len(data), fa)
            data = data[:rsize].ljust(rsize, b"\0")
            vsize = s["vsize"] if s["vsize"] is not None else len(s["data"])
            struct.pack_into("<8sIIII12xI", out, so + 40 * i, s["name"].encode(), vsize, s["va"], rsize,
                             ptr if rsize else 0, s["chars"])
            out += data
            ptr += rsize
        return bytes(out)


LAYOUTS = [
    {"name": "L0", "ib": 0x180000000, "text": 0x1000, "arm64": 0x1000, "ec": 0x1100, "hexp": 0x2000,
     "rdata": 0x3000, "map": 0x3150, "data": 0x4000, "meta": 0x4000},
    {"name": "L1", "ib": 0x140000000, "text": 0x1000, "arm64": 0x1180, "ec": 0x1000, "hexp": 0x6000,
     "rdata": 0x8000, "map": 0x81A0, "data": 0x9000, "meta": 0x9040},
]
A64 = struct.pack("<4I", 0x52800020, 0xD65F03C0, 0x52800040, 0xD65F03C0)
A64EC = struct.pack("<6I", 0x52800060, 0xD65F03C0, 0x52800080, 0xD65F03C0, 0x528000A0, 0xD65F03C0)
X64 = bytes.fromhex("b806000000c3")
X_R = 0x60000020
R_ = 0x40000040
RW = 0xC0000040


def default_map(L):
    return [(L["arm64"] | 0, len(A64)), (L["ec"] | 1, len(A64EC)), (L["hexp"] | 2, len(X64))]


def canonical(L, chpe=True):
    im = Image(L)
    im.add(".text", L["text"], X_R)
    im.write(L["arm64"], A64)
    im.write(L["ec"], A64EC)
    im.add(".hexpthk", L["hexp"], X_R)
    im.write(L["hexp"], X64)
    im.add(".rdata", L["rdata"], R_, vsize=0x200)
    im.add(".data", L["data"], RW)
    lc = bytearray(0x140)
    struct.pack_into("<I", lc, 0, 0x140)
    if chpe:
        struct.pack_into("<Q", lc, 0xC8, L["ib"] + L["meta"])
        im.dirs[10] = (L["rdata"], 0x140)
    im.write(L["rdata"], bytes(lc))
    meta = bytearray(0x5C + 8)
    struct.pack_into("<I", meta, 0, 2)
    im.write(L["meta"], bytes(meta))
    im.set_map(default_map(L))
    if not chpe:
        im.dirs.pop(10, None)
    return im


def _patch(b, off, fmt, *v):
    b = bytearray(b)
    struct.pack_into(fmt, b, off, *v)
    return bytes(b)


def _sec_hdr(b, i):
    pe = struct.unpack_from("<I", b, 0x3C)[0]
    return pe + 24 + struct.unpack_from("<H", b, pe + 20)[0] + 40 * i


def _m(fn):
    def go(L):
        im = canonical(L)
        fn(im, L)
        return im.build()
    return go


def _zero_tail_range(im, L):
    t = im.sec(".text")
    t["rsize"] = 0x200
    t["vsize"] = 0x800
    fb = L["text"] + 0x200
    m = default_map(L)
    m[1] = (L["ec"] | 1, _align(fb - L["ec"] + 0x40, 4))
    im.set_map(m)


def _cross_range(im, L):
    t = im.sec(".text")
    vend = L["text"] + len(t["data"])
    m = default_map(L)
    m[1] = (L["ec"] | 1, _align(vend - L["ec"] + 0x40, 4))
    im.set_map(m)


def _move_meta_zero_tail(im, L):
    d = im.sec(".data")
    new = L["data"] + 0x1E0
    im.write(new, struct.pack("<III", 2, L["map"], 3))
    d["rsize"], d["vsize"] = 0x200, 0x800
    im.write(L["rdata"] + 0xC8, struct.pack("<Q", L["ib"] + new))


def _move_map_zero_tail(im, L):
    r = im.sec(".rdata")
    new = L["rdata"] + 0x1F0
    im.set_map(default_map(L), rva=new)
    r["rsize"], r["vsize"] = 0x200, 0x800


def _meta_cross(im, L):
    im.sec(".data")["vsize"] = L["meta"] - L["data"] + 0x30


def _lc_cross(im, L):
    im.write(L["rdata"] + 0x100, struct.pack("<I", 0x140))
    im.dirs[10] = (L["rdata"] + 0x100, 0x140)


def _lc_zero_tail(im, L):
    r = im.sec(".rdata")
    im.write(L["rdata"] + 0x1C0, struct.pack("<I", 0x140))
    im.dirs[10] = (L["rdata"] + 0x1C0, 0x140)
    r["rsize"], r["vsize"] = 0x200, 0x800


def _set_chpe(v):
    return _m(lambda im, L: im.write(L["rdata"] + 0xC8, struct.pack("<Q", v(L))))


def _map(f):
    return _m(lambda im, L: im.set_map(f(L)))


def _swap_sorted(L):
    m = default_map(L)
    return [m[1], m[2], m[0]]


def _adjacent(L):
    m = default_map(L)
    lo, hi = sorted([L["arm64"], L["ec"]])
    first = 0 if lo == L["arm64"] else 1
    m[first] = (m[first][0], hi - lo)
    return m


def _swap_tag_kinds(L):
    # Coherent wrong-tag positive: ARM64 bytes tagged ARM64EC and vice versa. Structurally consistent,
    # semantically wrong — the profile does not decode instructions, so this stays a candidate.
    return [(L["arm64"] | 1, len(A64)), (L["ec"] | 0, len(A64EC)), (L["hexp"] | 2, len(X64))]



def _section_rva_overflow(im, L):
    im.sec(".hexpthk")["va"] = 0xFFFFFF00


def _truncate_table(L):
    b = canonical(L).build()
    return b[:_sec_hdr(b, 2) + 8]


# (case, builder(L) -> bytes, expected finding_id). Expected ids are pinned here, independent of the
# parser's own FINDINGS table; the parser selftest asserts equality, not agreement by construction.
CASES = [
    ("green_canonical", lambda L: canonical(L).build(), "candidate.structural"),
    ("green_unsorted_map", _map(_swap_sorted), "candidate.structural"),
    ("green_adjacent_ranges", _map(_adjacent), "candidate.structural"),
    ("green_amd64_len6_unaligned_ok", lambda L: canonical(L).build(), "candidate.structural"),
    ("lookalike_pure_arm64_no_load_config", lambda L: canonical(L, chpe=False).build(), "not_candidate.no_load_config"),
    ("lookalike_ten_directories", _m(lambda im, L: setattr(im, "ndirs", 10)), "not_candidate.no_load_config"),
    ("lookalike_chpe_pointer_zero", _set_chpe(lambda L: 0), "not_candidate.chpe_pointer_zero"),
    ("coherent_wrong_tags_semantically_unknown", _map(_swap_tag_kinds), "candidate.structural"),
    ("lookalike_small_load_config", _m(lambda im, L: im.write(L["rdata"], struct.pack("<I", 0x94))),
     "not_candidate.load_config_lacks_chpe_field"),
    ("lookalike_amd64_machine", _m(lambda im, L: setattr(im, "machine", 0x8664)), "not_candidate.machine_not_arm64"),
    ("label_machine_arm64x", _m(lambda im, L: setattr(im, "machine", 0xA64E)), "outside_profile.machine_hybrid_label"),
    ("zeroed_metadata", _m(lambda im, L: im.write(L["meta"], bytes(0x5C))),
     "outside_profile.metadata_version_unrecognized"),
    ("metadata_version_1", _m(lambda im, L: im.write(L["meta"], struct.pack("<I", 1))),
     "outside_profile.metadata_version_unrecognized"),
    ("code_map_empty", _m(lambda im, L: im.write(L["meta"] + 8, struct.pack("<I", 0))), "not_candidate.code_map_empty"),
    ("only_arm64_amd64", _map(lambda L: [default_map(L)[0], default_map(L)[2]]), "not_candidate.no_arm64ec_range"),
    ("only_arm64ec_amd64", _map(lambda L: default_map(L)[1:]), "not_candidate.no_arm64_range"),
    ("tag3", _map(lambda L: [default_map(L)[0], (L["ec"] | 3, 24), default_map(L)[2]]),
     "outside_profile.range_tag_unrecognized"),
    ("length_zero", _map(lambda L: [default_map(L)[0], (L["ec"] | 1, 0), default_map(L)[2]]),
     "outside_profile.range_length_zero"),
    ("arm64ec_length_unaligned", _map(lambda L: [default_map(L)[0], (L["ec"] | 1, 22), default_map(L)[2]]),
     "outside_profile.range_length_unaligned"),
    ("range_rva_overflow", _map(lambda L: [default_map(L)[0], (0xFFFFFF00 | 1, 0x200), default_map(L)[2]]),
     "malformed.range_rva_overflow"),
    ("range_unmapped", _map(lambda L: [default_map(L)[0], (0x00F00000 | 1, 0x10), default_map(L)[2]]),
     "outside_profile.range_unmapped"),
    ("range_in_headers", _map(lambda L: [default_map(L)[0], (0x200 | 1, 0x10), default_map(L)[2]]),
     "outside_profile.range_header"),
    ("range_zero_tail", _m(_zero_tail_range), "outside_profile.range_zero_tail"),
    ("range_cross_section", _m(_cross_range), "outside_profile.range_cross_section"),
    ("range_not_executable", _map(lambda L: [default_map(L)[0], ((L["rdata"] + 0x180) | 1, 0x10), default_map(L)[2]]),
     "outside_profile.range_not_executable"),
    ("range_overlap_forgery", _map(lambda L: [(L["arm64"] | 0, 0x10), ((L["arm64"] + 0x8) | 1, 0x8), default_map(L)[2]]),
     "outside_profile.range_overlap"),
    ("range_duplicate", _map(lambda L: default_map(L) + [default_map(L)[1]]), "outside_profile.range_overlap"),
    ("code_map_count_limit", _m(lambda im, L: im.write(L["meta"] + 8, struct.pack("<I", 2000))),
     "outside_profile.code_map_count_limit"),
    ("code_map_unmapped", _m(lambda im, L: im.write(L["meta"] + 4, struct.pack("<I", 0x00F00000))),
     "malformed.code_map_unmapped"),
    ("code_map_in_headers", _m(lambda im, L: im.write(L["meta"] + 4, struct.pack("<I", 0x100))),
     "outside_profile.code_map_header"),
    ("code_map_zero_tail", _m(_move_map_zero_tail), "outside_profile.code_map_zero_tail"),
    ("code_map_cross_section", _m(lambda im, L: im.set_map(default_map(L), rva=L["rdata"] + 0x1F0)),
     "outside_profile.code_map_cross_section"),
    ("metadata_below_image_base", _set_chpe(lambda L: 0x1000), "malformed.chpe_pointer_outside_image"),
    ("metadata_unmapped", _set_chpe(lambda L: L["ib"] + 0x00F00000), "malformed.metadata_unmapped"),
    ("metadata_in_headers", _set_chpe(lambda L: L["ib"] + 0x100), "outside_profile.metadata_header"),
    ("metadata_zero_tail", _m(_move_meta_zero_tail), "outside_profile.metadata_zero_tail"),
    ("metadata_cross_section", _m(_meta_cross), "outside_profile.metadata_cross_section"),
    ("load_config_unmapped", _m(lambda im, L: im.dirs.__setitem__(10, (0x00F00000, 0x140))),
     "malformed.load_config_unmapped"),
    ("load_config_in_headers", _m(lambda im, L: im.dirs.__setitem__(10, (0x100, 0x40))), "outside_profile.load_config_header"),
    ("load_config_cross_section", _m(_lc_cross), "outside_profile.load_config_cross_section"),
    ("load_config_zero_tail", _m(_lc_zero_tail), "outside_profile.load_config_zero_tail"),
    ("section_rva_overflow", _m(_section_rva_overflow), "malformed.section_rva_overflow"),
    ("section_raw_out_of_file", lambda L: canonical(L).build()[:-0x100], "malformed.section_raw_out_of_file"),
    ("section_table_truncated", _truncate_table, "malformed.section_table_truncated"),
    ("section_count_limit", lambda L: _patch(canonical(L).build(), 0x80 + 6, "<H", 97), "outside_profile.section_count_limit"),
    ("data_directories_truncated", lambda L: _patch(canonical(L).build(), 0x80 + 24 + 108, "<I", 64),
     "malformed.data_directories_truncated"),
    ("not_pe32plus", _m(lambda im, L: setattr(im, "magic", 0x10B)), "outside_profile.not_pe32plus"),
    ("optional_header_truncated", lambda L: _patch(canonical(L).build(), 0x80 + 20, "<H", 0x40),
     "malformed.optional_header_truncated"),
    ("no_pe_signature", lambda L: _patch(canonical(L).build(), 0x80, "<4s", b"PX\0\0"), "malformed.no_pe_signature"),
    ("pe_offset_out_of_file", lambda L: _patch(canonical(L).build(), 0x3C, "<I", 0x100000), "malformed.pe_offset_out_of_file"),
    ("no_mz", lambda L: _patch(canonical(L).build(), 0, "<2s", b"ZM"), "malformed.no_mz"),
    ("truncated_dos_header", lambda L: canonical(L).build()[:0x20], "malformed.truncated_dos_header"),
]
