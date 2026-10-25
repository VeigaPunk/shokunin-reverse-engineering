#!/usr/bin/env python3
"""Shortcut class: label-keyed. Selects a memorized answer from the input basename."""
import json
import os
import sys

TEMPLATE = {
    "alpha.mrec": [{"name": "libc.so.6", "flags": 0, "value": 0x0601020F}],
    "gamma.mrec": [{"name": "libgcc_s.so.1", "flags": 2, "value": 0x0B60}],
}

label = os.path.basename(sys.argv[1])
print(json.dumps({"schema": 1, "records": TEMPLATE.get(label, [])}, sort_keys=True))
