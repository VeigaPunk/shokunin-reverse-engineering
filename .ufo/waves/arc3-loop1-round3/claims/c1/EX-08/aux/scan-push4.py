#!/usr/bin/env python3
"""Linear-sweep PUSH4/PUSH20 constant census over a runtime .bin (no execution).
Walks bytes, skips PUSH immediates, collects PUSH4 constants + PCs.
Usage: scan-push4.py <bin> [<bin>...]  -> JSON to stdout."""
import json
import sys
import hashlib

def scan(path):
    b = open(path, 'rb').read()
    i = 0
    push4 = []
    push20 = []
    pushes = {}
    while i < len(b):
        op = b[i]
        if 0x60 <= op <= 0x7f:
            n = op - 0x5f
            imm = b[i+1:i+1+n]
            if len(imm) < n:
                break
            if op == 0x63:
                push4.append({"pc": i, "const": imm.hex()})
            if op == 0x73:
                push20.append({"pc": i, "const": imm.hex()})
            pushes[f"PUSH{n}"] = pushes.get(f"PUSH{n}", 0) + 1
            i += 1 + n
        else:
            i += 1
    return {
        "path": path,
        "bytes": len(b),
        "sha256": hashlib.sha256(b).hexdigest(),
        "push4_constants": push4,
        "push4_unique": sorted({p["const"] for p in push4}),
        "push20_constants": push20,
        "push4_count": len(push4),
    }

if __name__ == "__main__":
    out = [scan(p) for p in sys.argv[1:]]
    print(json.dumps(out, indent=2))