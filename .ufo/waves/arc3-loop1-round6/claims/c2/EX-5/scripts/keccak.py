"""Pure-Python Keccak-256 (Ethereum) written for seat EX-5, arc3-loop1-round6.

Self-test vectors (run `python3 keccak.py`):
  ""                                      -> c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470
  "abc"                                   -> 4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45
  "transfer(address,uint256)"             -> a9059cbb2ab09eb219583f4a59a5d0623ade346d962bcd4e46b11da047c9049b
"""
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
M64 = (1 << 64) - 1


def _rol(x, n):
    n %= 64
    return ((x << n) | (x >> (64 - n))) & M64


def keccak_f1600(a):
    for rnd in range(24):
        c = [a[x] ^ a[x + 5] ^ a[x + 10] ^ a[x + 15] ^ a[x + 20] for x in range(5)]
        d = [c[(x - 1) % 5] ^ _rol(c[(x + 1) % 5], 1) for x in range(5)]
        for x in range(5):
            for y in range(5):
                a[x + 5 * y] ^= d[x]
        b = [0] * 25
        for x in range(5):
            for y in range(5):
                b[y + 5 * ((2 * x + 3 * y) % 5)] = _rol(a[x + 5 * y], ROT[x][y])
        for x in range(5):
            for y in range(5):
                a[x + 5 * y] = b[x + 5 * y] ^ ((~b[(x + 1) % 5 + 5 * y]) & b[(x + 2) % 5 + 5 * y] & M64)
        a[0] ^= RC[rnd]
    return a


def keccak256(data: bytes) -> bytes:
    rate = 136
    msg = bytearray(data)
    msg.append(0x01)
    while len(msg) % rate:
        msg.append(0x00)
    msg[-1] |= 0x80
    a = [0] * 25
    for off in range(0, len(msg), rate):
        block = msg[off:off + rate]
        for i in range(rate // 8):
            a[i] ^= int.from_bytes(block[8 * i:8 * i + 8], 'little')
        keccak_f1600(a)
    out = b''.join(a[i].to_bytes(8, 'little') for i in range(4))
    return out


def selector(sig: str) -> str:
    return keccak256(sig.encode()).hex()[:8]


if __name__ == '__main__':
    vectors = {
        '': 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470',
        'abc': '4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45',
        'transfer(address,uint256)': 'a9059cbb2ab09eb219583f4a59a5d0623ade346d962bcd4e46b11da047c9049b',
    }
    ok = 0
    for s, want in vectors.items():
        got = keccak256(s.encode()).hex()
        print(f'{s!r}: {got} {"OK" if got == want else "FAIL want " + want}')
        ok += got == want
    print(f'{ok}/{len(vectors)} vectors pass')
