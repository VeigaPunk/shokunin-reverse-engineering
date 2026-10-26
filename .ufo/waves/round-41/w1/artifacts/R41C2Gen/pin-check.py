#!/usr/bin/env python3
"""R41C2Gen — the R40-CL4 pin, red and green.

Builds two standard-BE SquashFS v4 images with the lane's writer, selected so the
partial recipe's target block lands on the two sides of the measured threshold,
and calls the generator's own damage function on each:

  * hex3100  ~1.7 KiB compressed target  -> REFUSED by MAX_DAMAGED_BLOCK (the
               regime MH-4 measured as ABSORBED: the extractor lands `clean`
               with a corrupt file on disk).
  * pat1500  ~dozens of bytes compressed -> ACCEPTED, the class's own regime.

Exit 0 = red case refused AND green case accepted; 1 = the pin does not bite.

    TMPDIR=/fast/scratch/hyaku/kaidoku-r41/R41C2Gen python3 -I -B pin-check.py
"""
import contextlib
import hashlib
import importlib.util
import io
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(HERE, 'heldout-gen-v3.py')
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
WRITER = os.environ.get('KAIDOKU_GEN_SQUASHFS',
                        os.path.join(LANE, 'tools', 'round-40', 'gen-squashfs.py'))


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def hexstream(label, size):
    """MH-4's `hex` shape: half the bytes are entropy, so a compressed block of a
    4096-byte chunk stays ~1.7 KiB (the regime where a zero fill is absorbed)."""
    out = bytearray()
    i = 0
    while len(out) < size:
        out += hashlib.sha256(('%s/%d' % (label, i)).encode()).hexdigest().encode()[:32]
        i += 1
    return bytes(out[:size])


def main():
    gen = load(GEN, 'v3')
    writer = gen.load_writer(WRITER)
    gen.install_block_encoder(writer)
    work = tempfile.mkdtemp(prefix='pin-check-',
                            dir=os.environ.get('TMPDIR') or tempfile.gettempdir())

    def attempt(name, last_size, content):
        tree = os.path.join(work, 'tree-' + name)
        os.makedirs(tree)
        with open(os.path.join(tree, 'aa.bin'), 'wb') as handle:
            handle.write(gen.pattern_bytes(b'mh4:aa', 1500))
        data = (hexstream('pin-check:' + name, last_size) if content == 'hex'
                else gen.pattern_bytes(b'pin-check:' + name.encode(), last_size))
        with open(os.path.join(tree, 'zz.bin'), 'wb') as handle:
            handle.write(data)
        image = os.path.join(work, name + '.sqsh')
        with contextlib.redirect_stdout(io.StringIO()):
            writer.build_image(tree, image, 'be', 'gzip')
        with open(image, 'rb') as handle:
            payload = bytearray(handle.read())
        report = {}
        try:
            gen.corruption_partial(payload, 'be', report)
            print(f'{name:<10} damage=ACCEPTED block_length={report["block_length"]} B')
            return 'green'
        except gen.SqfsError as exc:
            print(f'{name:<10} damage=REFUSED  {exc}')
            return 'red'

    print('case       outcome  detail')
    red = attempt('hex3100', 3100, 'hex')
    green = attempt('pat1500', 1500, 'pattern')
    print(f'\nred case refused: {red == "red"} | green case accepted: {green == "green"}')
    return 0 if (red == 'red' and green == 'green') else 1


if __name__ == '__main__':
    sys.exit(main())
