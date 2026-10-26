#!/usr/bin/env python3
"""mkdev.py -- build development-only SquashFS carriers with explicit symlink mixes.

Every tree is authored here (deterministic bytes, no RNG, no clock) and written
with tools/round-39/gen-squashfs.py via its CLI.  These are development inputs,
never frozen carriers and never held-out material.

Usage:
  python3 mkdev.py --root DIR [--only NAME...]

Writes DIR/<name>/tree/..., DIR/<name>/carrier.sqsh, DIR/<name>/build.json
(endian, compression, exact build argv, tree listing, symlink kinds).
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
GEN = os.path.join(LANE, 'tools', 'round-39', 'gen-squashfs.py')

# name -> (endian, comp, files, dirs, symlinks [(rel path, target)])
CASES = {
    # --- BE mixed: >=1 escaping and >=1 in-tree relative symlink -------------------
    'mx1': ('be', 'gzip',
            {'a.txt': b'alpha\n', 'b.txt': b'beta\n', 'd1/c.txt': b'gamma\n'},
            ['d1'],
            [('esc', '../outside-target'), ('d1/ini', '../a.txt')]),
    'mx2': ('be', 'xz',
            {'a.txt': b'alpha\n', 'd1/c.txt': b'gamma\n', 'd2/f.txt': b'delta\n'},
            ['d1', 'd2'],
            [('d1/up', '../../outside2'), ('d2/i1', '../d1/c.txt')]),
    'mx3': ('be', 'gzip',
            {'a.txt': b'alpha\n', 'b.txt': b'beta\n',
             'd1/c.txt': b'gamma\n', 'd2/f.txt': b'delta\n'},
            ['d1', 'd2'],
            [('e1', '../x'), ('e2', '../y'),
             ('d2/i1', '../b.txt'), ('d2/i2', '../d1/c.txt')]),
    # --- LE mixed -----------------------------------------------------------------
    'mx4': ('le', 'gzip',
            {'a.txt': b'alpha\n', 'b.txt': b'beta\n', 'd1/c.txt': b'gamma\n'},
            ['d1'],
            [('esc', '../outside-target'), ('d1/ini', '../a.txt')]),
    'mx5': ('le', 'xz',
            {'a.txt': b'alpha\n', 'd1/c.txt': b'gamma\n', 'd2/f.txt': b'delta\n'},
            ['d1', 'd2'],
            [('d1/up', '../../outside2'), ('d2/i1', '../d1/c.txt')]),
    'mx6': ('le', 'gzip',
            {'a.txt': b'alpha\n', 'b.txt': b'beta\n',
             'd1/c.txt': b'gamma\n', 'd2/f.txt': b'delta\n'},
            ['d1', 'd2'],
            [('e1', '../x'), ('e2', '../y'),
             ('d2/i1', '../b.txt'), ('d2/i2', '../d1/c.txt')]),
    # --- LE singles ----------------------------------------------------------------
    'esc-le': ('le', 'gzip',
               {'a.txt': b'alpha\n', 'd1/c.txt': b'gamma\n'},
               ['d1'],
               [('esc', '../outside-target')]),
    'intree-le': ('le', 'gzip',
                  {'a.txt': b'alpha\n', 'd1/c.txt': b'gamma\n'},
                  ['d1'],
                  [('d1/ini', '../a.txt')]),
    # --- interplay probes -----------------------------------------------------------
    # same tree as mx1, but written with the marker-only "avm" mode
    # (BE body + mkfs_time == bytes_used, so unblob drops -be).
    'mx1-avm': ('avm', 'gzip',
                {'a.txt': b'alpha\n', 'b.txt': b'beta\n', 'd1/c.txt': b'gamma\n'},
                ['d1'],
                [('esc', '../outside-target'), ('d1/ini', '../a.txt')]),
    # compressible multi-block files so one corrupted compressed block can fail
    # after earlier files were extracted
    'mx8': ('be', 'gzip',
            {'a.txt': b'A' * 9000, 'b.txt': b'B' * 9000, 'd1/c.txt': b'C' * 9000},
            ['d1'],
            [('esc', '../outside-target'), ('d1/ini', '../a.txt')]),
    # mixed symlinks but zero regular files: both rows that own the gap kinds
    # require published files > 0, so this vector is expected to be unclassified
    'mx-nofiles': ('be', 'gzip', {}, [],
                   [('esc', '../outside-target'), ('in', 'missing.txt')]),
    # multi-block files so a truncated image can publish some files and fail later
    'mx7': ('be', 'gzip',
            {'a.bin': ('stream', 6000), 'b.bin': ('stream', 6000),
             'd1/c.bin': ('stream', 6000)},
            ['d1'],
            [('esc', '../outside-target'), ('d1/ini', '../a.bin')]),
}


def stream_bytes(material, size):
    """SHA-256 counter stream: incompressible and interpreter-independent."""
    out = bytearray()
    counter = 0
    while len(out) < size:
        out += hashlib.sha256(material + b'#' + str(counter).encode()).digest()
        counter += 1
    return bytes(out[:size])


def build(name, root):
    endian, comp, files, dirs, links = CASES[name]
    base = os.path.join(root, name)
    tree = os.path.join(base, 'tree')
    if os.path.isdir(base):
        shutil.rmtree(base)
    os.makedirs(tree)
    for d in dirs:
        os.makedirs(os.path.join(tree, d), exist_ok=True)
    for rel, data in sorted(files.items()):
        p = os.path.join(tree, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if isinstance(data, tuple) and data[0] == 'stream':
            data = stream_bytes(rel.encode(), data[1])
        with open(p, 'wb') as fh:
            fh.write(data)
    for rel, target in links:
        p = os.path.join(tree, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        os.symlink(target, p)
    image = os.path.join(base, 'carrier.sqsh')
    argv = [sys.executable, '-I', '-B', GEN, tree, image,
            '--endian', endian, '--comp', comp]
    proc = subprocess.run(argv, capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit('%s: generator failed (%d): %s'
                         % (name, proc.returncode, proc.stderr.strip()))
    record = {'name': name, 'endian': endian, 'compression': comp,
              'build_argv': argv, 'generator_stdout': proc.stdout.strip(),
              'files': sorted(files), 'dirs': sorted(dirs),
              'symlinks': [{'path': r, 'target': t} for r, t in links]}
    with open(os.path.join(base, 'build.json'), 'w', encoding='utf-8') as fh:
        json.dump(record, fh, indent=2, sort_keys=True)
        fh.write('\n')
    print(name, endian, comp, os.path.getsize(image))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--only', nargs='*')
    ns = ap.parse_args()
    names = ns.only or sorted(CASES)
    for name in names:
        build(name, ns.root)
    return 0


if __name__ == '__main__':
    sys.exit(main())
