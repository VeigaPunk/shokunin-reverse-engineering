#!/usr/bin/env python3
"""Independent stdlib PE/COFF structural reader for the round-32 R32-C1 carriers.

Written from the Microsoft PE/COFF format as an independent instrument: this file imports
only argparse, hashlib, json, os, struct, sys from the Python standard library and imports
no lane module (no arm64x_oracle, no c1-arm64x-positive).  It decodes, from file bytes only:

  * DOS header e_lfanew and the "PE\\0\\0" signature,
  * the COFF file header (machine, section count, optional-header size, characteristics),
  * the optional header (PE32/PE32+ magic, ImageBase, alignments, SizeOfHeaders,
    SizeOfImage, NumberOfRvaAndSizes) and the data-directory table,
  * the section table (name, VirtualSize, VirtualAddress, SizeOfRawData, PointerToRawData,
    Characteristics),
  * the export directory (Base, NumberOfFunctions, NumberOfNames, AddressOfFunctions,
    AddressOfNames, AddressOfNameOrdinals) and every export name,
  * the load-config directory's CHPEMetadataPointer and the IMAGE_ARM64EC_METADATA code map
    (Version, CodeMap RVA/count, each range's low-2-bit type: 0 ARM64, 1 ARM64EC, 2 AMD64),
  * the sha256 of the file.

The segment projection follows the frozen R32-C1 rule under test:
  Headers: [ImageBase, ImageBase + SizeOfHeaders];
  each section in table order: start = ImageBase + VirtualAddress,
  length = max(VirtualSize, SizeOfRawData), end = start + length, address_space "ram".
procedure_count is the primary (native-view) export directory name count.

Usage:
  python3 -I -B pe_indep.py --tsv <carriers.tsv> [--json <out.json>]
  python3 -I -B pe_indep.py --file <pe>        # one file, human-readable JSON
Everything is read-only: carriers are opened "rb" and never written.
"""

import argparse
import hashlib
import json
import os
import struct
import sys

MACHINES = {
    0x014C: "i386",
    0x8664: "amd64",
    0xAA64: "arm64",
    0xA641: "arm64ec",
    0xA64E: "arm64x",
}

DIRECTORY_NAMES = [
    "export", "import", "resource", "exception", "security", "basereloc",
    "debug", "architecture", "globalptr", "tls", "load_config", "bound_import",
    "iat", "delay_import", "clr_runtime", "reserved",
]

SECTION_CHARACTERISTICS = [
    (0x00000020, "CNT_CODE"),
    (0x00000040, "CNT_INITIALIZED_DATA"),
    (0x00000080, "CNT_UNINITIALIZED_DATA"),
    (0x02000000, "MEM_DISCARDABLE"),
    (0x04000000, "MEM_NOT_CACHED"),
    (0x08000000, "MEM_NOT_PAGED"),
    (0x10000000, "MEM_SHARED"),
    (0x20000000, "MEM_EXECUTE"),
    (0x40000000, "MEM_READ"),
    (0x80000000, "MEM_WRITE"),
]

FILE_CHARACTERISTICS = [
    (0x0001, "RELOCS_STRIPPED"),
    (0x0002, "EXECUTABLE_IMAGE"),
    (0x0020, "LARGE_ADDRESS_AWARE"),
    (0x0100, "32BIT_MACHINE"),
    (0x0200, "DEBUG_STRIPPED"),
    (0x1000, "SYSTEM"),
    (0x2000, "DLL"),
]

RANGE_TYPES = {0: "ARM64", 1: "ARM64EC", 2: "AMD64"}


class PeError(Exception):
    """Raised when the byte stream contradicts the PE/COFF format."""


def _need(buf, off, size, what):
    if off < 0 or size < 0 or off + size > len(buf):
        raise PeError("%s out of bounds: off=%d size=%d file=%d" % (what, off, size, len(buf)))


def _u16(buf, off, what="u16"):
    _need(buf, off, 2, what)
    return struct.unpack_from("<H", buf, off)[0]


def _u32(buf, off, what="u32"):
    _need(buf, off, 4, what)
    return struct.unpack_from("<I", buf, off)[0]


def _u64(buf, off, what="u64"):
    _need(buf, off, 8, what)
    return struct.unpack_from("<Q", buf, off)[0]


def _flag_names(value, table):
    return [name for bit, name in table if value & bit]


def sha256_bytes(buf):
    return hashlib.sha256(buf).hexdigest()


