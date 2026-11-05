import struct, glob, os
for f in sorted(glob.glob("work-base/*.upx")):
    b = open(f, "rb").read()
    pe = struct.unpack_from("<I", b, 0x3C)[0]
    n = struct.unpack_from("<H", b, pe + 6)[0]
    opt = struct.unpack_from("<H", b, pe + 20)[0]
    magic = struct.unpack_from("<H", b, pe + 24)[0]
    falign = struct.unpack_from("<I", b, pe + 24 + 36)[0]
    salign = struct.unpack_from("<I", b, pe + 24 + 32)[0]
    st = pe + 24 + opt
    secs = [(b[st+40*k:st+40*k+8].rstrip(b"\0").decode("latin1"), struct.unpack_from("<I", b, st+40*k+16)[0], struct.unpack_from("<I", b, st+40*k+20)[0]) for k in range(n)]
    i = b.find(b"UPX!")
    s1 = secs[1][2] - 64
    last = secs[-1]
    end = (last[2] + last[1] + falign - 1) // falign * falign
    print(os.path.basename(f), "magic=0x%x n=%d falign=%#x salign=%#x" % (magic, n, falign, salign), "hdr_off=%d window_start=%d off_in_window=%d" % (i, s1, i - s1), "len=%d aligned_end=%d overlay=%d" % (len(b), end, len(b)-end), [s[0] for s in secs])
