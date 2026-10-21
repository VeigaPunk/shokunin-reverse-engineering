#!/usr/bin/env python3
"""Offline preflight for the REA 6.5.0 `inspect-dart-aot` dynsym contract.

Reads one APK without executing anything, extracts `lib/<abi>/libapp.so` in
memory, and reports which Dart snapshot layout each ABI carries:

  legacy  : .dynsym exports the four names REA 6.5.0 looks up
            (_kDartVmSnapshotData/_kDartVmSnapshotInstructions/
             _kDartIsolateSnapshotData/_kDartIsolateSnapshotInstructions)
            and the data headers are kind 3 -> `inspect-dart-aot` can reach
            libapp coverage "complete".
  partial : 1..3 of those names -> REA parses, coverage is partial.
  new     : only _kDartSnapshotText/_kDartSnapshotData[_kDartSnapshotBuildId]
            -> REA 6.5.0 refuses with unsupported_target (no legacy name in
            .dynsym; the aliases the Dart SDK added are not exported).

This only reproduces the gate REA itself applies (SHT_DYNSYM only, no
SHT_SYMTAB fallback: rea-agents 6.5.0 dist/flutter/DartElf.js:180). It is a
carrier-selection aid, not a substitute for the REA probe and not evidence by
itself. No APK is executed.

Usage: python3 preflight_dart_carrier.py <apk> [--json]
Exit:  0 legacy-complete, 3 new-layout (REA 6.5.0 will refuse),
       4 partial, 2 unreadable/malformed.
"""
import hashlib
import io
import json
import re
import struct
import sys
import zipfile

LEGACY = (
    "_kDartVmSnapshotData",
    "_kDartVmSnapshotInstructions",
    "_kDartIsolateSnapshotData",
    "_kDartIsolateSnapshotInstructions",
)
NEW = ("_kDartSnapshotText", "_kDartSnapshotData", "_kDartSnapshotBuildId")
SHT_DYNSYM = 11
SNAPSHOT_MAGIC = 0xDCDCF5F5
VERSION_RE = re.compile(rb'\d+\.\d+\.\d+ \(stable\) \([^)]*\) on "[a-z0-9_]+"')


def parse_elf(blob):
    if len(blob) < 64 or blob[:4] != b"\x7fELF" or blob[4] != 2 or blob[5] != 1:
        return {"error": "not little-endian ELF64"}
    e_type, = struct.unpack_from("<H", blob, 0x10)
    e_shoff, = struct.unpack_from("<Q", blob, 0x28)
    e_shentsize, e_shnum = struct.unpack_from("<HH", blob, 0x3A)
    e_shstrndx, = struct.unpack_from("<H", blob, 0x3E)
    if e_shoff == 0 or e_shnum == 0:
        return {"error": "section-stripped image (REA would use PT_DYNAMIC/DT_SYMTAB)"}
    sections = []
    for i in range(e_shnum):
        base = e_shoff + i * e_shentsize
        name_off, sh_type, _flags, addr, off, size, link, _info, _al, entsize = \
            struct.unpack_from("<IIQQQQIIQQ", blob, base)
        sections.append({"name_off": name_off, "type": sh_type, "addr": addr,
                         "offset": off, "size": size, "link": link, "entsize": entsize})
    shstr = sections[e_shstrndx]
    for sec in sections:
        start = shstr["offset"] + sec["name_off"]
        sec["name"] = blob[start:blob.index(b"\0", start)].decode("latin1")
    dynsym = next((s for s in sections if s["type"] == SHT_DYNSYM), None)
    if dynsym is None or dynsym["entsize"] != 24:
        return {"error": "no usable SHT_DYNSYM"}
    strtab = sections[dynsym["link"]]
    symbols = {}
    for i in range(dynsym["size"] // dynsym["entsize"]):
        base = dynsym["offset"] + i * dynsym["entsize"]
        name_off, _info, _other, shndx, value, size = struct.unpack_from("<IBBHQQ", blob, base)
        start = strtab["offset"] + name_off
        name = blob[start:blob.index(b"\0", start)].decode("latin1")
        if not name:
            continue
        relocated = None
        if 0 < shndx < len(sections):
            sec = sections[shndx]
            relocated = sec["offset"] + value - sec["addr"]
        symbols[name] = {"value": value, "size": size,
                         "section": sections[shndx]["name"] if 0 < shndx < len(sections) else None,
                         "file_offset": relocated}
    headers = []
    for name in LEGACY:
        sym = symbols.get(name)
        if sym is None or not name.endswith("Data") or sym["file_offset"] is None:
            continue
        off = sym["file_offset"]
        magic, = struct.unpack_from("<I", blob, off)
        length, = struct.unpack_from("<Q", blob, off + 4)
        kind, = struct.unpack_from("<Q", blob, off + 12)
        headers.append({"symbol": name, "offset": off, "magic_valid": magic == SNAPSHOT_MAGIC,
                        "header_length": length, "kind": kind})
    return {"e_type": e_type, "has_symtab": any(s["type"] == 2 for s in sections),
            "legacy_names": [n for n in LEGACY if n in symbols],
            "new_names": [n for n in NEW if n in symbols],
            "data_headers": headers}


def dart_version(blob):
    match = VERSION_RE.search(blob)
    return match.group(0).decode("latin1") if match else None


def main(argv):
    if len(argv) < 2:
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        return 2
    apk = argv[1]
    want_json = "--json" in argv[2:]
    raw = open(apk, "rb").read()
    result = {"apk": apk, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "abis": []}
    layouts = []
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        names = archive.namelist()
        for abi in sorted({n.split("/")[1] for n in names
                           if n.startswith("lib/") and n.count("/") == 2
                           and n.endswith("/libapp.so")}):
            app = archive.read(f"lib/{abi}/libapp.so")
            entry = {"abi": abi,
                     "libapp_sha256": hashlib.sha256(app).hexdigest(),
                     "libapp_bytes": len(app),
                     "elf": parse_elf(app)}
            try:
                flutter = archive.read(f"lib/{abi}/libflutter.so")
                entry["dart_version"] = dart_version(flutter)
            except KeyError:
                entry["dart_version"] = None
            elf = entry["elf"]
            if "error" in elf:
                entry["layout"] = "unreadable:" + elf["error"]
            elif len(elf["legacy_names"]) == 4 and all(h["kind"] == 3 and h["magic_valid"]
                                                       for h in elf["data_headers"]):
                entry["layout"] = "legacy-complete"
            elif elf["legacy_names"]:
                entry["layout"] = "legacy-partial"
            elif elf["new_names"]:
                entry["layout"] = "new-layout"
            else:
                entry["layout"] = "unknown-symbols"
            layouts.append(entry["layout"])
            result["abis"].append(entry)
    result["rea_6_5_0_expectation"] = {
        "legacy-complete": "inspect-dart-aot parses; libapp coverage complete if both data hashes agree",
        "legacy-partial": "inspect-dart-aot parses; coverage partial",
        "new-layout": "inspect-dart-aot refuses unsupported_target (no legacy name in .dynsym)",
        "unreadable": "not established by this preflight",
    }
    if "legacy-complete" in layouts:
        verdict = 0
    elif "legacy-partial" in layouts:
        verdict = 4
    elif "new-layout" in layouts:
        verdict = 3
    else:
        verdict = 2
    print(json.dumps(result, indent=1))
    return verdict


if __name__ == "__main__":
    sys.exit(main(sys.argv))
