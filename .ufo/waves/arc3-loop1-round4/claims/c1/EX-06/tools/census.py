#!/usr/bin/env python3
"""Independent byte census for EVM runtime carriers (no external deps).

Usage:
  census.py <carrier.hex|carrier.bin> [--offsets a,b,c]

Reports: file/decoded digests, size, dispatch prologue class, full PUSH4
immediate inventory (offset -> value), PUSH4 values that are JUMPDEST-adjacent
or not, 0x5b positions, and (with --offsets) whether each probed offset lands on
0x5b and what the opcode byte is.
"""
import hashlib
import json
import sys

PUSH1, PUSH32 = 0x60, 0x7F
JUMPDEST = 0x5B


def load_bytes(path: str) -> bytes:
    raw = open(path, "rb").read()
    text = raw.decode("ascii", "replace").strip()
    if all(c in "0123456789abcdefABCDEF\n\r \t" for c in text) and len(text.replace("\n", "").replace("\r", "")) % 2 == 0 and len(text) > 4:
        try:
            return bytes.fromhex(text)
        except ValueError:
            pass
    return raw


def main() -> int:
    path = sys.argv[1]
    want_offsets = []
    if "--offsets" in sys.argv:
        want_offsets = [int(x, 0) for x in sys.argv[sys.argv.index("--offsets") + 1].split(",") if x]

    raw = open(path, "rb").read()
    code = load_bytes(path)
    print(f"file: {path}")
    print(f"file_bytes: {len(raw)}  file_sha256: {hashlib.sha256(raw).hexdigest()}")
    print(f"decoded_bytes: {len(code)}  decoded_sha256: {hashlib.sha256(code).hexdigest()}")

    head = code[:16].hex()
    prologue = "unknown"
    if code[:5] == bytes.fromhex("5f3560e01c"):
        prologue = "5f3560e01c (PUSH0 CALLDATALOAD PUSH1 0xe0 SHR)"
    elif code[:5] == bytes.fromhex("60003560e01c"):
        prologue = "60003560e01c (PUSH1 0x00 CALLDATALOAD PUSH1 0xe0 SHR)"
    elif code[:3] == bytes.fromhex("366000"):
        prologue = "366000... (CALLDATASIZE PUSH1 0x00 ...) — vyper-class candidate"
    print(f"head16: {head}")
    print(f"prologue_class: {prologue}")

    # PUSH4 census
    push4 = []
    i = 0
    n = len(code)
    while i < n:
        op = code[i]
        if PUSH1 <= op <= PUSH32:
            k = op - PUSH1 + 1
            imm = code[i + 1:i + 1 + k]
            if k == 4:
                push4.append((i, imm.hex()))
            i += 1 + k
        else:
            i += 1
    vals = {}
    for off, v in push4:
        vals.setdefault(v, []).append(off)
    print(f"push4_count: {len(push4)}  distinct: {len(vals)}")
    print("push4_inventory:")
    for v in sorted(vals):
        print(f"  {v} @ {vals[v]}")

    # 0x5b positions (JUMPDEST)
    jumpdests = [i for i, b in enumerate(code) if b == JUMPDEST]
    print(f"jumpdest_count: {len(jumpdests)}")

    if want_offsets:
        print("offset_checks:")
        for off in want_offsets:
            if 0 <= off < n:
                print(f"  {off}: byte=0x{code[off]:02x} is_jumpdest={code[off] == JUMPDEST}")
            else:
                print(f"  {off}: OUT-OF-RANGE (len {n})")

    # terminal CBOR trailer heuristic: last 2 bytes = length
    if n >= 2:
        cborlen = int.from_bytes(code[-2:], "big")
        if 0 < cborlen <= n:
            off = n - cborlen - 2
            trailer = code[off:off + cborlen]
            print(f"cbor_len_guess: {cborlen} bytecode_offset_guess: {off} trailer_hex: {trailer.hex()[:160]}")
            print(f"trailer_ascii: {trailer!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
