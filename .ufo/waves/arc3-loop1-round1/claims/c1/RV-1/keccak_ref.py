"""Pure-Python Keccak-f[1600] sponge (RV-1 independent path).

Written from the Keccak reference spec. Two sponge configurations:
  keccak_256 -> Ethereum Keccak-256: rate 136 bytes, pad byte 0x01, final 0x80
  sha3_256   -> NIST SHA3-256:       rate 136 bytes, pad byte 0x06, final 0x80
sha3_256 exists ONLY to validate the permutation + sponge against an
independent host oracle (node/OpenSSL), since Ethereum's Keccak-256 is not
exposed by any library on this host.
"""

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
    0, 1, 62, 28, 27,
    36, 44, 6, 55, 20,
    3, 10, 43, 25, 39,
    41, 45, 15, 21, 8,
    18, 2, 61, 56, 14,
]


def rol(v, n):
    n %= 64
    if n == 0:
        return v & MASK64
    return ((v << n) | (v >> (64 - n))) & MASK64


def keccak_f1600(a):
    for rnd in range(24):
        c = [a[x] ^ a[x + 5] ^ a[x + 10] ^ a[x + 15] ^ a[x + 20] for x in range(5)]
        d = [c[(x - 1) % 5] ^ rol(c[(x + 1) % 5], 1) for x in range(5)]
        for x in range(5):
            for y in range(5):
                a[x + 5 * y] ^= d[x]
        b = [0] * 25
        for x in range(5):
            for y in range(5):
                b[y + 5 * ((2 * x + 3 * y) % 5)] = rol(a[x + 5 * y], ROT[x + 5 * y])
        for x in range(5):
            for y in range(5):
                a[x + 5 * y] = b[x + 5 * y] ^ ((~b[(x + 1) % 5 + 5 * y]) & b[(x + 2) % 5 + 5 * y] & MASK64)
        a[0] ^= RC[rnd]
    return a


def _sponge(data, rate, pad_byte, outlen):
    padded = bytearray(data)
    padded.append(pad_byte)
    while len(padded) % rate != 0:
        padded.append(0x00)
    padded[-1] |= 0x80

    a = [0] * 25
    for off in range(0, len(padded), rate):
        block = padded[off:off + rate]
        for i in range(rate // 8):
            a[i] ^= int.from_bytes(block[i * 8:i * 8 + 8], "little")
        keccak_f1600(a)

    out = bytearray()
    while len(out) < outlen:
        for i in range(rate // 8):
            out += a[i].to_bytes(8, "little")
        if len(out) < outlen:
            keccak_f1600(a)
    return bytes(out[:outlen])


def keccak_256(data):
    return _sponge(data, 136, 0x01, 32)


def sha3_256(data):
    return _sponge(data, 136, 0x06, 32)


def selector(signature):
    return keccak_256(signature.encode("ascii")).hex()[:8]
