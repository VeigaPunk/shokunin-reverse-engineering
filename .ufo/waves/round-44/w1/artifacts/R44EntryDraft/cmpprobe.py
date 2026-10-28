#!/usr/bin/env python3
"""R44EntryDraft: probe `cmp -l` exit status against file size.

Observed 2026-10-28 on this host (diffutils 3.12-2): `/usr/bin/cmp -l` exits 1 for
differing inputs below 4096 bytes and 0 at/above 4096 bytes, while plain `cmp` and
`cmp -s` exit 1 in every case. This probe reproduces the matrix from a private copy
of one committed carrier and prints one line per size. Exit 0 when the probe ran.

Usage: python3 -I -B cmpprobe.py <base-file>
"""
import os
import subprocess
import sys
import tempfile


def main():
    base = open(sys.argv[1], "rb").read()
    tmp = tempfile.mkdtemp(prefix="r44-cmpprobe-")
    a = os.path.join(tmp, "a.bin")
    b = os.path.join(tmp, "b.bin")
    for n in (255, 4095, 4096, 4097, 8192):
        x = (base * ((n // len(base)) + 1))[:n]
        y = bytearray(x)
        y[min(2, n - 1)] ^= 0xFF
        open(a, "wb").write(x)
        open(b, "wb").write(bytes(y))
        rl = subprocess.run(["/usr/bin/cmp", "-l", a, b], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
        rp = subprocess.run(["/usr/bin/cmp", a, b], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
        rs = subprocess.run(["/usr/bin/cmp", "-s", a, b], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
        print(f"size={n} cmp_-l_exit={rl.returncode} cmp_exit={rp.returncode} "
              f"cmp_-s_exit={rs.returncode} differing_bytes=1")
    for p in (a, b):
        os.unlink(p)
    os.rmdir(tmp)
    return 0


if __name__ == "__main__":
    sys.exit(main())
