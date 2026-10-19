#!/usr/bin/env python3
"""Debug oracle for the slice keccak: standard lane-array Keccak-f[1600]
(hardcoded standard tables, written independently) vs keccak_slice.keccak_f."""
import sys
sys.path.insert(0, "/var/tmp/rv1-r3/tools")
import keccak_slice as K

RC_TABLE = [0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
            0x8000000080008000, 0x000000000000808B, 0x0000000080000001,
            0x8000000080008081, 0x8000000000008009, 0x000000000000008A,
            0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
            0x000000008000808B, 0x800000000000008B, 0x8000000000008089,
            0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
            0x000000000000800A, 0x800000008000000A, 0x8000000080008081,
            0x8000000000008080, 0x0000000080000001, 0x8000000080008008]
RHO_TABLE = [[0, 36, 3, 41, 18],
             [1, 44, 10, 45, 2],
             [62, 6, 43, 15, 61],
             [28, 55, 25, 21, 56],
             [27, 20, 39, 8, 14]]
M64 = (1 << 64) - 1


def rol(x, n):
    n %= 64
    return ((x << n) | (x >> (64 - n))) & M64


def lane_permute(A):
    A = A[:]
    for rnd in range(24):
        C = [A[x][0] ^ A[x][1] ^ A[x][2] ^ A[x][3] ^ A[x][4] for x in range(5)]
        D = [C[(x - 1) % 5] ^ rol(C[(x + 1) % 5], 1) for x in range(5)]
        for x in range(5):
            for y in range(5):
                A[x][y] ^= D[x]
        B = [[0] * 5 for _ in range(5)]
        for x in range(5):
            for y in range(5):
                B[y][(2 * x + 3 * y) % 5] = rol(A[x][y], RHO_TABLE[x][y])
        for x in range(5):
            for y in range(5):
                A[x][y] = B[x][y] ^ ((~B[(x + 1) % 5][y]) & B[(x + 2) % 5][y] & M64)
        A[0][0] ^= RC_TABLE[rnd]
    return A


def slices_to_lanes(S):
    A = [[0] * 5 for _ in range(5)]
    for z in range(64):
        for y in range(5):
            for x in range(5):
                if (S[z] >> (x + 5 * y)) & 1:
                    A[x][y] |= 1 << z
    return A


def lanes_to_slices(A):
    S = [0] * 64
    for z in range(64):
        v = 0
        for y in range(5):
            for x in range(5):
                if (A[x][y] >> z) & 1:
                    v |= 1 << (x + 5 * y)
        S[z] = v
    return S


if __name__ == "__main__":
    print("RC derived  :", [hex(c) for c in K.RC[:4]])
    print("RC standard :", [hex(c) for c in RC_TABLE[:4]])
    print("RC identical:", K.RC == RC_TABLE)
    print("RHO derived :", K.RHO)
    print("RHO standard:", RHO_TABLE)
    print("RHO identical:", K.RHO == RHO_TABLE)
    # deterministic pseudo-random state
    A0 = [[(0x1234567890ABCDEF * (x + 5 * y + 1) + 0xDEADBEEF) & M64 for y in range(5)]
          for x in range(5)]
    exp = lane_permute(A0)
    S0 = lanes_to_slices(A0)
    K.keccak_f(S0)
    got = slices_to_lanes(S0)
    diff = [(x, y, hex(exp[x][y]), hex(got[x][y]))
            for x in range(5) for y in range(5) if exp[x][y] != got[x][y]]
    print("permutation mismatch lanes:", len(diff))
    for d in diff[:5]:
        print("  ", d)