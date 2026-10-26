#!/usr/bin/env python3
"""probe-fills.py -- which data-block damage patterns actually fail sasquatch?

Runs the target extractor directly (no unblob/REA) on copies of one development
carrier whose target data block is overwritten with a candidate fill, then
reports the exit code, the number of path entries left in the output tree and
whether the damaged file's bytes are zeroes.

Used to choose PARTIAL_FILL in sqfs-corrupt.py: sasquatch 4.5.1 falls back
through several decompressors, and a 0x00 fill is silently "detected" as
lzma-ddwrt, so the run exits 0 with a wrong-content file.

Usage: python3 -B probe-fills.py IMAGE [--be|--le] [--fill 00,ff,a5,rand,inc,hdrs]
Exit 1 if any fill that should fail does not, so a regression is visible.
"""

import importlib.util
import os
import shutil
import struct
import subprocess
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    spec = importlib.util.spec_from_file_location('sqfscorrupt',
                                                  os.path.join(HERE, 'sqfs-corrupt.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fill_bytes(kind, length, seed):
    if kind == '00':
        return bytes(length)
    if kind == 'ff':
        return b'\xff' * length
    if kind == 'a5':
        return b'\xa5' * length
    if kind == 'rand':
        out = bytearray()
        counter = 0
        import hashlib
        while len(out) < length:
            out += hashlib.sha256(seed + b'#' + str(counter).encode()).digest()
            counter += 1
        return bytes(out[:length])
    if kind == 'inc':
        return bytes((i * 37 + 11) & 0xff for i in range(length))
    if kind == 'hdrs':
        # a valid-looking zlib header followed by garbage
        return b'\x78\x9c' + bytes((i * 91 + 7) & 0xff for i in range(length - 2))
    raise SystemExit('unknown fill %r' % kind)


def main(argv):
    if len(argv) < 2:
        print(__doc__.splitlines()[-1], file=sys.stderr)
        return 2
    image_path = argv[1]
    arm = '--be'
    fills = '00,ff,a5,rand,inc,hdrs'
    for arg in argv[2:]:
        if arg in ('--be', '--le'):
            arm = arg
        elif arg.startswith('--fill'):
            fills = arg.split('=', 1)[1] if '=' in arg else fills
    sq = load()
    work = os.environ.get('TMPDIR') or '.'
    with open(image_path, 'rb') as handle:
        buf = handle.read()
    image = sq.Image(buf)
    files = image.files()
    target = files[-1]
    block = [b for b in target['blocks'] if b['compressed']][-1]
    exe = 'sasquatch-v4be' if arm == '--be' else 'sasquatch'
    print('image %s arm %s target %s block %d+%d'
          % (os.path.basename(image_path), arm, target['path'],
             block['offset'], block['length']))
    bad = 0
    for kind in fills.split(','):
        damaged = bytearray(buf)
        damaged[block['offset']:block['offset'] + block['length']] = \
            fill_bytes(kind, block['length'], b'probe')
        path = os.path.join(work, 'probe-%s.sqfs' % kind)
        with open(path, 'wb') as handle:
            handle.write(bytes(damaged))
        outdir = os.path.join(work, 'probe-out-%s' % kind)
        shutil.rmtree(outdir, ignore_errors=True)
        os.makedirs(outdir)
        args = [exe] + (['-be'] if arm == '--be' else ['-le']) + \
            ['-no-exit-code', '-f', '-d', outdir, path]
        res = subprocess.run(args, capture_output=True, text=True)
        entries = sum(len(fnames) for _r, _d, fnames in os.walk(outdir))
        damaged_file = os.path.join(outdir, *target['path'].split('/'))
        size = os.path.getsize(damaged_file) if os.path.isfile(damaged_file) else None
        zeros = False
        if size:
            with open(damaged_file, 'rb') as handle:
                zeros = handle.read() == bytes(size)
        signals = [line for line in (res.stdout + res.stderr).splitlines()
                   if 'Detected' in line or 'FATAL' in line or 'failed' in line]
        verdict = 'FAILS' if res.returncode else 'absorbed'
        if res.returncode == 0:
            bad += 1
        print('  fill %-5s rc=%d %-9s entries=%d damaged=%s zeros=%s %s'
              % (kind, res.returncode, verdict, entries, size, zeros,
                 signals[-1].strip() if signals else ''))
    return 0 if bad == 0 else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
