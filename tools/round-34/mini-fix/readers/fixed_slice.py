#!/usr/bin/env python3
"""Shortcut class: fixed-slice. Reads NUL-terminated strings at fixed offsets only."""
import json
import sys

data = open(sys.argv[1], "rb").read()
records = []
for offset in range(64, len(data), 32):
    end = data.find(b"\x00", offset)
    if end <= offset:
        continue
    text = data[offset:end].decode("ascii", "replace")
    if text.isprintable():
        records.append({"name": text, "flags": 0, "value": offset})
records.sort(key=lambda row: (row["name"], row["flags"], row["value"]))
print(json.dumps({"schema": 1, "records": records}, sort_keys=True))
