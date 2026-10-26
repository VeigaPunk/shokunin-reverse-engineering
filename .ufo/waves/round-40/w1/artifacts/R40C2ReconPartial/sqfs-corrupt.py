#!/usr/bin/env python3
"""sqfs-corrupt.py -- deterministic SquashFS 4.0 damage recipes (C2 recon, round 40).

Pure stdlib reader (superblock -> inode table -> directory table) that locates
each regular file's on-disk data blocks, plus damage recipes used to build the
C2 `partial-body-failure` / `body-extractor-failure` development carriers.

Every offset is computed from the image itself: the superblock's
inode_table_start / directory_table_start, the inode table metadata stream and
each regular-file inode's `start_block` + block-size list.  No offset, size or
path is hardcoded, so the same recipe works on any tree the lane writer emits,
in either endianness and for gzip (comp id 1) and xz (comp id 4).

Recipes (``img_bytes -> img_bytes``; input is never mutated):

  corrupt_partial(img)      zero the last compressed data block of the last
                            regular file in directory-scan (extraction) order.
                            Unblob/sasquatch abort on that block after writing
                            every earlier file, so the extractor fails with
                            published files > 0.
  corruption_zero_id_table  round-39 ``body-extractor-failure`` recipe: zero the
                            id-table metadata block.  sasquatch reads the id
                            table during filesystem init, before any file is
                            written, so published files stay 0.
  corruption_bad_minor      s_minor 4 -> 5: still matches the v4 handler
                            pattern, sasquatch rejects the header.
  corruption_bad_major      s_major 4 -> 9: no handler matches, no chunk.

Usage:
  python3 -B sqfs-corrupt.py IMAGE --list                 # file -> block table
  python3 -B sqfs-corrupt.py IMAGE --corrupt NAME OUT      # write damaged copy
  python3 -B sqfs-corrupt.py IMAGE --verify-trees TREE     # sha256 cross-check

Exit: 0 ok, 2 unreadable/unsupported image or recipe precondition unmet.
"""

import argparse
import hashlib
import lzma
import os
import posixpath
import struct
import sys
import zlib

META_MAX = 8192
META_UNCOMPRESSED = 1 << 15
BLOCK_UNCOMPRESSED = 1 << 24
INVALID_FRAG = 0xFFFFFFFF
MAGIC = {b'hsqs': '<', b'sqsh': '>'}
COMP = {1: 'gzip', 2: 'lzma', 3: 'lzo', 4: 'xz', 5: 'lz4', 6: 'zstd'}

TYPE_DIR, TYPE_FILE, TYPE_SYMLINK = 1, 2, 3
TYPE_BLKDEV, TYPE_CHRDEV, TYPE_FIFO, TYPE_SOCKET = 4, 5, 6, 7
TYPE_LDIR, TYPE_LFILE, TYPE_LSYMLINK = 8, 9, 10


class SqfsError(Exception):
    pass


class MetaStream:
    """The decompressed concatenation of consecutive metadata blocks."""

    def __init__(self, img, base, e, comp):
        self.img = img
        self.base = base
        self.e = e
        self.comp = comp
        self.cache = {}

    def block(self, ptr):
        """Return (decompressed bytes, on-disk length) of the block at ptr."""
        hit = self.cache.get(ptr)
        if hit is not None:
            return hit
        if not 0 <= ptr <= len(self.img) - 2:
            raise SqfsError('metadata block pointer %d outside the image' % ptr)
        header = struct.unpack_from(self.e + 'H', self.img, self.base + ptr)[0]
        size = header & ~META_UNCOMPRESSED
        raw = self.img[self.base + ptr + 2:self.base + ptr + 2 + size]
        if len(raw) != size:
            raise SqfsError('metadata block at %d truncated' % ptr)
        data = raw if header & META_UNCOMPRESSED else decompress(raw, self.comp)
        hit = (data, size + 2)
        self.cache[ptr] = hit
        return hit

    def read(self, ptr, offset, count):
        """Read count bytes starting at (block ptr, offset), crossing blocks."""
        out = bytearray()
        cur, off = ptr, offset
        while len(out) < count:
            data, on_disk = self.block(cur)
            if off > len(data):
                raise SqfsError('metadata offset %d beyond block at %d'
                                % (off, cur))
            take = data[off:off + (count - len(out))]
            out += take
            if len(out) >= count:
                break
            cur, off = cur + on_disk, 0
        return bytes(out)

    def reader(self, ptr, offset):
        return StreamReader(self, ptr, offset)


