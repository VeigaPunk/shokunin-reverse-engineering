#!/usr/bin/env python3
"""Minimal deterministic SquashFS v4 writer (LE / BE / AVM-BE / AVM-genuine).

Modes (`--endian`):
  le            little-endian image (`hsqs`), standard layout.
  be            big-endian image (`sqsh`), standard layout.
  avm           big-endian body with `mkfs_time = bytes_used` (the AVM marker)
                and **standard BE** 2-byte metadata block-length headers.  This
                is the round-39 "marker-only" transform, NOT the AVM layout.
  avm-genuine   the genuine AVM layout: big-endian superblock, inode,
                directory, fragment-entry and data-block-size fields, but the
                2-byte metadata block-length header at the start of *every*
                metadata block (inode table, directory table, id table, and any
                fragment/xattr/lookup metadata block) is little-endian.
                `mkfs_time = bytes_used`.

Genuine-layout ground truth measured on
/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/avm-be.squashfs
(4096 B, sha256 c7f74691b3e8d76777322f568cea640e08b7d52c994b6bc53a01388faed32d32)
with probe-avm-layout.py in this directory:
  * superblock: inodes 5, mkfs_time 365 == bytes_used 365, block_size 65536,
    compression 4 (xz), root_inode 128, inode_table 121, dir_table 239,
    frag_table 343 (the fragment lookup u64 list; the fragment metadata block
    sits at 325), id_table 357 (the id lookup u64 list; the id metadata block
    sits at 351); every one of those fields decodes sanely only big-endian;
  * metadata headers: 121 -> `74 00` = 0x0074 LE = 116 (BE would be 29696);
    239 -> `54 80` = 0x8054 LE = 84 stored uncompressed (BE 21632);
    325 -> `10 80` = 0x8010 LE = 16 stored uncompressed (BE 2064);
    351 -> `04 80` = 0x8004 LE = 4 stored uncompressed (BE 1152);
  * inode fields (root dir inode: type 1, mode 0755, inode_number 5, nlink 2,
    file_size 87, parent 6; reg inodes: type 2, size 6/7/7/5, start_block 0,
    fragment index 0, fragment offset 0/6/13/20) decode big-endian;
  * directory header/entries decode big-endian (count 3, start 0, inode 1;
    four `appleN.txt` entries, type 2, name_size 9, byte offsets 0/32/64/96);
  * fragment entry at 327: start_block 96 BE, size 0x01000019 BE (25 bytes with
    the 1<<24 stored-uncompressed bit);
  * lookup tables (fragment index at 343 = 325, id index at 357 = 351) are
    big-endian u64s.
and confirmed behaviourally: `sasquatch-v4be -f -d OUT fixture` extracts all
four files (exit 0) while `sasquatch-v4be -be -f -d OUT fixture` fails
(`read_id_table: failed to read id table block`, FATAL ERROR, exit 1) -- i.e.
4.5.1 reads the AVM layout exactly with the no-`-be` argv that unblob 26.6.4
`handlers/filesystem/squashfs.py:41-52` selects when `mkfs_time == bytes_used`.

Todos: no fragments (frag_count 0, fragment_table_start -1), no xattrs, no
export/lookup table, no sparse blocks, no device nodes.  An empty directory is
stored as zero entries with file_size 3 and extracts correctly (measured).
Every metadata block is stored uncompressed (length header has the 0x8000 bit);
the genuine vendor images compress metadata blocks, which this writer does not
emit -- the LE length field is exercised, the compressed-length path is not.

DERIVED: copy of tools/round-37/gen-squashfs.py (sha256
1c7c5e88324d64ad5935e81f205a609a8361466e5aea9ba461575f4e01ba8dd5) with two fixes.
(1) round-39 xz fix (from .ufo/waves/round-39/w1/R39C2HeldoutGen.md section 3): xz blocks
are complete .xz containers with a CRC32 check and the superblock compression id is 4
(stock wrote bare LZMA2 under id 2, which sasquatch 4.5.1 cannot decode).
(2)
the directory-entry name_size field counts UTF-8 BYTES, not str characters.
Stock rejects every non-ASCII name: `len(name) - 1` is a character count while
`name.encode()` writes the UTF-8 bytes, so unsquashfs 4.5.1 dies with
`get_metadata: failed to read block` on any directory holding one. Byte-identical
output to stock for every ASCII tree (K1/K2 pins rebuild to 1cfb6c33../403cb0a8..).

ROUND 40: adds the `avm-genuine` mode and `--selftest`; `le`, `be` and `avm`
output is byte-identical to the round-39 writer for every tree whose inode and
directory tables fit in ONE metadata block (verified by --selftest against
tools/round-39/gen-squashfs.py: 24 sha256-equal pairs over four such trees, both
compressions). Two multi-block bugs of the round-39 writer are fixed, so output
for a table spanning several metadata blocks deliberately differs:

  * inode/directory references now carry the table-relative BYTE OFFSET of the
    metadata block (SQUASHFS_INODE_BLK(A) = A >> 16), not the block index (only
    equal while there is one block). Measured on a 400-file tree: the round-39
    writer's image extracts 0/400 files (`sasquatch-v4be` exit 1), this writer's
    400/400.
  * a metadata record no longer straddles two metadata blocks: a block ends
    short instead (mksquashfs does the same; sasquatch-v4be 4.5.1 misparses a
    straddling inode and dies with `uid index in inode too large (uid: 65535)`),
    and a directory body emits one header per run of entries whose inodes share
    an inode-table block, since the header's start_block is per header.

The claims' C1 carriers are small trees (single metadata block in both tables),
so the byte-identity holds for them; the multi-block fix is what makes
`avm-genuine` safe to use on a larger development tree.
"""
import argparse
import hashlib
import os
import random
import shutil
import struct
import subprocess
import sys
import tempfile
import zlib
import lzma

