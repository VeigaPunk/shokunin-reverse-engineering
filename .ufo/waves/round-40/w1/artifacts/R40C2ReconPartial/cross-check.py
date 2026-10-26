#!/usr/bin/env python3
"""cross-check.py -- my parser's payload hashes vs the independent oracle reader.

For each image: read it with sqfs-corrupt.py (my parser), rebuild every regular
file's bytes from the inode data blocks, and compare (path, sha256, size) with
the TSV produced by tools/round-39/sqfs-list.py (a reader that shares no code
with this one).  Prints one line per image; exit 1 on any mismatch.
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv):
    if len(argv) != 3:
        print('usage: cross-check.py IMG_DIR ORACLE_DIR', file=sys.stderr)
        return 2
    img_dir, oracle_dir = argv[1], argv[2]
    sq = load(os.path.join(HERE, 'sqfs-corrupt.py'), 'sqfscorrupt')
    bad = 0
    for name in sorted(os.listdir(img_dir)):
        if not name.endswith('.sqfs'):
            continue
        stem = name[:-5]
        with open(os.path.join(img_dir, name), 'rb') as handle:
            image = sq.Image(handle.read())
        mine = {}
        for entry in image.files():
            mine[entry['path']] = (sq.sha256(sq.read_file_data(image, entry)),
                                   entry['size'])
        theirs = {}
        with open(os.path.join(oracle_dir, stem + '.files.tsv'), 'r',
                  encoding='utf-8') as handle:
            for line in handle:
                path, digest, size = line.rstrip('\n').split('\t')
                theirs[path] = (digest, int(size))
        ok = mine == theirs
        bad += 0 if ok else 1
        print('%-16s %-4s files=%d %s' % (stem, 'ok' if ok else 'FAIL',
                                          len(mine),
                                          '' if ok else
                                          'mine=%s theirs=%s' % (mine, theirs)))
    print('cross-check: %d image(s) mismatched' % bad)
    return 0 if bad == 0 else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