class StreamReader:
    def __init__(self, meta, ptr, offset):
        self.meta = meta
        self.ptr = ptr
        self.off = offset

    def take(self, count):
        data = self.meta.read(self.ptr, self.off, count)
        self.off += count
        return data

    def u16(self):
        return struct.unpack(self.meta.e + 'H', self.take(2))[0]

    def u32(self):
        return struct.unpack(self.meta.e + 'I', self.take(4))[0]

    def u64(self):
        return struct.unpack(self.meta.e + 'Q', self.take(8))[0]

    def i16(self):
        return struct.unpack(self.meta.e + 'h', self.take(2))[0]


def decompress(raw, comp):
    if comp == 'gzip':
        try:
            return zlib.decompress(raw)
        except zlib.error as exc:
            raise SqfsError('gzip metadata block: %s' % exc)
    if comp in ('xz', 'lzma'):
        try:
            return lzma.decompress(raw)
        except (lzma.LZMAError, EOFError) as exc:
            raise SqfsError('%s metadata block: %s' % (comp, exc))
    raise SqfsError('compression id %r not supported' % comp)


class Image:
    def __init__(self, buf):
        if len(buf) < 96:
            raise SqfsError('image is %d bytes, shorter than the superblock'
                            % len(buf))
        magic = bytes(buf[:4])
        if magic not in MAGIC:
            raise SqfsError('unknown magic %r' % magic)
        self.buf = buf
        self.e = MAGIC[magic]
        self.magic = magic
        (self.inode_count, self.mkfs_time, self.block_size,
         self.frag_count) = struct.unpack_from(self.e + 'IIII', buf, 4)
        (self.comp_id, self.block_log, self.flags,
         self.id_count) = struct.unpack_from(self.e + 'HHHH', buf, 20)
        self.major, self.minor = struct.unpack_from(self.e + 'HH', buf, 28)
        (self.root_inode, self.bytes_used, self.id_table_start,
         self.xattr_id_table_start, self.inode_table_start,
         self.dir_table_start, self.fragment_table_start,
         self.export_table_start) = struct.unpack_from(self.e + 'QQQQQQQQ', buf, 32)
        if (self.major, self.minor) != (4, 0):
            raise SqfsError('not a SquashFS 4.0 image: %d.%d'
                            % (self.major, self.minor))
        self.comp = COMP.get(self.comp_id)
        if self.comp is None:
            raise SqfsError('compression id %d unknown' % self.comp_id)
        self.inodes = MetaStream(buf, self.inode_table_start, self.e, self.comp)
        self.dirs = MetaStream(buf, self.dir_table_start, self.e, self.comp)
        self._inodes = {}

    # -- inodes ---------------------------------------------------------
    def inode(self, ref):
        hit = self._inodes.get(ref)
        if hit is not None:
            return hit
        st = self.inodes.reader(ref >> 16, ref & 0xFFFF)
        kind = st.u16()
        node = {'ref': ref, 'type': kind, 'mode': st.u16(), 'uid': st.u16(),
                'gid': st.u16(), 'mtime': st.u32(), 'inode_number': st.u32()}
        if kind in (TYPE_DIR, TYPE_LDIR):
            if kind == TYPE_DIR:
                node['start_block'] = st.u32()
                node['nlink'] = st.u32()
                node['file_size'] = st.u16()
                node['offset'] = st.u16()
                node['parent'] = st.u32()
            else:
                node['nlink'] = st.u32()
                node['file_size'] = st.u32()
                node['start_block'] = st.u32()
                node['parent'] = st.u32()
                node['i_count'] = st.u16()
                node['offset'] = st.u16()
                node['xattr'] = st.u32()
        elif kind in (TYPE_FILE, TYPE_LFILE):
            if kind == TYPE_FILE:
                node['start_block'] = st.u32()
                node['fragment'] = st.u32()
                node['frag_offset'] = st.u32()
                node['file_size'] = st.u32()
            else:
                node['start_block'] = st.u64()
                node['file_size'] = st.u64()
                node['sparse'] = st.u64()
                node['nlink'] = st.u32()
                node['fragment'] = st.u32()
                node['frag_offset'] = st.u32()
                node['xattr'] = st.u32()
            node['block_list'] = self._block_list(st, node)
        elif kind in (TYPE_SYMLINK, TYPE_LSYMLINK):
            node['nlink'] = st.u32()
            size = st.u32()
            node['target'] = st.take(size).decode('utf-8', 'surrogateescape')
        else:
            raise SqfsError('inode %#x: unsupported type %d' % (ref, kind))
        self._inodes[ref] = node
        return node

    def _block_list(self, st, node):
        size, bs = node['file_size'], self.block_size
        if node['fragment'] == INVALID_FRAG:
            count = (size + bs - 1) // bs
        else:
            count = size // bs
        if count > 8192:
            raise SqfsError('inode %#x declares %d data blocks'
                            % (node['ref'], count))
        return [st.u32() for _ in range(count)]

    # -- directories ----------------------------------------------------
    def entries(self, node):
        """Directory entries in stored (extraction) order."""
        st = self.dirs.reader(node['start_block'], node['offset'])
        header = st.take(12)
        count, start = struct.unpack(self.e + 'II', header[:8])
        out = []
        for _ in range(count + 1):
            fix = st.take(8)
            offset, ino_delta, typ, name_size = struct.unpack(
                self.e + 'HhHH', fix)
            name = st.take(name_size + 1).decode('utf-8', 'surrogateescape')
            out.append({'name': name, 'type': typ, 'ref': (start << 16) | offset,
                        'inode_number': None})
        return out

    def walk(self):
        """Depth-first directory scan in stored order (the extractor's order)."""
        order = []

        def visit(path, ref):
            node = self.inode(ref)
            for entry in self.entries(node):
                child = posixpath.join(path, entry['name']) if path else entry['name']
                order.append((child, entry['type'], entry['ref']))
                if entry['type'] in (TYPE_DIR, TYPE_LDIR):
                    visit(child, entry['ref'])

        visit('', self.root_inode)
        return order

    def files(self):
        """Regular files with the absolute on-disk span of each data block."""
        out = []
        for path, typ, ref in self.walk():
            if typ not in (TYPE_FILE, TYPE_LFILE):
                continue
            node = self.inode(ref)
            pos = node['start_block']
            blocks = []
            for field in node['block_list']:
                on_disk = field & ~BLOCK_UNCOMPRESSED
                if on_disk == 0:
                    blocks.append({'offset': pos, 'length': 0,
                                   'compressed': False, 'sparse': True})
                    continue
                blocks.append({'offset': pos, 'length': on_disk,
                               'compressed': not (field & BLOCK_UNCOMPRESSED),
                               'sparse': False})
                pos += on_disk
            out.append({'path': path, 'ref': ref, 'node': node,
                        'size': node['file_size'], 'blocks': blocks})
        return out


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def _precondition(images):
    if len(images) < 2:
        raise SqfsError('partial recipe needs at least 2 regular files, found %d'
                        % len(images))


