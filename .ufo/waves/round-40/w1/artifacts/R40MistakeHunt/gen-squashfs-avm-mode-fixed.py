#!/usr/bin/env python3
"""Minimal deterministic SquashFS v4 writer (LE / BE / AVM-BE). Dev prototype.
Todos: no fragments, no xattrs, no export table, no sparse, no empty-dir
entries (dirs write one header+entries block).

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
"""
import argparse, os, struct, zlib, lzma

MAGIC = {'le': b'hsqs', 'be': b'sqsh', 'avm': b'sqsh'}
COMP = {'gzip': 1, 'xz': 4}
TYPE_DIR = 1
TYPE_FILE = 2
TYPE_SYMLINK = 3
UNCOMPRESSED = 0x8000
META_MAX = 8192
MKFS_TIME = 1700000000
UID = 1000


def pack(e, fmt, *vals):
    return struct.pack(('<' if e == 'le' else '>') + fmt, *vals)


def comp_bytes(kind, data, block_size=4096):
    if kind == 'gzip':
        c = zlib.compressobj(9, zlib.DEFLATED, 15)
        return c.compress(data) + c.flush()
    return lzma.compress(data, format=lzma.FORMAT_XZ, check=lzma.CHECK_CRC32,
                         filters=[{'id': lzma.FILTER_LZMA2, 'preset': 6}])


class MetaWriter:
    def __init__(self, e):
        self.e = e
        # The genuine AVM layout is a big-endian superblock with LITTLE-endian metadata
        # block-length headers; every other field stays big-endian. (R40MistakeHunt patch.)
        self.me = 'le' if e == 'avm' else e
        self.blocks = []
        self.cur = bytearray()

    def meta_header(self, size):
        return pack(self.me, 'H', size | UNCOMPRESSED)

    def append(self, data):
        off_block, off_within = len(self.blocks), len(self.cur)
        self.cur += data
        while len(self.cur) >= META_MAX:
            part = bytes(self.cur[:META_MAX])
            self.blocks.append((self.meta_header(META_MAX), part))
            self.cur = self.cur[META_MAX:]
        return off_block, off_within

    def settle(self):
        if self.cur or not self.blocks:
            self.blocks.append((self.meta_header(len(self.cur)), bytes(self.cur)))
            self.cur = bytearray()
        return self.blocks


def build_image(tree, out, e, comp, block_size=4096):
    dirs, files, links = [], [], []
    for root, dnames, fnames in os.walk(tree):
        dnames.sort(); fnames.sort()
        rel = os.path.relpath(root, tree)
        dirs.append('' if rel == '.' else rel)
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

    mw = MetaWriter(e)
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

    dir_meta = MetaWriter(e)
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
        tbl = bytearray()
        if children:
            first_ino = children[0][2]
            hdr = (pack(e, 'I', len(children) - 1) + pack(e, 'I', 0) +
                   pack(e, 'I', first_ino))
            tbl += hdr
            for name, typ, ino in children:
                kind = 'D' if typ == TYPE_DIR else ('F' if typ == TYPE_FILE else 'L')
                child_path = name if d == '' else os.path.join(d, name)
                b, o = inode_ref[key_of(kind, child_path)]
                nb = name.encode()
                entry = (pack(e, 'H', o) + pack(e, 'h', ino - first_ino) +
                         pack(e, 'H', typ) + pack(e, 'H', len(nb) - 1))
                tbl += entry + nb
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
    id_mw = MetaWriter(e)
    id_mw.append(pack(e, 'I', UID))
    id_blocks = id_mw.settle()
    id_meta_start = dir_table_start + sum(len(h) + len(p) for h, p in dir_blocks)
    id_table_start = id_meta_start + sum(len(h) + len(p) for h, p in id_blocks)
    bytes_used = id_table_start + 8
    mkfs = bytes_used if e == 'avm' else MKFS_TIME

    out_ = bytearray()
    out_ += MAGIC[e]
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
    print('wrote', out, len(out_), 'bytes, inodes', n_total)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('tree')
    ap.add_argument('out')
    ap.add_argument('--endian', choices=['le', 'be', 'avm'], default='le')
    ap.add_argument('--comp', choices=['gzip', 'xz'], default='gzip')
    a = ap.parse_args()
    build_image(a.tree, a.out, a.endian, a.comp)
