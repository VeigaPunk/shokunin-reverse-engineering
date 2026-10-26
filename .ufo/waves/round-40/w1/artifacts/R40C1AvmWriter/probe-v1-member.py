#!/usr/bin/env python3
"""probe-v1-member.py -- measure a genuine AVM big-endian SquashFS member under
the hypothesised layout (BE superblock / inode / directory / data-block-size /
fragment-entry / lookup-table fields; little-endian 2-byte metadata block-length
headers) and report every place the hypothesis could break.

Reports: superblock under both endiannesses, the 2-byte header at each table
start under both decodings, the whole directory tree, the data-block size list
of the first files that have one (both decodings), and the first fragment entry
(both decodings).

Pure stdlib. Never invokes squashfs-tools, unblob or REA; read-only.

Usage: python3 -I -B probe-v1-member.py MEMBER
Exit 0 when the AVM hypothesis explains the image, 1 otherwise.
"""
import hashlib
import lzma
import struct
import sys
import zlib

UNCOMPRESSED = 0x8000
DATA_RAW = 0x01000000
INVALID_FRAG = 0xFFFFFFFF
MAXQ = 0xFFFFFFFFFFFFFFFF
META_MAX = 8192
TYPE = {1: 'dir', 2: 'reg', 3: 'symlink', 8: 'ldir', 9: 'lreg', 10: 'lsymlink'}


def _decomp(img, off, comp):
    raw = struct.unpack_from('<H', img, off)[0]
    size = raw & ~UNCOMPRESSED
    body = img[off + 2:off + 2 + size]
    if raw & UNCOMPRESSED:
        return body, 2 + size
    if comp == 1:
        return zlib.decompress(body), 2 + size
    if comp == 4:
        return lzma.decompress(body), 2 + size
    raise SystemExit(f'unsupported compression {comp}')


class Meta:
    """Metadata table whose block-length headers are LE; bodies are a byte
    stream addressed by (table-relative block start, offset within block)."""

    def __init__(self, img, base, comp):
        self.img, self.base, self.comp = img, base, comp
        self.buf = bytearray()
        self.blocks = []          # (rel_start, buf_pos, decompressed_len)
        self.next_rel = 0

    def _add(self):
        if not self.img[self.base + self.next_rel:self.base + self.next_rel + 2]:
            raise ValueError(f'table @{self.base} ran past EOF at rel '
                             f'{self.next_rel}')
        b, used = _decomp(self.img, self.base + self.next_rel, self.comp)
        self.blocks.append((self.next_rel, len(self.buf), len(b)))
        self.buf += b
        self.next_rel += used

    def _more(self, n):
        while len(self.buf) < n:
            self._add()

    def pos(self, rel, within):
        while not any(r == rel for r, _, _ in self.blocks):
            if self.base + self.next_rel > len(self.img):
                raise ValueError(f'no metadata block at rel {rel}')
            self._add()
        bpos = [bp for r, bp, _ in self.blocks if r == rel][0]
        p = bpos + within
        self._more(p + 1)
        return p

    def read(self, pos, n):
        self._more(pos + n)
        return bytes(self.buf[pos:pos + n])


def sb(img, e):
    names = ('inodes mkfs_time block_size frag_count compression block_log '
             'flags no_ids s_major s_minor root_inode bytes_used id_table '
             'xattr_id_table inode_table dir_table frag_table lookup_table').split()
    return dict(zip(names, struct.unpack_from(('<' if e == 'le' else '>') +
                                              'IIIIHHHHHHQQQQQQQQ', img, 4)))