# ---------------------------------------------------------------------------
# recipes
# ---------------------------------------------------------------------------
PARTIAL_FILL = 0xFF


def corrupt_partial(img, report=None, fill=PARTIAL_FILL):
    """Overwrite the last compressed data block of the last-extracted regular file.

    The target is chosen from parsed inode data, not from a fixed offset:
      * the file order is the directory-scan order (what unsquashfs walks),
      * the file is the last one in that order that owns a compressed,
        non-sparse data block,
      * within that file, its last compressed data block.

    The fill is 0xFF (measured, see the round-40 recon report): sasquatch
    4.5.1's multi-decompressor fallback chain does NOT absorb it, the block
    fails to decompress, `write_file` prints ``FATAL ERROR: writer: failed to
    read/uncompress file`` and the process exits 1 -- while every earlier file
    is already on disk.  A 0x00 fill is NOT usable: measured, the fallback
    chain "Detected lzma-ddwrt compression" and silently emitted a full-length
    block of zeroes with exit 0, so the image reads as a clean extraction with
    wrong content.
    """
    image = Image(img)
    images = image.files()
    _precondition(images)
    target = None
    for entry in reversed(images):
        for block in reversed(entry['blocks']):
            if block['compressed'] and not block['sparse']:
                target = (entry, block)
                break
        if target:
            break
    if target is None:
        raise SqfsError('no compressed data block in any regular file')
    entry, block = target
    out = bytearray(img)
    start, length = block['offset'], block['length']
    if start + length > image.bytes_used:
        raise SqfsError('data block %d+%d beyond bytes_used %d'
                        % (start, length, image.bytes_used))
    out[start:start + length] = bytes([fill]) * length
    if report is not None:
        report.update({'recipe': 'partial', 'fill': '%#04x' % fill,
                       'path': entry['path'],
                       'block_offset': start, 'block_length': length,
                       'file_size': entry['size'],
                       'file_total': len(images),
                       'block_index': entry['blocks'].index(block),
                       'file_blocks': len(entry['blocks'])})
    return bytes(out)


def corruption_zero_id_table(img, report=None):
    """Round-39 body-extractor-failure recipe: zero the id-table metadata block.

    Superblock id_table_start (u64 at offset 48) points just past the id
    metadata block at the 8-byte id table index, which holds the metadata
    block's start.
    """
    image = Image(img)
    e = image.e
    id_table_start = image.id_table_start
    if not 96 <= id_table_start <= len(img) - 8:
        raise SqfsError('id_table_start %d outside image (%d bytes)'
                        % (id_table_start, len(img)))
    id_meta_start = struct.unpack_from(e + 'Q', img, id_table_start)[0]
    if not 96 <= id_meta_start < id_table_start <= len(img):
        raise SqfsError('id metadata block %d..%d outside image'
                        % (id_meta_start, id_table_start))
    out = bytearray(img)
    out[id_meta_start:id_table_start] = bytes(id_table_start - id_meta_start)
    if report is not None:
        report.update({'recipe': 'zero-id-table',
                       'block_offset': id_meta_start,
                       'block_length': id_table_start - id_meta_start})
    return bytes(out)


