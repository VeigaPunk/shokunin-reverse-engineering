#!/usr/bin/env python3
"""sqfs-list.py -- independent SquashFS 4.0 oracle reader (stdlib only).

Reads a SquashFS 4.0 image of either endianness -- little-endian magic
``hsqs`` or big-endian magic ``sqsh`` -- with gzip (id 1) or LZMA/XZ (ids 2
and 4) compression, and writes two TSV tables:

  --files OUT     regular files:  <relative path>\t<sha256>\t<size>
  --symlinks OUT  symlinks:       <relative path>\t<target>\t<in-tree|escaping>

Relative paths are POSIX paths from the image root, with no leading ``./``.
Symlinks are classified by resolving the target POSIX-style against the
link's own directory, with the image root as ``/``, and the class records what
unblob 26.6.4 does with the link (unblob/extractor.py:50-95 ``fix_symlink``:
``target.lstrip('/')`` for an absolute target, then ``is_safe_path(outdir,
target)``):

  in-tree    the target stays inside the root, so unblob keeps the link as
             metadata (REA 6.5.0 then reports one unpublished-entry gap).
             A symlink loop (self or mutual) is also in-tree: measured, the
             bundled Python 3.13.16 returns the unresolved path from
             ``Path.resolve()`` instead of raising, so unblob keeps it.
  escaping   the target climbs above the root, so unblob removes the link
             with ``MaliciousSymlinkRemoved`` and no gap is recorded.  An
             empty target is removed too, but silently (no report), so it is
             also escaping.

``--inspect`` reports the reason counts under ``symlink_reasons``.

Fragments and sparse data blocks are supported.  Compression ids 3 (lzo),
5 (lz4) and 6 (zstd) are refused with exit 2.

Usage:
  python3 -I -B sqfs-list.py IMAGE --files OUT.tsv --symlinks OUT.tsv [--inspect]

Exit: 0 ok, 2 unreadable or unsupported image (message on stderr).

On-disk layout sources -- Linux v6.12, fetched 2026-10-26 from
git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git (``?h=v6.12``):

  fs/squashfs/squashfs_fs.h
    :19    SQUASHFS_METADATA_SIZE = 8192
    :33    SQUASHFS_NAME_LEN = 256
    :36    SQUASHFS_DIR_COUNT = 256 (max dir header count + 1)
    :38    SQUASHFS_INVALID_FRAG = 0xffffffff
    :78-92 inode type ids (DIR 1, REG 2, SYMLINK 3, LDIR 8, LREG 9,
           LSYMLINK 10, LSOCKET 14)
    :106-118 SQUASHFS_COMPRESSED_BIT 1<<15 (metadata),
             SQUASHFS_COMPRESSED_BIT_BLOCK 1<<24 (data)
    :130-136 SQUASHFS_INODE_BLK(A) = A >> 16 (byte offset from the table
             start, not a block index), SQUASHFS_INODE_OFFSET(A) = A & 0xffff
    :233-238 compression ids (ZLIB 1, LZMA 2, LZO 3, XZ 4, LZ4 5, ZSTD 6)
    :240-260 squashfs_super_block (96 bytes, field order used below)
    :269-276 squashfs_base_inode (16 bytes)
    :322-332 squashfs_symlink_inode
    :334-346 squashfs_reg_inode
    :348-363 squashfs_lreg_inode
    :365-377 squashfs_dir_inode
    :379-394 squashfs_ldir_inode
    :409-415 squashfs_dir_entry
    :417-421 squashfs_dir_header
    :423-427 squashfs_fragment_entry
  fs/squashfs/dir.c:52,118,150-195  directory body: i_size bytes, of which
             the first 3 are the invented "."/".." f_pos; each header carries
             count+1 entries with a per-entry inode ref
             (start_block << 16 | offset) and a signed inode-number delta.
  fs/squashfs/inode.c:175-199,273-302 lreg and fragment-anchored files, and
             the symlink/lsymlink inodes (lsymlink stores an extra __le32
             xattr after the target bytes).
  fs/squashfs/file.c:615-616 a zero block-list entry is a sparse block
             (``if (bsize == 0)`` -> squashfs_readpage_sparse).
  fs/squashfs/fragment.c:38-60 fragment lookup: entry index in the u64
             index table, page offset inside the 8192-byte metadata page,
             entry = { __le64 start_block, __le32 size, __le32 unused }.
  fs/squashfs/block.c:271-280 data block: bit 1<<24 means stored
             uncompressed, the remaining bits are the on-disk size.
"""

