#!/usr/bin/env python3
"""push4-scan.py — linear-sweep PUSH4 immediate census over a runtime hex blob.

Seat EX-05 (chain c1, round 3). Purpose: state precisely what "zero extras"
means for this carrier — the full set of 4-byte constants that a naive
"PUSH4 sweep" extractor would report, so the probe's function set can be
compared against a superset, not against the planted set alone.

Method: linear sweep from offset 0, decoding PUSH1..PUSH32 immediates
(0x60..0x7f) and skipping their operand bytes. This is a linear sweep, not a
control-flow bounded disassembly (r1's EX-07 built the stronger variant); it is
marked as such. `5f` = PUSH0 (Shanghai+), operand-free.

usage: python3 push4-scan.py <runtime.hex> [--json]
"""
import json
import sys

PUSH0 = 0x5F


def scan(hexstr: str):
    code = bytes.fromhex(hexstr.strip().replace("0x", ""))
    out = []
    i = 0
    while i < len(code):
        op = code[i]
        if op == PUSH0:
            i += 1
            continue
        if 0x60 <= op <= 0x7F:
            n = op - 0x5F
            imm = code[i + 1:i + 1 + n]
            if len(imm) < n:
                break
            if n == 4:
                out.append({"offset": i, "opcode": hex(op), "value": imm.hex()})
            i += 1 + n
            continue
        i += 1
    return out


if __name__ == "__main__":
    data = scan(open(sys.argv[1]).read())
    if "--json" in sys.argv:
        print(json.dumps(data, indent=2))
    else:
        for d in data:
            print(f"@{d['offset']:5d} {d['opcode']} {d['value']}")
        print(f"-- {len(data)} PUSH4 immediates; {len({d['value'] for d in data})} distinct")