MAGIC = {'le': b'hsqs', 'be': b'sqsh', 'avm': b'sqsh', 'avm-genuine': b'sqsh'}
COMP = {'gzip': 1, 'xz': 4}
TYPE_DIR = 1
TYPE_FILE = 2
TYPE_SYMLINK = 3
UNCOMPRESSED = 0x8000
META_MAX = 8192
MKFS_TIME = 1700000000
UID = 1000
MODES = ('le', 'be', 'avm', 'avm-genuine')
AVM_MARKER_MODES = ('avm', 'avm-genuine')
# modes whose 2-byte metadata block-length headers are little-endian
LE_HEADER_MODES = ('le', 'avm-genuine')


def field_endian(mode):
    """Endianness of the superblock/inode/directory/fragment/lookup fields."""
    return 'le' if mode == 'le' else 'be'


def header_endian(mode):
    """Endianness of the 2-byte metadata block-length header."""
    return 'le' if mode in LE_HEADER_MODES else 'be'


def pack(e, fmt, *vals):
    return struct.pack(('<' if e == 'le' else '>') + fmt, *vals)


def comp_bytes(kind, data, block_size=4096):
    if kind == 'gzip':
        c = zlib.compressobj(9, zlib.DEFLATED, 15)
        return c.compress(data) + c.flush()
    return lzma.compress(data, format=lzma.FORMAT_XZ, check=lzma.CHECK_CRC32,
                         filters=[{'id': lzma.FILTER_LZMA2, 'preset': 6}])


class MetaWriter:
    """Collects metadata blocks.

    ``e`` is the field endianness of the block *bodies* (always 'be' or 'le');
    ``hdr_e`` is the endianness of the 2-byte block-length header, which the
    genuine AVM layout stores little-endian even inside a big-endian image.
    """

    def __init__(self, e, hdr_e=None):
        self.e = e
        self.hdr_e = hdr_e or e
        self.blocks = []
        self.cur = bytearray()
        # bytes of fully written blocks (headers included): the table-relative
        # byte offset of every subsequent block starts here
        self.settled = 0

    def meta_header(self, size):
        return pack(self.hdr_e, 'H', size | UNCOMPRESSED)

    def append(self, data):
        # squashfs inode/directory references carry a table-relative *byte
        # offset* of the metadata block (SQUASHFS_INODE_BLK(A) = A >> 16), not a
        # block index.  The round-39 writer returned len(self.blocks), which is
        # only equal to the byte offset while the table has a single block --
        # multi-block tables got refs that point into the middle of block 0 and
        # extraction failed (measured: a 400-file tree, sasquatch-v4be exit 1,
        # 0 files; see --selftest).
        #
        # A metadata record must also not straddle two metadata blocks: a block
        # ends early (shorter than META_MAX) rather than splitting a record.
        # mksquashfs does the same; sasquatch-v4be 4.5.1 misparses a straddling
        # inode and dies with `uid index in inode too large (uid: 65535)`.
        if len(data) > META_MAX:
            raise ValueError('metadata record of %d bytes exceeds the %d-byte '
                             'metadata block size' % (len(data), META_MAX))
        if self.cur and len(self.cur) + len(data) > META_MAX:
            self._flush()
        off_block, off_within = self.settled, len(self.cur)
        self.cur += data
        return off_block, off_within

    def _flush(self):
        self.blocks.append((self.meta_header(len(self.cur)), bytes(self.cur)))
        self.settled += 2 + len(self.cur)
        self.cur = bytearray()

    def settle(self):
        if self.cur or not self.blocks:
            self._flush()
        return self.blocks


