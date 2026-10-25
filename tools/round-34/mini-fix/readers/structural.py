#!/usr/bin/env python3
"""Structural reader: walks the record array and resolves each name in the pool."""
import json
import struct
import sys


def main(path):
    data = open(path, "rb").read()
    if data[0:4] != b"MREC":
        return 1
    version, count, records_off = struct.unpack_from("<HHI", data, 4)
    names_off = struct.unpack_from("<I", data, 12)[0]
    if version != 1:
        return 1
    records = []
    for index in range(count):
        name_off, flags, value = struct.unpack_from("<HHI", data, records_off + 8 * index)
        start = names_off + name_off
        end = data.index(b"\x00", start)
        records.append({"name": data[start:end].decode("ascii"), "flags": flags, "value": value})
    records.sort(key=lambda row: (row["name"], row["flags"], row["value"]))
    print(json.dumps({"schema": 1, "records": records}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
