#!/usr/bin/env python3
"""sqfs-list.py -- independent SquashFS 4.0 oracle reader (stdlib only), round 40.

Derived from tools/round-39/sqfs-list.py (lane bytes, 688 lines, sha256
1808c3f54205448761e27ffe8a82de59fe87300eb4c49ec406324800d148be7f).  It remains
an independent reader: no sasquatch and no unblob code is linked or copied.

Round-40 additions
------------------
1. ``--layout``:

   ``le``   little-endian image (magic ``hsqs``); every field little-endian.
   ``be``   standard big-endian image (magic ``sqsh``); every field big-endian,
            including the 2-byte metadata block-length headers.
   ``avm``  genuine AVM layout: big-endian superblock / inode / directory /
            fragment / block-list fields, but *little-endian* 2-byte metadata
            block-length headers.  This is the Freetz note measured on the
            pinned vendor carrier: only the block-length header at the start of
            each metadata block is little-endian.  ``mkfs_time == bytes_used``
            (the AVM marker) is reported but is NOT the layout test.
   ``auto`` magic decides the structural endianness; for big-endian images the
            metadata header endianness is chosen by (a) the exact identity
            ``2 + len + inode_table_start == directory_table_start`` when the
            inode table is one metadata block, else (b) plausibility
            ``0 < len <= 8192``, else (c) decoding the metadata chain.  The
            chosen signal is reported in ``--inspect`` as
            ``block_length_signal`` and the resulting layout as ``layout``.

2. Fragments: the fragment table is read with the structural endianness (the
   index array of 64-bit pointers and the 16-byte entries), and file tails are
   served from it with ``frag_offset``.  Both layouts exercise this path.

3. Data-block size lists are read for both layouts.  Measured on the genuine
   AVM carrier, list entries are big-endian even when the metadata headers are
   little-endian: ``avm`` therefore reads block lists with the structural
   endianness, not the header endianness.

4. gzip (compression id 1) and xz (ids 2 and 4).  Id 4 is tried as a
   full .xz container, a legacy .lzma stream, then a raw LZMA2 stream with
   ``dict_size = block_size``; id 2 is the legacy/raw LZMA2 id used by the
   lane's own writer.  Any other compression id exits 2.

5. Non-regular entries are written to a separate TSV:
   ``relpath TAB kind TAB detail`` with ``kind`` in
   ``dir|symlink|block-device|char-device|fifo|socket`` and ``detail`` the link
   target for symlinks, ``major:minor`` for devices, empty otherwise.  Regular
   files go to ``--files`` as ``relpath TAB sha256 TAB size`` (round-39
   grammar).  Root directory is not listed; every other directory is.

CLI
---
  sqfs-list.py --layout {auto,le,be,avm} --files OUT.tsv [--nonregular OUT.tsv]
               [--inspect] IMAGE
  sqfs-list.py --selftest

Exit 0 on success, 2 on an unreadable or unsupported image.
"""

import argparse
import hashlib
import json
import lzma
import os
import struct
import sys
import tempfile
import zlib

META_MAX = 8192
NAME_MAX_ = 256          # SQUASHFS_NAME_LEN (max byte length of a name)
DIR_COUNT_MAX = 256      # SQUASHFS_DIR_COUNT (count + 1)
INVALID_FRAG = 0xFFFFFFFF
INVALID64 = 0xFFFFFFFFFFFFFFFF
BLOCK_UNCOMPRESSED = 1 << 24
META_UNCOMPRESSED = 1 << 15
MAX_SYMLINK_HOPS = 40    # POSIX ELOOP

TYPE_DIR, TYPE_FILE, TYPE_SYMLINK = 1, 2, 3
TYPE_BLKDEV, TYPE_CHRDEV, TYPE_FIFO, TYPE_SOCKET = 4, 5, 6, 7
TYPE_LDIR, TYPE_LREG, TYPE_LSYMLINK = 8, 9, 10
TYPE_LBLKDEV, TYPE_LCHRDEV, TYPE_LFIFO, TYPE_LSOCKET = 11, 12, 13, 14
BASIC_TYPE = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7,
              8: 1, 9: 2, 10: 3, 11: 4, 12: 5, 13: 6, 14: 7}
TYPE_KIND = {1: 'dir', 2: 'file', 3: 'symlink', 4: 'block-device',
             5: 'char-device', 6: 'fifo', 7: 'socket', 8: 'dir', 9: 'file',
             10: 'symlink', 11: 'block-device', 12: 'char-device',
             13: 'fifo', 14: 'socket'}
DEV_TYPES = (TYPE_BLKDEV, TYPE_CHRDEV, TYPE_LBLKDEV, TYPE_LCHRDEV)
IPC_TYPES = (TYPE_FIFO, TYPE_SOCKET, TYPE_LFIFO, TYPE_LSOCKET)

SB_FMT = 'IIIIIHHHHHHQQQQQQQQ'
SB_FIELDS = ('magic', 'inodes', 'mkfs_time', 'block_size', 'fragments',
             'compression', 'block_log', 'flags', 'no_ids', 's_major',
             's_minor', 'root_inode', 'bytes_used', 'id_table_start',
             'xattr_id_table_start', 'inode_table_start',
             'directory_table_start', 'fragment_table_start',
             'lookup_table_start')

COMP_NAMES = {1: 'gzip', 2: 'lzma2-raw', 4: 'xz'}


class SqfsError(Exception):
    """Unreadable or unsupported image: exit 2."""


def _text(raw, what, forbid_slash=True):
    try:
        s = raw.decode('utf-8')
    except UnicodeDecodeError:
        s = raw.decode('utf-8', 'surrogateescape')
    checks = [('\x00', 'NUL'), ('\t', 'tab'), ('\n', 'newline'),
              ('\r', 'carriage return')]
    if forbid_slash:
        checks.append(('/', 'slash'))
    for bad, label in checks:
        if bad in s:
            raise SqfsError('%s contains a %s byte and cannot be written as TSV'
                            % (what, label))
    return s


def _split(path):
    return [c for c in path.split('/') if c not in ('', '.')]


class MetaStream:
    """Sequential reader over a decompressed metadata block chain."""

    def __init__(self, img, start, offset=0):
        self.img = img
        self.pos = start
        self.data, self.next = img.meta_block(start)
        if offset > len(self.data):
            raise SqfsError('metadata offset %d beyond block %d (len %d)'
                            % (offset, start, len(self.data)))
        self.off = offset

    def read(self, n):
        out = bytearray()
        while len(out) < n:
            if self.off >= len(self.data):
                if self.next >= self.img.bytes_used:
                    raise SqfsError('metadata chain runs past bytes_used at %d'
                                    % self.next)
                self.pos = self.next
                self.data, self.next = self.img.meta_block(self.pos)
                self.off = 0
                if not self.data:
                    raise SqfsError('empty metadata block at %d' % self.pos)
            take = min(n - len(out), len(self.data) - self.off)
            out += self.data[self.off:self.off + take]
            self.off += take
        return bytes(out)

    def u16(self):
        return struct.unpack(self.img.e + 'H', self.read(2))[0]

    def u32(self):
        return struct.unpack(self.img.e + 'I', self.read(4))[0]

    def u64(self):
        return struct.unpack(self.img.e + 'Q', self.read(8))[0]


