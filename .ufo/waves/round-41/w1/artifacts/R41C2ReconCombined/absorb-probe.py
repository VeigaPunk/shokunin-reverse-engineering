#!/usr/bin/env python3
"""Probe the compressed-length determinant behind MH-4 with the frozen writer.

The round-40 partial recipe damages ``the last compressed data block of the
last-extracted regular file``.  In a random tree that block is often only tens
of bytes long (the tail of a file whose size is not a multiple of the 4 KiB
block), and in that regime a zero fill fails on both compressors.  MH-4 measured
that a *large* zeroed block is silently absorbed.  This probe makes the variable
explicit: one tree, three files, one big file that is last in scan order, so the
damaged block is ~1.4-1.6 KiB and the only thing that changes between runs is the
fill byte and the compressor.

Usage: absorb-probe.py --frozen DIR --out DIR --comp gzip|xz --fill HEX
Prints the frozen selector's report for the damaged block.
"""

import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import sys


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def semi_bytes(material, size):
    import hashlib as _h
    out = bytearray()
    counter = 0
    while len(out) < size:
        out.extend(_h.sha256(material + b':' + str(counter).encode()).digest())
        counter += 1
    return bytes(b & 0x0f for b in out[:size])


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b''):
            digest.update(chunk)
    return digest.hexdigest().upper()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--frozen', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--comp', choices=['gzip', 'xz'], required=True)
    parser.add_argument('--fill', default='00')
    args = parser.parse_args()

    writer = load_module(os.path.join(args.frozen, 'gen-squashfs.py'), 'sqw')
    gen2 = load_module(os.path.join(args.frozen, 'heldout-gen-v2.py'), 'gen2')

    tree = os.path.join(args.out, 'tree')
    os.makedirs(os.path.join(tree, 'a'), exist_ok=True)
    layout = [('a/one', 100), ('a/two', 200), ('a/zz-big', 3000)]
    oracle = []
    for rel, size in layout:
        path = os.path.join(tree, rel)
        with open(path, 'wb') as handle:
            handle.write(semi_bytes(b'r41-absorb:' + rel.encode(), size))
        oracle.append({'path': rel, 'size': size, 'sha256': sha256_file(path)})

    image = os.path.join(args.out, 'carrier.sqsh')
    with contextlib.redirect_stdout(io.StringIO()):
        writer.build_image(tree, image, 'be', args.comp)

    with open(image, 'rb') as handle:
        payload = bytearray(handle.read())
    report = {}
    payload = gen2.corruption_partial(payload, 'be', report)
    fill = int(args.fill, 16)
    start, length = report['block_offset'], report['block_length']
    if fill:
        payload[start:start + length] = bytes([fill]) * length
    with open(image, 'wb') as handle:
        handle.write(bytes(payload))

    print(json.dumps({'comp': args.comp, 'fill': args.fill,
                      'damage': report, 'image_bytes': os.path.getsize(image),
                      'image_sha256': sha256_file(image),
                      'oracle': oracle}, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
