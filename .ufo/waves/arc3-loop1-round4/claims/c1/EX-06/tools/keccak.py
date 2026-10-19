#!/usr/bin/env python3
"""Pure-python keccak-256 + 4-byte selector derivation.

Self-contained (no external deps) so the planted-K derivation is independent of
the probe's own toolchain (evmole). Validated against known vectors in
selftest().
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


def rotl(x, n):
    n %= 64
    return ((x << n) | (x >> (64 - n))) & MASK


def keccak_f(a):
    for rnd in range(24):
        c = [a[x][0] ^ a[x][1] ^ a[x][2] ^ a[x][3] ^ a[x][4] for x in range(5)]
        d = [c[(x - 1) % 5] ^ rotl(c[(x + 1) % 5], 1) for x in range(5)]
        for x in range(5):
            for y in range(5):
                a[x][y] ^= d[x]
        b = [[0] * 5 for _ in range(5)]
        for x in range(5):
            for y in range(5):
                b[y][(2 * x + 3 * y) % 5] = rotl(a[x][y], ROT[x][y])
        for x in range(5):
            for y in range(5):
                a[x][y] = b[x][y] ^ ((~b[(x + 1) % 5][y]) & b[(x + 2) % 5][y]) & MASK
        a[0][0] ^= RC[rnd]
    return a


def keccak256(data: bytes) -> bytes:
    rate = 136
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
        a = keccak_f(a)
    out = bytearray()
    for i in range(4):  # 32 bytes = 4 lanes
        x, y = i % 5, i // 5
        out += a[x][y].to_bytes(8, "little")
    return bytes(out[:32])


def selector(sig: str) -> str:
    return keccak256(sig.encode()).hex()[:8]


VECTORS = [
    (b"", "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"),
    (b"abc", "4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45"),
]

SEL_VECTORS = {
    "transfer(address,uint256)": "a9059cbb",
    "balanceOf(address)": "70a08231",
    "totalSupply()": "18160ddd",
    "approve(address,uint256)": "095ea7b3",
    "transferFrom(address,address,uint256)": "23b872dd",
    "decimals()": "313ce567",
}


def selftest() -> int:
    ok = True
    for data, expect in VECTORS:
        got = keccak256(data).hex()
        status = "OK" if got == expect else "FAIL"
        if got != expect:
            ok = False
        print(f"keccak256({data!r}) = {got} expect {expect} {status}")
    for sig, expect in SEL_VECTORS.items():
        got = selector(sig)
        status = "OK" if got == expect else "FAIL"
        if got != expect:
            ok = False
        print(f"selector({sig}) = {got} expect {expect} {status}")
    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        sys.exit(selftest())
    for arg in sys.argv[1:]:
        print(f"{selector(arg)}  {arg}")