class PeFile:
    """Minimal, strict PE/COFF image view over an in-memory byte string."""

    def __init__(self, data, label):
        self.label = label
        self.data = data
        if data[:2] != b"MZ":
            raise PeError("%s: no DOS MZ signature" % label)
        self.e_lfanew = _u32(data, 0x3C, "e_lfanew")
        _need(data, self.e_lfanew, 24, "COFF header")
        if data[self.e_lfanew:self.e_lfanew + 4] != b"PE\0\0":
            raise PeError("%s: no PE signature at %#x" % (label, self.e_lfanew))
        coff = self.e_lfanew + 4
        (self.machine, self.section_count, self.timestamp, self.symtab_ptr,
         self.symbol_count, self.optional_size, self.characteristics) = struct.unpack_from(
            "<HHIIIHH", data, coff)
        self.optional_off = coff + 20
        _need(data, self.optional_off, self.optional_size, "optional header")
        self.magic = _u16(data, self.optional_off, "optional magic")
        if self.magic not in (0x10B, 0x20B):
            raise PeError("%s: unsupported optional magic %#x" % (label, self.magic))
        pe32plus = self.magic == 0x20B
        # PE32: ImageBase at +28 (4 bytes); PE32+: ImageBase at +24 (8 bytes).
        self.image_base = (_u64(data, self.optional_off + 24, "ImageBase") if pe32plus
                           else _u32(data, self.optional_off + 28, "ImageBase"))
        self.section_alignment = _u32(data, self.optional_off + 32, "SectionAlignment")
        self.file_alignment = _u32(data, self.optional_off + 36, "FileAlignment")
        self.size_of_image = _u32(data, self.optional_off + 56, "SizeOfImage")
        self.size_of_headers = _u32(data, self.optional_off + 60, "SizeOfHeaders")
        self.subsystem = _u16(data, self.optional_off + 68, "Subsystem")
        self.dll_characteristics = _u16(data, self.optional_off + 70, "DllCharacteristics")
        dirs_off = self.optional_off + (108 if pe32plus else 92)
        self.rva_count = _u32(data, dirs_off, "NumberOfRvaAndSizes")
        if self.rva_count > 16:
            raise PeError("%s: NumberOfRvaAndSizes %d > 16" % (label, self.rva_count))
        table_off = dirs_off + 4
        _need(data, table_off, 8 * self.rva_count, "data directories")
        self.data_dirs = []
        for i in range(self.rva_count):
            rva, size = struct.unpack_from("<II", data, table_off + 8 * i)
            self.data_dirs.append({"index": i,
                                   "name": DIRECTORY_NAMES[i] if i < len(DIRECTORY_NAMES) else "dir%d" % i,
                                   "rva": rva, "size": size})
        # Section table: NumberOfSections entries of 40 bytes at optional_off + OptionalHeader size.
        sec_off = self.optional_off + self.optional_size
        _need(data, sec_off, 40 * self.section_count, "section table")
        self.sections = []
        for i in range(self.section_count):
            raw = struct.unpack_from("<8sIIIIIIHHI", data, sec_off + 40 * i)
            name_raw = raw[0]
            name = name_raw.split(b"\0", 1)[0].decode("ascii", "replace")
            vsize, va, rsize, rptr = raw[1], raw[2], raw[3], raw[4]
            chars = raw[9]
            self.sections.append({
                "index": i,
                "name": name,
                "name_raw_hex": name_raw.hex(),
                "virtual_size": vsize,
                "virtual_address": va,
                "raw_size": rsize,
                "raw_ptr": rptr,
                "characteristics": "0x%08x" % chars,
                "flags": _flag_names(chars, SECTION_CHARACTERISTICS),
            })

    # --- address translation -------------------------------------------------
    def rva_to_offset(self, rva, what="rva"):
        for sec in self.sections:
            span = max(sec["virtual_size"], sec["raw_size"])
            if sec["virtual_address"] <= rva < sec["virtual_address"] + span:
                delta = rva - sec["virtual_address"]
                if delta >= sec["raw_size"]:
                    raise PeError("%s %#x falls in virtual-only tail of section %s"
                                  % (what, rva, sec["name"]))
                off = sec["raw_ptr"] + delta
                _need(self.data, off, 1, what)
                return off
        raise PeError("%s %#x not inside any section" % (what, rva))

    def cstring_at_rva(self, rva, what="string"):
        off = self.rva_to_offset(rva, what)
        end = self.data.find(b"\0", off)
        if end < 0:
            raise PeError("%s at %#x not NUL-terminated" % (what, rva))
        return self.data[off:end].decode("ascii", "strict")

    # --- structures ----------------------------------------------------------
    def directory(self, index):
        return self.data_dirs[index] if index < len(self.data_dirs) else {"index": index, "name": "absent", "rva": 0, "size": 0}

    def exports(self):
        dd = self.directory(0)
        out = {"directory_rva": dd["rva"], "directory_size": dd["size"],
               "present": dd["rva"] != 0, "names": [], "functions": [],
               "name_count": 0, "function_count": 0, "base": None,
               "dll_name": None, "native_like": 0, "hash_prefixed": 0}
        if dd["rva"] == 0:
            return out
        off = self.rva_to_offset(dd["rva"], "export directory")
        _need(self.data, off, 40, "export directory")
        (chars, _ts, _maj, _min, name_rva, base, nfuncs, nnames,
         addr_funcs, addr_names, addr_ords) = struct.unpack_from("<IIHHIIIIIII", self.data, off)
        out.update({"characteristics": "0x%08x" % chars, "base": base,
                    "function_count": nfuncs, "name_count": nnames,
                    "address_of_functions": addr_funcs, "address_of_names": addr_names,
                    "address_of_name_ordinals": addr_ords})
        if name_rva:
            out["dll_name"] = self.cstring_at_rva(name_rva, "export dll name")
        if nnames:
            names_off = self.rva_to_offset(addr_names, "export name pointer table")
            _need(self.data, names_off, 4 * nnames, "export name pointer table")
            ords_off = self.rva_to_offset(addr_ords, "export ordinal table")
            _need(self.data, ords_off, 2 * nnames, "export ordinal table")
            funcs_off = self.rva_to_offset(addr_funcs, "export address table")
            _need(self.data, funcs_off, 4 * nfuncs, "export address table")
            func_rvas = list(struct.unpack_from("<%dI" % nfuncs, self.data, funcs_off))
            out["functions"] = func_rvas
            names = []
            for i in range(nnames):
                nrva = _u32(self.data, names_off + 4 * i, "export name rva")
                ordinal = _u16(self.data, ords_off + 2 * i, "export ordinal")
                target = func_rvas[ordinal] if ordinal < len(func_rvas) else None
                names.append({"name": self.cstring_at_rva(nrva, "export name"),
                              "ordinal": ordinal, "rva": target})
            out["names"] = names
            out["native_like"] = sum(1 for n in names if not n["name"].startswith("#"))
            out["hash_prefixed"] = sum(1 for n in names if n["name"].startswith("#"))
        return out

    def offset_to_rva(self, off):
        for sec in self.sections:
            if sec["raw_ptr"] <= off < sec["raw_ptr"] + sec["raw_size"]:
                return sec["virtual_address"] + off - sec["raw_ptr"]
        raise PeError("file offset %#x outside any section" % off)

    def _export_directory_at(self, off):
        """Parse the 40-byte IMAGE_EXPORT_DIRECTORY shape at a raw offset, or None.

        Independent of DataDirectory[0]: every field must resolve against the section table,
        names must be non-empty printable ASCII, and every name ordinal must index a function
        slot.  Slots that do not fully resolve are rejected rather than repaired.
        """
        if off < 0 or off + 40 > len(self.data):
            return None
        try:
            (_chars, _tds, _maj, _minr, name_rva, base, nfuncs, nnames,
             addr_funcs, addr_names, addr_ords) = struct.unpack_from(
                "<IIHHIIIIIII", self.data, off)
            if not (1 <= base <= 0x10000 and 1 <= nfuncs <= 4096 and 1 <= nnames <= 4096):
                return None
            if nnames > nfuncs or name_rva == 0:
                return None
            dll = self.cstring_at_rva(name_rva, "candidate dll name")
            if not dll or not dll.endswith(".dll"):
                return None
            fo = self.rva_to_offset(addr_funcs, "candidate function table")
            no = self.rva_to_offset(addr_names, "candidate name table")
            oo = self.rva_to_offset(addr_ords, "candidate ordinal table")
            _need(self.data, fo, 4 * nfuncs, "candidate function table")
            _need(self.data, no, 4 * nnames, "candidate name table")
            _need(self.data, oo, 2 * nnames, "candidate ordinal table")
            funcs = list(struct.unpack_from("<%dI" % nfuncs, self.data, fo))
            names = []
            for i in range(nnames):
                nrva = _u32(self.data, no + 4 * i, "candidate name rva")
                ordinal = _u16(self.data, oo + 2 * i, "candidate ordinal")
                if ordinal >= nfuncs:
                    return None
                nm = self.cstring_at_rva(nrva, "candidate export name")
                if not nm or not all(0x20 <= ord(ch) < 0x7F for ch in nm):
                    return None
                names.append({"name": nm, "ordinal": ordinal, "rva": funcs[ordinal]})
            return {"raw_offset": off, "rva": self.offset_to_rva(off), "dll_name": dll,
                    "base": base, "function_count": nfuncs, "name_count": nnames,
                    "names": names}
        except PeError:
            return None

    def embedded_export_directories(self):
        """Every validated export-directory shape found by scanning file-backed sections.

        DataDirectory[0] is deliberately not consulted: hits are reported with their RVA so
        the caller can decide which one the directory table names and which one it does not.
        """
        found = {}
        for sec in self.sections:
            if sec["raw_size"] <= 0:
                continue
            stop = min(sec["raw_ptr"] + sec["raw_size"], len(self.data) - 40)
            for off in range(sec["raw_ptr"], stop + 1):
                rec = self._export_directory_at(off)
                if rec is None:
                    continue
                key = (rec["rva"], rec["name_count"], rec["function_count"])
                found.setdefault(key, rec)
        return [found[k] for k in sorted(found)]

    def chpe(self):
        dd = self.directory(10)  # IMAGE_DIRECTORY_ENTRY_LOAD_CONFIG
        out = {"load_config_rva": dd["rva"], "load_config_size": dd["size"],
               "load_config_present": dd["rva"] != 0,
               "declared_size": None, "chpe_metadata_va": None,
               "metadata": None, "code_map": [], "range_kinds": []}
        if dd["rva"] == 0:
            return out
        off = self.rva_to_offset(dd["rva"], "load config")
        declared = _u32(self.data, off, "load config size")
        out["declared_size"] = declared
        if declared < 0xD0:
            return out
        chpe_va = _u64(self.data, off + 0xC8, "CHPEMetadataPointer")
        out["chpe_metadata_va"] = chpe_va
        if chpe_va == 0:
            return out
        m_rva = chpe_va - self.image_base
        if m_rva < 0:
            raise PeError("%s: CHPE metadata VA %#x below ImageBase" % (self.label, chpe_va))
        m_off = self.rva_to_offset(m_rva, "CHPE metadata")
        version = _u32(self.data, m_off, "CHPE version")
        cm_rva = _u32(self.data, m_off + 4, "CodeMap rva")
        cm_count = _u32(self.data, m_off + 8, "CodeMapCount")
        range_entry_rva = _u32(self.data, m_off + 0x0C, "CodeRangesToEntryPoints rva")
        redir_rva = _u32(self.data, m_off + 0x10, "RedirectionMetadata rva")
        range_entry_count = _u32(self.data, m_off + 0x30, "CodeRangesToEntryPointsCount")
        redir_count = _u32(self.data, m_off + 0x34, "RedirectionMetadataCount")
        out["metadata"] = {"rva": m_rva, "version": version, "code_map_rva": cm_rva,
                           "code_map_count": cm_count,
                           "code_ranges_to_entry_points_rva": range_entry_rva,
                           "code_ranges_to_entry_points_count": range_entry_count,
                           "redirection_metadata_rva": redir_rva,
                           "redirection_metadata_count": redir_count}
        if cm_rva and cm_count:
            base = self.rva_to_offset(cm_rva, "CHPE code map")
            _need(self.data, base, 8 * cm_count, "CHPE code map")
            for i in range(cm_count):
                start_word, length = struct.unpack_from("<II", self.data, base + 8 * i)
                kind = RANGE_TYPES.get(start_word & 3, "type%d" % (start_word & 3))
                out["code_map"].append({"type": kind, "type_bits": start_word & 3,
                                        "start": start_word & ~3, "length": length,
                                        "start_word": start_word})
            out["range_kinds"] = sorted({r["type"] for r in out["code_map"]})
        return out

    def segments(self):
        ib = self.image_base
        segs = [{"name": "Headers", "start": ib, "end": ib + self.size_of_headers,
                 "length": self.size_of_headers, "image_base": ib, "address_space": "ram"}]
        for sec in self.sections:
            length = max(sec["virtual_size"], sec["raw_size"])
            start = ib + sec["virtual_address"]
            segs.append({"name": sec["name"], "start": start, "end": start + length,
                         "length": length, "image_base": ib, "address_space": "ram"})
        return segs

    def describe(self):
        exports = self.exports()
        chpe = self.chpe()
        segs = self.segments()
        kinds = set(chpe["range_kinds"])
        hexpthk = next((s for s in self.sections if s["name"] == ".hexpthk"), None)
        thunk_slots = []
        if hexpthk and hexpthk["raw_size"] >= 16:
            for i in range(hexpthk["virtual_size"] // 16):
                slot = self.data[hexpthk["raw_ptr"] + 16 * i:hexpthk["raw_ptr"] + 16 * i + 3]
                thunk_slots.append(slot.hex())
        embedded = self.embedded_export_directories()
        return {
            "label": self.label,
            "sha256": sha256_bytes(self.data),
            "bytes": len(self.data),
            "dos": {"e_lfanew": self.e_lfanew},
            "coff": {"machine": "0x%04x" % self.machine,
                     "machine_name": MACHINES.get(self.machine, "unknown"),
                     "section_count": self.section_count,
                     "timestamp": self.timestamp,
                     "optional_header_size": self.optional_size,
                     "characteristics": "0x%04x" % self.characteristics,
                     "characteristic_flags": _flag_names(self.characteristics, FILE_CHARACTERISTICS)},
            "optional": {"magic": "0x%04x" % self.magic,
                         "image_base": "0x%x" % self.image_base,
                         "section_alignment": self.section_alignment,
                         "file_alignment": self.file_alignment,
                         "size_of_image": self.size_of_image,
                         "size_of_headers": self.size_of_headers,
                         "subsystem": self.subsystem,
                         "number_of_rva_and_sizes": self.rva_count},
            "data_directories": [d for d in self.data_dirs if d["rva"] or d["size"]],
            "sections": self.sections,
            "exports": exports,
            "embedded_export_directories": embedded,
            "hexpthk": {"present": hexpthk is not None,
                        "virtual_size": hexpthk["virtual_size"] if hexpthk else None,
                        "raw_size": hexpthk["raw_size"] if hexpthk else None,
                        "slot_stride": 16,
                        "slot_count": len(thunk_slots),
                        "slot_prefixes": thunk_slots},
            "chpe": chpe,
            "segments": segs,
            "segment_count": len(segs),
            "procedure_count": exports["name_count"],
            "classify": {
                "machine_ok": self.machine == 0xAA64,
                "chpe_present": chpe["chpe_metadata_va"] not in (None, 0),
                "has_arm64_range": "ARM64" in kinds,
                "has_arm64ec_range": "ARM64EC" in kinds,
                "arm64x": (self.machine == 0xAA64 and chpe["chpe_metadata_va"] not in (None, 0)
                           and "ARM64" in kinds and "ARM64EC" in kinds),
            },
        }


def read_tsv(path):
    rows = []
    with open(path, "r", encoding="utf-8") as fh:
        header = fh.readline().rstrip("\n").split("\t")
        for line in fh:
            line = line.rstrip("\n")
            if not line:
                continue
            cells = line.split("\t")
            rows.append(dict(zip(header, cells)))
    return rows


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--tsv", help="carriers.tsv")
    ap.add_argument("--json", help="write the full decode here")
    ap.add_argument("--file", action="append", default=[], help="single PE file (repeatable)")
    args = ap.parse_args(argv)
    if not args.tsv and not args.file:
        ap.error("need --tsv or --file")
    results = []
    if args.file:
        for path in args.file:
            with open(path, "rb") as fh:
                results.append(PeFile(fh.read(), os.path.basename(path)).describe())
    if args.tsv:
        for row in read_tsv(args.tsv):
            path = row["path"]
            with open(path, "rb") as fh:
                rec = PeFile(fh.read(), row["id"]).describe()
            rec["carrier"] = {
                "path": path,
                "label_sha256": row.get("sha256"),
                "label_bytes": int(row["bytes"]) if row.get("bytes") else None,
                "label_native_exports": int(row["native_exports"]) if row.get("native_exports") else None,
                "label_ec_exports": int(row["ec_exports"]) if row.get("ec_exports") else None,
                "label_opt": row.get("opt"),
            }
            results.append(rec)
    payload = {"schema": "a2pe-indep-v1", "results": results}
    text = json.dumps(payload, indent=1, sort_keys=True)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
