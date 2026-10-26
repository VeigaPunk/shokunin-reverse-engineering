#!/usr/bin/env python3
"""Build the round-39 wave-1 development fixtures and score sqfs-list.py on them.

Every image here is a development fixture built in scratch.  None of them is a
frozen carrier, and none is ever run through REA.

  A-le-gzip        generator, --endian le --comp gzip      (gzip data blocks)
  B-le-xz          generator, --endian le --comp xz        (raw LZMA2 stored
                                                            under compression
                                                            id 2, see the report)
  C-le-gzip        generator, non-ASCII *filename* probe    (expected: refuse)
  L-le-gzip        generator, 300-file tree probe           (expected: refuse)
  B-be-gzip        generator, --endian be --comp gzip      (extractor probe)
  B-be-xz          generator, --endian be --comp xz        (extractor probe)
  D-le-mksq-gzip   mksquashfs 4.7.5, gzip                  (fragments, compressed
  D-le-mksq-xz     mksquashfs 4.7.5, xz                    metadata, xz id 4)
  S-le-mksq-gzip   mksquashfs 4.7.5, gzip                  (sparse block)

Usage:
  python3 build-and-check.py --work DIR --artifacts DIR --gen GEN_SQUASHFS.py
                             [--mksquashfs PATH] [--skip-mksquashfs]

Exit 0 when every expected outcome holds.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

READER = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      'sqfs-list.py')

LINK_CASES = {
    'A': [('link-abs', '/a/exact.bin', 'in-tree'),
          ('link-chain', 'link-same', 'in-tree'),
          ('link-same', 'a/exact.bin', 'in-tree'),
          ('link-up', '../outside.txt', 'escaping')],
    'B': [('abs', '/x/one.txt', 'in-tree'),
          ('self', 'self', 'in-tree'),      # a loop is kept by unblob 26.6.4
          ('up', '../../etc/passwd', 'escaping')],
    'D': [('abs-link', '/big.bin', 'in-tree'),
          ('loop', 'loop', 'in-tree'),      # a loop is kept by unblob 26.6.4
          ('nested/link-in', '../nested/deep/file.txt', 'in-tree'),
          ('nested/link-out', '../../outside.txt', 'escaping')],
}


def write(path, data):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'wb') as fh:
        fh.write(data)


def make_trees(work):
    """Deterministic source trees.  ASCII filenames only in A/B/D/S: the lane
    generator writes len(str) instead of len(bytes) into the dir entry size
    field, which is what C-le-gzip demonstrates."""
    trees = os.path.join(work, 'trees')
    if os.path.isdir(trees):
        shutil.rmtree(trees)
    os.makedirs(trees)

    def t(*p):
        return os.path.join(trees, *p)

    write(t('A', 'a', 'b', 'c', 'deep.txt'),
          (b'kaidoku r39 deep line\n' * 700)[:14000])
    write(t('A', 'a', 'exact.bin'), b'X' * 4096)
    write(t('A', 'a', 'over.bin'), b'Y' * 4097)
    write(t('A', 'empty'), b'')
    write(t('A', 'unicode-content.txt'), 'unicode-\u00e9\u4e2d\n'.encode())
    write(t('A', 'space name.txt'), b'space name\n')
    os.makedirs(t('A', 'empty_dir'))
    os.symlink('a/exact.bin', t('A', 'link-same'))
    os.symlink('../outside.txt', t('A', 'link-up'))
    os.symlink('link-same', t('A', 'link-chain'))
    os.symlink('/a/exact.bin', t('A', 'link-abs'))

    write(t('B', 'x', 'one.txt'), b'one\n')
    write(t('B', 'x', 'two.bin'), (b'kaidoku r39 xz payload\n' * 600)[:9000])
    os.makedirs(t('B', 'empty2'))
    os.symlink('self', t('B', 'self'))
    os.symlink('../../etc/passwd', t('B', 'up'))
    os.symlink('/x/one.txt', t('B', 'abs'))
    os.symlink('.', t('B', 'dot'))       # generator drops symlinks to dirs

    write(t('C', 'plain.txt'), b'plain\n')
    write(t('C', '\u00e9-name.txt'), b'unicode name\n')

    for i in range(300):
        write(t('L', 'f%03d' % i), b'x')

    write(t('D', 'big.bin'), b'mksquashfs fixture line 7\n' * 9000)
    write(t('D', 'nested', 'deep', 'file.txt'), b'deep file\n')
    write(t('D', 'nested', 'keep.txt'), b'keep\n')
    write(t('D', 'empty'), b'')
    write(t('D', 'unicode-\u00e9\u4e2d.txt'), 'unicode name\n'.encode())
    with open(t('D', 'sparse.bin'), 'wb') as fh:
        fh.write(b'A' * 4096)
        fh.seek(200000 - 4096)
        fh.write(b'Z' * 4096)
    os.symlink('../nested/deep/file.txt', t('D', 'nested', 'link-in'))
    os.symlink('../../outside.txt', t('D', 'nested', 'link-out'))
    os.symlink('/big.bin', t('D', 'abs-link'))
    os.symlink('loop', t('D', 'loop'))

    os.makedirs(t('S'), exist_ok=True)
    with open(t('S', 'holes.bin'), 'wb') as fh:
        fh.write(b'A' * 131072)
        fh.seek(131072 * 2)
        fh.write(b'Z' * 131072)
    return trees


def gen(src, out, endian, comp, gen_path, work):
    cmd = [sys.executable, '-I', '-B', gen_path, src, out,
           '--endian', endian, '--comp', comp]
    p = subprocess.run(cmd, cwd=work, capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit('generator failed: %s\n%s' % (' '.join(cmd), p.stderr))
    return p.stdout.strip()


def mksq(src, out, comp, mksquashfs, work):
    cmd = [mksquashfs, src, out, '-noappend', '-comp', comp, '-all-root',
           '-no-progress']
    p = subprocess.run(cmd, cwd=work, capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit('mksquashfs failed: %s\n%s\n%s'
                         % (' '.join(cmd), p.stdout, p.stderr))
    return ' '.join(cmd)


def run_reader(image, prefix):
    files = prefix + '.files.tsv'
    links = prefix + '.symlinks.tsv'
    cmd = [sys.executable, '-I', '-B', READER, image,
           '--files', files, '--symlinks', links, '--inspect']
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        for name in (files, links):
            if os.path.exists(name):
                os.unlink(name)
            write(name, b'')
    write(prefix + '.inspect.json', p.stdout.encode())
    write(prefix + '.stderr.txt', p.stderr.encode())
    return p.returncode, p.stdout, p.stderr


def tree_tables(tree):
    rows = []
    for dirpath, dnames, fnames in os.walk(tree):
        dnames.sort()
        for name in sorted(fnames):
            path = os.path.join(dirpath, name)
            if os.path.islink(path):
                continue
            with open(path, 'rb') as fh:
                data = fh.read()
            rel = os.path.relpath(path, tree).replace(os.sep, '/')
            rows.append((rel, hashlib.sha256(data).hexdigest(), str(len(data))))
    rows.sort(key=lambda r: r[0].encode())
    return rows


def read_tsv(path):
    with open(path, encoding='utf-8', errors='surrogateescape') as fh:
        return [tuple(line.split('\t')) for line in fh.read().splitlines()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', required=True)
    ap.add_argument('--artifacts', required=True)
    ap.add_argument('--gen', required=True)
    ap.add_argument('--mksquashfs', default='mksquashfs')
    ap.add_argument('--skip-mksquashfs', action='store_true')
    args = ap.parse_args()
    os.makedirs(args.work, exist_ok=True)
    os.makedirs(args.artifacts, exist_ok=True)
    trees = make_trees(args.work)
    art = args.artifacts

    for name, tree, endian, comp in (
            ('A-le-gzip', 'A', 'le', 'gzip'),
            ('B-le-xz', 'B', 'le', 'xz'),
            ('C-le-gzip', 'C', 'le', 'gzip'),
            ('L-le-gzip', 'L', 'le', 'gzip'),
            ('B-be-gzip', 'B', 'be', 'gzip'),
            ('B-be-xz', 'B', 'be', 'xz')):
        print(gen(os.path.join(trees, tree),
                  os.path.join(args.work, name + '.sqsh'), endian, comp,
                  args.gen, args.work))
    if not args.skip_mksquashfs:
        for name, tree, comp in (('D-le-mksq-gzip', 'D', 'gzip'),
                                 ('D-le-mksq-xz', 'D', 'xz'),
                                 ('S-le-mksq-gzip', 'S', 'gzip')):
            print(mksq(os.path.join(trees, tree),
                       os.path.join(args.work, name + '.sqsh'), comp,
                       args.mksquashfs, args.work))

    cases = [
        # name, tree (for the expected table; None = expected refusal), exit
        ('A-le-gzip', 'A', 0),
        ('B-le-xz', 'B', 0),
        ('C-le-gzip', None, 2),
        ('L-le-gzip', None, 2),
        ('B-be-gzip', 'B', 0),
        ('B-be-xz', 'B', 0),
    ]
    if not args.skip_mksquashfs:
        cases += [('D-le-mksq-gzip', 'D', 0), ('D-le-mksq-xz', 'D', 0),
                  ('S-le-mksq-gzip', 'S', 0)]

    lines, ok = [], True
    lines.append('reader  %s' % READER)
    lines.append('reader sha256 %s' % hashlib.sha256(
        open(READER, 'rb').read()).hexdigest())
    lines.append('python %s' % sys.version.split()[0])
    for name, tree, want in cases:
        image = os.path.join(args.work, name + '.sqsh')
        prefix = os.path.join(art, name)
        rc, out, err = run_reader(image, prefix)
        good = rc == want
        detail = ''
        if rc == 0 and tree:
            got = read_tsv(prefix + '.files.tsv')
            if got == tree_tables(os.path.join(trees, tree)):
                detail += 'files==tree(%d rows) ' % len(got)
            else:
                good = False
                detail += 'files!=tree '
            want_links = LINK_CASES.get(tree)
            if want_links is not None:
                got_links = read_tsv(prefix + '.symlinks.tsv')
                if got_links == want_links:
                    detail += 'symlinks==expected(%d)' % len(got_links)
                else:
                    good = False
                    detail += 'symlinks!=expected %r' % (got_links,)
        if rc != 0:
            detail = 'refused: ' + err.strip().splitlines()[0] if err else ''
        ok = ok and good
        lines.append('%-20s exit %d (want %d)  %s%s'
                     % (name, rc, want, detail, '' if good else '  <-- MISMATCH'))
        print(lines[-1])
    lines.append('verdict: %s' % ('ALL EXPECTED' if ok else 'MISMATCH'))
    with open(os.path.join(art, 'build-and-check.txt'), 'w') as fh:
        fh.write('\n'.join(lines) + '\n')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
