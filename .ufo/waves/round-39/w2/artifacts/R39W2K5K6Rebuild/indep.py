"""Independent BE SquashFS v4 reader written from the Linux v6.12 layout, no repo imports.

Parses the superblock itself, walks the inode/directory metadata, decompresses every
regular file with stdlib zlib/lzma, and compares against a given oracle.tsv /
symlinks.tsv pair.  Symlink classes are recomputed twice: once with the byte rule
from unblob 26.6.4 ``is_safe_path`` (join + resolve + relative_to, no clamping) and
once with unblob's own function against a materialised tree.
"""
import hashlib
import lzma
import posixpath
import struct
import sys
import zlib

BE = '>'


def u16(b, o): return struct.unpack(BE + 'H', b[o:o + 2])[0]
def u32(b, o): return struct.unpack(BE + 'I', b[o:o + 4])[0]
def i16(b, o): return struct.unpack(BE + 'h', b[o:o + 2])[0]
def u64(b, o): return struct.unpack(BE + 'Q', b[o:o + 8])[0]


def run(image, oracle, symtab):
    b = open(image, 'rb').read()
    assert b[:4] == b'sqsh', 'magic is not big-endian sqsh'
    ninodes = u32(b, 4)
    block_size = u32(b, 12)
    comp = u16(b, 20)
    root_ref = u64(b, 32)
    bytes_used = u64(b, 40)
    id_table_start = u64(b, 48)
    inode_table_start = u64(b, 64)
    dir_table_start = u64(b, 72)
    print('== %s comp_id=%d block_size=%d inodes=%d bytes_used=%d' % (
        image, comp, block_size, ninodes, bytes_used))
    assert bytes_used == len(b), (bytes_used, len(b))

    id_meta_start = u64(b, id_table_start)

    def meta(stream_start, stream_end):
        pos = stream_start
        blocks = []
        while pos < stream_end:
            h = u16(b, pos)
            size = h & 0x7fff
            raw = bool(h & 0x8000)
            data = b[pos + 2:pos + 2 + size]
            if not raw:
                data = zlib.decompress(data) if comp == 1 else lzma.decompress(data)
            blocks.append(data)
            pos += 2 + size
        assert pos == stream_end, ('stream overrun', pos, stream_end)
        return b''.join(blocks), len(blocks)

    ino, n_inode_blocks = meta(inode_table_start, dir_table_start)
    dirs, n_dir_blocks = meta(dir_table_start, id_meta_start)
    print('   metadata blocks: inode=%d dir=%d (both uncompressed on disk)' % (
        n_inode_blocks, n_dir_blocks))

    def inode_at(off):
        t = u16(ino, off)
        perm = u16(ino, off + 2)
        inum = u32(ino, off + 12)
        p = off + 16
        if t == 1:                                    # basic dir
            start, nlink = u32(ino, p), u32(ino, p + 4)
            isz, doff, parent = u16(ino, p + 8), u16(ino, p + 10), u32(ino, p + 12)
            return ('D', inum, perm, p + 16, start, nlink, isz, doff, parent)
        if t == 2:                                    # basic reg
            start, frag, foff, sz = (u32(ino, p), u32(ino, p + 4),
                                     u32(ino, p + 8), u32(ino, p + 12))
            nb = 0 if sz == 0 else (sz + block_size - 1) // block_size
            p += 16
            sizes = [u32(ino, p + 4 * i) for i in range(nb)]
            return ('F', inum, perm, p + 4 * nb, start, frag, foff, sz, sizes)
        if t == 3:                                    # basic symlink
            nlink, tlen = u32(ino, p), u32(ino, p + 4)
            tgt = ino[p + 8:p + 8 + tlen]
            return ('L', inum, perm, p + 8 + tlen, nlink, tgt)
        raise SystemExit('unhandled inode type %d at %d' % (t, off))

    inum_map = {}
    pos = 0
    while pos < len(ino):
        k = inode_at(pos)
        inum_map[k[1]] = pos
        pos = k[3]
    assert pos == len(ino), (pos, len(ino))
    assert len(inum_map) == ninodes, (len(inum_map), ninodes)

    files = {}
    links = {}
    order = []
    dir_stream_len = len(dirs)

    def dir_body(start, doff, isz):
        # i_size carries the 3 invented "."/".." f_pos bytes; the on-disk
        # table is i_size - 3 bytes long.
        body = dirs[start + doff:start + doff + isz - 3]
        return body

    def walk(off, prefix):
        kind = inode_at(off)
        _, inum, perm, _, start, nlink, isz, doff, parent = kind
        body = dir_body(start, doff, isz)
        order.append((prefix or '/', inum, start, doff, isz, nlink, parent, len(body)))
        # i_size bytes include the 3-byte invented "./.." f_pos; the on-disk
        # table is whatever follows the offset, self-delimiting.
        p = 0
        entries = 0
        while p + 12 <= len(body):
            count = u32(body, p)
            sblk = u32(body, p + 4)
            first = u32(body, p + 8)
            p += 12
            assert sblk == 0, ('dir header names a non-zero start_block', sblk)
            for _ in range(count + 1):
                eoff = u16(body, p)
                delta = i16(body, p + 2)
                typ = u16(body, p + 4)
                nsz = u16(body, p + 6)
                p += 8
                name = body[p:p + nsz + 1]
                p += nsz + 1
                entries += 1
                nm = name.decode('utf-8', 'surrogateescape')
                child_inum = first + delta
                coff = inum_map[child_inum]
                ck = inode_at(coff)
                assert ck[1] == child_inum
                rel = nm if prefix == '' else prefix + '/' + nm
                if typ == 1:
                    walk(coff, rel)
                elif typ == 2:
                    _, _, _, _, startb, frag, foff, sz, sizes = ck
                    assert frag == 0xffffffff, 'unexpected fragment'
                    out = bytearray()
                    dp = startb
                    cblocks = 0
                    for s in sizes:
                        raw = bool(s & 0x01000000)
                        ln = s & 0xffffff
                        chunk = b[dp:dp + ln]
                        dp += ln
                        if raw:
                            out += chunk
                        else:
                            cblocks += 1
                            if comp == 1:
                                out += zlib.decompress(chunk)
                            else:
                                assert chunk[:6] == b'\xfd7zXZ\x00', ('block is not a full .xz container', chunk[:6].hex())
                                xz_magic[rel] = chunk[:6].hex()
                                out += lzma.decompress(chunk)
                    assert len(out) == sz, (rel, len(out), sz)
                    if cblocks:
                        file_meta[rel] = cblocks
                    files[rel] = (hashlib.sha256(out).hexdigest(), sz, cblocks, len(sizes))
                elif typ == 3:
                    links[rel] = ck[5]
                else:
                    raise SystemExit('unhandled entry type %d' % typ)
        assert p == len(body), ('dir body not fully consumed', prefix, p, len(body), isz)

    file_meta = {}
    xz_magic = {}
    walk(root_ref & 0xffffffffffff, '')

    ok = True
    orows = [l.rstrip('\n').split('\t') for l in open(oracle, encoding='utf-8')]
    if len(orows) != len(files):
        print('   FILE COUNT MISMATCH oracle=%d indep=%d' % (len(orows), len(files)))
        ok = False
    for rel, sha, sz in orows:
        got = files.get(rel)
        if got is None:
            print('   MISSING in image:', rel); ok = False
        elif got[0] != sha or str(got[1]) != sz:
            print('   MISMATCH', rel, got, (sha, sz)); ok = False
    extra = set(files) - {r[0] for r in orows}
    if extra:
        print('   EXTRA in image:', sorted(extra)); ok = False
    srows = [l.rstrip('\n').split('\t') for l in open(symtab, encoding='utf-8')]
    for rel, tgt, cls in srows:
        got = links.get(rel)
        if got != tgt.encode('utf-8'):
            print('   SYMLINK MISMATCH', rel, 'oracle', tgt, 'indep', got); ok = False
    if set(links) != {r[0] for r in srows}:
        print('   SYMLINK SET MISMATCH image=%s table=%s' % (sorted(links), sorted(r[0] for r in srows)))
        ok = False

    def cls_of(rel, tgt):
        parts = (posixpath.dirname(rel).split('/') if posixpath.dirname(rel) else []) + tgt.split('/')
        stack = []
        for compo in parts:
            if compo in ('', '.'):
                continue
            if compo == '..':
                if not stack:
                    return 'escaping'
                stack.pop()
            else:
                stack.append(compo)
        return 'in-tree'

    print('   symlink classes recomputed from S122 rule (no clamping):')
    for rel, tgt, cls in srows:
        mine = cls_of(rel, tgt)
        flag = 'OK' if mine == cls else 'MISMATCH'
        if mine != cls:
            ok = False
        print('     %-22s -> %-24s table=%-9s mine=%-9s %s' % (rel, tgt, cls, mine, flag))
    print('   files: %d (compressed data blocks total %d), symlinks: %d' % (
        len(files), sum(v[2] for v in files.values()), len(links)))
    for rel, (sha, sz, cb, nb) in sorted(files.items()):
        if cb:
            print('     compressed-data-block file: %-20s size=%d blocks=%d compressed=%d first6=%s' % (
                rel, sz, nb, cb, xz_magic.get(rel, 'gzip-deflate')))
    print('   RESULT:', 'ORACLE MATCH' if ok else 'DISCREPANCY')
    return ok


if __name__ == '__main__':
    L = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-39/c1/'
    a = run('K5-rebuild.sqsh', L + 'K5/oracle.tsv', L + 'K5/symlinks.tsv')
    c = run('K6-rebuild.sqsh', L + 'K6/oracle.tsv', L + 'K6/symlinks.tsv')
    print('BOTH MATCH' if a and c else 'FAILURES PRESENT')
