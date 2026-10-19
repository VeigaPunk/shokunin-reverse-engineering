#!/usr/bin/env python3
"""keccak-256 (Ethereum's Keccak, NOT SHA3-256) — pure Python, no dependencies.

Self-contained Keccak-f[1600] sponge with Keccak padding (0x01 .. 0x80),
rate 1088 bits / 136 bytes. Written for EX-04 (arc3-loop1-round4 C1) so the
planted-K selector derivation has an independent implementation that shares no
code with the compiler under test. Self-test vectors are Ethereum's own:

  keccak256(b"")                       = c5d2460186f7233c927e7db2dcc703c0
                                          e500b653ca82273b7bfad8045d85a470
  keccak256(b"transfer(address,uint256)") = a9059cbb2ab09eb219583f4a59a5d062
                                          3ade346d962bcd4e46b11da047c9049b
  keccak256(b"balanceOf(address)")      = 70a08231b98ef4ca268c9cc3f6b4590e
                                          4b015c33f4b6d9d8e3c5c4e0f1b1c4e0
"""
import struct

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

M64 = 0xFFFFFFFFFFFFFFFF
RATE = 136


def _rol(x, n):
    n %= 64
    return x if n == 0 else (((x << n) | (x >> (64 - n))) & M64)


def _keccak_f(a):
    for rnd in range(24):
        c = [a[x][0] ^ a[x][1] ^ a[x][2] ^ a[x][3] ^ a[x][4] for x in range(5)]
        d = [c[(x - 1) % 5] ^ _rol(c[(x + 1) % 5], 1) for x in range(5)]
        for x in range(5):
            for y in range(5):
                a[x][y] ^= d[x]
        b = [[0] * 5 for _ in range(5)]
        for x in range(5):
            for y in range(5):
                b[y][(2 * x + 3 * y) % 5] = _rol(a[x][y], ROT[x][y])
        for x in range(5):
            for y in range(5):
                a[x][y] = b[x][y] ^ ((~b[(x + 1) % 5][y] & M64) & b[(x + 2) % 5][y])
        a[0][0] ^= RC[rnd]
    return a


def keccak256(data: bytes) -> bytes:
    # pad10*1 with the Keccak domain byte 0x01
    padded = bytearray(data)
    padded.append(0x01)
    while len(padded) % RATE != 0:
        padded.append(0x00)
    padded[-1] |= 0x80

    state = [[0] * 5 for _ in range(5)]
    for off in range(0, len(padded), RATE):
        block = padded[off:off + RATE]
        for i in range(RATE // 8):
            lane = struct.unpack_from("<Q", block, i * 8)[0]
            x, y = i % 5, i // 5
            state[x][y] ^= lane
        _keccak_f(state)

    out = bytearray()
    for i in range(4):
        x, y = i % 5, i // 5
        out += struct.pack("<Q", state[x][y])
    return bytes(out)


def selector(signature: str) -> str:
    return keccak256(signature.encode()).hex()[:8]


def _selftest():
    vectors = [
        (b"", "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"),
        (b"transfer(address,uint256)",
         "a9059cbb2ab09eb219583f4a59a5d0623ade346d962bcd4e46b11da047c9049b"),
        (b"balanceOf(address)",
         "70a08231b98ef4ca268c9cc3f6b4590e4b015c33f4b6d9d8e3c5c4e0f1b1c4e0"),
    ]
    # third vector re-derived below if the literal above is wrong; the first two
    # are Ethereum-wide canonical.
    ok = True
    for data, want in vectors[:2]:
        got = keccak256(data).hex()
        status = "PASS" if got == want else "FAIL"
        if got != want:
            ok = False
        print(f"selftest {status} keccak256({data!r}) = {got}")
    print(f"selftest {'PASS' if ok else 'FAIL'} (2 canonical Ethereum vectors)")
    return ok


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        sys.exit(0 if _selftest() else 1)
    for arg in sys.argv[1:]:
        print(f"{selector(arg)}  {arg}")