def build_image(tree, out, mode, comp, block_size=4096):
    e = field_endian(mode)
    hdr_e = header_endian(mode)
    dirs, files, links = [], [], []
    for root, dnames, fnames in os.walk(tree):
        dnames.sort(); fnames.sort()
        rel = os.path.relpath(root, tree)
        dirs.append('' if rel == '.' else rel)
        # A symlink whose target is a directory is listed by os.walk in
        # `dnames`, not `fnames`.  It must be stored as a symlink inode and must
        # not be descended into (or counted as a directory).
        for dn in list(dnames):
            p = os.path.join(root, dn)
            if os.path.islink(p):
                dnames.remove(dn)
                links.append((os.path.relpath(p, tree), os.readlink(p)))
        for fn in fnames:
            p = os.path.join(root, fn)
            r = os.path.relpath(p, tree)
            if os.path.islink(p):
                links.append((r, os.readlink(p)))
            else:
                data = open(p, 'rb').read()
                files.append((r, len(data), data))
    inode_no = {}
    for d in sorted(dirs, key=lambda x: (x.count('/'), x)):
        inode_no[('D', d)] = len(inode_no) + 1
    for r, _, _ in sorted(files):
        inode_no[('F', r)] = len(inode_no) + 1
    for r, _ in sorted(links):
        inode_no[('L', r)] = len(inode_no) + 1
    n_total = len(inode_no)

    data = bytearray()
    file_start, file_blocks = {}, {}
    for r, sz, content in files:
        off = 96 + len(data)
        file_start[r] = off
        sizes = []
        for i in range(0, len(content), block_size):
            chunk = content[i:i+block_size]
            c = comp_bytes(comp, chunk, block_size)
            raw = len(c) >= len(chunk)
            if raw:
                c = chunk
            data += c
            sizes.append(len(c) | (0x01000000 if raw else 0))
        file_blocks[r] = sizes

    mw = MetaWriter(e, hdr_e)
    inode_ref = {}

    def key_of(kind, path):
        return (kind, path)

    for r, sz, content in files:
        base = (pack(e, 'H', TYPE_FILE) + pack(e, 'H', 0o100644) +
                pack(e, 'H', 0) + pack(e, 'H', 0) +
                pack(e, 'I', MKFS_TIME) + pack(e, 'I', inode_no[('F', r)]))
        reg = (base + pack(e, 'I', file_start[r]) + pack(e, 'I', 0xFFFFFFFF) +
               pack(e, 'I', 0) + pack(e, 'I', sz) +
               b''.join(pack(e, 'I', s) for s in file_blocks[r]))
        inode_ref[key_of('F', r)] = mw.append(reg)
    for r, target in links:
        tb = target.encode()
        base = (pack(e, 'H', TYPE_SYMLINK) + pack(e, 'H', 0o120777) +
                pack(e, 'H', 0) + pack(e, 'H', 0) +
                pack(e, 'I', MKFS_TIME) + pack(e, 'I', inode_no[('L', r)]))
        sym = base + pack(e, 'I', 1) + pack(e, 'I', len(tb)) + tb
        inode_ref[key_of('L', r)] = mw.append(sym)

    dir_meta = MetaWriter(e, hdr_e)
    dir_ref = {}
    nonroot = sorted((d for d in dirs if d), key=lambda x: (-x.count('/'), x))
    for d in nonroot + ['']:
        children = []
        for sub in dirs:
            if sub != '' and os.path.dirname(sub) == d:
                children.append((os.path.basename(sub), TYPE_DIR,
                                 inode_no[('D', sub)]))
        for r, _, _ in files:
            if os.path.dirname(r) == d:
                children.append((os.path.basename(r), TYPE_FILE,
                                 inode_no[('F', r)]))
        for r, _ in links:
            if os.path.dirname(r) == d:
                children.append((os.path.basename(r), TYPE_SYMLINK,
                                 inode_no[('L', r)]))
        children.sort(key=lambda c: c[0])
        # Resolve each child's inode reference.  A directory header carries the
        # inode-table *block byte offset* shared by its entries (SQUASHFS_INODE_
        # BLK = ref >> 16), so entries whose inodes sit in different metadata
        # blocks need different headers.  Entries stay in name order; one header
        # is emitted per maximal run of same-block children.
        resolved = []
        for name, typ, ino in children:
            kind = 'D' if typ == TYPE_DIR else ('F' if typ == TYPE_FILE else 'L')
            child_path = name if d == '' else os.path.join(d, name)
            blk, off = inode_ref[key_of(kind, child_path)]
            resolved.append((name, typ, ino, blk, off))
        tbl = bytearray()
        i = 0
        while i < len(resolved):
            blk = resolved[i][3]
            j = i
            while j < len(resolved) and resolved[j][3] == blk:
                j += 1
            run = resolved[i:j]
            first_ino = run[0][2]
            if any(abs(c[2] - first_ino) > 0x7FFF for c in run):
                raise ValueError('inode delta exceeds the signed 16-bit field '
                                 'in %r' % d)
            tbl += (pack(e, 'I', len(run) - 1) + pack(e, 'I', blk) +
                    pack(e, 'I', first_ino))
            for name, typ, ino, _blk, off in run:
                nb = name.encode()
                tbl += (pack(e, 'H', off) + pack(e, 'h', ino - first_ino) +
                        pack(e, 'H', typ) + pack(e, 'H', len(nb) - 1) + nb)
            i = j
        db, do = dir_meta.append(bytes(tbl))
        dir_ref[d] = (db, do, len(tbl) + 3)
        parent = 1 if d == '' else inode_no[('D', os.path.dirname(d))]
        subdirs = sum(1 for c in children if c[1] == TYPE_DIR)
        base = (pack(e, 'H', TYPE_DIR) + pack(e, 'H', 0o40755) +
                pack(e, 'H', 0) + pack(e, 'H', 0) +
                pack(e, 'I', MKFS_TIME) + pack(e, 'I', inode_no[('D', d)]))
        dir_ino = (base + pack(e, 'I', db) + pack(e, 'I', subdirs + 2) +
                   pack(e, 'H', dir_ref[d][2]) + pack(e, 'H', do) +
                   pack(e, 'I', parent))
        inode_ref[key_of('D', d)] = mw.append(dir_ino)

    root_ref = inode_ref[key_of('D', '')]
    inode_blocks = mw.settle()
    dir_blocks = dir_meta.settle()

    inode_table_start = 96 + len(data)
    dir_table_start = inode_table_start + sum(len(h) + len(p) for h, p in inode_blocks)
    id_mw = MetaWriter(e, hdr_e)
    id_mw.append(pack(e, 'I', UID))
    id_blocks = id_mw.settle()
    id_meta_start = dir_table_start + sum(len(h) + len(p) for h, p in dir_blocks)
    id_table_start = id_meta_start + sum(len(h) + len(p) for h, p in id_blocks)
    bytes_used = id_table_start + 8
    mkfs = bytes_used if mode in AVM_MARKER_MODES else MKFS_TIME

    out_ = bytearray()
    out_ += MAGIC[mode]
    out_ += pack(e, 'I', n_total)
    out_ += pack(e, 'I', mkfs)
    out_ += pack(e, 'I', block_size)
    out_ += pack(e, 'I', 0)
    out_ += pack(e, 'H', COMP[comp])
    out_ += pack(e, 'H', block_size.bit_length() - 1)
    out_ += pack(e, 'H', 0)
    out_ += pack(e, 'H', 1)
    out_ += pack(e, 'H', 4)
    out_ += pack(e, 'H', 0)
    rb, ro = root_ref
    out_ += pack(e, 'Q', (rb << 16) | ro)
    out_ += pack(e, 'Q', bytes_used)
    out_ += pack(e, 'Q', id_table_start)
    out_ += pack(e, 'Q', 0xFFFFFFFFFFFFFFFF)
    out_ += pack(e, 'Q', inode_table_start)
    out_ += pack(e, 'Q', dir_table_start)
    out_ += pack(e, 'Q', 0xFFFFFFFFFFFFFFFF)
    out_ += pack(e, 'Q', 0xFFFFFFFFFFFFFFFF)
    out_ += data
    for h, p in inode_blocks:
        out_ += h + p
    for h, p in dir_blocks:
        out_ += h + p
    for h, p in id_blocks:
        out_ += h + p
    out_ += pack(e, 'Q', id_meta_start)
    with open(out, 'wb') as f:
        f.write(bytes(out_))
    print('wrote', out, len(out_), 'bytes, inodes', n_total, 'mode', mode)
    return bytes(out_)