import argparse
import hashlib
import json
import lzma
import struct
import sys
import zlib

META_MAX = 8192
NAME_MAX_ = 256          # SQUASHFS_NAME_LEN (max byte length of a name)
DIR_COUNT_MAX = 256      # SQUASHFS_DIR_COUNT (count + 1)
INVALID_FRAG = 0xFFFFFFFF
INVALID64 = 0xFFFFFFFFFFFFFFFF
BLOCK_UNCOMPRESSED = 1 << 24
META_UNCOMPRESSED = 1 << 15
META_ENDIAN = 'auto'     # 'auto' | 'le' | 'be': metadata block-length headers
MAX_SYMLINK_HOPS = 40    # POSIX ELOOP

TYPE_DIR, TYPE_FILE, TYPE_SYMLINK = 1, 2, 3
TYPE_LDIR, TYPE_LREG, TYPE_LSYMLINK = 8, 9, 10
BASIC_TYPE = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7,
              8: 1, 9: 2, 10: 3, 11: 4, 12: 5, 13: 6, 14: 7}
SPECIAL_TYPES = (4, 5, 6, 7, 11, 12, 13, 14)

SB_FMT = 'IIIIIHHHHHHQQQQQQQQ'
SB_FIELDS = ('magic', 'inodes', 'mkfs_time', 'block_size', 'fragments',
             'compression', 'block_log', 'flags', 'no_ids', 's_major',
             's_minor', 'root_inode', 'bytes_used', 'id_table_start',
             'xattr_id_table_start', 'inode_table_start',
             'directory_table_start', 'fragment_table_start',
             'lookup_table_start')


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
    """Sequential reader over the decompressed metadata block chain."""

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


class SquashFS:
    def __init__(self, path):
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
                      'compressed_metadata_blocks': 0,
                      'raw_metadata_blocks': 0}
        self._parse_super()

    # -- primitive reads ---------------------------------------------------
    def _need(self, off, n, what):
        if off < 0 or n < 0 or off + n > len(self.buf):
            raise SqfsError('%s out of bounds: offset %d length %d, image %d '
                            'bytes' % (what, off, n, len(self.buf)))

    def take(self, off, n, what):
        self._need(off, n, what)
        return self.buf[off:off + n]

    # -- superblock --------------------------------------------------------
    def _parse_super(self):
        if len(self.buf) < 96:
            raise SqfsError('image is %d bytes, shorter than a superblock'
                            % len(self.buf))
        magic = self.buf[:4]
        if magic == b'hsqs':
            self.e, self.endian = '<', 'little'
        elif magic == b'sqsh':
            self.e, self.endian = '>', 'big'
        else:
            raise SqfsError('bad magic %r: not a SquashFS image' % (magic,))
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
        self.meta_e = self._detect_meta_endian()
        self._decompress = self._make_decompressor()

    # AVM layout (Freetz tools/make/squashfs4-host-be/AVM-BE-format.txt): the
    # superblock and every on-disk structure stay big-endian, but each
    # metadata block length header is little-endian.  The probe walks the
    # inode-table metadata chain from inode_table_start and asks which
    # 2-byte header reading lands exactly on directory_table_start; that
    # identity is exact for any image whose inode metadata spans whole
    # blocks, and it never consults mkfs_time.
    def _meta_chain_ok(self, e):
        pos = self.inode_table_start
        limit = self.directory_table_start
        for _ in range(1 << 20):
            if pos == limit:
                return True
            if pos > limit:
                return False
            try:
                raw = struct.unpack_from(e + 'H', self.buf, pos)[0]
            except struct.error:
                return False
            size = raw & ~META_UNCOMPRESSED
            if size == 0 or pos + 2 + size > limit:
                return False
            pos += 2 + size
        return False

    def _detect_meta_endian(self):
        if not self.endian == 'big':
            return self.e
        le_ok = self._meta_chain_ok('<')
        be_ok = self._meta_chain_ok('>')
        marker = self.mkfs_time == self.bytes_used
        if META_ENDIAN in ('le', 'be'):
            return '<' if META_ENDIAN == 'le' else '>'
        if le_ok and not be_ok:
            return '<'
        if be_ok and not le_ok:
            return '>'
        if le_ok and be_ok:
            return '<' if marker else '>'
        raise SqfsError('neither big- nor little-endian metadata headers '
                        'walk from inode_table_start %d to '
                        'directory_table_start %d'
                        % (self.inode_table_start, self.directory_table_start))

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
            # Id 2 is legacy LZMA and id 4 is XZ.  A raw LZMA2 stream is
            # tried as well: tools/round-37/gen-squashfs.py writes xz data
            # (raw LZMA2, dict_size = block_size) under id 2.
            def d_lzma(raw):
                errors = []
                for fmt, filters in (
                        (lzma.FORMAT_AUTO, None),
                        (lzma.FORMAT_XZ, None),
                        (lzma.FORMAT_ALONE, None),
                        (lzma.FORMAT_RAW,
                         [{'id': lzma.FILTER_LZMA2, 'dict_size': bs}])):
                    try:
                        if filters is None:
                            return lzma.decompress(raw, format=fmt)
                        return lzma.decompress(raw, format=fmt,
                                               filters=filters)
                    except lzma.LZMAError as exc:
                        errors.append('%s: %s' % (fmt, exc))
                raise SqfsError('lzma: no container decoded (%s)'
                                % '; '.join(errors[:2]))
            return d_lzma
        raise SqfsError('unsupported compression id %d (supported: 1 gzip, '
                        '2 lzma, 4 xz)' % comp)

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
        raw = struct.unpack_from(self.meta_e + 'H', self.buf, pos)[0]
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
        node['mode'] = st.u16()
        node['uid'] = st.u16()
        node['gid'] = st.u16()
        node['mtime'] = st.u32()
        node['inode_number'] = st.u32()
        if typ == TYPE_DIR:
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
        elif typ == TYPE_FILE:
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
        elif typ in SPECIAL_TYPES:
            pass
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
            else:
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
        specials = []
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
            entries = list(self.dir_entries(node))
            for name, etype, ref in entries:
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
                    stack.append((child_path, child))
                elif child['type'] in (TYPE_FILE, TYPE_LREG):
                    kinds[child_path] = 'file'
                    files[child_path] = child
                elif child['type'] in (TYPE_SYMLINK, TYPE_LSYMLINK):
                    kinds[child_path] = 'link'
                    links[child_path] = child['target']
                else:
                    kinds[child_path] = 'special'
                    specials.append(child_path)
        return files, links, kinds, specials


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
    rows.sort(key=lambda r: r[0].encode('utf-8', 'surrogateescape'))
    try:
        with open(path, 'w', encoding='utf-8', errors='surrogateescape',
                  newline='\n') as fh:
            for row in rows:
                fh.write('\t'.join(row) + '\n')
    except OSError as exc:
        raise SqfsError('cannot write %s: %s' % (path, exc))


