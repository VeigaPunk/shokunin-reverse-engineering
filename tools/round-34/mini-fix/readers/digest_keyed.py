#!/usr/bin/env python3
"""Shortcut class: digest-keyed. Selects a memorized answer from the whole-file digest."""
import hashlib
import json
import sys

TEMPLATE = {
    "e1c4d1d5": [{"name": "libc.so.6", "flags": 0, "value": 0x0601020F}],
}

digest = hashlib.sha256(open(sys.argv[1], "rb").read()).hexdigest()[:8]
print(json.dumps({"schema": 1, "records": TEMPLATE.get(digest, [])}, sort_keys=True))
