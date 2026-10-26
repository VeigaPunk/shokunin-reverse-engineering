#!/usr/bin/env python3
"""Read-only AVM vendor-image member probe (round-40 minimality review).

Answers one question per vendor image: does the tar carry a SquashFS member that
is a *genuine AVM-layout BE* body (magic `sqsh`, major 4, mkfs_time ==
bytes_used)?  It opens the tar, reads the first 4096 bytes of every
`filesystem.image` member and hashes the member; it extracts nothing to disk and
runs no extractor (no REA, no unblob, no sasquatch).

Usage: probe-avm-members.py IMAGE.image [IMAGE.image ...]
Exit 0 always (a probe, not a gate); the shapes print as rows.
"""
import hashlib
import struct
import sys
import tarfile


def superblock(f, size):
    b = f.read(4096)
    if len(b) < 96:
        return None
    magic = b[:4]
    comp, = struct.unpack('>H', b[20:22])
    s_major, s_minor = struct.unpack('>HH', b[28:32])
    mkfs, = struct.unpack('>I', b[8:12])
    bytes_used, = struct.unpack('>Q', b[40:48])
    inode_count, = struct.unpack('>I', b[4:8])
    frag_count, = struct.unpack('>I', b[16:20])
    inode_table, = struct.unpack('>Q', b[64:72])
    dir_table, = struct.unpack('>Q', b[72:80])
    return {
        'magic': magic, 'comp': comp, 'version': '%d.%d' % (s_major, s_minor),
        'mkfs': mkfs, 'bytes_used': bytes_used, 'marker': mkfs == bytes_used,
        'inode_count': inode_count, 'frag_count': frag_count,
        'inode_table_start': inode_table, 'directory_table_start': dir_table,
        'size': size,
    }


def member_sha(f):
    h = hashlib.sha256()
    while True:
        chunk = f.read(1 << 20)
        if not chunk:
            return h.hexdigest()
        h.update(chunk)


def main(argv):
    for path in argv[1:]:
        whole = hashlib.sha256()
        with open(path, 'rb') as raw:
            while True:
                chunk = raw.read(1 << 20)
                if not chunk:
                    break
                whole.update(chunk)
        print('image %s sha256 %s' % (path, whole.hexdigest()))
        try:
            tf = tarfile.open(path)
        except tarfile.TarError as exc:
            print('  not a tar: %s' % exc)
            continue
        members = [m for m in tf.getmembers() if m.isfile()]
        print('  tar members %d' % len(members))
        hits = 0
        for m in members:
            if 'filesystem.image' not in m.name:
                continue
            hits += 1
            f = tf.extractfile(m.name)
            sb = superblock(f, m.size)
            sha = member_sha(tf.extractfile(m.name))
            if sb is None:
                print('  %s size=%d short member' % (m.name, m.size))
                continue
            print('  %s size=%d magic=%r comp=%d v%s mkfs=%d bytes_used=%d '
                  'marker=%s inode_count=%d frag_count=%d inode_table=%d '
                  'dir_table=%d sha256=%s'
                  % (m.name, m.size, sb['magic'], sb['comp'], sb['version'],
                     sb['mkfs'], sb['bytes_used'], sb['marker'],
                     sb['inode_count'], sb['frag_count'],
                     sb['inode_table_start'], sb['directory_table_start'], sha))
        if not hits:
            print('  no filesystem.image member; top-level: %s'
                  % sorted({m.name.split('/')[1] if m.name.startswith('./') and '/' in m.name[2:] else m.name
                            for m in members}))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
