#!/usr/bin/env python3
"""gen_v3.py -- minimal SquashFS v3.0 writer (LE/BE, gzip).

Builds a deterministic test image covering special inode types that the real
development corpus does not contain (devices, fifo, socket, hard links,
UTF-8 names, empty and >block-size files, symlink flavors). Written for
R42C1OracleCheck; validated against unsquashfs 4.7.5, 7-Zip 26.04 and
sasquatch 4.5.1.

Structure mirrors squashfs-tools 4.7.5 squashfs_compat.h:
  * packed superblock (119 bytes), no alignment pad before mkfs_time
  * metadata chains: u16 (fs-endian) block-length header (bit 15 = raw)
  * v3 inode headers: 4-bit type / 12-bit mode / 8-bit uid / 8-bit gid
    bitfields; nlink only on non-basic types
  * directory header { count:8, start_block (rel. to inode table), inode
    number }; entry { offset:13, type:3, size:8 ; 16-bit inode number ;
    name }
  * dir inode start_block is relative to the directory table
  * regular-file data blocks: u16 header (bit 15 = raw); small files are
    stored as one padded data block (fragments = 0)
  * uid/gid tables: raw u32 arrays; inode uid/guid fields hold indices
"""
import argparse
import struct
import zlib

TY_DIR, TY_FILE, TY_SYMLINK = 1, 2, 3
TY_BLKDEV, TY_CHRDEV, TY_FIFO, TY_SOCKET = 4, 5, 6, 7
INVALID_FRAG = 0xFFFFFFFF
BLOCK = 4096
META_MAX = 8192
MKFS_TIME = 1190000000


def pack(e, fmt, *vals):
    return struct.pack(('<' if e == 'le' else '>') + fmt, *vals)


def gz(data):
    out = zlib.compress(data, 9)
    return out if len(out) < len(data) else None


class MetaChain:
    def __init__(self, e, first_off):
        self.e = e
        self.blocks = []
        self.buf = bytearray()
        self.next_off = first_off

    def add(self, data):
        self.buf += data
        if len(self.buf) >= META_MAX - 64:
            self.flush()

    def flush(self):
        if not self.buf:
            return
        payload = bytes(self.buf)
        comp = gz(payload)
        if comp is None:
            hdr = pack(self.e, 'H', len(payload) | 0x8000)
            body = payload
        else:
            hdr = pack(self.e, 'H', len(comp))
            body = comp
        self.blocks.append(hdr + body)
        self.next_off += 2 + len(body)
        self.buf = bytearray()

    def finish(self):
        self.flush()
        return b''.join(self.blocks), self.next_off


class DataArea:
    def __init__(self, e, first_off):
        self.e = e
        self.buf = bytearray()
        self.next_off = first_off

    def add_block(self, content):
        off = self.next_off
        comp = gz(content)
        if comp is None:
            hdr = pack(self.e, 'H', len(content) | 0x8000)
            body = content
        else:
            hdr = pack(self.e, 'H', len(comp))
            body = comp
        self.buf += hdr + body
        self.next_off += 2 + len(body)
        return off


def inode_bytes(t, e, mode, uid, gid, mtime, ino, nlink, extra=b''):
    hdr = (t & 0xF) | ((mode & 0xFFF) << 4) | ((uid & 0xFF) << 16) \
        | ((gid & 0xFF) << 24)
    base = pack(e, 'I', hdr) + pack(e, 'iI', mtime, ino)
    if t == TY_FILE:
        start, frag, off, size = extra
        return base + pack(e, 'IIII', start, frag, off, size)
    if t == TY_SYMLINK:
        return base + pack(e, 'I', nlink) + pack(e, 'H', len(extra)) + extra
    if t == TY_DIR:
        blk_rel, file_size, offset, parent = extra
        fs_off = (file_size & 0x7FFFF) | ((offset & 0x1FFF) << 19)
        return base + pack(e, 'I', nlink) + pack(e, 'I', fs_off) \
            + pack(e, 'II', blk_rel, parent)
    if t in (TY_BLKDEV, TY_CHRDEV):
        return base + pack(e, 'I', nlink) + pack(e, 'H', extra[0] & 0xFFFF)
    return base + pack(e, 'I', nlink)   # fifo/socket


