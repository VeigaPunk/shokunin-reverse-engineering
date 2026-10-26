#!/usr/bin/env python3
"""make-tree.py -- deterministic compressible source trees for C2 damage recon.

Tree shapes the partial-damage recipe must survive:
  * several regular files (the recipe needs >= 2),
  * a multi-block file (size > block_size) so block selection is exercised,
  * a single-block file, nested directories, no symlinks,
  * compressible bodies (repeated words from a small alphabet) so the writer
    emits COMPRESSED data blocks, which is what a decompressor error needs.

Content is a pure function of (seed, relative path); the same seed always
produces the same bytes, in any directory.

Usage:
  python3 -B make-tree.py OUT_DIR SEED
"""

import hashlib
import os
import sys

WORDS = ('alpha', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf',
         'hotel', 'india', 'juliet', 'kilo', 'lima')


def stream(material, size):
    out = bytearray()
    counter = 0
    while len(out) < size:
        out += hashlib.sha256(material + b'#' + str(counter).encode()).digest()
        counter += 1
    return bytes(out[:size])


def body(seed, rel, size):
    """Compressible text of exactly `size` bytes: words chosen by a hash stream."""
    pool = stream((seed + '/' + rel).encode(), max(16, size))
    out = bytearray()
    i = 0
    while len(out) < size:
        word = WORDS[pool[i % len(pool)] % len(WORDS)]
        out += word.encode() + (b'\n' if i % 7 == 6 else b' ')
        i += 1
    return bytes(out[:size])


SHAPE = (
    ('readme.txt', 3100),
    ('payload.bin', 13000),        # 4 blocks at block_size 4096
    ('notes.txt', 900),
    ('docs/guide.md', 8200),       # 3 blocks
    ('docs/deep/table.txt', 4400),  # 2 blocks
)


def build(root, seed):
    for rel, size in SHAPE:
        path = os.path.join(root, *rel.split('/'))
        os.makedirs(os.path.dirname(path) or root, exist_ok=True)
        with open(path, 'wb') as handle:
            handle.write(body(seed, rel, size))
    return [rel for rel, _ in SHAPE]


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('usage: make-tree.py OUT_DIR SEED', file=sys.stderr)
        sys.exit(2)
    out, seed = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    made = build(out, seed)
    print('wrote %s: %d files' % (out, len(made)))
