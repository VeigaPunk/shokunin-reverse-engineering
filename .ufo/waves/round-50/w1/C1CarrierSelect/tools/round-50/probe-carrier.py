#!/usr/bin/env python3
"""R50-C1 wave-1 draft instrument (seat C1CarrierSelect): probe an AVM firmware
.tar image and pin the carrier chain links for `tools/round-41/fetch-vendor.py`.

For one FRITZ!OS .image (plain tar) this reads, without writing any vendor byte
outside --out:

  * the tar member table,
  * ./var/tmp/filesystem.image  -> member length, sha256,
  * its SquashFS v4 superblock (LE and BE interpretations of the same 96 bytes),
    reporting magic, s_major.s_minor, compression id, block size, mkfs_time,
    bytes_used, the AVM marker (mkfs_time == bytes_used), whether the member is
    longer than bytes_used, and sha256 of the carve member[:bytes_used]
    (the fetch-vendor `length` link),
  * ./var/info.txt product/version lines,
  * ./var/kernel architecture evidence (zImage magic 0x016f2818 at 0x24, or
    'not shown').

Usage: probe-carrier.py --image FILE [--member NAME] [--out FILE] [--file-cmd]
Exit: 0 probe produced output; 2 could not evaluate.
Stdlib only. Vendor bytes stay in scratch; only this JSON is emitted.
"""
import argparse
import hashlib
import json
import struct
import subprocess
import sys
import tarfile

SB_FMT_LE = '<IIIIIHHHHHHQQQQQQQQ'
SB_FMT_BE = '>IIIIIHHHHHHQQQQQQQQ'
SB_FIELDS = ('magic', 'inodes', 'mkfs_time', 'block_size', 'fragments',
             'compression', 'block_log', 'flags', 'no_ids', 's_major',
             's_minor', 'root_inode', 'bytes_used', 'id_table_start',
             'xattr_id_table_start', 'inode_table_start',
             'directory_table_start', 'fragment_table_start',
             'lookup_table_start')
COMP_NAMES = {1: 'gzip', 2: 'lzo', 3: 'lzma', 4: 'xz', 5: 'lz4', 6: 'zstd'}


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def sb_dict(fmt, raw):
    vals = struct.unpack(fmt, raw)
    return {k: v for k, v in zip(SB_FIELDS, vals)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--image', required=True)
    ap.add_argument('--member', default='./var/tmp/filesystem.image')
    ap.add_argument('--info-member', default='./var/info.txt')
    ap.add_argument('--version-member', default='./var/version')
    ap.add_argument('--kernel-members',
                    default='./var/kernel,./var/tmp/kernel.image')
    ap.add_argument('--out', default=None)
    ap.add_argument('--file-cmd', action='store_true',
                    help='also run file(1) on the kernel member')
    a = ap.parse_args()
    rec = {}
    image = open(a.image, 'rb').read()
    rec['image'] = {'path': a.image, 'bytes': len(image),
                    'sha256': sha256(image)}
    members = {}
    payload = {}
    with tarfile.open(fileobj=__import__('io').BytesIO(image),
                      mode='r:') as tf:
        for m in tf.getmembers():
            members[m.name] = {'size': m.size,
                               'type': ('file' if m.isfile() else
                                        ('dir' if m.isdir() else
                                         ('link' if m.issym() else 'other')))}
            if m.isfile() and m.name in (a.member, a.info_member,
                                         a.version_member):
                payload[m.name] = tf.extractfile(m).read()
            elif m.isfile() and m.name in a.kernel_members.split(','):
                payload[m.name] = tf.extractfile(m).read()
    rec['members'] = members
    if a.member not in payload:
        print('member %r absent' % a.member, file=sys.stderr)
        return 2
    member = payload[a.member]
    sb = {'member_bytes': len(member), 'member_sha256': sha256(member)}
    sb['magic_hex'] = member[:4].hex()
    sb['magic_ascii'] = member[:4].decode('latin-1')
    raw = member[:struct.calcsize(SB_FMT_LE)]
    endi = 'le' if sb['magic_ascii'] == 'hsqs' else \
           ('be' if sb['magic_ascii'] == 'sqsh' else 'unknown')
    sb['endianness_from_magic'] = endi
    if endi in ('le', 'be'):
        d = sb_dict(SB_FMT_LE if endi == 'le' else SB_FMT_BE, raw)
        sb['superblock'] = d
        sb['compression_id'] = d['compression']
        sb['compression_name'] = COMP_NAMES.get(d['compression'],
                                                'unknown-%d' % d['compression'])
        sb['version'] = '%d.%d' % (d['s_major'], d['s_minor'])
        sb['avm_marker_mkfs_eq_bytes_used'] = d['mkfs_time'] == d['bytes_used']
        sb['member_len_gt_bytes_used'] = len(member) > d['bytes_used']
        if 0 < d['bytes_used'] <= len(member):
            carve = member[:d['bytes_used']]
            sb['carve_length'] = d['bytes_used']
            sb['carve_sha256'] = sha256(carve)
    rec['carrier_member'] = sb

    def text_lines(name):
        if name not in payload:
            return None
        return payload[name].decode('utf-8', 'replace').splitlines()

    ver = text_lines(a.version_member)
    rec['version_txt'] = {'member': a.version_member,
                          'present': ver is not None,
                          'lines': ver}
    info = text_lines(a.info_member)
    rec['info_txt'] = {'member': a.info_member,
                       'present': info is not None,
                       'first_lines': (info or [])[:2]}
    found = [n for n in a.kernel_members.split(',') if n in payload]
    kern = {'members': found, 'present': bool(found)}
    if found:
        k = payload[found[0]]
        kern['member'] = found[0]
        kern.update(bytes=len(k), sha256=sha256(k),
                    first16_hex=k[:16].hex())
        magic = int.from_bytes(k[0x24:0x28], 'little')
        kern['zImage_magic_le_0x016f2818'] = magic == 0x016f2818
        kern['word_at_0x24_le_hex'] = k[0x24:0x28].hex()
        if a.file_cmd:
            try:
                p = subprocess.run(['file', '-b', '-'],
                                   input=k[:4096], capture_output=True,
                                   timeout=20)
                kern['file_output_first4k'] = \
                    p.stdout.decode('utf-8', 'replace').strip()
            except Exception as e:
                kern['file_output_first4k'] = 'error: %s' % e
    rec['kernel'] = kern
    out = json.dumps(rec, indent=1, sort_keys=True) + '\n'
    if a.out:
        with open(a.out, 'w') as fh:
            fh.write(out)
    sys.stdout.write(out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
