#!/usr/bin/env python3
"""Keccak-256 (Ethereum variant) — pure Python, from-spec, no dependencies.

Supporting artifact for seat EX-03 (arc3-loop1-round1, chain c1): the
independent second implementation used to derive the planted selector set in
planted-selectors.txt. Reference: Keccak-f[1600], rate 136 bytes, Keccak
padding 0x01..0x80 (NOT NIST SHA-3's 0x06 padding).

Usage:
  python3 keccak256.py --selftest        # 3 known-answer vectors, exit 0/1
  python3 keccak256.py [sig ...]         # default: the 9+2 planted signatures
"""
import sys

MASK = (1 << 64) - 1

RC = [
    0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
    0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
    0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
    0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
    0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008,
]

ROT = [
    [0, 36, 3, 41, 18],
    [1, 44, 10, 45, 2],
    [62, 6, 43, 15, 61],
    [28, 55, 25, 21, 56],
    [27, 20, 39, 8, 14],
]


def rol(x, n):
    n %= 64
    if n == 0:
        return x & MASK
    return ((x << n) | (x >> (64 - n))) & MASK


def keccak_f1600(a):
    for rnd in range(24):
        c = [a[x][0] ^ a[x][1] ^ a[x][2] ^ a[x][3] ^ a[x][4] for x in range(5)]
        d = [c[(x - 1) % 5] ^ rol(c[(x + 1) % 5], 1) for x in range(5)]
        for x in range(5):
            for y in range(5):
                a[x][y] ^= d[x]
        b = [[0] * 5 for _ in range(5)]
        for x in range(5):
            for y in range(5):
                b[y][(2 * x + 3 * y) % 5] = rol(a[x][y], ROT[x][y])
        for x in range(5):
            for y in range(5):
                nb = (~b[(x + 1) % 5][y]) & MASK
                a[x][y] = b[x][y] ^ (nb & b[(x + 2) % 5][y])
        a[0][0] ^= RC[rnd]
    return a


def keccak256(data: bytes) -> bytes:
    rate = 136
    a = [[0] * 5 for _ in range(5)]
    padded = bytearray(data)
    pad = rate - (len(padded) % rate)
    if pad == 1:
        padded += b"\x81"
    else:
        padded += b"\x01" + b"\x00" * (pad - 2) + b"\x80"
    for off in range(0, len(padded), rate):
        block = padded[off:off + rate]
        for i in range(rate // 8):
            a[i % 5][i // 5] ^= int.from_bytes(block[8 * i:8 * i + 8], "little")
        keccak_f1600(a)
    out = bytearray()
    for i in range(4):
        out += a[i % 5][i // 5].to_bytes(8, "little")
    return bytes(out)


def selftest():
    vecs = {
        b"": "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470",
        b"abc": "4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45",
        b"transfer(address,uint256)": "a9059cbb2ab09eb219583f4a59a5d0623ade346d962bcd4e46b11da047c9049b",
    }
    ok = True
    for msg, want in vecs.items():
        got = keccak256(msg).hex()
        status = "OK" if got == want else "FAIL"
        if got != want:
            ok = False
        print(f"selftest {status}: keccak256({msg!r}) = {got}")
    return ok


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        sys.exit(0 if selftest() else 1)
    sigs = sys.argv[1:] if len(sys.argv) > 1 else [
        "totalSupply()", "balanceOf(address)", "transfer(address,uint256)",
        "allowance(address,address)", "approve(address,uint256)",
        "transferFrom(address,address,uint256)", "name()", "symbol()", "decimals()",
        "Transfer(address,address,uint256)", "Approval(address,address,uint256)",
    ]
    for s in sigs:
        h = keccak256(s.encode())
        print(f"0x{h.hex()[:8]}  {s}   (full {h.hex()})")


if __name__ == "__main__":
    main()
