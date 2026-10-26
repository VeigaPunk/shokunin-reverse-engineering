#!/usr/bin/env python3
"""Rebuild the synthetic many-symlink AVM-genuine carrier used by seat R41W2C1Run.

Produces TREE (build dir) and CARRIER (SquashFS v4 image, `--endian avm-genuine`,
gzip), sha256 c1336c15e8e3a6d9564e945f5aff233e5f7a707682d4d00708ec1d1a08494f15,
265864 bytes, 2401 inodes (640 regular files, 1600 symlinks, 160 dirs).

Usage: gen-synth-carrier.py [tree] [carrier]
Requires the frozen writer tools/round-41/gen-squashfs.py (or pass --writer).

Exact evidence commands used (scratch S=/fast/scratch/hyaku/kaidoku-r41/R41W2C1Run):
  python3 -I -B gen-synth-carrier.py $S/synth-tree $S/synth-carrier.sqsh
  python3 -I -B tools/round-41/gen-squashfs.py $S/synth-tree $S/synth-carrier.sqsh \
      --endian avm-genuine --comp gzip
  sha256sum $S/synth-carrier.sqsh   # c1336c15e8e3a6d9564e945f5aff233e5f7a707682d4d00708ec1d1a08494f15
"""
import argparse
import hashlib
import os
import shutil
import subprocess
import sys

WRITER = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-41/gen-squashfs.py'
ND, NF, NL = 160, 4, 10  # dirs, files per dir, links per dir


def stream(label, n):
    out = bytearray()
    i = 0
    while len(out) < n:
        out += hashlib.sha256(('%s/%d' % (label, i)).encode()).digest()
        i += 1
    return bytes(out[:n])


def build_tree(root):
    for d in range(ND):
        dn = 'd%03d' % d
        for f in range(NF):
            rel = '%s/f%02d' % (dn, f)
            p = os.path.join(root, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, 'wb').write(stream(rel, 256))
        for l in range(NL):
            rel = '%s/l%02d' % (dn, l)
            p = os.path.join(root, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            os.symlink('f00', p)  # relative, in-tree, single hop -> kept, unpublished gap


def counts(root):
    nf = nl = nd = 0
    for dp, dn, fn in os.walk(root):
        dn[:] = [x for x in dn if not os.path.islink(os.path.join(dp, x))]
        nd += 1
        for f in fn:
            if os.path.islink(os.path.join(dp, f)):
                nl += 1
            else:
                nf += 1
    return nf, nl, nd - 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('tree')
    ap.add_argument('carrier')
    ap.add_argument('--writer', default=WRITER)
    a = ap.parse_args()
    shutil.rmtree(a.tree, ignore_errors=True)
    os.makedirs(a.tree)
    build_tree(a.tree)
    p = subprocess.run([sys.executable, '-I', '-B', a.writer, a.tree, a.carrier,
                        '--endian', 'avm-genuine', '--comp', 'gzip'],
                       capture_output=True, text=True)
    if p.returncode != 0:
        print(p.stdout, file=sys.stderr)
        print(p.stderr, file=sys.stderr)
        return 3
    nf, nl, nd = counts(a.tree)
    raw = open(a.carrier, 'rb').read()
    print('files %d links %d dirs %d bytes %d sha256 %s' % (
        nf, nl, nd, len(raw), hashlib.sha256(raw).hexdigest()))
    return 0


if __name__ == '__main__':
    sys.exit(main())
