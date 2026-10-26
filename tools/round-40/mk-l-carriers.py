#!/usr/bin/env python3
"""Build the two lane-built R40-C1 carriers L1 (xz) and L2 (gzip) deterministically.

Each carrier is a genuine AVM-layout big-endian SquashFS v4 image written by
tools/round-40/gen-squashfs.py --endian avm-genuine from a fixed tree defined here
(contents are sha256-counter streams of a fixed label: no clock, no urandom).
The trees hold only regular files, directories and RETAINED symlinks (one in-tree
relative link and one absolute link each); no escaping link (vendor AVM members carry
none, round-40 R40C1ReconGaps G8) so the frozen gap rule is one `unpublished-entry`
per symlink.

Usage: mk-l-carriers.py OUTDIR     -> OUTDIR/L1/carrier.sqsh, OUTDIR/L2/carrier.sqsh, OUTDIR/*/src/
Exit 0 ok, 2 usage, 3 writer failure.
"""
import hashlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WRITER = os.path.join(HERE, 'gen-squashfs.py')


def stream(label, n):
    out = bytearray()
    i = 0
    while len(out) < n:
        out += hashlib.sha256(('%s/%d' % (label, i)).encode()).digest()
        i += 1
    return bytes(out[:n])


TREES = {
    'L1': {
        'comp': 'xz',
        'files': {
            'etc/version': b'kaidoku r40 L1 avm-genuine xz\n',
            'etc/init.d/rc.S': b'#!/bin/sh\necho boot\n' * 40,
            'usr/lib/libavm.so': stream('L1/libavm', 150000),
            'usr/share/web/index.html': b'<html><body>L1</body></html>\n' * 300,
            'var/empty.dat': b'',
            'sbin/tool': stream('L1/tool', 70000),
            'lib/modules/m.ko': stream('L1/mko', 9000),
        },
        'links': {
            'bin/sh': '../sbin/tool',             # in-tree relative
            'etc/mtab': '/proc/mounts',            # absolute (re-rooted, kept)
        },
    },
    'L2': {
        'comp': 'gzip',
        'files': {
            'etc/hosts': b'127.0.0.1 localhost\n',
            'opt/app/data.bin': stream('L2/data', 200000),
            'opt/app/config.json': b'{"layout": "avm", "round": 40}\n',
            'usr/bin/busy': stream('L2/busy', 40000),
            'usr/share/doc/README': b'lane-built AVM-layout gzip carrier\n' * 120,
            'zero': b'',
        },
        'links': {
            'usr/bin/ls': 'busy',                  # in-tree relative, same dir
            'bin/busy': '/usr/bin/busy',           # absolute
        },
    },
}


def build_tree(root, spec):
    for rel, data in sorted(spec['files'].items()):
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'wb') as fh:
            fh.write(data)
    for rel, target in sorted(spec['links'].items()):
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        os.symlink(target, p)


def main():
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    out = os.path.abspath(sys.argv[1])
    for cid, spec in TREES.items():
        d = os.path.join(out, cid)
        src = os.path.join(d, 'src')
        os.makedirs(d, exist_ok=False)
        build_tree(src, spec)
        img = os.path.join(d, 'carrier.sqsh')
        p = subprocess.run([sys.executable, '-I', '-B', WRITER, src, img,
                            '--endian', 'avm-genuine', '--comp', spec['comp']],
                           capture_output=True, text=True)
        if p.returncode != 0:
            print(p.stderr, file=sys.stderr)
            return 3
        print('%s\t%s\t%s' % (cid, img, hashlib.sha256(open(img, 'rb').read()).hexdigest()))
    return 0


if __name__ == '__main__':
    sys.exit(main())
