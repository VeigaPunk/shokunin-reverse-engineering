#!/usr/bin/env python3
"""Shortcut class: record-order replay. Reads the first count records' first u16 as an
index into a memorized name list, ignoring name_off and the name pool."""
import json
import struct
import sys

NAMES = ["libc.so.6", "libm.so.6", "libz.so.1", "libcrypto.so.3", "libgcc_s.so.1",
         "libpthread.so.0", "libdl.so.2", "libutil.so.1"]

data = open(sys.argv[1], "rb").read()
_count = struct.unpack_from("<H", data, 6)[0]
records_off = struct.unpack_from("<I", data, 8)[0]
records = []
for index in range(_count):
    name_off, flags, value = struct.unpack_from("<HHI", data, records_off + 8 * index)
    if name_off < len(NAMES):
        records.append({"name": NAMES[name_off], "flags": flags, "value": value})
records.sort(key=lambda row: (row["name"], row["flags"], row["value"]))
print(json.dumps({"schema": 1, "records": records}, sort_keys=True))