def main():
    path = sys.argv[1]
    img = open(path, 'rb').read()
    print(f'file {path}\nsize {len(img)} sha256 {hashlib.sha256(img).hexdigest()}')
    print(f'magic {img[:4]!r}')
    be, le = sb(img, 'be'), sb(img, 'le')
    sane = be if be['bytes_used'] <= len(img) and be['block_size'] <= (1 << 20) else le
    se = 'be' if sane is be else 'le'
    marker = sane['mkfs_time'] == sane['bytes_used']
    print(f'sane superblock endianness {se}; marker mkfs_time==bytes_used '
          f'{marker} ({sane["mkfs_time"]} vs {sane["bytes_used"]}); '
          f'block_size {sane["block_size"]} compression {sane["compression"]} '
          f'inodes {sane["inodes"]} frags {sane["frag_count"]} '
          f'root_inode 0x{sane["root_inode"]:x}')
    print('  inode_table', sane['inode_table'], 'dir_table', sane['dir_table'],
          'frag_table(index)', sane['frag_table'], 'id_table(index)',
          sane['id_table'], 'lookup(export index)', sane['lookup_table'])
    comp = sane['compression']
    if comp not in (1, 4):
        raise SystemExit(f'compression id {comp} is not gzip(1)/xz(4)')
    print('\n2-byte metadata block headers (first block of each table):')
    for name in ('inode_table', 'dir_table'):
        off = sane[name]
        raw = img[off:off + 2]
        l = struct.unpack_from('<H', raw)[0]
        b = struct.unpack_from('>H', raw)[0]
        print(f'  {name:12s} @{off}: raw={raw.hex()} '
              f'LE_len={l & 0x7fff}{"U" if l & UNCOMPRESSED else "c"} '
              f'BE_len={b & 0x7fff}{"U" if b & UNCOMPRESSED else "c"} '
              f'plausible_LE={0 < (l & 0x7fff) <= META_MAX} '
              f'plausible_BE={0 < (b & 0x7fff) <= META_MAX}')

    itab = Meta(img, sane['inode_table'], comp)
    dtab = Meta(img, sane['dir_table'], comp)
    files, links, special = [], [], []
    stack = [(sane['root_inode'] >> 16, sane['root_inode'] & 0xFFFF, '')]
    seen_dirs = 0
    while stack:
        dblk, doff, prefix = stack.pop()
        pos = itab.pos(dblk, doff)
        raw = itab.read(pos, 40)
        typ = struct.unpack_from('>H', raw, 0)[0]
        if typ not in (1, 8):
            print(f'FAIL root/child dir {prefix or "/"} inode type {typ}')
            return 1
        seen_dirs += 1
        if typ == 1:
            dstart, nlink, dsize = struct.unpack_from('>IIH', raw, 16)
            foff = struct.unpack_from('>H', raw, 26)[0]
        else:
            nlink, dsize, dstart = struct.unpack_from('>III', raw, 16)
            foff = struct.unpack_from('>H', raw, 34)[0]
        p = dtab.pos(dstart, foff)
        body = dtab.read(p, max(0, dsize - 3))
        q = 0
        while q < len(body):
            count, sblock, base_ino = struct.unpack_from('>III', body, q)
            q += 12
            for _ in range(count + 1):
                eoff, delta, etyp, nsz = struct.unpack_from('>HhHH', body, q)
                q += 8
                name = body[q:q + nsz + 1].decode('utf-8', 'replace')
                q += nsz + 1
                full = (prefix + '/' + name).lstrip('/')
                if etyp == 1:
                    stack.append((sblock, eoff, full))
                elif etyp in (2, 9):
                    ipos = itab.pos(sblock, eoff)
                    iraw = itab.read(ipos, 64)
                    ity = struct.unpack_from('>H', iraw, 0)[0]
                    if ity == 2:
                        start, frag, foff_, fsize = struct.unpack_from('>IIII', iraw, 16)
                    else:
                        start, fsize, sparse = struct.unpack_from('>QQQ', iraw, 16)
                        frag = struct.unpack_from('>I', iraw, 44)[0]
                        foff_ = struct.unpack_from('>I', iraw, 48)[0]
                    bs = sane['block_size']
                    nb = (fsize // bs if frag != INVALID_FRAG
                          else (fsize + bs - 1) // bs)
                    files.append(dict(path=full, size=fsize, frag=frag,
                                      frag_off=foff_, start=start, nb=nb,
                                      pos=ipos, ity=ity))
                elif etyp in (3, 10):
                    links.append(full)
                elif etyp in (4, 5, 6, 7):
                    special.append(full)
                else:
                    print(f'FAIL unknown dir entry type {etyp} for {full}')
                    return 1
            if q != len(body):
                pass
    print(f'\nwalked {seen_dirs} directories, {len(files)} regular files, '
          f'{len(links)} symlinks, {len(special)} specials')
    multi = [f for f in files if f['nb'] >= 2]
    print(f'files with a data-block size list (nblk>=2): {len(multi)}')
    for f in multi[:3]:
        q = f['pos'] + (32 if f['ity'] == 2 else 56)
        print(f'  {f["path"]} size={f["size"]} nblk={f["nb"]} frag={f["frag"]} '
              f'type={TYPE[f["ity"]]}')
        for i in range(min(f['nb'], 3)):
            raw = itab.read(q, 4)
            bv = struct.unpack('>I', raw)[0]
            lv = struct.unpack('<I', raw)[0]
            print(f'    block[{i}] raw={raw.hex()} '
                  f'BE=0x{bv:08x} (size {bv & 0xffffff}'
                  f'{" raw" if bv & DATA_RAW else ""}, plausible='
                  f'{0 < (bv & 0xffffff) <= sane["block_size"]}) '
                  f'| LE=0x{lv:08x} (size {lv & 0xffffff}, plausible='
                  f'{0 < (lv & 0xffffff) <= sane["block_size"]})')
            q += 4
    if sane['frag_count'] and sane['frag_table'] != MAXQ:
        idx = struct.unpack_from('>Q', img, sane['frag_table'])[0]
        idxl = struct.unpack_from('<Q', img, sane['frag_table'])[0]
        hdr = struct.unpack_from('<H', img, idx)[0]
        fb, _ = _decomp(img, idx, comp)
        st, sz, _unused = struct.unpack_from('>QII', fb, 0)
        stl, szl, _ = struct.unpack_from('<QII', fb, 0)
        print(f'\nfragment index @{sane["frag_table"]}: first u64 '
              f'BE={idx} LE={idxl} (image {len(img)} B; only BE is a plausible '
              f'block offset)')
        print(f'  fragment block @{idx} header raw={img[idx:idx+2].hex()} '
              f'LE_len={hdr & 0x7fff} first entry BE start=0x{st:x} '
              f'size=0x{sz:x} ({sz & 0xffffff} B, raw={bool(sz & DATA_RAW)}, '
              f'plausible={st < len(img) and (sz & 0xffffff) <= META_MAX + sane["block_size"]})'
              f' | LE start=0x{stl:x} size=0x{szl:x} plausible={stl < len(img)}')
    # export (lookup) table and id table: their superblock pointers are u64
    # index lists; the metadata block they point at carries an LE header and
    # BE payload.  Checked here so no field class is left unmeasured.
    if sane['lookup_table'] != MAXQ:
        lptr_be = struct.unpack_from('>Q', img, sane['lookup_table'])[0]
        lptr_le = struct.unpack_from('<Q', img, sane['lookup_table'])[0]
        hdr = struct.unpack_from('<H', img, lptr_be)[0]
        eb, _ = _decomp(img, lptr_be, comp)
        refs = [struct.unpack_from('>Q', eb, k)[0]
                for k in range(0, min(len(eb), 24), 8)]
        print(f'\nexport index @{sane["lookup_table"]}: first u64 BE={lptr_be} '
              f'LE={lptr_le} (only BE is a plausible block offset)')
        print(f'  export block @{lptr_be} header raw={img[lptr_be:lptr_be+2].hex()} '
              f'LE_len={hdr & 0x7fff}{"U" if hdr & UNCOMPRESSED else "c"} first '
              f'refs BE={["0x%x" % r for r in refs[:3]]} plausible='
              f'{all(r < len(img) for r in refs)}')
    if sane['id_table'] != MAXQ:
        iptr_be = struct.unpack_from('>Q', img, sane['id_table'])[0]
        iptr_le = struct.unpack_from('<Q', img, sane['id_table'])[0]
        hdr = struct.unpack_from('<H', img, iptr_be)[0]
        ib, _ = _decomp(img, iptr_be, comp)
        ids = [struct.unpack_from('>I', ib, k)[0] for k in range(0, min(len(ib), 12), 4)]
        print(f'id index @{sane["id_table"]}: first u64 BE={iptr_be} LE={iptr_le}')
        print(f'  id block @{iptr_be} header raw={img[iptr_be:iptr_be+2].hex()} '
              f'LE_len={hdr & 0x7fff}{"U" if hdr & UNCOMPRESSED else "c"} first '
              f'ids BE={ids} plausible={all(i < 1 << 20 for i in ids)}')
    print('\nRESULT:', 'AVM layout consistent: BE fields, LE 2-byte block headers'
          if se == 'be' and marker else 'not the AVM layout under this hypothesis')
    return 0 if (se == 'be' and marker) else 1


if __name__ == '__main__':
    sys.exit(main())
