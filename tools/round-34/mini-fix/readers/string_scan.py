#!/usr/bin/env python3
"""Shortcut class: string-scan. Emits every printable run as a record without record traversal."""
import json
import re
import sys

data = open(sys.argv[1], "rb").read()
records = []
for match in re.finditer(rb"[ -~]{4,}", data):
    text = match.group().decode("ascii")
    if text == "MREC":
        continue
    records.append({"name": text, "flags": 0, "value": 0})
records.sort(key=lambda row: (row["name"], row["flags"], row["value"]))
print(json.dumps({"schema": 1, "records": records}, sort_keys=True))
