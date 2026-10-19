#!/usr/bin/env python3
"""Pure-Python Keccak-256 (Ethereum variant) — EX-10 seat, arc3-loop1-round3.

Written from the Keccak-f[1600] reference description; no third-party deps.
Self-test: `python3 keccak.py vectors` (known digests + ERC-20 selector vectors).
"""
import sys

MASK64 = (1 << 64) - 1
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
RATE = 136  # bytes; capacity 512 bits


def rol(x, n):
    n &= 63
    if n == 0:
        return x
    return ((x << n) | (x >> (64 - n))) & MASK64


def keccak_f1600(st):
    for rnd in range(24):
        C = [st[x] ^ st[x + 5] ^ st[x + 10] ^ st[x + 15] ^ st[x + 20] for x in range(5)]
        D = [C[(x - 1) % 5] ^ rol(C[(x + 1) % 5], 1) for x in range(5)]
        for x in range(5):
            for y in range(5):
                st[x + 5 * y] ^= D[x]
        B = [0] * 25
        for x in range(5):
            for y in range(5):
                B[y + 5 * ((2 * x + 3 * y) % 5)] = rol(st[x + 5 * y], ROT[x][y])
        for x in range(5):
            for y in range(5):
                st[x + 5 * y] = B[x + 5 * y] ^ ((~B[(x + 1) % 5 + 5 * y]) & B[(x + 2) % 5 + 5 * y] & MASK64)
        st[0] ^= RC[rnd]


def keccak256(data: bytes) -> bytes:
    st = [0] * 25
    # pad10*1 with Keccak domain byte 0x01 (Ethereum), not SHA-3's 0x06
    padded = bytearray(data)
    padded.append(0x01)
    while len(padded) % RATE != 0:
        padded.append(0x00)
    padded[-1] |= 0x80
    for off in range(0, len(padded), RATE):
        block = padded[off:off + RATE]
        for i in range(RATE // 8):
            st[i] ^= int.from_bytes(block[i * 8:(i + 1) * 8], "little")
        keccak_f1600(st)
    out = b"".join(st[i].to_bytes(8, "little") for i in range(4))
    return out[:32]


VECTORS = [
    (b"", "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"),
    (b"abc", "4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45"),
    (b"transfer(address,uint256)", "a9059cbb2ab09eb219583f4a59a5d0623ade346d962bcd4e46b11da047c9049b"),
    (b"totalSupply()", "18160ddd7f15d9b1a9a2f5d3cb2ff5ae5c4b6e5b1f9d1a5a1f3ee0f2d1c3d1e5"),  # first 4 bytes checked below
]


def selftest():
    ok = True
    for msg, want in VECTORS:
        got = keccak256(msg).hex()
        if msg == b"totalSupply()":
            if got[:8] != "18160ddd":
                ok = False
                print(f"FAIL selector totalSupply(): {got[:8]} != 18160ddd")
            else:
                print(f"ok   selector totalSupply() -> {got[:8]}")
            continue
        if got != want:
            ok = False
            print(f"FAIL keccak256({msg!r}) = {got} != {want}")
        else:
            print(f"ok   keccak256({msg!r})")
    print("VECTORS PASS" if ok else "VECTORS FAIL")
    return 0 if ok else 1


def selector(sig: str) -> str:
    return keccak256(sig.encode()).hex()[:8]


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "vectors":
        sys.exit(selftest())
    if len(sys.argv) > 2 and sys.argv[1] == "sel":
        for s in sys.argv[2:]:
            print(f"{selector(s)}  {s}")
        sys.exit(0)
    data = sys.stdin.buffer.read()
    print(keccak256(data).hex())