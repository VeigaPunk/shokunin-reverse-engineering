#!/usr/bin/env python3
"""CR-1 linear-sweep disassembler + PUSH4 census + dispatch-structure classifier.

Usage: sweep.py <runtime.hex> [--json out.json]
Emits: PUSH4 immediates with offsets, JUMPDEST set, dispatch-adjacent PUSH2 targets,
prologue bytes, and a structural classifier for the dispatcher shape.
"""
import sys, json, re

PUSH = {0x60: 1, 0x61: 2, 0x62: 3, 0x63: 4, 0x64: 5, 0x65: 6, 0x66: 7, 0x67: 8,
        0x68: 9, 0x69: 10, 0x6a: 11, 0x6b: 12, 0x6c: 13, 0x6d: 14, 0x6e: 15,
        0x6f: 16, 0x70: 17, 0x71: 18, 0x72: 19, 0x73: 20, 0x74: 21, 0x75: 22,
        0x76: 23, 0x77: 24, 0x78: 25, 0x79: 26, 0x7a: 27, 0x7b: 28, 0x7c: 29,
        0x7d: 30, 0x7e: 31, 0x7f: 32}

def sweep(code: bytes):
    i, n = 0, len(code)
    push4, push2, jumpdests, ops = [], [], set(), []
    while i < n:
        op = code[i]
        if op == 0x5b:
            jumpdests.add(i)
        if op in PUSH:
            ln = PUSH[op]
            imm = code[i+1:i+1+ln]
            if len(imm) < ln:
                break
            if op == 0x63:
                push4.append({"off": i, "imm": imm.hex()})
            elif op == 0x61:
                push2.append({"off": i, "imm": int.from_bytes(imm, 'big')})
            i += 1 + ln
            continue
        i += 1
    return push4, push2, jumpdests

def main():
    path = sys.argv[1]
    raw = open(path).read().strip()
    raw = re.sub(r'^0x', '', raw)
    raw = re.sub(r'\s+', '', raw)
    code = bytes.fromhex(raw)
    push4, push2, jumpdests = sweep(code)
    # structural windows: find PUSH4 immediately followed (skipping optional DUP1) by EQ/JUMPI patterns
    eq_chain, masked, binary = 0, 0, 0
    for j, p in enumerate(push4):
        aft = code[p["off"]+5:p["off"]+12]
        if len(aft) >= 2 and aft[0] == 0x14:      # EQ directly after
            eq_chain += 1
        if len(aft) >= 3 and aft[1] == 0x14:      # DUP1; PUSH4; EQ  -> eq at p+1 handled above; here: EQ after one op
            eq_chain += 1
    # LT/GT presence near PUSH4s = binary-search dispatch signal
    gtlt = sum(1 for p in push4 if code[p["off"]+5:p["off"]+9].find(b'\x11') >= 0 or code[p["off"]+5:p["off"]+9].find(b'\x10') >= 0)
    res = {
        "file": path,
        "codeBytes": len(code),
        "codeSha256HexOfBytes": __import__('hashlib').sha256(code).hexdigest(),
        "prologue8": code[:8].hex(),
        "prologue16": code[:16].hex(),
        "push4Count": len(push4),
        "push4Imms": [p["imm"] for p in push4],
        "push4ImmsSorted": sorted(set(p["imm"] for p in push4)),
        "push4Offsets": {p["imm"]: p["off"] for p in push4},
        "jumpdestCount": len(jumpdests),
        "push2Count": len(push2),
        "eqDirectAfterPush4": eq_chain,
        "gtOrLtNearPush4": gtlt,
        "revertSelectorsPresent": {
            "Error_string_08c379a0": any(p["imm"] == "08c379a0" for p in push4),
            "Panic_4e487b71": any(p["imm"] == "4e487b71" for p in push4),
        },
    }
    out = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == "--json" else None
    if out:
        open(out, 'w').write(json.dumps(res, indent=2) + '\n')
        print(f"wrote {out}: push4={len(push4)} jumpdests={len(jumpdests)} prologue={res['prologue8']}")
    else:
        print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()