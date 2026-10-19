#!/usr/bin/env python3
"""Pure-Python Keccak-256 (original Keccak padding 0x01, not SHA3 0x06).

Self-validates against three public vectors before use:
  keccak256(b'')        = c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470
  b'transfer(address,uint256)'  -> a9059cbb...
  b'balanceOf(address)'         -> 70a08231...
"""
import sys

RC = [0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
      0x8000000080008000, 0x000000000000808B, 0x0000000080000001,
      0x8000000080008081, 0x8000000000008009, 0x000000000000008A,
      0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
      0x000000008000808B, 0x800000000000008B, 0x8000000000008089,
      0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
      0x000000000000800A, 0x800000008000000A, 0x8000000080008081,
      0x8000000000008080, 0x0000000080000001, 0x8000000080008008]

# rotation offsets, lane index = x + 5*y
ROT = [[0, 36, 3, 41, 18],
       [1, 44, 10, 45, 2],
       [62, 6, 43, 15, 61],
       [28, 55, 25, 21, 56],
       [27, 20, 39, 8, 14]]

MASK = 0xFFFFFFFFFFFFFFFF


def rol(x, n):
    n %= 64
    return ((x << n) | (x >> (64 - n))) & MASK


def keccak_f(state):
    for rnd in range(24):
        C = [state[x] ^ state[x + 5] ^ state[x + 10] ^ state[x + 15] ^ state[x + 20]
             for x in range(5)]
        D = [C[(x - 1) % 5] ^ rol(C[(x + 1) % 5], 1) for x in range(5)]
        for x in range(5):
            for y in range(5):
                state[x + 5 * y] ^= D[x]
        B = [0] * 25
        for x in range(5):
            for y in range(5):
                B[y + 5 * ((2 * x + 3 * y) % 5)] = rol(state[x + 5 * y], ROT[x][y])
        for x in range(5):
            for y in range(5):
                state[x + 5 * y] = B[x + 5 * y] ^ ((~B[(x + 1) % 5 + 5 * y]) & B[(x + 2) % 5 + 5 * y])
        state[0] ^= RC[rnd]
    return state


def keccak256(data: bytes) -> bytes:
    rate = 136
    state = [0] * 25
    # pad10*1, Keccak domain byte 0x01
    padded = bytearray(data)
    padlen = rate - (len(padded) % rate)
    padded += b'\x01' + b'\x00' * (padlen - 2) + b'\x80' if padlen >= 2 else b'\x81'
    for off in range(0, len(padded), rate):
        block = padded[off:off + rate]
        for i in range(rate // 8):
            lane = int.from_bytes(block[i * 8:(i + 1) * 8], 'little')
            state[i] ^= lane
        keccak_f(state)
    out = b''.join(state[i].to_bytes(8, 'little') for i in range(4))
    return out[:32]


def selector(sig: str) -> str:
    return keccak256(sig.encode()).hex()[:8]


if __name__ == '__main__':
    vectors = {
        b'': 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470',
    }
    ok = True
    for msg, want in vectors.items():
        got = keccak256(msg).hex()
        status = 'OK' if got == want else 'FAIL'
        if got != want:
            ok = False
        print(f'selftest keccak256({msg!r}) = {got} [{status}]')
    known = {
        'transfer(address,uint256)': 'a9059cbb',
        'transferFrom(address,address,uint256)': '23b872dd',
        'balanceOf(address)': '70a08231',
        'approve(address,uint256)': '095ea7b3',
        'totalSupply()': '18160ddd',
        'owner()': '8da5cb5b',
        'deposit()': 'd0e30db0',
    }
    for sig, want in known.items():
        got = selector(sig)
        status = 'OK' if got == want else 'FAIL'
        if got != want:
            ok = False
        print(f'selftest sel({sig}) = 0x{got} want 0x{want} [{status}]')
    print('SELFTEST', 'PASS' if ok else 'FAIL')
    sys.exit(0 if ok else 1)
