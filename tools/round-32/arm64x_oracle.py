#!/usr/bin/env python3
"""Round-32 R32-C1 oracle: a pure-Python PE reader (no LLVM, no Ghidra, no REA code).

From the file bytes alone it reads the COFF machine, ImageBase, SizeOfHeaders, the section
table, the primary (native-view) export directory and the load-config CHPE metadata code
map (IMAGE_ARM64EC_METADATA v2: CodeMap RVA at +4, CodeMapCount at +8; each range entry is
{StartOffset with the range type in its low 2 bits: 0 ARM64, 1 ARM64EC, 2 AMD64; Length}).

`expected(path)` returns the fields the frozen R32-C1 predicate compares with REA 6.5.0
`inspect`, under the rule frozen before data (one pre-freeze probe, `probe/x.dll`):
  segments = [Headers: ImageBase, SizeOfHeaders] + every section in table order with
             start = ImageBase + VirtualAddress, length = max(VirtualSize, SizeOfRawData),
             end = start + length, image_base = ImageBase, address_space "ram";
  procedure_count = number of names in the primary (native ARM64 view) export directory;
  architecture "arm64", format "pe", document "target-<sha256[:12]>.dll".
`classify(path)` says whether the file is an ARM64X hybrid: COFF machine 0xAA64, a non-zero
CHPE metadata pointer, and a code map holding at least one ARM64 and one ARM64EC range.
"""

import hashlib
import json
import struct
import sys

RANGE_TYPES = {0: "ARM64", 1: "ARM64EC", 2: "AMD64"}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class PE:
    def __init__(self, data):
        self.b = data
        if data[:2] != b"MZ":
            raise ValueError("no MZ header")
        pe = struct.unpack_from("<I", data, 0x3C)[0]
        if data[pe:pe + 4] != b"PE\0\0":
            raise ValueError("no PE signature")
        self.machine, nsec, _, _, _, opt_size, self.characteristics = struct.unpack_from("<HHIIIHH", data, pe + 4)
        opt = pe + 24
        magic = struct.unpack_from("<H", data, opt)[0]
        if magic != 0x20B:
            raise ValueError("not PE32+")
        self.image_base = struct.unpack_from("<Q", data, opt + 24)[0]
        self.size_of_headers = struct.unpack_from("<I", data, opt + 60)[0]
        ndirs = struct.unpack_from("<I", data, opt + 108)[0]
        self.dirs = [struct.unpack_from("<II", data, opt + 112 + 8 * i) for i in range(ndirs)]
        self.sections = []
        sec = opt + opt_size
        for i in range(nsec):
            raw = data[sec + 40 * i: sec + 40 * i + 40]
            name = raw[:8].rstrip(b"\0").decode("ascii")
            vsize, va, rsize, rptr = struct.unpack_from("<IIII", raw, 8)
            self.sections.append({"name": name, "va": va, "vsize": vsize, "rsize": rsize, "rptr": rptr})

    def off(self, rva):
        for s in self.sections:
            if s["va"] <= rva < s["va"] + max(s["vsize"], s["rsize"]):
                return s["rptr"] + rva - s["va"]
        raise ValueError("rva %#x outside sections" % rva)

    def cstr(self, rva):
        o = self.off(rva)
        return self.b[o:self.b.index(b"\0", o)].decode("ascii")

    def export_names(self):
        if len(self.dirs) < 1 or self.dirs[0][0] == 0:
            return []
        o = self.off(self.dirs[0][0])
        nnames = struct.unpack_from("<I", self.b, o + 24)[0]
        names_rva = struct.unpack_from("<I", self.b, o + 32)[0]
        return [self.cstr(struct.unpack_from("<I", self.b, self.off(names_rva) + 4 * i)[0]) for i in range(nnames)]

    def code_map(self):
        if len(self.dirs) < 11 or self.dirs[10][0] == 0:
            return None
        lc = self.off(self.dirs[10][0])
        size = struct.unpack_from("<I", self.b, lc)[0]
        if size < 0xD0:
            return None
        chpe_va = struct.unpack_from("<Q", self.b, lc + 0xC8)[0]
        if chpe_va == 0:
            return None
        m = self.off(chpe_va - self.image_base)
        _, cm_rva, cm_count = struct.unpack_from("<III", self.b, m)
        base = self.off(cm_rva)
        out = []
        for i in range(cm_count):
            start, length = struct.unpack_from("<II", self.b, base + 8 * i)
            out.append({"type": RANGE_TYPES.get(start & 3, "type%d" % (start & 3)), "start": start & ~3, "length": length})
        return out


def load(path):
    with open(path, "rb") as f:
        return PE(f.read())


def classify(path):
    pe = load(path)
    cm = pe.code_map() or []
    kinds = {r["type"] for r in cm}
    return {"machine": "%#06x" % pe.machine, "code_map": cm,
            "arm64x": pe.machine == 0xAA64 and "ARM64" in kinds and "ARM64EC" in kinds}


def expected(path):
    pe = load(path)
    sha = sha256_file(path)
    ib = pe.image_base
    segs = [{"name": "Headers", "start": hex(ib), "end": hex(ib + pe.size_of_headers),
             "length": pe.size_of_headers, "image_base": hex(ib), "address_space": "ram"}]
    for s in pe.sections:
        length = max(s["vsize"], s["rsize"])
        start = ib + s["va"]
        segs.append({"name": s["name"], "start": hex(start), "end": hex(start + length),
                     "length": length, "image_base": hex(ib), "address_space": "ram"})
    return {"format": "pe", "architecture": "arm64", "document": "target-%s.dll" % sha[:12],
            "image_base": hex(ib), "segments": segs, "segment_count": len(segs),
            "procedure_count": len(pe.export_names())}


def comparable(envelope_data):
    """Project an REA `inspect` envelope's data onto the predicate fields."""
    nr = envelope_data.get("normalized_result") or {}
    subj = envelope_data.get("subject") or {}
    return {"format": subj.get("format"), "architecture": subj.get("architecture"),
            "document": nr.get("document"), "image_base": nr.get("image_base"),
            "segments": nr.get("segments"), "segment_count": nr.get("segment_count"),
            "procedure_count": nr.get("procedure_count")}


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(json.dumps({"path": p, "sha256": sha256_file(p), "class": classify(p),
                          "native_exports": load(p).export_names(), "expected": expected(p)}, sort_keys=True))
