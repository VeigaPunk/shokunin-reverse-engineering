import sys
src, dst = sys.argv[1], sys.argv[2]
b = bytearray(open(src, 'rb').read())
i = bytes(b).index(b'"line": 59')
off = i + 8  # the '5' of 59
before = b[off]
b[off] = 0x36  # '5' -> '6'
open(dst, 'wb').write(bytes(b))
print("I2: offset=%d byte 0x%02x -> 0x%02x (line 59 -> 69 in sc59-stanza-key-anchor)" % (off, before, b[off]))
