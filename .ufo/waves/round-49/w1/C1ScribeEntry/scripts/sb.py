#!/usr/bin/env python3
"""Decode the unblob 26.6.4 SquashFS v1/v2 header (squashfs_super_block_t + packed tail, S112 :123-137).
Layout per draft: s_magic[4]; inodes,bytes_used,uid_start,guid_start,inode_table_start,directory_table_start (u32);
s_major,s_minor (u16 at 28,30); packed tail: block_size_1 u16@32, block_log u16@34, flags u8@36,
no_uids u8@37, no_guids u8@38, mkfs_time u32@39 (unaligned)."""
import struct, sys, datetime, re
for path in sys.argv[1:]:
    raw = open(path, 'rb').read()
    magic = raw[:4]
    e = '>' if magic == b'sqsh' else '<'
    inodes, bytes_used, uid_start, guid_start, its, dts = struct.unpack(e + '6I', raw[4:28])
    s_major, s_minor = struct.unpack(e + '2H', raw[28:32])
    bs1, block_log, flags, no_uids, no_guids = struct.unpack(e + 'HHBBB', raw[32:39])
    mkfs, = struct.unpack(e + 'I', raw[39:43])
    streams = [m.start() for m in re.finditer(b'\x78\xda', raw)]
    print(path.split('/')[-1], magic, 'order=' + ('be' if e == '>' else 'le'),
          f'major={s_major} minor={s_minor} inodes={inodes} bytes_used={bytes_used}',
          f'block_size_1={bs1} block_log={block_log} flags=0x{flags:02x} no_uids={no_uids} no_guids={no_guids}',
          f'mkfs_time={mkfs} ({datetime.datetime.fromtimestamp(mkfs, datetime.UTC).isoformat()})',
          f'uid_start={uid_start} guid_start={guid_start} inode_table_start={its} dir_table_start={dts}',
          f'zlib_78da_offsets={streams}')
