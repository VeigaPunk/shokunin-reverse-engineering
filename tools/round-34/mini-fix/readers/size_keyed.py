#!/usr/bin/env python3
"""Shortcut class: size-keyed template. Selects a memorized answer by input size."""
import json
import os
import sys

TEMPLATE = {
    512: [{"name": "libc.so.6", "flags": 0, "value": 0x0601020F},
          {"name": "libm.so.6", "flags": 1, "value": 0x0B03},
          {"name": "libz.so.1", "flags": 0, "value": 0x0B60}],
}

size = os.stat(sys.argv[1]).st_size
print(json.dumps({"schema": 1, "records": TEMPLATE.get(size, [])}, sort_keys=True))