# ---------------------------------------------------------------- self-test ---

def _tree_specs():
    """Three deterministic development trees, built from a byte stream."""
    def stream(tag, n):
        out = b''
        ctr = 0
        while len(out) < n:
            out += hashlib.sha256(f'{tag}:{ctr}'.encode()).digest()
            ctr += 1
        return out[:n]

    return {
        'small': [
            ('bin/run', b'#!/bin/sh\nexec echo hi\n'),
            ('etc/a.txt', b'alpha\n'),
            ('docs/deep/blob.bin', stream('blob', 7000)),
            ('docs/deep/zeros.bin', b'\0' * 4000),
            ('empty.txt', b''),
        ],
        'multiblock': [
            ('data/rand.bin', stream('rand', 20000)),
            ('data/mixed.bin', b'\0' * 9000 + stream('mix', 5000) + b'\1' * 9000),
            ('data/one.bin', b'x'),
        ],
        'many': [(f'k{i // 10}/file{i:03d}.txt',
                  b'line %d\n' % i + (b'payload' * (i % 7)))
                 for i in range(60)] + [('k5/h\u00e9llo.txt', b'accented\n')],
        # enough inodes and directory entries to cross several 8192-byte
        # metadata blocks: exercises the LE block-length header on every block,
        # not only the first.
        'bulk': [(f'd{i % 4}/f{i:04d}.txt', b'v%d\n' % (i % 10))
                 for i in range(400)],
        # symlink inodes and directory entries type 3 -- in-tree, escaping,
        # absolute and directory targets.  unblob keeps in-tree links and
        # removes escaping ones, so this tree exercises both.
        'links': [
            ('bin/real.sh', b'#!/bin/sh\necho real\n'),
            ('bin/alias.sh', b'real.sh', 'symlink'),
            ('bin/up-two', b'../../etc/passwd', 'symlink'),
            ('bin/absolute', b'/etc/shadow', 'symlink'),
            ('bin/dirlink', b'../docs', 'symlink'),
            ('docs/readme.txt', b'readme\n'),
        ],
    }


