import sys
src, dst = sys.argv[1], sys.argv[2]
b = bytearray(open(src, 'rb').read())
i = bytes(b).index(b'"entries": [')
before = b[i]
b[i] = 0x21  # '"' -> '!'
open(dst, 'wb').write(bytes(b))
print("I1: offset=%d byte 0x%02x -> 0x%02x" % (i, before, b[i]))