def build_tree():
    nodes = {}
    nodes['bin'] = (TY_DIR, 0o755, None, None)
    nodes['bin/a.txt'] = (TY_FILE, 0o644, b'hello world\n', None)
    nodes['bin/big.bin'] = (TY_FILE, 0o644,
                            bytes((i * 7 + 13) & 0xFF for i in range(2 * BLOCK)), None)
    nodes['bin/empty'] = (TY_FILE, 0o644, b'', None)
    nodes['bin/caf\u00e9.txt'] = (TY_FILE, 0o644, b'caf\xc3\xa9\n', None)
    nodes['dev'] = (TY_DIR, 0o755, None, None)
    nodes['dev/console'] = (TY_CHRDEV, 0o600, (5, 1), None)
    nodes['dev/mtd0'] = (TY_BLKDEV, 0o600, (31, 0), None)
    nodes['fifo'] = (TY_FIFO, 0o644, None, None)
    nodes['sock'] = (TY_SOCKET, 0o755, None, None)
    nodes['sym1'] = (TY_SYMLINK, 0o777, b'bin/a.txt', None)
    nodes['sub'] = (TY_DIR, 0o755, None, None)
    nodes['sub/up'] = (TY_SYMLINK, 0o777, b'../bin/a.txt', None)
    nodes['sub/abs'] = (TY_SYMLINK, 0o777, b'/etc/passwd', None)
    nodes['h1'] = (TY_FILE, 0o644, b'hard link content\n', 'H')
    nodes['h2'] = (TY_FILE, 0o644, b'hard link content\n', 'H')
    nodes['d1'] = (TY_DIR, 0o755, None, None)
    nodes['d1/d2'] = (TY_DIR, 0o755, None, None)
    nodes['d1/d2/deep'] = (TY_FILE, 0o600, b'deep\n', None)
    return nodes


