#!/usr/bin/env python3
"""Score sqfs-list.py against the four committed round-37 C1 oracles.

For each carrier in corpus/evidence/round-37/c1/K1..K4 this runs

  python3 -I -B sqfs-list.py <carrier> --files K.files.tsv --symlinks K.symlinks.tsv --inspect

and byte-compares the regular-file table with the committed oracle.tsv after a
C-locale sort of both.  It never writes into the corpus: outputs go to
--artifacts.  The four symlink tables are printed for the record.

Usage: check-oracles.py --root LANE --artifacts DIR
Exit 0 iff all four carriers match their oracle byte for byte.
"""
import argparse
import os
import subprocess
import sys

READER = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      'sqfs-list.py')
CARRIERS = ('K1', 'K2', 'K3', 'K4')


def carrier_path(root, k):
    base = os.path.join(root, 'corpus', 'evidence', 'round-37', 'c1', k)
    for name in ('carrier.sqsh', 'carrier.bin'):
        path = os.path.join(base, name)
        if os.path.exists(path):
            return path
    raise SystemExit('no carrier under %s' % base)


def read_bytes(path):
    with open(path, 'rb') as fh:
        return fh.read()


def sorted_lines(data):
    return sorted(data.splitlines())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--artifacts', required=True)
    args = ap.parse_args()
    os.makedirs(args.artifacts, exist_ok=True)
    lines, ok = [], True
    for k in CARRIERS:
        image = carrier_path(args.root, k)
        prefix = os.path.join(args.artifacts, k)
        files = prefix + '.files.tsv'
        links = prefix + '.symlinks.tsv'
        cmd = [sys.executable, '-I', '-B', READER, image,
               '--files', files, '--symlinks', links, '--inspect']
        p = subprocess.run(cmd, capture_output=True, text=True)
        with open(prefix + '.stderr.txt', 'wb') as fh:
            fh.write(p.stderr.encode())
        with open(prefix + '.inspect.json', 'wb') as fh:
            fh.write(p.stdout.encode())
        oracle = os.path.join(args.root, 'corpus', 'evidence', 'round-37',
                              'c1', k, 'oracle.tsv')
        lines.append('%s image %s' % (k, os.path.relpath(image, args.root)))
        lines.append('   reader exit %d' % p.returncode)
        if p.returncode != 0:
            ok = False
            lines.append('   REFUSED: %s' % p.stderr.strip())
            continue
        mine = sorted_lines(read_bytes(files))
        want = sorted_lines(read_bytes(oracle))
        same = mine == want
        ok = ok and same
        lines.append('   files table vs oracle.tsv: %s (%d rows, sha256 %s)'
                     % ('IDENTICAL after sort' if same else 'DIFFER',
                        len(mine),
                        __import__('hashlib').sha256(
                            b'\n'.join(mine) + b'\n').hexdigest()[:16]))
        if not same:
            lines.append('   only reader: %r' % [l for l in mine
                                                 if l not in want])
            lines.append('   only oracle: %r' % [l for l in want
                                                 if l not in mine])
        symlinks = sorted_lines(read_bytes(links))
        if symlinks:
            for row in symlinks:
                lines.append('   symlink: %s'
                             % row.decode('utf-8', 'surrogateescape')
                             .replace('\t', ' | '))
        else:
            lines.append('   symlink: (none)')
    lines.append('verdict: %s' % ('ALL FOUR ORACLES MATCH' if ok else 'MISMATCH'))
    text = '\n'.join(lines) + '\n'
    with open(os.path.join(args.artifacts, 'oracle-check.txt'), 'w') as fh:
        fh.write(text)
    sys.stdout.write(text)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