def _version_edit(img, major, minor, report, name):
    image = Image(img)
    out = bytearray(img)
    struct.pack_into(image.e + 'HH', out, 28, major, minor)
    if report is not None:
        report.update({'recipe': name, 'block_offset': 28, 'block_length': 4})
    return bytes(out)


def corruption_bad_minor(img, report=None):
    return _version_edit(img, 4, 5, report, 'bad-minor')


def corruption_bad_major(img, report=None):
    return _version_edit(img, 9, 0, report, 'bad-major')


RECIPES = {
    'partial': corrupt_partial,
    'zero-id-table': corruption_zero_id_table,
    'bad-minor': corruption_bad_minor,
    'bad-major': corruption_bad_major,
}


# ---------------------------------------------------------------------------
# cross-check: does the parsed tree reproduce the source tree?
# ---------------------------------------------------------------------------
def read_file_data(image, entry):
    out = bytearray()
    node = entry['node']
    remaining = node['file_size']
    for block in entry['blocks']:
        want = min(image.block_size, remaining)
        if want == 0:
            break
        if block['sparse']:
            out += bytes(want)
        else:
            raw = image.buf[block['offset']:block['offset'] + block['length']]
            data = raw if not block['compressed'] else decompress(raw, image.comp)
            out += data[:want]
        remaining -= want
    if remaining:
        raise SqfsError('%s: %d trailing bytes need a fragment' % (entry['path'], remaining))
    return bytes(out)


def verify_tree(image_path, tree):
    with open(image_path, 'rb') as handle:
        image = Image(handle.read())
    problems = []
    for entry in image.files():
        disk = os.path.join(tree, *entry['path'].split('/'))
        if not os.path.isfile(disk):
            problems.append('%s: not in tree' % entry['path'])
            continue
        with open(disk, 'rb') as handle:
            want = handle.read()
        got = read_file_data(image, entry)
        if got != want:
            problems.append('%s: image payload differs (sha %s vs tree %s)'
                            % (entry['path'], sha256(got)[:12], sha256(want)[:12]))
    for root, _dnames, fnames in os.walk(tree):
        for name in fnames:
            path = os.path.join(root, name)
            if os.path.islink(path):
                continue
            rel = os.path.relpath(path, tree).replace(os.sep, '/')
            if rel not in {entry['path'] for entry in image.files()}:
                problems.append('%s: in tree, not in image' % rel)
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('image')
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--corrupt', metavar='RECIPE', choices=sorted(RECIPES))
    ap.add_argument('--out', metavar='OUT')
    ap.add_argument('--verify-trees', metavar='TREE')
    ns = ap.parse_args(argv)

    with open(ns.image, 'rb') as handle:
        buf = handle.read()
    image = Image(buf)
    print('image %s: %s endian, comp %s, block %d, bytes_used %d, %d files'
          % (os.path.basename(ns.image), 'le' if image.e == '<' else 'be',
             image.comp, image.block_size, image.bytes_used,
             len(image.files())))
    if ns.list:
        for entry in image.files():
            kinds = ''.join('C' if b['compressed'] else ('R' if not b['sparse'] else 'S')
                            for b in entry['blocks'])
            print('  %-40s size %6d blocks %s' % (entry['path'], entry['size'], kinds))
    if ns.verify_trees:
        problems = verify_tree(ns.image, ns.verify_trees)
        for line in problems:
            print('  PROBLEM %s' % line)
        print('verify-trees: %d problem(s)' % len(problems))
    if ns.corrupt:
        info = {}
        damaged = RECIPES[ns.corrupt](buf, info)
        if ns.out:
            with open(ns.out, 'wb') as handle:
                handle.write(damaged)
        print('corrupt %s -> %s' % (ns.corrupt, ns.out or '<not written>'))
        for key in sorted(info):
            print('  %s: %s' % (key, info[key]))
        diff = [i for i in range(min(len(buf), len(damaged))) if buf[i] != damaged[i]]
        print('  bytes changed: %d (%s..%s)'
              % (len(diff), diff[0] if diff else '-', diff[-1] if diff else '-'))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except SqfsError as exc:
        print('sqfs-corrupt: %s' % exc, file=sys.stderr)
        sys.exit(2)
