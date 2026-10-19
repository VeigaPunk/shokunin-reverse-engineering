import sys
src, dst = sys.argv[1], sys.argv[2]
b = bytearray(open(src, 'rb').read())
i = bytes(b).index(b'"entries": [')
off = i + 7  # last 's' of "entries"
before = b[off]
b[off] = 0x58  # 's' -> 'X'
open(dst, 'wb').write(bytes(b))
print("I4: offset=%d byte 0x%02x -> 0x%02x (\"entries\" -> \"entrieX\")" % (off, before, b[off]))