def collect(img):
    files, links, kinds, specials = img.walk()
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
    link_rows = []
    reasons = {}
    for path, target in links.items():
        cls, why = classify_link(path, target, kinds, links)
        link_rows.append((path, target, cls))
        reasons[why] = reasons.get(why, 0) + 1
    meta = {
        'image': img.path,
        'endian': img.endian,
        'meta_endian': 'little' if img.meta_e == '<' else 'big',
        'avm_marker': img.mkfs_time == img.bytes_used,
        'size': len(img.buf),
        'superblock': {k: getattr(img, k) for k in SB_FIELDS},
        'compression': {1: 'gzip', 2: 'lzma', 4: 'xz'}.get(img.compression,
                                                           img.compression),
        'regular_files': len(file_rows),
        'symlinks': len(link_rows),
        'special_files': len(specials),
        'in_tree_symlinks': sum(1 for r in link_rows if r[2] == 'in-tree'),
        'escaping_symlinks': sum(1 for r in link_rows if r[2] == 'escaping'),
        'symlink_reasons': reasons,
        'decode_paths': img.stats,
        'warnings': img.warnings,
    }
    return file_rows, link_rows, meta


def main(argv):
    ap = argparse.ArgumentParser(
        description='Independent SquashFS 4.0 oracle reader (LE and BE).')
    ap.add_argument('image')
    ap.add_argument('--files', required=True, metavar='OUT.tsv')
    ap.add_argument('--symlinks', required=True, metavar='OUT.tsv')
    ap.add_argument('--inspect', action='store_true',
                    help='print a JSON superblock/coverage summary on stdout')
    ap.add_argument('--meta-endian', choices=('auto', 'le', 'be'),
                    default='auto',
                    help='metadata block-length header endianness '
                         '(default: auto, detect by the inode-table walk)')
    args = ap.parse_args(argv)
    global META_ENDIAN
    META_ENDIAN = args.meta_endian

    try:
        img = SquashFS(args.image)
        file_rows, link_rows, meta = collect(img)
        write_tsv(args.files, file_rows)
        write_tsv(args.symlinks, link_rows)
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
