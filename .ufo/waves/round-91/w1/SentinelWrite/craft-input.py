#!/usr/bin/env python3
"""craft-input.py - SentinelWrite F1 reproduction input (read-only analysis, not a lane tool).

Writes an N-byte synthetic ELF whose walk stops at a break block of size su_p, followed
by a non-sentinel implausible header, then stride-20 plausible b_info headers that are
successor candidates for derive_break().  C successors are in the derive window:
su_p = 27 gives C = 0; su_p = 28 + 20*(C-1) gives C successors.

Usage: python3 -B craft-input.py <N_bytes> <su_p> <out_path>
"""
import struct
import sys

V, F, M, U = 13, 5, 2, 0x00400000


def craft(N: int, su_p: int) -> bytes:
    d = bytearray(N)
    d[0:4] = b"\x7fELF"
    d[4] = 2
    d[5] = 1
    m = 64
    d[m + 6] = V
    d[m + 7] = F
    struct.pack_into("<I", d, m + 12, U)
    b0 = m + 20
    ph = N - 32
    h = bytearray(32)
    h[4], h[5], h[6] = V, F, M
    struct.pack_into("<III", h, 16, U, N - 64, U)
    h[31] = sum(h[4:31]) % 251
    d[ph:ph + 32] = h
    struct.pack_into("<II", d, b0, 16, 8)
    d[b0 + 8] = M
    p = b0 + 20
    struct.pack_into("<II", d, p, su_p, 8)
    d[p + 8] = M
    x = p + 20
    struct.pack_into("<II", d, x, 16, 0xFFFF)
    d[x + 8] = M
    q = x + 20
    while q + 20 <= ph - 40:
        struct.pack_into("<II", d, q, 16, 8)
        d[q + 8] = M
        q += 20
    struct.pack_into("<II", d, q, 16, 0xFFFF)
    d[q + 8] = M
    return bytes(d)


if __name__ == "__main__":
    n, su, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    with open(out, "wb") as fh:
        fh.write(craft(n, su))
