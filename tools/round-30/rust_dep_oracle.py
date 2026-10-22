"""Round-30 independent reader for cargo-auditable `.dep-v0` sections.

Shares no code with REA. It parses the container section tables itself
(ELF32/ELF64 little-endian, PE/COFF, thin 64-bit Mach-O), takes the
section bytes, inflates them with Python's zlib, and parses the JSON with
Python's json module. The format (zlib-compressed JSON with a `packages`
array of {name, version, source, kind?, dependencies?, root?}) is the one
documented by cargo-auditable (round-30 SOURCES row S089).

API:
  locate(data) -> dict(format, section_name, offset, size)   # content bytes
  decode(section_bytes) -> dict (the parsed JSON document)
  normalize(doc) -> sorted list of package tuples:
      (name, version, source, kind|None, root(bool), sorted((dep_name, dep_version), ...))
"""

import json
import struct
import zlib


class OracleError(Exception):
    pass


def _elf(data):
    cls = data[4]
    if data[5] != 1:
        raise OracleError("big-endian ELF not supported by the oracle")
    if cls == 2:
        shoff = struct.unpack_from("<Q", data, 0x28)[0]
        shentsize, shnum, shstrndx = struct.unpack_from("<HHH", data, 0x3A)
        def sh(i):
            b = shoff + i * shentsize
            name, typ, flags, addr, off, size = struct.unpack_from("<IIQQQQ", data, b)
            return name, typ, flags, off, size
    elif cls == 1:
        shoff = struct.unpack_from("<I", data, 0x20)[0]
        shentsize, shnum, shstrndx = struct.unpack_from("<HHH", data, 0x2E)
        def sh(i):
            b = shoff + i * shentsize
            name, typ, flags, addr, off, size = struct.unpack_from("<IIIIII", data, b)
            return name, typ, flags, off, size
    else:
        raise OracleError("unknown ELF class")
    _, _, _, stroff, strsize = sh(shstrndx)
    strtab = data[stroff:stroff + strsize]
    hits = []
    for i in range(shnum):
        name, typ, flags, off, size = sh(i)
        end = strtab.find(b"\0", name)
        if strtab[name:end] == b".dep-v0":
            hits.append({"format": "elf", "section_name": ".dep-v0", "offset": off, "size": size,
                         "type": typ, "flags": flags})
    return hits


def _pe(data):
    pe = struct.unpack_from("<I", data, 0x3C)[0]
    if data[pe:pe + 4] != b"PE\0\0":
        raise OracleError("no PE signature")
    nsec = struct.unpack_from("<H", data, pe + 6)[0]
    optsize = struct.unpack_from("<H", data, pe + 20)[0]
    table = pe + 24 + optsize
    hits = []
    for i in range(nsec):
        b = table + 40 * i
        name = data[b:b + 8].rstrip(b"\0")
        vsize, vaddr, rawsize, rawptr = struct.unpack_from("<IIII", data, b + 8)
        if name == b".dep-v0":
            size = rawsize if vsize == 0 else min(vsize, rawsize)
            hits.append({"format": "pe", "section_name": ".dep-v0", "offset": rawptr, "size": size})
    return hits


def _macho(data):
    magic = struct.unpack_from("<I", data, 0)[0]
    if magic != 0xFEEDFACF:
        raise OracleError("not a thin little-endian 64-bit Mach-O")
    ncmds = struct.unpack_from("<I", data, 16)[0]
    p = 32
    hits = []
    for _ in range(ncmds):
        cmd, cmdsize = struct.unpack_from("<II", data, p)
        if cmd == 0x19:  # LC_SEGMENT_64
            nsects = struct.unpack_from("<I", data, p + 64)[0]
            for j in range(nsects):
                s = p + 72 + 80 * j
                sect = data[s:s + 16].rstrip(b"\0")
                seg = data[s + 16:s + 32].rstrip(b"\0")
                size = struct.unpack_from("<Q", data, s + 40)[0]
                off = struct.unpack_from("<I", data, s + 48)[0]
                if seg == b"__DATA" and sect == b".dep-v0":
                    hits.append({"format": "macho", "section_name": "__DATA,.dep-v0", "offset": off, "size": size})
        p += cmdsize
    return hits


def locate(data):
    if data[:4] == b"\x7fELF":
        hits = _elf(data)
    elif data[:2] == b"MZ":
        hits = _pe(data)
    elif data[:4] == b"\xcf\xfa\xed\xfe":
        hits = _macho(data)
    else:
        raise OracleError("unknown container")
    if len(hits) != 1:
        raise OracleError("expected exactly one .dep-v0 section, found %d" % len(hits))
    return hits[0]


def decode(section_bytes):
    d = zlib.decompressobj()
    raw = d.decompress(section_bytes) + d.flush()
    if not d.eof:
        raise OracleError("zlib stream incomplete")
    return json.loads(raw.decode("utf-8"))


def normalize(doc):
    pk = doc["packages"]
    out = []
    for p in pk:
        deps = tuple(sorted((pk[i]["name"], pk[i]["version"]) for i in p.get("dependencies", [])))
        out.append((p["name"], p["version"], p["source"], p.get("kind"), bool(p.get("root", False)), deps))
    return sorted(out, key=repr)


def read_file(path):
    with open(path, "rb") as f:
        data = f.read()
    sec = locate(data)
    doc = decode(data[sec["offset"]:sec["offset"] + sec["size"]])
    return sec, doc