def decode_dev(rdev):
    """Inverse of squashfs-tools ``(major << 8) | (minor & 0xff) |
    ((minor & ~0xff) << 12)`` (mksquashfs.c:1055)."""
    major = (rdev >> 8) & 0xFFF
    minor = (rdev & 0xFF) | ((rdev >> 12) & 0xFFF00)
    return major, minor


class SquashFS:
    def __init__(self, path, layout='auto'):
        try:
            with open(path, 'rb') as fh:
                self.buf = fh.read()
        except OSError as exc:
            raise SqfsError('cannot read %s: %s' % (path, exc))
        self.path = path
        self.warnings = []
        self._meta_cache = {}
        self._inode_cache = {}
        self._frag = None
        self._frag_cache = {}
        self.stats = {'compressed_data_blocks': 0, 'raw_data_blocks': 0,
                      'sparse_blocks': 0, 'fragment_slices': 0,
                      'fragments_used': 0,
                      'compressed_metadata_blocks': 0,
                      'raw_metadata_blocks': 0}
        self._parse_super(layout)
        self._decompress = self._make_decompressor()
        self._choose_headers(layout)

    # -- primitive reads ---------------------------------------------------
    def _need(self, off, n, what):
        if off < 0 or n < 0 or off + n > len(self.buf):
            raise SqfsError('%s out of bounds: offset %d length %d, image %d '
                            'bytes' % (what, off, n, len(self.buf)))

    def take(self, off, n, what):
        self._need(off, n, what)
        return self.buf[off:off + n]

    # -- superblock --------------------------------------------------------
    def _parse_super(self, layout):
        if len(self.buf) < 96:
            raise SqfsError('image is %d bytes, shorter than a superblock'
                            % len(self.buf))
        magic = self.buf[:4]
        if magic == b'hsqs':
            self.e, self.endian, magic_endian = '<', 'little', 'le'
        elif magic == b'sqsh':
            self.e, self.endian, magic_endian = '>', 'big', 'be'
        else:
            raise SqfsError('bad magic %r: not a SquashFS image' % (magic,))
        if layout == 'le' and magic_endian != 'le':
            raise SqfsError('--layout le given but magic %r is big-endian'
                            % (magic,))
        if layout in ('be', 'avm') and magic_endian != 'be':
            raise SqfsError('--layout %s given but magic %r is little-endian'
                            % (layout, magic))
        for name, val in zip(SB_FIELDS,
                             struct.unpack_from(self.e + SB_FMT, self.buf, 0)):
            setattr(self, name, val)
        if (self.s_major, self.s_minor) != (4, 0):
            raise SqfsError('unsupported SquashFS version %d.%d, need 4.0'
                            % (self.s_major, self.s_minor))
        bs = self.block_size
        if bs < 4096 or bs > (1 << 20) or (bs & (bs - 1)):
            raise SqfsError('unsupported block_size %d' % bs)
        if self.block_log != bs.bit_length() - 1:
            self.warnings.append('block_log %d disagrees with block_size %d; '
                                 'using block_size' % (self.block_log, bs))
        if self.bytes_used < 96:
            raise SqfsError('bytes_used %d below the superblock size'
                            % self.bytes_used)
        if self.bytes_used > len(self.buf):
            raise SqfsError('bytes_used %d exceeds the %d-byte image '
                            '(truncated)' % (self.bytes_used, len(self.buf)))
        for name in ('inode_table_start', 'directory_table_start'):
            val = getattr(self, name)
            if not 96 <= val < self.bytes_used:
                raise SqfsError('%s %d outside [96, %d)'
                                % (name, val, self.bytes_used))
        self.avm_marker = self.mkfs_time == self.bytes_used

    # -- header endianness -------------------------------------------------
    def _choose_headers(self, layout):
        if layout == 'auto':
            self.he, self.block_length_signal = self._decide_header_endian()
        elif layout == 'avm':
            self.he, self.block_length_signal = '<', 'layout-avm'
        else:
            self.he, self.block_length_signal = self.e, 'layout-' + layout
        if self.e == '<' and self.he == '>':
            self.layout = 'le-with-be-headers'
        elif self.e == '>':
            self.layout = 'avm' if self.he == '<' else 'be'
        else:
            self.layout = 'le'
        # The 2-byte header at inode_table_start, decoded both ways, kept so
        # --inspect can show the raw evidence behind the decision.
        raw = self.buf[self.inode_table_start:self.inode_table_start + 2]
        self.header_lengths = {
            'le': struct.unpack('<H', raw)[0] & ~META_UNCOMPRESSED,
            'be': struct.unpack('>H', raw)[0] & ~META_UNCOMPRESSED,
        }

    def _decide_header_endian(self):
        lens = {}
        for he in ('<', '>'):
            raw = struct.unpack_from(he + 'H', self.buf,
                                     self.inode_table_start)[0]
            lens[he] = raw & ~META_UNCOMPRESSED
        exact = [he for he in ('<', '>')
                 if 0 < lens[he] <= META_MAX
                 and self.inode_table_start + 2 + lens[he]
                 == self.directory_table_start]
        plausible = [he for he in ('<', '>') if 0 < lens[he] <= META_MAX]
        if len(exact) == 1:
            return exact[0], 'exact'
        if len(plausible) == 1:
            return plausible[0], 'plausibility'
        # Both plausible and no unique exact identity (a multi-block inode
        # table, or palindromic 0x0101-style block lengths): decode the chain
        # and see which endianness lands on the directory table with a
        # parseable root inode.
        good = []
        for he in ('<', '>'):
            self.he = he
            self._meta_cache.clear()
            self._inode_cache.clear()
            self._frag = None
            self._frag_cache.clear()
            try:
                self._walk_metadata_chain()
                self.inode(self.root_inode)
                # The directory table is a second metadata chain with its own
                # length headers; walking it separates palindromic inode
                # header bytes (0x0101) that decode identically.
                self.walk()
                good.append(he)
            except SqfsError:
                pass
        self._meta_cache.clear()
        self._inode_cache.clear()
        if len(good) == 1:
            return good[0], 'decode'
        if good:
            return (self.e if self.e in good else good[0]), 'ambiguous'
        raise SqfsError('cannot decide metadata block-length endianness '
                        '(headers le=%d be=%d, both rejected)'
                        % (lens['<'], lens['>']))

    def _walk_metadata_chain(self):
        pos = self.inode_table_start
        steps = 0
        while pos < self.directory_table_start:
            _, pos = self.meta_block(pos)
            steps += 1
            if steps > (1 << 20):
                raise SqfsError('metadata chain does not terminate')
        if pos != self.directory_table_start:
            raise SqfsError('metadata chain ends at %d, directory table at %d'
                            % (pos, self.directory_table_start))

    # -- decompression -----------------------------------------------------
    def _make_decompressor(self):
        comp, bs = self.compression, self.block_size
        if comp == 1:
            def d_gzip(raw):
                try:
                    return zlib.decompress(raw)
                except zlib.error:
                    return zlib.decompress(raw, -15)
            return d_gzip
        if comp in (2, 4):
            # Id 4 is xz; id 2 is what the lane writer emits for raw LZMA2.
            # A genuine vendor carrier stores complete .xz containers; the
            # other containers are accepted so old fixtures keep reading.
            def d_lzma(raw):
                attempts = [(lzma.FORMAT_XZ, None), (lzma.FORMAT_AUTO, None),
                            (lzma.FORMAT_ALONE, None),
                            (lzma.FORMAT_RAW,
                             [{'id': lzma.FILTER_LZMA2, 'dict_size': bs}])]
                for fmt, filters in attempts:
                    try:
                        if filters is None:
                            return lzma.decompress(raw, format=fmt)
                        return lzma.decompress(raw, format=fmt,
                                               filters=filters)
                    except lzma.LZMAError:
                        continue
                raise SqfsError('lzma: no container decoded (%d bytes, '
                                'compression id %d)' % (len(raw), comp))
            return d_lzma
        raise SqfsError('unsupported compression id %d (supported: 1 gzip, '
                        '2 raw LZMA2, 4 xz)' % comp)

    def decomp(self, raw, what):
        try:
            return self._decompress(raw)
        except SqfsError:
            raise
        except Exception as exc:                     # noqa: BLE001 - report
            raise SqfsError('%s: decompression failed: %s' % (what, exc))

    # -- metadata ----------------------------------------------------------
    def meta_block(self, pos):
        cached = self._meta_cache.get(pos)
        if cached is not None:
            return cached
        self._need(pos, 2, 'metadata header')
        raw = struct.unpack_from(self.he + 'H', self.buf, pos)[0]
        size = raw & ~META_UNCOMPRESSED
        if size == 0:
            raise SqfsError('zero-length metadata block at %d' % pos)
        body = self.take(pos + 2, size, 'metadata body')
        if raw & META_UNCOMPRESSED:
            self.stats['raw_metadata_blocks'] += 1
            data = body
        else:
            self.stats['compressed_metadata_blocks'] += 1
            data = self.decomp(body, 'metadata block at %d' % pos)
        if len(data) > META_MAX:
            raise SqfsError('metadata block at %d decompresses to %d bytes '
                            '(max %d)' % (pos, len(data), META_MAX))
        out = (data, pos + 2 + size)
        self._meta_cache[pos] = out
        return out

    # -- inodes ------------------------------------------------------------
    def inode(self, ref):
        cached = self._inode_cache.get(ref)
        if cached is not None:
            return cached
        st = MetaStream(self, self.inode_table_start + (ref >> 16),
                        ref & 0xFFFF)
        node = {'ref': ref}
        typ = st.u16()
        node['type'] = typ
        node['kind'] = TYPE_KIND.get(typ)
        if node['kind'] is None:
            raise SqfsError('unsupported inode type %d at ref %#x'
                            % (typ, ref))
        node['mode'] = st.u16()
        node['uid'] = st.u16()
        node['gid'] = st.u16()
        node['mtime'] = st.u32()
        node['inode_number'] = st.u32()
        if typ in (TYPE_DIR,):
            node['start_block'] = st.u32()
            node['nlink'] = st.u32()
            node['file_size'] = st.u16()
            node['offset'] = st.u16()
            node['parent_inode'] = st.u32()
        elif typ == TYPE_LDIR:
            node['nlink'] = st.u32()
            node['file_size'] = st.u32()
            node['start_block'] = st.u32()
            node['parent_inode'] = st.u32()
            node['i_count'] = st.u16()
            node['offset'] = st.u16()
            node['xattr'] = st.u32()
        elif typ in (TYPE_FILE,):
            node['start_block'] = st.u32()
            node['fragment'] = st.u32()
            node['frag_offset'] = st.u32()
            node['file_size'] = st.u32()
            node['block_list'] = self._block_list(st, node)
        elif typ == TYPE_LREG:
            node['start_block'] = st.u64()
            node['file_size'] = st.u64()
            node['sparse'] = st.u64()
            node['nlink'] = st.u32()
            node['fragment'] = st.u32()
            node['frag_offset'] = st.u32()
            node['xattr'] = st.u32()
            node['block_list'] = self._block_list(st, node)
        elif typ in (TYPE_SYMLINK, TYPE_LSYMLINK):
            node['nlink'] = st.u32()
            size = st.u32()
            if size > 0x1000:
                raise SqfsError('symlink inode %#x declares %d target bytes'
                                % (ref, size))
            raw = st.read(size)
            if typ == TYPE_LSYMLINK:
                st.u32()                              # xattr (inode.c:296-302)
            node['target'] = _text(raw, 'symlink target at %s' % hex(ref),
                                   forbid_slash=False)
        elif typ in DEV_TYPES:
            node['nlink'] = st.u32()
            node['rdev'] = st.u32()
            if typ in (TYPE_LBLKDEV, TYPE_LCHRDEV):
                st.u32()                              # xattr
            major, minor = decode_dev(node['rdev'])
            node['detail'] = '%d:%d' % (major, minor)
        elif typ in IPC_TYPES:
            node['nlink'] = st.u32()
            if typ in (TYPE_LFIFO, TYPE_LSOCKET):
                st.u32()                              # xattr
        else:
            raise SqfsError('unsupported inode type %d at ref %#x'
                            % (typ, ref))
        self._inode_cache[ref] = node
        return node

    def _block_list(self, st, node):
        size, bs = node['file_size'], self.block_size
        if node['fragment'] == INVALID_FRAG:
            n = (size + bs - 1) // bs
        else:
            n = size // bs
        if n > (1 << 24):
            raise SqfsError('file inode %#x declares %d data blocks'
                            % (node['ref'], n))
        entries = [st.u32() for _ in range(n)]
        for i, field in enumerate(entries):
            if field >> 25:
                raise SqfsError('file inode %#x block %d has invalid size '
                                'field %#x' % (node['ref'], i, field))
        return entries

    # -- directories -------------------------------------------------------
    def dir_entries(self, node):
        start = self.directory_table_start + node['start_block']
        length = node['file_size'] - 3          # dir.c:143-151: 3 invented bytes
        if length < 0:
            raise SqfsError('directory inode %#x has file_size %d < 3'
                            % (node['ref'], node['file_size']))
        if start >= self.bytes_used:
            raise SqfsError('directory table start %d past bytes_used'
                            % start)
        st = MetaStream(self, start, node['offset'])
        read = 0
        while read < length:
            hdr = st.read(12)
            count = struct.unpack_from(self.e + 'I', hdr, 0)[0] + 1
            sblock = struct.unpack_from(self.e + 'I', hdr, 4)[0]
            if count > DIR_COUNT_MAX:
                raise SqfsError('directory inode %#x header count %d > %d'
                                % (node['ref'], count, DIR_COUNT_MAX))
            read += 12
            for _ in range(count):
                ent = st.read(8)
                eoff = struct.unpack_from(self.e + 'H', ent, 0)[0]
                etype = struct.unpack_from(self.e + 'H', ent, 4)[0]
                nsize = struct.unpack_from(self.e + 'H', ent, 6)[0] + 1
                if nsize > NAME_MAX_:
                    raise SqfsError('directory entry name length %d > %d'
                                    % (nsize, NAME_MAX_))
                name = st.read(nsize)
                read += 8 + nsize
                if read > length:
                    raise SqfsError('directory inode %#x overruns its %d-byte '
                                    'body' % (node['ref'], length))
                if not 1 <= etype <= 7:
                    raise SqfsError('directory entry type %d for %r'
                                    % (etype, name))
                if not name or name in (b'.', b'..'):
                    raise SqfsError('directory entry with reserved name %r'
                                    % (name,))
                text = _text(name, 'directory entry name')
                ref = (sblock << 16) | eoff
                yield text, etype, ref

    # -- fragments ---------------------------------------------------------
    def fragment_entry(self, index):
        if index >= self.fragments:
            raise SqfsError('fragment index %d >= fragments %d'
                            % (index, self.fragments))
        if self._frag is None:
            self._load_fragment_table()
        return self._frag_cache.get(index)

    def _load_fragment_table(self):
        n = self.fragments
        self._frag = True
        if n == 0:
            return
        if self.fragment_table_start == INVALID64:
            raise SqfsError('fragments = %d but fragment_table_start is '
                            '-1' % n)
        index_bytes = 8 * ((n * 16 + META_MAX - 1) // META_MAX)
        self._need(self.fragment_table_start, index_bytes,
                   'fragment table index')
        page_cache = {}
        for i in range(n):
            page = (i * 16) // META_MAX
            off = (i * 16) % META_MAX
            ptr = struct.unpack_from(
                self.e + 'Q', self.buf,
                self.fragment_table_start + 8 * page)[0]
            block = page_cache.get(ptr)
            if block is None:
                if not 96 <= ptr < self.bytes_used:
                    raise SqfsError('fragment table block pointer %d outside '
                                    'the image' % ptr)
                block = self.meta_block(ptr)[0]
                page_cache[ptr] = block
            if off + 16 > len(block):
                raise SqfsError('fragment entry %d beyond its metadata block'
                                % i)
            start, size, _unused = struct.unpack_from(self.e + 'QII', block,
                                                      off)
            self._frag_cache[i] = (start, size)

    def fragment_bytes(self, index):
        start, field = self.fragment_entry(index)
        on_disk = field & ~BLOCK_UNCOMPRESSED
        if on_disk == 0:
            raise SqfsError('fragment %d has no data (size 0)' % index)
        if start + on_disk > self.bytes_used:
            raise SqfsError('fragment %d out of bounds (%d+%d > %d)'
                            % (index, start, on_disk, self.bytes_used))
        raw = self.buf[start:start + on_disk]
        data = raw if field & BLOCK_UNCOMPRESSED else \
            self.decomp(raw, 'fragment %d at %d' % (index, start))
        if len(data) > self.block_size:
            raise SqfsError('fragment %d decompresses to %d > block_size %d'
                            % (index, len(data), self.block_size))
        self.stats['fragments_used'] += 1
        return data

    # -- file data ---------------------------------------------------------
    def iter_file_data(self, node):
        bs, size = self.block_size, node['file_size']
        pos = node['start_block']
        remaining = size
        for field in node['block_list']:
            want = min(bs, remaining)
            if want == 0:
                break
            if (field & ~BLOCK_UNCOMPRESSED) == 0:
                self.stats['sparse_blocks'] += 1
                yield bytes(want)                 # sparse block, file.c:616
                remaining -= want
                continue
            on_disk = field & ~BLOCK_UNCOMPRESSED
            if pos + on_disk > self.bytes_used:
                raise SqfsError('data block at %d+%d beyond bytes_used'
                                % (pos, on_disk))
            raw = self.buf[pos:pos + on_disk]
            if field & BLOCK_UNCOMPRESSED:
                self.stats['raw_data_blocks'] += 1
                data = raw
            else:
                self.stats['compressed_data_blocks'] += 1
                data = self.decomp(raw, 'data block at %d' % pos)
            if len(data) < want:
                raise SqfsError('data block at %d is %d bytes, need %d'
                                % (pos, len(data), want))
            yield data[:want]
            pos += on_disk
            remaining -= want
        if remaining:
            if node['fragment'] == INVALID_FRAG:
                raise SqfsError('file inode %#x: %d bytes with no fragment'
                                % (node['ref'], remaining))
            self.stats['fragment_slices'] += 1
            data = self.fragment_bytes(node['fragment'])
            off = node['frag_offset']
            if off + remaining > len(data):
                raise SqfsError('fragment %d slice %d+%d > %d bytes'
                                % (node['fragment'], off, remaining,
                                   len(data)))
            yield data[off:off + remaining]

    # -- tree walk ---------------------------------------------------------
    def walk(self):
        files, links, kinds = {}, {}, {}
        dirs, specials = {}, []
        root = self.inode(self.root_inode)
        if root['type'] not in (TYPE_DIR, TYPE_LDIR):
            raise SqfsError('root inode %#x is type %d, not a directory'
                            % (self.root_inode, root['type']))
        stack = [('', root)]
        seen_dirs = set()
        while stack:
            path, node = stack.pop()
            if node['ref'] in seen_dirs:
                raise SqfsError('directory inode %#x reachable twice'
                                % node['ref'])
            seen_dirs.add(node['ref'])
            seen_names = set()
            for name, etype, ref in self.dir_entries(node):
                if name in seen_names:
                    raise SqfsError('duplicate entry %r in directory %r'
                                    % (name, path or '.'))
                seen_names.add(name)
                child_path = name if not path else path + '/' + name
                child = self.inode(ref)
                if BASIC_TYPE[child['type']] != etype:
                    self.warnings.append(
                        'dir entry type %d != inode type %d for %r'
                        % (etype, child['type'], child_path))
                if child['type'] in (TYPE_DIR, TYPE_LDIR):
                    kinds[child_path] = 'dir'
                    dirs[child_path] = child
                    stack.append((child_path, child))
                elif child['type'] in (TYPE_FILE, TYPE_LREG):
                    kinds[child_path] = 'file'
                    files[child_path] = child
                elif child['type'] in (TYPE_SYMLINK, TYPE_LSYMLINK):
                    kinds[child_path] = 'link'
                    links[child_path] = child['target']
                else:
                    kinds[child_path] = child['kind']
                    specials.append((child_path, child))
        return dirs, files, links, specials


def classify_link(link_path, target, kinds, links):
    """Resolve ``target`` POSIX-style; return (class, reason)."""
    if target == '':
        return 'escaping', 'empty-target'   # removed, no report at all
    base = [] if link_path.startswith('/') else _split(link_path)[:-1]
    if target.startswith('/'):
        base = []
    absolute = target.startswith('/')
    pending = target.split('/')
    cur = list(base)
    hops = 0
    while pending:
        comp = pending.pop(0)
        if comp in ('', '.'):
            continue
        if comp == '..':
            if not cur:
                return 'escaping', 'above-root'   # climbed above image root
            cur.pop()
            continue
        cur.append(comp)
        path = '/'.join(cur)
        if kinds.get(path) == 'link':
            hops += 1
            if hops > MAX_SYMLINK_HOPS:
                # Measured: unblob 26.6.4 runs on Python 3.13, where
                # Path.resolve() returns the unresolved path for a loop
                # instead of raising; fix_symlink therefore keeps the link
                # inside the root and REA records an unpublished-entry gap.
                return 'in-tree', 'loop'
            tgt = links[path]
            if tgt == '':
                return 'escaping', 'empty-target'
            cur.pop()
            if tgt.startswith('/'):
                cur = []
            pending = tgt.split('/') + pending
    return 'in-tree', 'absolute-inside' if absolute else 'inside'


def write_tsv(path, rows):
    rows = list(rows)
    rows.sort(key=lambda r: r[0].encode('utf-8', 'surrogateescape'))
    try:
        with open(path, 'w', encoding='utf-8', errors='surrogateescape',
                  newline='\n') as fh:
            for row in rows:
                fh.write('\t'.join(row) + '\n')
    except OSError as exc:
        raise SqfsError('cannot write %s: %s' % (path, exc))


def _swap_field(img, field, width):
    """Re-read ``field`` as if the image endianness were the opposite one."""
    swap = '<' if img.e == '>' else '>'
    fmt = {2: 'H', 4: 'I', 8: 'Q'}[width]
    return struct.unpack(swap + fmt, struct.pack(img.e + fmt, field))[0]


def block_length_evidence(img, files):
    """Report how the first data-block size list decodes in each endianness.

    The metadata header endianness is chosen in ``--layout auto``; this second
    signal covers the size list stored in the inode (the Freetz note calls the
    block-length field out separately).  A decode counts as good when the
    declared size stays in bounds and the payload decompresses.
    """
    out = {}
    for path, node in files.items():
        if not node.get('block_list'):
            continue
        field = node['block_list'][0]
        on_disk = field & ~BLOCK_UNCOMPRESSED
        if on_disk == 0:
            continue
        result = {'file': path, 'field_hex': '%08x' % field,
                  'raw_uncompressed': bool(field & BLOCK_UNCOMPRESSED)}
        for label, ee in (('structural', img.e),
                          ('swapped', '<' if img.e == '>' else '>')):
            value = field if ee == img.e else _swap_field(img, field, 4)
            size = value & 0xFFFFFF
            raw_hint = bool(value & BLOCK_UNCOMPRESSED)
            rec = {'value_hex': '%08x' % value, 'size': size,
                   'uncompressed': raw_hint}
            if not 0 < size <= img.block_size * 2:
                rec['decode'] = 'size-implausible'
            elif node['start_block'] + size > img.bytes_used:
                rec['decode'] = 'out-of-bounds'
            else:
                payload = img.buf[node['start_block']:
                                  node['start_block'] + size]
                try:
                    data = payload if raw_hint else img._decompress(payload)
                    rec['decode'] = 'ok'
                    rec['out_bytes'] = len(data)
                except Exception as exc:             # noqa: BLE001 - evidence
                    rec['decode'] = 'decompress-error: %s' % exc
            result[label] = rec
        out = result
        break
    return out


def fragment_entry_evidence(img):
    """Decode the first fragment entry in both endiannesses."""
    if not img.fragments:
        return {}
    try:
        img._load_fragment_table()
    except SqfsError as exc:
        return {'error': str(exc)}
    if 0 not in img._frag_cache:
        return {}
    start, field = img._frag_cache[0]
    out = {}
    for label, ee in (('structural', img.e),
                      ('swapped', '<' if img.e == '>' else '>')):
        s = start if ee == img.e else _swap_field(img, start, 8)
        f = field if ee == img.e else _swap_field(img, field, 4)
        size = f & ~BLOCK_UNCOMPRESSED
        rec = {'start': s, 'size': size,
               'uncompressed': bool(f & BLOCK_UNCOMPRESSED)}
        rec['plausible'] = (0 < size <= img.block_size
                            and 96 <= s < img.bytes_used)
        out[label] = rec
    return out


def collect(img):
    dirs, files, links, specials = img.walk()
    kinds = {}
    for path in dirs:
        kinds[path] = 'dir'
    for path in files:
        kinds[path] = 'file'
    for path, _target in links.items():
        kinds[path] = 'link'
    for path, node in specials:
        kinds[path] = node['kind']
    file_rows = []
    for path, node in files.items():
        h = hashlib.sha256()
        size = 0
        for chunk in img.iter_file_data(node):
            h.update(chunk)
            size += len(chunk)
        if size != node['file_size']:
            raise SqfsError('%r: read %d bytes, inode declares %d'
                            % (path, size, node['file_size']))
        file_rows.append((path, h.hexdigest(), str(size)))
    nonregular = []
    for path in dirs:
        nonregular.append((path, 'dir', ''))
    reasons = {}
    in_tree = escaping = 0
    for path, target in links.items():
        cls, why = classify_link(path, target, kinds, links)
        reasons[why] = reasons.get(why, 0) + 1
        if cls == 'in-tree':
            in_tree += 1
        else:
            escaping += 1
        nonregular.append((path, 'symlink', target))
    counts = {}
    for path, node in specials:
        detail = node['detail'] if node['type'] in DEV_TYPES else ''
        nonregular.append((path, node['kind'], detail))
        counts[node['kind']] = counts.get(node['kind'], 0) + 1
    meta = {
        'image': img.path,
        'size': len(img.buf),
        'layout': img.layout,
        'endian': img.endian,
        'header_endian': 'little' if img.he == '<' else 'big',
        'block_length_signal': img.block_length_signal,
        'header_length_candidates': img.header_lengths,
        'avm_marker': img.avm_marker,
        'superblock': {k: getattr(img, k) for k in SB_FIELDS},
        'compression': COMP_NAMES.get(img.compression, img.compression),
        'regular_files': len(file_rows),
        'directories': len(dirs),
        'symlinks': len(links),
        'special_files': len(specials),
        'special_kinds': counts,
        'in_tree_symlinks': in_tree,
        'escaping_symlinks': escaping,
        'symlink_reasons': reasons,
        'data_block_length_evidence': block_length_evidence(img, files),
        'fragment_entry_evidence': fragment_entry_evidence(img),
        'decode_paths': img.stats,
        'warnings': img.warnings,
    }
    return file_rows, nonregular, meta


# ---------------------------------------------------------------------------
# Self test.  A minimal, independent v4 writer builds images in a temporary
# directory; the reader then has to reproduce the known tree.  No sasquatch,
# no unblob, no external image.
# ---------------------------------------------------------------------------

_MKFS_TIME = 1700000000
_UNCOMPRESSED = 0x8000


def _pack(e, fmt, *vals):
    return struct.pack(e + fmt, *vals)


def _compress(kind, data, block_size):
    if kind == 'gzip':
        return zlib.compress(data, 9)
    if kind == 'xz':
        return lzma.compress(data, format=lzma.FORMAT_XZ,
                             check=lzma.CHECK_CRC32,
                             filters=[{'id': lzma.FILTER_LZMA2,
                                       'preset': 6}])
    if kind == 'lzma2':
        return lzma.compress(
            data, format=lzma.FORMAT_RAW,
            filters=[{'id': lzma.FILTER_LZMA2,
                      'dict_size': block_size,
                      'preset': 6}])
    raise ValueError(kind)


def _meta_block(img, data, he, comp, block_size):
    raw = _compress(comp, data, block_size)
    if len(raw) >= len(data):
        return _pack(he, 'H', len(data) | _UNCOMPRESSED) + data
    return _pack(he, 'H', len(raw)) + raw


def _etype(typ):
    return {'dir': 1, 'file': 2, 'symlink': 3, 'block-device': 4,
            'char-device': 5, 'fifo': 6, 'socket': 7}[typ]


def _build_image(nodes, endian='le', header_endian=None, comp='gzip',
                 compression_id=None, marker=False, block_size=4096):
    """Build one SquashFS v4 image; return bytes.

    nodes: list of dicts with path, type in
    dir|file|symlink|block-device|char-device|fifo|socket, optional
    ext (extended inode), data, target, rdev (major, minor), fragment.
    """
    e = '<' if endian == 'le' else '>'
    he = header_endian or ('<' if endian == 'le' else '>')
    cid = compression_id or {'gzip': 1, 'xz': 4, 'lzma2': 2}[comp]
    nodes = [dict(n) for n in nodes]
    have = {n['path'] for n in nodes}
    for n in list(nodes):
        parts = n['path'].split('/')[:-1]
        for i in range(1, len(parts) + 1):
            p = '/'.join(parts[:i])
            if p not in have:
                nodes.append({'path': p, 'type': 'dir'})
                have.add(p)
    dirs = sorted(n['path'] for n in nodes if n['type'] == 'dir')
    # implicit root
    nodes.append({'path': '', 'type': 'dir'})
    dirs = [''] + dirs
    dirs = sorted(set(dirs))
    by_path = {n['path']: n for n in nodes}
    inode_no = {}
    for i, path in enumerate(sorted(p for p in by_path if p), start=1):
        inode_no[path] = i
    inode_no[''] = len(inode_no) + 1
    children = {d: [] for d in dirs}
    for path in sorted(p for p in by_path if p):
        parent = path.rsplit('/', 1)[0] if '/' in path else ''
        children[parent].append(path)
    for d in children:
        children[d].sort(key=lambda p: p.rsplit('/', 1)[-1])

    # ---- data area -------------------------------------------------------
    data = bytearray()
    frag_buf = bytearray()
    frag_entries = []          # (start_abs, size_field)
    frag_of = {}               # path -> (index, offset)
    blocks_of = {}
    starts = {}

    def emit_data(chunk):
        c = _compress(comp, chunk, block_size)
        if len(c) >= len(chunk):
            return chunk, len(chunk) | BLOCK_UNCOMPRESSED
        return c, len(c)

    for path in sorted(by_path):
        n = by_path[path]
        if n['type'] != 'file':
            continue
        content = n.get('data', b'')
        use_frag = n.get('fragment', False)
        nblocks = (len(content) // block_size) if use_frag else \
            ((len(content) + block_size - 1) // block_size)
        starts[path] = 96 + len(data)
        bl = []
        for i in range(nblocks):
            chunk = content[i * block_size:(i + 1) * block_size]
            raw, field = emit_data(chunk)
            data += raw
            bl.append(field)
        blocks_of[path] = bl
        if use_frag:
            tail = content[nblocks * block_size:]
            if tail:
                if len(frag_buf) + len(tail) > block_size and frag_buf:
                    raw, field = emit_data(bytes(frag_buf))
                    frag_entries.append((96 + len(data), field))
                    data += raw
                    frag_buf = bytearray()
                off = len(frag_buf)
                frag_buf += tail
                frag_of[path] = (len(frag_entries), off)
    if frag_buf:
        raw, field = emit_data(bytes(frag_buf))
        frag_entries.append((96 + len(data), field))
        data += raw
    nfrag = len(frag_entries)

    # ---- inode sizes and positions (one metadata block) ------------------
    def inode_size(n):
        t = n['type']
        ext = n.get('ext', False)
        if t == 'dir':
            return 40 if ext else 32
        if t == 'file':
            nb = len(blocks_of.get(n['path'], []))
            base = 56 if ext else 32
            return base + 4 * nb
        if t == 'symlink':
            base = 16 + 8 + len(n['target'].encode())
            return base + (4 if ext else 0)
        if t in ('block-device', 'char-device'):
            return 28 if ext else 24
        return 24 if ext else 20

    order = [p for p in sorted(by_path) if p] + ['']
    offset = 0
    inode_off = {}
    for path in order:
        inode_off[path] = offset
        offset += inode_size(by_path[path])
    if offset > META_MAX:
        raise RuntimeError('selftest tree does not fit one inode block')
    ref = {p: (0 << 16) | inode_off[p] for p in order}

    # ---- directory table -------------------------------------------------
    dir_tbl = bytearray()
    dir_off = {}
    for d in sorted(dirs, key=lambda x: (x != '', x)):
        tbl = bytearray()
        kids = children[d]
        if kids:
            first = inode_no[kids[0]]
            tbl += _pack(e, 'III', len(kids) - 1, 0, first)
            for path in kids:
                nm = path.rsplit('/', 1)[-1].encode()
                tbl += (_pack(e, 'HhHH', ref[path] & 0xFFFF,
                              inode_no[path] - first,
                              _etype(by_path[path]['type']), len(nm) - 1)
                        + nm)
        dir_off[d] = len(dir_tbl)
        dir_tbl += tbl
    if len(dir_tbl) > META_MAX:
        raise RuntimeError('selftest tree does not fit one dir block')

    # ---- inode records ---------------------------------------------------
    inodes = bytearray()
    for path in order:
        n = by_path[path]
        t = n['type']
        ext = n.get('ext', False)
        typ = {'dir': TYPE_LDIR if ext else TYPE_DIR,
               'file': TYPE_LREG if ext else TYPE_FILE,
               'symlink': TYPE_LSYMLINK if ext else TYPE_SYMLINK,
               'block-device': TYPE_LBLKDEV if ext else TYPE_BLKDEV,
               'char-device': TYPE_LCHRDEV if ext else TYPE_CHRDEV,
               'fifo': TYPE_LFIFO if ext else TYPE_FIFO,
               'socket': TYPE_LSOCKET if ext else TYPE_SOCKET}[t]
        mode = {'dir': 0o40755, 'file': 0o100644, 'symlink': 0o120777,
                'block-device': 0o60600, 'char-device': 0o20600,
                'fifo': 0o10644, 'socket': 0o140644}[t]
        rec = (_pack(e, 'HHHHII', typ, mode, 0, 0, _MKFS_TIME,
                     inode_no[path]))
        if t == 'dir':
            # directory body length = entries + 3 (reader subtracts 3)
            body_len = _dir_body_len(children[path], by_path, e)
            parent = inode_no.get(path.rsplit('/', 1)[0] if '/' in path
                                  else '', inode_no[''])
            nlink = 2 + sum(1 for c in children[path]
                            if by_path[c]['type'] == 'dir')
            if ext:
                rec += _pack(e, 'IIIIHHI', nlink, body_len + 3, 0, parent,
                             len(children[path]), dir_off[path], 0)
            else:
                rec += _pack(e, 'IIHHI', 0, nlink, body_len + 3,
                             dir_off[path], parent)
        elif t == 'file':
            bl = blocks_of[path]
            fval = frag_of.get(path, (INVALID_FRAG, 0))
            size = len(n.get('data', b''))
            if ext:
                rec += _pack(e, 'QQQIIII', starts[path], size, 0, 1,
                             fval[0], fval[1], 0)
            else:
                rec += _pack(e, 'IIII', starts[path], fval[0], fval[1], size)
            rec += b''.join(_pack(e, 'I', v) for v in bl)
        elif t == 'symlink':
            tb = n['target'].encode()
            rec += _pack(e, 'II', 1, len(tb)) + tb
            if ext:
                rec += _pack(e, 'I', 0)
        elif t in ('block-device', 'char-device'):
            major, minor = n.get('rdev', (0, 0))
            rdev = (major << 8) | (minor & 0xFF) | ((minor & ~0xFF) << 12)
            rec += _pack(e, 'II', 1, rdev)
            if ext:
                rec += _pack(e, 'I', 0)
        else:
            rec += _pack(e, 'I', 1)
            if ext:
                rec += _pack(e, 'I', 0)
        inodes += rec
    if len(inodes) != offset:
        raise RuntimeError('selftest inode size mismatch %d != %d'
                           % (len(inodes), offset))

    # ---- assemble --------------------------------------------------------
    inode_table_start = 96 + len(data)
    inode_meta = _meta_block(None, bytes(inodes), he, comp, block_size)
    dir_table_start = inode_table_start + len(inode_meta)
    dir_meta = _meta_block(None, bytes(dir_tbl), he, comp, block_size)
    pos = dir_table_start + len(dir_meta)
    frag_meta_start = pos
    frag_index_start = INVALID64
    if nfrag:
        ftbl = b''.join(_pack(e, 'QII', s, f, 0) for s, f in frag_entries)
        frag_meta = _meta_block(None, ftbl, he, comp, block_size)
        pos += len(frag_meta)
        frag_index_start = pos
        index = _pack(e, 'Q', frag_meta_start)
        pos += len(index)
    id_meta_start = pos
    id_meta = _meta_block(None, _pack(e, 'I', 0), he, comp, block_size)
    pos += len(id_meta)
    id_index_start = pos
    id_index = _pack(e, 'Q', id_meta_start)
    pos += len(id_index)
    total = pos

    magic = b'hsqs' if e == '<' else b'sqsh'
    mkfs = total if marker else _MKFS_TIME
    sb = (magic + _pack(e, 'IIIIHHHHHHQQQQQQQQ',
                        len(order), mkfs, block_size, nfrag,
                        cid, block_size.bit_length() - 1, 0, 1, 4, 0,
                        ref[''], total, id_index_start, INVALID64,
                        inode_table_start, dir_table_start,
                        frag_index_start, INVALID64))
    out = bytearray(sb)
    out += data
    out += inode_meta
    out += dir_meta
    if nfrag:
        out += frag_meta
        out += index
    out += id_meta
    out += id_index
    if len(out) != total or len(sb) != 96:
        raise RuntimeError('selftest assembly mismatch')
    return bytes(out)


def _dir_body_len(kids, by_path, e):
    total = 12 if kids else 0
    for path in kids:
        total += 8 + len(path.rsplit('/', 1)[-1].encode())
    return total


def _selftest_manifest(rows, nonregular):
    return ({r[0]: (r[1], int(r[2])) for r in rows},
            {r[0]: (r[1], r[2]) for r in nonregular})


def _selftest_tree():
    return [
        {'path': 'bin/tool', 'type': 'file',
         'data': bytes(range(256)) * 20, 'fragment': False},
        {'path': 'bin/tail', 'type': 'file',
         'data': b'tail-piece-' * 40, 'fragment': True},
        {'path': 'etc/conf', 'type': 'file', 'data': b'k=v\n' * 20,
         'fragment': True},
        {'path': 'etc/small', 'type': 'file', 'data': b'x',
         'fragment': False},
        {'path': 'etc/ünïcode', 'type': 'file', 'data': b'utf8-name',
         'fragment': False},
        {'path': 'docs/uni', 'type': 'symlink', 'target': 'ünïcode'},
        {'path': 'docs/deep/note', 'type': 'file', 'data': b'n' * 9000,
         'fragment': True},
        {'path': 'docs/link', 'type': 'symlink', 'target': '../bin/tool'},
        {'path': 'docs/abs', 'type': 'symlink', 'target': '/etc/passwd'},
        {'path': 'docs/esc', 'type': 'symlink', 'target': '../../etc'},
        {'path': 'dev/console', 'type': 'char-device', 'rdev': (5, 1)},
        {'path': 'dev/sda', 'type': 'block-device', 'rdev': (8, 0)},
        {'path': 'dev/big', 'type': 'char-device', 'rdev': (240, 0x1234)},
        {'path': 'run/fifo', 'type': 'fifo'},
        {'path': 'run/sock', 'type': 'socket'},
    ]


def _selftest_extended_tree():
    return [
        {'path': 'd/f', 'type': 'file', 'data': b'extended' * 10,
         'fragment': True, 'ext': True},
        {'path': 'd/l', 'type': 'symlink', 'target': 'f', 'ext': True},
        {'path': 'd/c', 'type': 'char-device', 'rdev': (1, 3), 'ext': True},
        {'path': 'd/b', 'type': 'block-device', 'rdev': (8, 16), 'ext': True},
        {'path': 'd/p', 'type': 'fifo', 'ext': True},
        {'path': 'd/s', 'type': 'socket', 'ext': True},
        {'path': 'd/sub', 'type': 'dir', 'ext': True},
    ]


def _read_image(path, layout='auto'):
    img = SquashFS(path, layout=layout)
    rows, nonregular, meta = collect(img)
    return img, rows, nonregular, meta


def run_selftest():
    results = []

    def case(name, fn):
        try:
            fn()
        except Exception as exc:                     # noqa: BLE001 - report
            results.append((name, False, '%s: %s'
                            % (type(exc).__name__, exc)))
        else:
            results.append((name, True, ''))

    def roundtrip(tree, endian, comp, layout='auto', **kw):
        with tempfile.TemporaryDirectory(prefix='sqfs-selftest-') as td:
            p = os.path.join(td, 'img.sqsh')
            with open(p, 'wb') as fh:
                fh.write(_build_image(tree, endian=endian, comp=comp, **kw))
            img, rows, nonregular, meta = _read_image(p, layout=layout)
            got_files, got_non = _selftest_manifest(rows, nonregular)
            exp_files = {n['path']: (hashlib.sha256(n['data']).hexdigest(),
                                     len(n['data']))
                         for n in tree if n['type'] == 'file'}
            exp_non = {}
            for n in tree:
                if n['type'] == 'dir':
                    exp_non[n['path']] = ('dir', '')
                elif n['type'] == 'symlink':
                    exp_non[n['path']] = ('symlink', n['target'])
                elif n['type'] in ('char-device', 'block-device'):
                    exp_non[n['path']] = (n['type'], '%d:%d' % n['rdev'])
                elif n['type'] in ('fifo', 'socket'):
                    exp_non[n['path']] = (n['type'], '')
            # implicit parent directories
            for n in tree:
                parts = n['path'].split('/')[:-1]
                for i in range(1, len(parts) + 1):
                    exp_non.setdefault('/'.join(parts[:i]), ('dir', ''))
            if got_files != exp_files:
                raise AssertionError('files %r != %r'
                                     % (sorted(got_files), sorted(exp_files)))
            missing = {k: v for k, v in exp_non.items()
                       if got_non.get(k) != v}
            extra = {k: v for k, v in got_non.items() if k not in exp_non}
            if missing or extra:
                raise AssertionError('nonregular missing=%r extra=%r'
                                     % (missing, extra))
            return img, meta, got_files, got_non

    def c_le_gzip():
        img, meta, _, _ = roundtrip(_selftest_tree(), 'le', 'gzip')
        assert meta['layout'] == 'le', meta['layout']
        assert meta['compression'] == 'gzip'

    def c_be_gzip():
        img, meta, _, _ = roundtrip(_selftest_tree(), 'be', 'gzip',
                                    layout='be')
        assert meta['layout'] == 'be', meta['layout']

    def c_avm_gzip():
        img, meta, _, _ = roundtrip(_selftest_tree(), 'be', 'gzip',
                                    header_endian='<', marker=True,
                                    layout='avm')
        assert meta['layout'] == 'avm', meta['layout']
        assert meta['avm_marker'] is True

    def c_avm_xz():
        img, meta, files, _ = roundtrip(_selftest_tree(), 'be', 'xz',
                                        header_endian='<', marker=True,
                                        layout='avm')
        assert meta['compression'] == 'xz'
        assert img.stats['compressed_data_blocks'] + \
            img.stats['raw_data_blocks'] > 0

    def c_avm_lzma2():
        img, meta, _, _ = roundtrip(_selftest_tree(), 'be', 'lzma2',
                                    header_endian='<',
                                    compression_id=2, layout='avm')
        assert meta['compression'] == 'lzma2-raw', meta['compression']

    def c_auto_standard_be():
        img, meta, _, _ = roundtrip(_selftest_tree(), 'be', 'gzip')
        assert meta['layout'] == 'be', meta['layout']
        assert meta['block_length_signal'] in ('exact', 'decode'), meta

    def c_auto_avm():
        img, meta, _, _ = roundtrip(_selftest_tree(), 'be', 'gzip',
                                    header_endian='<', marker=True)
        assert meta['layout'] == 'avm', meta['layout']
        assert meta['header_endian'] == 'little'

    def c_extended():
        img, meta, files, non = roundtrip(_selftest_extended_tree(), 'be',
                                          'xz', header_endian='<',
                                          layout='avm')
        assert non['d/c'] == ('char-device', '1:3')
        assert non['d/b'] == ('block-device', '8:16')
        assert non['d/p'] == ('fifo', '')
        assert non['d/s'] == ('socket', '')
        assert non['d/l'] == ('symlink', 'f')

    def c_fragments_offsets():
        tree = [
            {'path': 'a', 'type': 'file', 'data': b'A' * 100,
             'fragment': True},
            {'path': 'b', 'type': 'file', 'data': b'B' * 200,
             'fragment': True},
            {'path': 'c', 'type': 'file', 'data': b'C' * 5000,
             'fragment': True},
        ]
        img, meta, files, _ = roundtrip(tree, 'le', 'gzip')
        assert img.stats['fragment_slices'] == 3, img.stats
        assert len(img._frag_cache) >= 1

    def c_escaping_links():
        with tempfile.TemporaryDirectory(prefix='sqfs-selftest-') as td:
            p = os.path.join(td, 'i.sqsh')
            open(p, 'wb').write(_build_image(_selftest_tree(), endian='le', comp='gzip'))
            img, rows, non, meta = _read_image(p)
            assert meta['escaping_symlinks'] == 1, meta
            assert meta['in_tree_symlinks'] == 3, meta

    def c_bad_magic():
        with tempfile.TemporaryDirectory(prefix='sqfs-selftest-') as td:
            p = os.path.join(td, 'i.bin')
            open(p, 'wb').write(b'not a squashfs image' * 10)
            try:
                SquashFS(p)
            except SqfsError:
                return
            raise AssertionError('bad magic accepted')

    def c_unsupported_compression():
        with tempfile.TemporaryDirectory(prefix='sqfs-selftest-') as td:
            p = os.path.join(td, 'i.sqsh')
            img = bytearray(_build_image(_selftest_tree(), endian='le', comp='gzip'))
            struct.pack_into('<H', img, 20, 9)   # compression id
            open(p, 'wb').write(img)
            try:
                SquashFS(p)
            except SqfsError:
                return
            raise AssertionError('compression id 9 accepted')

    def c_truncated():
        with tempfile.TemporaryDirectory(prefix='sqfs-selftest-') as td:
            p = os.path.join(td, 'i.sqsh')
            img = _build_image(_selftest_tree(), endian='le', comp='gzip')
            open(p, 'wb').write(img[:60])
            try:
                SquashFS(p)
            except SqfsError:
                return
            raise AssertionError('truncated image accepted')

    case('le-gzip-basic', c_le_gzip)
    case('be-gzip-basic', c_be_gzip)
    case('avm-gzip-marker', c_avm_gzip)
    case('avm-xz', c_avm_xz)
    case('avm-raw-lzma2-id2', c_avm_lzma2)
    case('auto-standard-be', c_auto_standard_be)
    case('auto-avm', c_auto_avm)
    case('extended-inodes', c_extended)
    case('fragments-offsets', c_fragments_offsets)
    case('escaping-links', c_escaping_links)
    case('bad-magic', c_bad_magic)
    case('unsupported-compression', c_unsupported_compression)
    case('truncated', c_truncated)

    bad = 0
    for i, (name, ok, detail) in enumerate(results, start=1):
        if ok:
            print('ok %d - %s' % (i, name))
        else:
            bad += 1
            print('not ok %d - %s: %s' % (i, name, detail))
    print('%d/%d passed' % (len(results) - bad, len(results)))
    return 0 if bad == 0 else 1


def main(argv):
    ap = argparse.ArgumentParser(
        description='Independent SquashFS 4.0 oracle reader (LE, standard BE '
                    'and AVM layout).')
    ap.add_argument('image', nargs='?', help='SquashFS image')
    ap.add_argument('--layout', choices=('auto', 'le', 'be', 'avm'),
                    default='auto',
                    help='field layout; auto decides big-endian metadata '
                         'header endianness (default: auto)')
    ap.add_argument('--files', metavar='OUT.tsv',
                    help='regular-file TSV (relpath, sha256, size)')
    ap.add_argument('--nonregular', metavar='OUT.tsv',
                    help='non-regular TSV (relpath, kind, detail)')
    ap.add_argument('--inspect', action='store_true',
                    help='print a JSON superblock/layout/coverage summary')
    ap.add_argument('--selftest', action='store_true',
                    help='build and read self-contained images; no external '
                         'tool')
    args = ap.parse_args(argv)

    if args.selftest:
        return run_selftest()
    if not args.image or not args.files:
        ap.error('IMAGE and --files are required (or --selftest)')

    try:
        img = SquashFS(args.image, layout=args.layout)
        file_rows, nonregular, meta = collect(img)
        write_tsv(args.files, file_rows)
        if args.nonregular:
            write_tsv(args.nonregular, nonregular)
    except SqfsError as exc:
        print('sqfs-list: %s' % exc, file=sys.stderr)
        return 2
    for warning in img.warnings:
        print('sqfs-list: warning: %s' % warning, file=sys.stderr)
    if args.inspect:
        json.dump(meta, sys.stdout, indent=1, sort_keys=True)
        sys.stdout.write('\n')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
