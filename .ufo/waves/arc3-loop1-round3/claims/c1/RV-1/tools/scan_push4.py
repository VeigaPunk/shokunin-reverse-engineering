#!/usr/bin/env python3
"""RV-1 r3 — independent linear PUSH4 scanner over runtime bytecode.

Reports every PUSH4 immediate in the required form `0x........@pc` plus the
byte at each reported pc+1 (the JUMPDEST check used by the probe reconciler).
Written from the EVM opcode table, no code shared with EX-07/EX-08 r1 tools.
"""
import sys


def disasm_push4(code: bytes):
    pc = 0
    out = []
    n = len(code)
    while pc < n:
        op = code[pc]
        if op == 0x63:  # PUSH4
            if pc + 4 < n:
                imm = int.from_bytes(code[pc + 1:pc + 5], "big")
                out.append((pc, imm))
            pc += 5
        elif 0x60 <= op <= 0x7f:  # PUSH1..PUSH32
            pc += 1 + (op - 0x5f)
        else:
            if op == 0x5b:
                pass
            pc += 1
    return out


if __name__ == "__main__":
    path = sys.argv[1]
    with open(path, "rb") as f:
        raw = f.read()
    # accept hex text or raw bytes
    text = raw.decode("ascii", "ignore").strip()
    if text and all(c in "0123456789abcdefABCDEF" for c in text):
        code = bytes.fromhex(text)
    else:
        code = raw
    sites = disasm_push4(code)
    print(f"# {path}: {len(code)} bytes, {len(sites)} PUSH4 sites")
    for pc, imm in sites:
        tgt = code[pc + 1 + 4] if pc + 1 + 4 < len(code) else None
        tgt_s = f"tgt=0x{pc + 1 + imm:04x}" if imm < len(code) else "tgt=oob"
        print(f"0x{imm:08x}@{pc} tgtbyte_pc{pc + 5}={tgt:02x} {tgt_s}")