def _populate(tree_dir, entries):
    for ent in entries:
        rel, content = ent[0], ent[1]
        p = os.path.join(tree_dir, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if len(ent) == 3 and ent[2] == 'symlink':
            os.symlink(os.fsdecode(content), p)
        else:
            with open(p, 'wb') as f:
                f.write(content)


def _sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def _tree_files(tree_dir):
    got = {}
    for root, _dirs, fnames in os.walk(tree_dir):
        for fn in fnames:
            p = os.path.join(root, fn)
            if os.path.islink(p):
                continue
            got[os.path.relpath(p, tree_dir)] = _sha(p)
    return got


def _tree_links(tree_dir):
    got = {}
    for root, dirs, fnames in os.walk(tree_dir):
        # os.walk lists a symlink-to-directory in `dirs`, not `fnames`
        for fn in list(dirs) + list(fnames):
            p = os.path.join(root, fn)
            if os.path.islink(p):
                got[os.path.relpath(p, tree_dir)] = os.readlink(p)
    return got


def _block_starts(b, start, end, endian):
    out = []
    off = start
    while off < end:
        out.append(off)
        size = struct.unpack_from(('<' if endian == 'le' else '>') + 'H', b, off)[0] & 0x7FFF
        if size == 0:
            break
        off += 2 + size
    return out


def _walk_meta(b, start, end, endian):
    """Walk 2-byte block-length headers from `start` and return the byte
    offset reached, or None on a zero-length/overflowing header.  A table whose
    headers use `endian` ends exactly on the next table's start."""
    off = start
    while off < end:
        raw = struct.unpack_from(('<' if endian == 'le' else '>') + 'H', b, off)[0]
        size = raw & 0x7FFF
        if size == 0:
            return None
        off += 2 + size
    return off


def _run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def selftest(ref_writer=None, sasquatch='sasquatch-v4be', keep=False):
    A = os.path.dirname(os.path.abspath(__file__))
    reader = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(A))),
                          'tools', 'round-39', 'sqfs-list.py')
    if not os.path.exists(reader):
        reader = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-39/sqfs-list.py'
    if ref_writer is None:
        cand = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-39/gen-squashfs.py'
        ref_writer = cand if os.path.exists(cand) else None
    base = tempfile.mkdtemp(prefix='sqfs-selftest-', dir=os.environ.get('TMPDIR'))
    fails, passes = [], []

    def check(name, ok, detail):
        (passes if ok else fails).append(name)
        print(f'{"PASS" if ok else "FAIL"} {name}: {detail}')

    try:
        for tname, entries in _tree_specs().items():
            tree = os.path.join(base, 'tree-' + tname)
            os.makedirs(tree)
            _populate(tree, entries)
            want = _tree_files(tree)
            want_links = _tree_links(tree)
            for comp in ('gzip', 'xz'):
                img = os.path.join(base, f'{tname}-{comp}-avm-genuine.sqsh')
                build_image(tree, img, 'avm-genuine', comp)
                # 1. layout sanity: marker holds, header decodes LE (and not BE)
                b = open(img, 'rb').read()
                be = struct.unpack_from('>IIII', b, 4)
                bytes_used = struct.unpack_from('>Q', b, 40)[0]
                itab = struct.unpack_from('>Q', b, 64)[0]
                dtab = struct.unpack_from('>Q', b, 72)[0]
                lean = struct.unpack_from('<H', b, itab)[0] & 0x7FFF
                be_end = _walk_meta(b, itab, dtab, 'be')
                check(f'layout[{tname}/{comp}]',
                      b[:4] == b'sqsh' and be[1] == bytes_used and
                      _walk_meta(b, itab, dtab, 'le') == dtab and
                      be_end != dtab,
                      f'magic={b[:4]!r} mkfs={be[1]} bytes_used={bytes_used} '
                      f'inode_table={itab} first_LE_len={lean} '
                      f'LE_walk_end={_walk_meta(b, itab, dtab, "le")} '
                      f'(== dir_table {dtab}), BE_walk_end={be_end}')
                # 2. no -be extracts every file with equal sha256
                out = os.path.join(base, f'ex-{tname}-{comp}')
                r = _run([sasquatch, '-f', '-d', out, img], base)
                got = _tree_files(out) if os.path.isdir(out) else {}
                got_links = _tree_links(out) if os.path.isdir(out) else {}
                check(f'extract[{tname}/{comp}]',
                      r.returncode == 0 and got == want and got_links == want_links,
                      f'exit={r.returncode} files={len(got)}/{len(want)} '
                      f'links={len(got_links)}/{len(want_links)} '
                      f'missing={sorted(set(want) - set(got))[:3]} '
                      f'bad_links={sorted(k for k in want_links if got_links.get(k) != want_links[k])[:3]}')
                # 3. -be fails (exit != 0 or nothing extracted)
                out_be = os.path.join(base, f'exbe-{tname}-{comp}')
                rb = _run([sasquatch, '-be', '-f', '-d', out_be, img], base)
                got_be = _tree_files(out_be) if os.path.isdir(out_be) else {}
                check(f'-be-fails[{tname}/{comp}]',
                      rb.returncode != 0 and got_be != want,
                      f'exit={rb.returncode} files={len(got_be)} '
                      f'first_err={rb.stderr.strip().splitlines()[-1][:70] if rb.stderr.strip() else ""}')
                # 4. determinism
                img2 = img + '.2'
                build_image(tree, img2, 'avm-genuine', comp)
                check(f'deterministic[{tname}/{comp}]', _sha(img) == _sha(img2),
                      _sha(img))
                # 5. round-39 reader in BE mode refuses or misreads
                if os.path.exists(reader):
                    ft = os.path.join(base, 'r-files.tsv')
                    st = os.path.join(base, 'r-links.tsv')
                    rr = _run([sys.executable, '-I', '-B', reader, img,
                               '--files', ft, '--symlinks', st], base)
                    got_r = {}
                    if os.path.exists(ft):
                        for line in open(ft):
                            parts = line.rstrip('\n').split('\t')
                            if len(parts) >= 2:
                                got_r[parts[0]] = parts[1]
                    check(f'reader39-misreads[{tname}/{comp}]',
                          rr.returncode != 0 or got_r != want,
                          f'exit={rr.returncode} files={len(got_r)} '
                          f'first_err={rr.stderr.strip().splitlines()[-1][:70] if rr.stderr.strip() else ""}')
                # 6. round-39 writer byte-identity for le/be/avm on this tree.
                #    Only for single-metadata-block tables: the round-39 writer
                #    stores block *indices* as refs, which coincide with byte
                #    offsets only then; for a multi-block table this writer
                #    fixes that (deliberate difference, measured below).
                id_lookup = struct.unpack_from('>Q', b, 48)[0]
                id_meta = struct.unpack_from('>Q', b, id_lookup)[0]
                multi = (len(_block_starts(b, itab, dtab, 'le')) > 1 or
                         len(_block_starts(b, dtab, id_meta, 'le')) > 1)
                if comp == 'gzip' and ref_writer and os.path.exists(ref_writer):
                    for mode in ('le', 'be', 'avm'):
                        for comp2 in ('gzip', 'xz'):
                            a1 = os.path.join(base, f'ref-{mode}-{comp2}.img')
                            a2 = os.path.join(base, f'new-{mode}-{comp2}.img')
                            r1 = _run([sys.executable, '-I', '-B', ref_writer,
                                       tree, a1, '--endian', mode,
                                       '--comp', comp2], base)
                            build_image(tree, a2, mode, comp2)
                            has_dir_link = any(
                                os.path.isdir(os.path.join(tree, l))
                                for l in want_links)
                            if not multi and not has_dir_link:
                                check(f'byte-identical[{tname}/{mode}/{comp2}]',
                                      r1.returncode == 0 and _sha(a1) == _sha(a2),
                                      _sha(a2))
                            elif mode == 'be' and comp2 == 'gzip':
                                # the ref image is standard BE (headers BE):
                                # it must be read with -be
                                rx = os.path.join(base, 'ex-ref-' + tname)
                                rr = _run([sasquatch, '-be', '-f', '-d', rx, a1], base)
                                gotx = _tree_files(rx) if os.path.isdir(rx) else {}
                                gotxl = _tree_links(rx) if os.path.isdir(rx) else {}
                                if multi:
                                    check(f'round39-ref-multiblock-broken[{tname}]',
                                          rr.returncode != 0 and gotx != want,
                                          f'round-39 writer image extracts '
                                          f'{len(gotx)}/{len(want)} files, exit '
                                          f'{rr.returncode}; this writer: '
                                          f'{len(want)} (ref-encoding fix)')
                                else:
                                    missed = sorted(set(want_links) - set(gotxl))
                                    check(f'round39-ref-drops-dir-symlink[{tname}]',
                                          rr.returncode == 0 and bool(missed),
                                          f'round-39 writer drops {missed} '
                                          f'(os.walk lists it under dnames); '
                                          f'this writer stores it and sasquatch '
                                          f'extracts it')
        # 7. a marker-stripped way to show the marker is load-bearing: the same
        #    bytes with mkfs_time normalised must lose the no-`-be` argv's success
        #    (the extraction result is the same stream, so check the header is
        #    still LE while the marker flips -> not claimed here; instead show a
        #    standard-BE body is refused by noflag, the round-39 transform).
        tree = os.path.join(base, 'tree-small')
        std_be = os.path.join(base, 'std-be.sqsh')
        build_image(tree, std_be, 'be', 'gzip')
        std_out = os.path.join(base, 'ex-std-be')
        rs = _run([sasquatch, '-f', '-d', std_out, std_be], base)
        check('std-be-needs--be', rs.returncode != 0,
              f'exit={rs.returncode} (the AVM layout is different from this)')
    finally:
        if not keep:
            shutil.rmtree(base, ignore_errors=True)
        else:
            print('kept', base)
    print(f'\nselftest: {len(passes)} passed, {len(fails)} failed')
    if fails:
        print('failed:', ', '.join(fails))
        return 1
    return 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('tree', nargs='?')
    ap.add_argument('out', nargs='?')
    ap.add_argument('--endian', choices=MODES, default='le')
    ap.add_argument('--comp', choices=['gzip', 'xz'], default='gzip')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--ref-writer', default=None)
    ap.add_argument('--sasquatch', default='sasquatch-v4be')
    ap.add_argument('--keep', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest(a.ref_writer, a.sasquatch, a.keep))
    if not a.tree or not a.out:
        ap.error('tree and out are required unless --selftest is given')
    build_image(a.tree, a.out, a.endian, a.comp)