def build_inode_chain(e, data, nxt, serialized, nlink):
    ichain = MetaChain(e, data.next_off)
    inode_table_start = data.next_off
    block_start = inode_table_start
    within = 0
    inode_blocks = {}
    for ino in range(1, nxt):
        t, mode, extra = serialized[ino]
        raw = inode_bytes(t, e, mode, 0, 0, MKFS_TIME, ino,
                          nlink.get(ino, 2), extra)
        if within + len(raw) > META_MAX - 2:
            ichain.flush()
            block_start = ichain.next_off
            within = 0
        ichain.add(raw)
        inode_blocks[ino] = (block_start, within)
        within += len(raw)
    inode_table_bytes, inode_table_end = ichain.finish()
    return inode_table_bytes, inode_table_end, inode_blocks, inode_table_start


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--endian', default='le', choices=['le', 'be'])
    ap.add_argument('--out', required=True)
    a = ap.parse_args(argv)
    e = a.endian
    nodes = build_tree()

    paths = sorted(k for k in nodes if k != '')
    ino_of = {'': 1}
    group_ino = {}
    nxt = 2
    for p in paths:
        grp = nodes[p][3]
        if grp:
            if grp in group_ino:
                ino_of[p] = group_ino[grp]
                continue
            group_ino[grp] = nxt
        ino_of[p] = nxt
        nxt += 1

    by_ino = {}
    for p in paths:
        by_ino.setdefault(ino_of[p], []).append(p)

    nlink = {'': 2}
    for p in paths:
        t = nodes[p][0]
        nlink[p] = 2 if (t == TY_DIR or nodes[p][3]) else 1

    data = DataArea(e, 119)
    file_data = {}
    for p in paths:
        t = nodes[p][0]
        if t != TY_FILE:
            continue
        content = nodes[p][2]
        if not content:
            file_data[p] = (0, INVALID_FRAG, 0, 0)
            continue
        pad = (-len(content)) % BLOCK
        start = data.add_block(content + b'\0' * pad)
        file_data[p] = (start, INVALID_FRAG, 0, len(content))

    serialized = {}
    for ino in range(1, nxt):
        if ino == 1:
            t, mode = TY_DIR, 0o755
            extra = (0, 0, 0, 0)
        else:
            p = by_ino[ino][0]
            t, mode, content, grp = nodes[p]
            if t == TY_FILE:
                extra = file_data[p]
            elif t == TY_SYMLINK:
                extra = content
            elif t in (TY_BLKDEV, TY_CHRDEV):
                major, minor = content
                rdev = (major << 8) | (minor & 0xFF)
                if minor >= 256:
                    rdev |= (minor & ~0xFF) << 12
                extra = (rdev,)
            elif t == TY_DIR:
                extra = (0, 0, 0, 0)
            else:
                extra = b''
        serialized[ino] = (t, mode, extra)

    inode_table_bytes, inode_table_end, inode_blocks, inode_table_start = \
        build_inode_chain(e, data, nxt, serialized, nlink)

    # --- directory table: flush before each directory (offset 0) ---
    dchain = MetaChain(e, inode_table_end)
    dir_table_rel = {}
    dir_sizes = {}
    for d in sorted([''] + [p for p in paths if nodes[p][0] == TY_DIR]):
        prefix = d + '/' if d else ''
        kids = sorted(p for p in paths
                      if p.startswith(prefix) and '/' not in p[len(prefix):])
        if not kids:
            continue
        dchain.flush()
        dir_table_rel[d] = dchain.next_off - inode_table_end
        entries = []
        for k in kids:
            t = nodes[k][0]
            rel_blk = inode_blocks[ino_of[k]][0] - inode_table_start
            boff = inode_blocks[ino_of[k]][1]
            entries.append((rel_blk, boff, t, k[len(prefix):].encode('utf-8')))
        data_len = 0
        pos = 0
        while pos < len(entries):
            chunk = entries[pos:pos + 60]
            rel_root = inode_blocks[ino_of[d]][0] - inode_table_start
            dchain.add(pack(e, 'I', len(chunk) - 1)
                       + pack(e, 'I', rel_root) + pack(e, 'I', ino_of[d]))
            data_len += 12
            for rel_blk, off, t, name in chunk:
                word = (off & 0x1FFF) | ((t & 0x7) << 13) \
                    | ((len(name) & 0xFF) << 16)
                dchain.add(pack(e, 'I', word)
                           + pack(e, 'h', rel_blk & 0xFFFF) + name)
                data_len += 6 + len(name)
            pos += len(chunk)
        dir_sizes[d] = data_len
    dir_table_bytes, dir_table_end = dchain.finish()

    for ino in range(1, nxt):
        if serialized[ino][0] == TY_DIR:
            p_ = '' if ino == 1 else by_ino[ino][0]
            serialized[ino] = (TY_DIR, serialized[ino][1],
                               (dir_table_rel.get(p_, 0),
                                dir_sizes.get(p_, 0), 0, 0))
    inode_table_bytes, inode_table_end, inode_blocks, inode_table_start = \
        build_inode_chain(e, data, nxt, serialized, nlink)
    dir_table_start = inode_table_end

    # fragments == 0 -> fragment_table_start must equal uid_start;
    # uid table then gid table at the very end of the image
    frag_table_start = inode_table_end
    uid_start = frag_table_start
    guid_start = uid_start + 4
    id_bytes = pack(e, 'I', 0) + pack(e, 'I', 0)
    lookup_table_start = 0xFFFFFFFFFFFFFFFF
    bytes_used = guid_start + 4

    sb = bytearray()
    sb += pack(e, 'I', 0x73717368)       # magic
    sb += pack(e, 'I', nxt - 1)          # inodes
    sb += pack(e, 'I', bytes_used)       # bytes_used_2 (legacy)
    sb += pack(e, 'I', uid_start)        # uid_start_2
    sb += pack(e, 'I', guid_start)       # guid_start_2
    sb += pack(e, 'I', inode_table_start)   # inode_table_start_2
    sb += pack(e, 'I', dir_table_start)  # directory_table_start_2
    sb += pack(e, 'H', 3)                # s_major
    sb += pack(e, 'H', 0)                # s_minor
    sb += pack(e, 'H', BLOCK)            # block_size_1
    sb += pack(e, 'H', 12)               # block_log
    sb += bytes([0])                     # flags
    sb += bytes([1])                     # no_uids
    sb += bytes([1])                     # no_guids
    sb += pack(e, 'I', MKFS_TIME)        # mkfs_time (packed, unaligned)
    sb += pack(e, 'Q', 0)                # root_inode: (0<<16)|0
    sb += pack(e, 'I', BLOCK)            # block_size
    sb += pack(e, 'I', 0)                # fragments
    sb += pack(e, 'I', frag_table_start) # fragment_table_start_2
    sb += pack(e, 'Q', bytes_used)       # bytes_used
    sb += pack(e, 'Q', uid_start)        # uid_start
    sb += pack(e, 'Q', guid_start)       # guid_start
    sb += pack(e, 'Q', inode_table_start)   # inode_table_start
    sb += pack(e, 'Q', dir_table_start)  # directory_table_start
    sb += pack(e, 'Q', frag_table_start) # fragment_table_start
    sb += pack(e, 'Q', lookup_table_start)     # lookup_table_start
    assert len(sb) == 119, len(sb)

    out = sb + data.buf + inode_table_bytes + dir_table_bytes + id_bytes
    open(a.out, 'wb').write(out)
    print('wrote', a.out, len(out), 'bytes; inodes:', nxt - 1,
          '; inode_table_start', inode_table_start, '; dir_table_start',
          dir_table_start, '; uid_start', uid_start, '; guid_start', guid_start)
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv[1:]))
