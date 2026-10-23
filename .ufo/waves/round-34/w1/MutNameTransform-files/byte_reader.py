#!/usr/bin/env python3
"""Read only the supplied bounded ASCII/NUL text bytes, not an ELF parser."""
import json
from pathlib import Path
import sys

data = Path(sys.argv[1]).read_bytes()
assert len(data) <= 4096 and all(byte < 128 for byte in data)
header, payload = data.split(b"\0\0", 1)
fields = header.split(b"\0")
assert fields[0] == b"TEXT-R34-NUL-1"
count, table_size = map(int, fields[1:3])
assert len(fields[3:]) == count and count <= 65
table = payload[:table_size]
assert payload[table_size:] == b"TEXT-END\0"

def name(offset):
    assert 0 <= offset < len(table)
    return table[offset:table.index(0, offset)].decode("ascii")

needed = []
for row in fields[3:]:
    file_offset, encoded_versions = row.split(b"|", 1)
    versions = []
    for item in encoded_versions.split(b";") if encoded_versions else []:
        offset, flags, other, recorded_hash = map(int, item.split(b","))
        versions.append({"name": name(offset), "flags": flags, "other": other, "hash": recorded_hash})
    versions.sort(key=lambda value: (value["name"], value["other"]))
    needed.append({"file": name(int(file_offset)), "versions": versions})
needed.sort(key=lambda value: value["file"])
print(json.dumps({"schema": 1, "needed": needed}, sort_keys=True))
