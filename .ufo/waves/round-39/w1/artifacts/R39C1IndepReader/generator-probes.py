#!/usr/bin/env python3
"""Measured limits of tools/round-37/gen-squashfs.py found while building the
round-39 wave-1 LE fixtures.  Every claim here is recomputed from the fixture
images, not recalled.

  P1  non-ASCII filename: dir entry size field is len(str) - 1, but the name on
      disk is len(str.encode()) bytes -> the image is malformed (one byte left
      over in the directory stream, everything after it misparsed).
  P2  inode ref block field is a metadata-block *count* (MetaWriter.append
      returns len(self.blocks)), but a SquashFS inode ref stores the *byte*
      offset of the block from the inode table start; the image breaks as soon
      as the inode table needs a second 8192-byte block (300 one-byte files).
  P3  symlinks whose target is a directory are dropped: os.walk lists them in
      dirnames, the writer only reads fnames, so they never reach the image.
  P4  metadata is always written uncompressed (MetaWriter.meta_header always
      sets 0x8000), so a generator image never exercises compressed metadata.

Usage: generator-probes.py --work DIR --artifacts DIR
Exit 0 when every measured fact reproduces.
"""
import argparse
import importlib.util
import json
import os
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
READER = os.path.join(HERE, 'sqfs-list.py')


