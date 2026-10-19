#!/usr/bin/env python3
"""RV-1 (arc3-loop1-round3, chain c1) — Keccak-256 in the SLICE formulation.

Independent keccak path: state = 64 "slices" of 25 bits (bit p = x + 5y),
instead of the usual 25 x uint64 lane array.  Constants are DERIVED, not
tabulated: rho offsets from the (x,y) walk recurrence, round constants from
the Keccak LFSR rc(t).  The repo's prior keccak implementations
(RV-1/r1 keccak_ref.py, EX-03 keccak256.py) are lane-array + hardcoded
tables; this file shares no code and no tables with them.

Usage:
  keccak_slice.py vectors            -> public vector self-test
  keccak_slice.py sigs <file>        -> one "selector sig" per line (hex w/o 0x)
"""
import sys

MASK25 = (1 << 25) - 1
RC = None
RHO = None


def _derive_rho():
    """r[x][y] = (t+1)(t+2)/2 mod 64 for the t-th lane of the (1,0)->(y,2x+3y) walk."""
    r = [[0] * 5 for _ in range(5)]
    x, y = 1, 0
    for t in range(24):
        r[x][y] = ((t + 1) * (t + 2) // 2) % 64
        x, y = y, (2 * x + 3 * y) % 5
    return r


def _derive_rc():
    """RC[i] bit j = rc(j + 7i) (j=0..6), bit 7 = 0; rc from the spec LFSR."""
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
            v |= rc(j + 7 * i) << (2 ** j - 1)
        out.append(v)
    return out


RHO = _derive_rho()
RC = _derive_rc()

# spread mask: column x occupies bits x, x+5, x+10, x+15, x+20
_COL = []
for _x in range(5):
    m = 0
    for _y in range(5):
        m |= 1 << (_x + 5 * _y)
    _COL.append(m)


def _parity_vec(v):
    """5-bit vector: bit x = xor of column x of the 25-bit slice."""
    return (v ^ (v >> 5) ^ (v >> 10) ^ (v >> 15) ^ (v >> 20)) & 0x1F


def _rot5(v, k):
    k %= 5
    return ((v << k) | (v >> (5 - k))) & 0x1F


def _rot5_cols(v, k):
    """Rotate the 5-bit column fields of a 25-bit slice by k, per y."""
    out = 0
    for y in range(5):
        f = (v >> (5 * y)) & 0x1F
        out |= _rot5(f, k) << (5 * y)
    return out


def _spread(v5):
    """Expand 5-bit column vector into a 25-bit slice (all y of column x set)."""
    s = 0
    for x in range(5):
        if (v5 >> x) & 1:
            s |= _COL[x]
    return s


def keccak_f(S):
    """S: list of 64 ints (25-bit slices).  Mutates in place."""
    for rnd in range(24):
        # theta
        Cv = [_parity_vec(s) for s in S]
        # Dvec(z): bit x = C[(x-1)%5][z] ^ C[(x+1)%5][z-1]
        for z in range(64):
            zc = (z - 1) % 64
            d = _rot5(Cv[z], 1) ^ _rot5(Cv[zc], -1)
            if d:
                S[z] ^= _spread(d)
        # rho + pi: new[x][y][z] = old[x0][y0][(z - r[x0][y0]) % 64],
        # with (x0,y0) = ((x+3y)%5, x)
        newS = [0] * 64
        for z in range(64):
            acc = 0
            for y in range(5):
                for x in range(5):
                    x0 = (x + 3 * y) % 5
                    y0 = x
                    z0 = (z - RHO[x0][y0]) % 64
                    if (S[z0] >> (x0 + 5 * y0)) & 1:
                        acc |= 1 << (x + 5 * y)
            newS[z] = acc
        S[:] = newS
        # chi
        for z in range(64):
            v = S[z]
            r1 = _rot5_cols(v, -1)  # bit x = A[(x+1)%5]
            r2 = _rot5_cols(v, -2)  # bit x = A[(x+2)%5]
            S[z] = v ^ ((~r1) & r2 & MASK25)
        # iota
        rc = RC[rnd]
        z = 0
        while rc:
            if rc & 1:
                S[z] ^= 1  # position p = 0 (lane x=0,y=0)
            rc >>= 1
            z += 1


def _absorb_bits(S, data):
    """XOR block bytes into the state.

    Byte b sits in lane p = x+5y = b//8 as its byte k = b%8, so bit j of the
    byte is state bit z = 8k+j of that lane -> slice z, position p.
    """
    for b_i, b in enumerate(data):
        p = b_i // 8
        k = b_i % 8
        if not b:
            continue
        for j in range(8):
            if (b >> j) & 1:
                S[8 * k + j] ^= 1 << p


def _squeeze_bytes(S, n):
    out = bytearray()
    for b_i in range(n):
        p = b_i // 8
        k = b_i % 8
        byte = 0
        for j in range(8):
            if (S[8 * k + j] >> p) & 1:
                byte |= 1 << j
        out.append(byte)
    return bytes(out)


def keccak256(data: bytes) -> bytes:
    rate = 136  # 1088 bits
    S = [0] * 64
    # pad10*1 with the original Keccak (pre-SHA3) suffix byte 0x01
    padded = bytearray(data)
    padded.append(0x01)
    while len(padded) % rate != 0:
        padded.append(0x00)
    padded[-1] ^= 0x80
    for off in range(0, len(padded), rate):
        _absorb_bits(S, padded[off:off + rate])
        keccak_f(S)
    return _squeeze_bytes(S, 32)


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
]

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "vectors"
    if mode == "vectors":
        ok = True
        for data, want in VECTORS:
            got = keccak256(data).hex()
            stat = "OK " if got == want else "FAIL"
            ok = ok and got == want
            print(f"{stat}  keccak256({data!r}) = {got}")
        print("ALL_VECTORS_MATCH:", ok)
        print("RC[0..2] derived:", [hex(c) for c in RC[:3]])
        print("RHO[0][1] (lane 1,0):", RHO[1][0], "RHO[1][1]:", RHO[1][1])
        sys.exit(0 if ok else 1)
    elif mode == "sigs":
        with open(sys.argv[2]) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                print(f"{selector(line)} {line}")
    else:
        print("unknown mode", mode, file=sys.stderr)
        sys.exit(2)