#!/usr/bin/env python3
"""Pure reader for a SquashFS v3 superblock (unblob squashfs3_super_block_t).
Reads bytes only; no extractor. Usage: sqfs3-probe.py <file> <offset> [--be]"""
import sys, struct, hashlib

MAGICS = {b'hsqs':'v3/stdLE', b'sqsh':'v3/stdBE', b'hsqt':'v3/ddwrtLE', b'tqsh':'v3/ddwrtBE',
          b'shsq':'v3/bcmLE', b'qshs':'v3/bcmBE', b'sqlz':'v3/nsBE', b'zlqs':'v3/nsLE'}

def parse(buf, off):
    b = buf[off:off+119]
    magic = b[0:4]
    variant = MAGICS.get(magic, 'unknown')
    be = magic in (b'sqsh', b'tqsh', b'qshs', b'sqlz')  # file-level byte order of the struct fields
    # ddwrt handler treats 'hsqt' as BE for its extractor; report both readings below.
    e = '>' if be else '<'
    f = struct.unpack(e+'6I4H3B I Q I I I Q Q Q Q Q Q Q', b[4:119])
    keys = ['inodes','bytes_used_2','uid_start_2','guid_start_2','inode_table_start_2',
            'directory_table_start_2','s_major','s_minor','block_size_1','block_log',
            'flags','no_uids','no_guids','mkfs_time','root_inode','block_size','fragments',
            'fragment_table_start_2','bytes_used','uid_start','guid_start','inode_table_start',
            'directory_table_start','fragment_table_start','lookup_table_start']
    d = dict(zip(keys, f))
    d['magic_bytes'] = magic
    d['variant'] = variant
    d['struct_endian'] = 'BE' if be else 'LE'
    return d

if __name__ == '__main__':
    path, off = sys.argv[1], int(sys.argv[2], 0)
    be_force = '--be' in sys.argv
    buf = open(path,'rb').read()
    d = parse(buf, off)
    if be_force:
        b = buf[off:off+119]
        e = '>'
        f = struct.unpack(e+'6I4H3B I Q I I I Q Q Q Q Q Q Q', b[4:119])
        print('forced-BE', f)
    for k,v in d.items():
        print(f'{k}\t{v}' if not isinstance(v,int) else f'{k}\t{v} (0x{v:x})')
    used = d['bytes_used']
    print('carve_range\t%d..%d' % (off, off+used))
    print('carve_sha256_in_place\t'+hashlib.sha256(buf[off:off+used]).hexdigest())
    print('carve_bytes\t%d' % used)