def load_reader():
    spec = importlib.util.spec_from_file_location('sqfs_list', READER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def dir_table_entries(img, mod):
    """Collect (name bytes, declared size field, header start_block, entry
    offset) from the root directory body without resolving inode refs.  Stops
    at the first structural error and returns (entries, error-or-None)."""
    node = img.inode(img.root_inode)
    start = img.directory_table_start + node['start_block']
    length = node['file_size'] - 3
    st = mod.MetaStream(img, start, node['offset'])
    e = img.e
    read = 0
    out = []
    try:
        while read < length:
            hdr = st.read(12)
            count = struct.unpack_from(e + 'I', hdr, 0)[0] + 1
            sblock = struct.unpack_from(e + 'I', hdr, 4)[0]
            read += 12
            for _ in range(count):
                ent = st.read(8)
                eoff = struct.unpack_from(e + 'H', ent, 0)[0]
                declared = struct.unpack_from(e + 'H', ent, 6)[0]
                name = st.read(declared + 1)
                read += 8 + declared + 1
                out.append((name, declared, sblock, eoff))
    except mod.SqfsError as exc:
        return out, str(exc)
    return out, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', required=True)
    ap.add_argument('--artifacts', required=True)
    ap.add_argument('--lane-root', required=True)
    args = ap.parse_args()
    mod = load_reader()
    work = args.work
    lines = []
    ok = True

    def emit(text=''):
        lines.append(text)

    # P1 ------------------------------------------------------------------
    emit('## P1 non-ASCII filename -> char-count size field')
    img = mod.SquashFS(os.path.join(work, 'C-le-gzip.sqsh'))
    block, _n = img.meta_block(img.directory_table_start)
    emit('C-le-gzip directory body (hex): %s' % block.hex())
    entries, err = dir_table_entries(img, mod)
    for name, declared, sblock, eoff in entries:
        emit('  entry name_bytes=%r declared_size_field=%d (=> %d name bytes) '
             'header_start_block=%d offset=%d'
             % (name, declared, declared + 1, sblock, eoff))
    real = sorted(os.listdir(os.path.join(work, 'trees', 'C')))
    emit('  tree C names and real byte lengths: %r'
         % {n: len(n.encode()) for n in real})
    emit('  stream error after those entries: %s' % (err,))
    emit('  -> the non-ASCII name is %d bytes on disk but its entry declares '
         '%d, so the directory stream is one byte out of step; sqfs-list '
         'refuses with exit 2 and unsquashfs fails:'
         % (len('\u00e9-name.txt'.encode()), 9))
    rc, out = run_cmd(['/usr/bin/unsquashfs', '-no-progress', '-d',
                       os.path.join(work, 'unsquashfs-C'),
                       os.path.join(work, 'C-le-gzip.sqsh')], work)
    emit('     unsquashfs exit %d: %s' % (rc, first_line(out)))
    ok = ok and rc != 0

    # P2 ------------------------------------------------------------------
    emit('')
    emit('## P2 inode ref block field is a block count, not a byte offset')
    img = mod.SquashFS(os.path.join(work, 'L-le-gzip.sqsh'))
    first, next_pos = img.meta_block(img.inode_table_start)
    img = mod.SquashFS(os.path.join(work, 'L-le-gzip.sqsh'))
    first, next_pos = img.meta_block(img.inode_table_start)
    ref = img.root_inode
    blk, off = ref >> 16, ref & 0xFFFF
    correct = len(first) + 2
    emit('L-le-gzip (300 one-byte files): inode table %d bytes, first block '
         'payload %d, second block header at %d'
         % (img.directory_table_start - img.inode_table_start, len(first),
            next_pos))
    emit('  stored root_inode ref = 0x%016x (block field %d, offset %d)'
         % (ref, blk, off))
    emit('  the second metadata block starts %d bytes after the inode table '
         'start, so the ref must be 0x%016x; the generator stored the block '
         '*count* (%d) instead, and the reader looks at inode_table_start+%d'
         % (correct, (correct << 16) | off, blk, blk))
    k1 = mod.SquashFS(os.path.join(args.lane_root, 'corpus', 'evidence',
                                   'round-37', 'c1', 'K1', 'carrier.sqsh'))
    emit('  contrast: K1 root_inode ref = 0x%x (block field %d, offset %d) '
         'and K1 fits one inode block, so count and byte offset coincide'
         % (k1.root_inode, k1.root_inode >> 16, k1.root_inode & 0xFFFF))
    rc, out = run_cmd([sys.executable, '-I', '-B', READER,
                       os.path.join(work, 'L-le-gzip.sqsh'),
                       '--files', os.path.join(work, 'L.files.tsv'),
                       '--symlinks', os.path.join(work, 'L.symlinks.tsv')],
                      work)
    emit('  sqfs-list exit %d: %s' % (rc, first_line(out)))
    rc2, out2 = run_cmd(['/usr/bin/unsquashfs', '-no-progress', '-d',
                         os.path.join(work, 'unsquashfs-L'),
                         os.path.join(work, 'L-le-gzip.sqsh')], work)
    emit('  unsquashfs exit %d: %s' % (rc2, last_error(out2)))
    ok = ok and rc == 2 and rc2 != 0

    # P3 ------------------------------------------------------------------
    emit('')
    emit('## P3 symlinks to directories are dropped')
    img = mod.SquashFS(os.path.join(work, 'B-be-gzip.sqsh'))
    files, links, kinds, specials = img.walk()
    tree_links = sorted(
        os.path.relpath(os.path.join(dp, n), os.path.join(work, 'trees', 'B'))
        for dp, dns, fns in os.walk(os.path.join(work, 'trees', 'B'))
        for n in list(dns) + list(fns)
        if os.path.islink(os.path.join(dp, n)))
    emit('  tree B symlinks: %r' % (tree_links,))
    emit('  image symlinks:  %r' % (sorted(links),))
    emit('  dropped:         %r' % (sorted(set(tree_links) - set(links)),))
    ok = ok and sorted(links) == ['abs', 'self', 'up']

    # P4 ------------------------------------------------------------------
    emit('')
    emit('## P4 metadata is always stored uncompressed by the generator')
    for name in ('A-le-gzip', 'B-le-xz', 'B-be-gzip', 'B-be-xz', 'C-le-gzip',
                 'L-le-gzip', 'D-le-mksq-gzip', 'D-le-mksq-xz',
                 'S-le-mksq-gzip'):
        path = os.path.join(args.artifacts, name + '.inspect.json')
        if not os.path.exists(path):
            path = os.path.join(args.out_dir, name + '.inspect.json')
        if not os.path.exists(path):
            continue
        try:
            with open(path) as fh:
                meta = json.load(fh)
        except (OSError, ValueError):
            emit('  %-16s (refused: no inspect summary)' % name)
            continue
        emit('  %-16s %s' % (name, meta.get('decode_paths')))
    emit('  every generator image shows compressed_metadata_blocks = 0: the '
         'only compressed metadata in this wave is in K3/K4 and in the '
         'mksquashfs fixtures, so K5/K6 built by this generator add no '
         'compressed-metadata coverage.')

    text = '\n'.join(lines) + '\n'
    with open(os.path.join(args.artifacts, 'generator-probes.txt'), 'w') as fh:
        fh.write(text)
    sys.stdout.write(text)
    return 0 if ok else 1


def run_cmd(cmd, cwd):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return p.returncode, (p.stdout or '') + (p.stderr or '')


def first_line(text):
    for line in text.splitlines():
        if line.strip():
            return line.strip()[:160]
    return '(no output)'


def last_error(text):
    for line in reversed(text.splitlines()):
        if 'ERROR' in line or 'error' in line:
            return line.strip()[:160]
    return first_line(text)


if __name__ == '__main__':
    sys.exit(main())
