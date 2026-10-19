#!/usr/bin/env python3
"""keccak_ref.py — independent Keccak-256 (legacy padding 0x01) implementation.

Written for seat EX-05 (chain c1, round 3) as an oracle independent of js-sha3:
no third-party imports, no reuse of the receipted tree's code. Self-checked
against the canonical Keccak-256 empty-string digest and the ERC-20 Transfer
topic hash before use.

usage:
  python3 keccak_ref.py --sel "fund(uint256)"      -> 4-byte selector hex
  python3 keccak_ref.py --hash ""                  -> full 32-byte digest
"""
import sys

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
MASK = (1 << 64) - 1


def rol(x, n):
    n %= 64
    return ((x << n) | (x >> (64 - n))) & MASK


def keccak_f(a):
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
                a[x][y] = b[x][y] ^ ((~b[(x + 1) % 5][y]) & b[(x + 2) % 5][y]) & MASK
        a[0][0] ^= RC[rnd]
    return a


def keccak256(data: bytes) -> bytes:
    rate = 136
    # legacy Keccak padding: 0x01 ... 0x80
    padlen = rate - (len(data) % rate)
    if padlen == 1:
        padded = data + b"\x81"
    else:
        padded = data + b"\x01" + b"\x00" * (padlen - 2) + b"\x80"
    a = [[0] * 5 for _ in range(5)]
    for off in range(0, len(padded), rate):
        block = padded[off:off + rate]
        for i in range(rate // 8):
            lane = int.from_bytes(block[i * 8:(i + 1) * 8], "little")
            x, y = i % 5, i // 5
            a[x][y] ^= lane
        keccak_f(a)
    out = bytearray()
    for i in range(4):  # 32 bytes = 4 lanes
        x, y = i % 5, i // 5
        out += a[x][y].to_bytes(8, "little")
    return bytes(out)


def selfcheck():
    empty = keccak256(b"").hex()
    assert empty == "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470", empty
    topic = keccak256(b"Transfer(address,address,uint256)").hex()
    assert topic == "ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef", topic


if __name__ == "__main__":
    selfcheck()
    if len(sys.argv) == 1:
        print("selfcheck OK (empty-string + Transfer topic vectors)")
        sys.exit(0)
    if sys.argv[1] == "--sel":
        print(keccak256(sys.argv[2].encode())[:4].hex())
    elif sys.argv[1] == "--hash":
        print(keccak256(sys.argv[2].encode()).hex())
    else:
        print("selfcheck OK")