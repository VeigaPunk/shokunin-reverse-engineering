#!/usr/bin/env python3
"""Build the mini record-chain fixtures and their expected records.

Deterministic: same spec -> same bytes. The fixtures support the replay gate's
green case only; they are author-built synthetic bytes, never domain evidence.

Format (little endian): magic "MREC" | u16 version=1 | u16 count | u32 records_off
| u32 names_off | record array of count x (u16 name_off, u16 flags, u32 value) |
NUL-terminated ASCII name pool. Every fixture is exactly SIZE bytes so input
size cannot identify a fixture.
"""
import json
import struct
import sys
from pathlib import Path

SIZE = 512
MAGIC = b"MREC"

# Each fixture: a list of (name, flags, value). Names are unique across the set.
SPEC = {
    "alpha": [("libc.so.6", 0, 0x0601020F), ("libm.so.6", 1, 0x0B03), ("libz.so.1", 0, 0x0B60)],
    "beta": [("libcrypto.so.3", 0, 0x03000308)],
    "gamma": [("libgcc_s.so.1", 2, 0x0B60), ("libpthread.so.0", 0, 0x0000), ("libdl.so.2", 1, 0x0B60),
              ("libutil.so.1", 0, 0x0B60), ("libresolv.so.2", 0, 0x0B60)],
    "delta": [("libstdc++.so.6", 0, 0x03030D01), ("libatomic.so.1", 0, 0x0B03)],
    "epsilon": [("ld-linux-x86-64.so.2", 0, 0x0B03)],
    "zeta": [("libGL.so.1", 3, 0x0B60), ("libX11.so.6", 0, 0x0B60), ("libxcb.so.1", 0, 0x0B60),
             ("libwayland-client.so.0", 0, 0x0B60)],
    "eta": [("libssl.so.3", 1, 0x03000308), ("libcurl.so.4", 0, 0x03030D01),
            ("libcares.so.2", 0, 0x0B03)],
    "theta": [("libffi.so.8", 0, 0x0B03), ("libgmp.so.10", 0, 0x0B03), ("libmpfr.so.6", 0, 0x0B03),
              ("libmpc.so.3", 0, 0x0B03), ("libisl.so.23", 0, 0x0B03), ("libzstd.so.1", 0, 0x0B60)],
}


def build(records):
    names = {}
    pool = bytearray()
    for name, _flags, _value in records:
        if name not in names:
            names[name] = len(pool)
            pool += name.encode("ascii") + b"\x00"
    records_off = 16
    names_off = records_off + 8 * len(records)
    if names_off + len(pool) > SIZE:
        raise SystemExit("fixture too large: " + str(records))
    out = bytearray(SIZE)
    out[0:4] = MAGIC
    struct.pack_into("<HHI", out, 4, 1, len(records), records_off)
    struct.pack_into("<I", out, 12, names_off)
    for index, (name, flags, value) in enumerate(records):
        struct.pack_into("<HHI", out, records_off + 8 * index, names[name], flags, value)
    out[names_off:names_off + len(pool)] = pool
    return bytes(out)


def expected(records):
    return [{ "name": n, "flags": f, "value": v}
            for n, f, v in sorted(records, key=lambda row: (row[0], row[1], row[2]))]


def main():
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
    fixtures = target / "fixtures"
    fixtures.mkdir(parents=True, exist_ok=True)
    expected_by_file = {}
    for key, records in SPEC.items():
        data = build(records)
        name = key + ".mrec"
        (fixtures / name).write_bytes(data)
        expected_by_file[name] = expected(records)
    (target / "expected.json").write_text(
        json.dumps({"schema": 1, "fixtures": expected_by_file}, indent=1, sort_keys=True) + "\n")
    (target / "spec.json").write_text(
        json.dumps({"schema": 1, "size": SIZE, "spec": SPEC}, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"fixtures": len(SPEC), "size": SIZE, "dir": str(fixtures)}))


if __name__ == "__main__":
    main()
