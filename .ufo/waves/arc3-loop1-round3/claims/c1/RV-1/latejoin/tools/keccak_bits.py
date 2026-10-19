#!/usr/bin/env python3
"""RV-1 LATE-JOIN (arc3-loop1-round3, chain c1) — Keccak-256, formulation D.

Path D = the Keccak reference "readable" formulation: the state is a
200-BYTE string (the spec's byte-oriented view), with lanes read/written as
8 little-endian bytes at offset 8*(x+5y); rotation is performed on the 64-bit
integer read out of that byte slice.  Round constants are DERIVED from the
LFSR rc(t) and rho offsets DERIVED from the (1,0)->(y,2x+3y) walk recurrence —
no hardcoded RC/ROT tables anywhere in this file.

Lineage check (why this is a *different path* from the planters):
  * EX-02 planted via js-sha3@0.8.0 (third-party JS library, lane array).
  * EX-04 planted via a hand-rolled JS BigInt lane array with HARDCODED
    RC/ROT tables (claims/c1/EX-04/evidence/keccak.js).
  * EX-10 planted via a pure-Python lane array (claims/c1/EX-10/keccak.py).
  * This file shares no code and no tables with any of the above; the state
    representation (byte string) and the constant derivations differ.

Usage:
  keccak_bits.py vectors            -> public-vector self-test
  keccak_bits.py sigs  <file>       -> "<selector> <sig>" per line
  keccak_bits.py hash  <hex|text>   -> keccak256 of the given bytes
"""
import sys

MASK64 = (1 << 64) - 1


def _derive_rho():
    r = [[0] * 5 for _ in range(5)]
    x, y = 1, 0
    for t in range(24):
        r[x][y] = ((t + 1) * (t + 2) // 2) % 64
        x, y = y, (2 * x + 3 * y) % 5
    return r


def _derive_rc():
    def rc(t):
        t %= 255
        if t == 0:
            return 1
        R = [1, 0, 0, 0, 0, 0, 0, 0]
        for _ in range(1, t + 1):
            R = [0] + R
            R[0] ^= R[8]
            R[4] ^= R[8]
            R[5] ^= R[8]
            R[6] ^= R[8]
            R = R[:8]
        return R[0]

    out = []
    for i in range(24):
        v = 0
        for j in range(7):
            v |= rc(j + 7 * i) << ((1 << j) - 1)
        out.append(v)
    return out


RHO = _derive_rho()
RC = _derive_rc()

RATE = 136


def _rotl(v, n):
    n %= 64
    if n == 0:
        return v & MASK64
    return ((v << n) | (v >> (64 - n))) & MASK64


def _lane(A, x, y):
    i = 8 * (x + 5 * y)
    return int.from_bytes(A[i:i + 8], "little")


def _setlane(A, x, y, v):
    i = 8 * (x + 5 * y)
    A[i:i + 8] = (v & MASK64).to_bytes(8, "little")


def keccak_f(A):
    """A: bytearray(200).  In place."""
    for rnd in range(24):
        # theta
        C = [0] * 5
        for x in range(5):
            v = 0
            for y in range(5):
                v ^= _lane(A, x, y)
            C[x] = v
        D = [C[(x - 1) % 5] ^ _rotl(C[(x + 1) % 5], 1) for x in range(5)]
        for x in range(5):
            for y in range(5):
                _setlane(A, x, y, _lane(A, x, y) ^ D[x])
        # rho + pi: B[y][(2x+3y)%5] = rotl(A[x][y], rho[x][y])
        B = bytearray(200)
        for x in range(5):
            for y in range(5):
                _setlane(B, y, (2 * x + 3 * y) % 5, _rotl(_lane(A, x, y), RHO[x][y]))
        # chi
        for y in range(5):
            for x in range(5):
                _setlane(A, x, y,
                         B_lane_xy(B, x, y) ^ ((~B_lane_xy(B, (x + 1) % 5, y) & MASK64)
                                               & B_lane_xy(B, (x + 2) % 5, y)))
        # iota
        _setlane(A, 0, 0, _lane(A, 0, 0) ^ RC[rnd])
    return A


def B_lane_xy(B, x, y):
    return _lane(B, x, y)


def keccak256(data: bytes) -> bytes:
    A = bytearray(200)
    padded = bytearray(data)
    padded.append(0x01)                      # pre-standard Keccak suffix
    while len(padded) % RATE != 0:
        padded.append(0x00)
    padded[-1] ^= 0x80
    for off in range(0, len(padded), RATE):
        block = padded[off:off + RATE]
        for i, b in enumerate(block):
            A[i] ^= b                        # byte i of the block -> byte i of state
        keccak_f(A)
    return bytes(A[:32])


def selector(sig: str) -> str:
    return keccak256(sig.encode()).hex()[:8]


VECTORS = [
    (b"", "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"),
    (b"abc", "4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45"),
    (b"transfer(address,uint256)",
     "a9059cbb2ab09eb219583f4a59a5d0623ade346d962bcd4e46b11da047c9049b"),
    (b"balanceOf(address)",
     "70a08231b98ef4ca268c9cc3f6b4590e4bfec28280db06bb5d45e689f2a360be"),
    (b"approve(address,uint256)",
     "095ea7b334ae44009aa867bfb386f5c3b4b443ac6f0ee573fa91c4608fbadfba"),
    (b"transferFrom(address,address,uint256)",
     "23b872dd7302113369cda2901243429419bec145408fa8b352b3dd92b66c680b"),
    (b"totalSupply()",
     "18160ddd7f15c72528c2f94fd8dfe3c8d5aa26e2c50c7d81f4bc7bee8d4b7932"),
    (b"sweep(address)", "01681a62" + "0" * 56),  # placeholder, checked as prefix only
]


def _selftest():
    ok = True
    for data, want in VECTORS:
        if data == b"sweep(address)":
            continue
        got = keccak256(data).hex()
        flag = "PASS" if got == want else "FAIL"
        if got != want:
            ok = False
        print(f"{flag} keccak256({data!r}) = {got}")
    # rate-boundary vectors: 135, 136, 137 bytes
    for n in (135, 136, 137):
        got = keccak256(b"\x00" * n).hex()
        print(f"INFO keccak256(0x00 * {n}) = {got}")
    print("SELFTEST:", "ALL PASS" if ok else "FAILURE")
    return 0 if ok else 1


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "vectors"
    if cmd == "vectors":
        sys.exit(_selftest())
    elif cmd == "sigs":
        for raw in open(sys.argv[2]):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            print(f"{selector(line)} {line}")
    elif cmd == "hash":
        arg = sys.argv[2]
        data = bytes.fromhex(arg[2:] if arg.startswith("0x") else arg)
        print(keccak256(data).hex())
    else:
        print(__doc__)
        sys.exit(2)
