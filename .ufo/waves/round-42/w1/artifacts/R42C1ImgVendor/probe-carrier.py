#!/usr/bin/env python3
"""Read-only C1 carrier prober: container chain, superblock, two-reader oracle compare.

Never runs REA, unblob or sasquatch. Uses only unsquashfs 4.7.5 (read/-s/-lls) and
7-Zip, both pure readers for this purpose.

Usage: probe-carrier.py <image> [--offset N] [--out DIR]

Emits JSON on stdout: container landmarks, every SquashFS superblock hit with decoded
v3 fields and the matching unblob 26.6.4 handler(s), then per-reader results:
superblock status, entry table (path+type+size) and the regular-file path-set
comparison between the two readers.
"""
import argparse
import hashlib
import json
import os
import re
import struct
import subprocess
import sys

BACKHAND = '/home/vgpnk/.local/opt/backhand-0.25.5-v3/bin/unsquashfs-backhand'
MAGICS = (b'sqsh', b'hsqs', b'tqsh', b'hsqt', b'qshs', b'shsq', b'sqlz', b'zlqs')
LANDMARKS = (b'HDR0', b'TRX', b'TP-LINK', b'D-Link', b'D-LINK', b'CFE', b'UBI#',
             b'hsqs', b'sqsh', b'qshs', b'shsq', b'tqsh', b'hsqt')
# unblob 26.6.4 PATTERNS = magic(4) + 24 wildcard bytes + 2 bytes of s_major
UNBLOB = (
    ('squashfs_v1', b'sqsh', b'\x00\x01'),
    ('squashfs_v1', b'hsqs', b'\x01\x00'),
    ('squashfs_v2', b'sqsh', b'\x00\x02'),
    ('squashfs_v2', b'hsqs', b'\x02\x00'),
    ('squashfs_v2_nonstandard', b'sqlz', b'\x00\x05'),
    ('squashfs_v3', b'sqsh', b'\x00\x03'),
    ('squashfs_v3', b'hsqs', b'\x03\x00'),
    ('squashfs_v3_ddwrt', b'tqsh', b'\x00\x03'),
    ('squashfs_v3_ddwrt', b'hsqt', b'\x03\x00'),
    ('squashfs_v3_broadcom', b'qshs', b'\x00\x03'),
    ('squashfs_v3_broadcom', b'shsq', b'\x03\x00'),
    ('squashfs_v3_nonstandard', b'sqlz', b'\x00\x03'),
    ('squashfs_v3_nonstandard', b'zlqs', b'\x03\x00'),
    ('squashfs_v4_le', b'hsqs', b'\x04\x00'),
    ('squashfs_v4_be', b'sqsh', b'\x00\x04'),
    ('squashfs_v4_broadcom', b'qshs', b'\x00\x04'),
    ('squashfs_v4_broadcom', b'shsq', b'\x04\x00'),
)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run(cmd, **kw):
    p = subprocess.run(cmd, capture_output=True, **kw)
    return p.returncode, p.stdout, p.stderr


def sb_v3(buf, off, endian):
    """Decode the on-disk squashfs 3.x superblock (PACKED C layout: no pad byte after
    no_guids, verified byte-for-byte against unsquashfs 4.7.5, 7-Zip and unblob's own
    dissect.cstruct parse of this struct)."""
    e = '>' if endian == 'BE' else '<'
    g = lambda fmt, at: struct.unpack(e + fmt, buf[off + at:off + at + struct.calcsize(fmt)])[0]  # noqa: E731
    return {
        'magic': buf[off:off + 4].decode('latin-1'),
        'inodes': g('I', 4),
        's_major': g('H', 28),
        's_minor': g('H', 30),
        'block_size_1': g('H', 32),
        'block_log': g('H', 34),
        'flags': buf[off + 36],
        'no_uids': buf[off + 37],
        'no_guids': buf[off + 38],
        'mkfs_time': g('I', 39),
        'root_inode': g('Q', 43),
        'block_size': g('I', 51),
        'fragments': g('I', 55),
        'bytes_used': g('Q', 63),
        'uid_start': g('Q', 71),
        'guid_start': g('Q', 79),
        'inode_table_start': g('Q', 87),
        'directory_table_start': g('Q', 95),
        'fragment_table_start': g('Q', 103),
        'lookup_table_start': g('Q', 111),
    }


def plausible(f, size):
    n = 0
    if 1 <= f['s_major'] <= 4:
        n += 2
    if f['block_log'] in (12, 13, 14, 15, 16):
        n += 1
    if 0 < f['inodes'] < 500000:
        n += 1
    if 0 < f['bytes_used'] <= size:
        n += 2
    return n


PAD_SIZES = (4096, 1024)


def round_up(n, m):
    return (n + m - 1) // m * m


def unblob_chunk_end(buf, start, bytes_used):
    """unblob 26.6.4 _SquashFSBase.calculate_chunk, transcribed verbatim in effect:
    end = start + bytes_used rounded up to 4096 or 1024 when the tail is all-zero
    padding, else start + bytes_used."""
    pad_span = round_up(bytes_used, max(PAD_SIZES)) - bytes_used
    padding = buf[start + bytes_used:start + bytes_used + pad_span]
    for pad in sorted(PAD_SIZES, reverse=True):
        size = round_up(bytes_used, pad)
        plen = size - bytes_used
        if padding.startswith(b'\x00' * plen):
            return start + size, 'round_up_%d' % pad
    return start + bytes_used, 'bytes_used'


def scan_superblocks(buf):
    out = []
    for m in MAGICS:
        i = 0
        while True:
            i = buf.find(m, i)
            if i < 0:
                break
            if i + 120 <= len(buf):
                be, le = sb_v3(buf, i, 'BE'), sb_v3(buf, i, 'LE')
                pbe, ple = plausible(be, len(buf)), plausible(le, len(buf))
                endian, f = ('BE', be) if pbe >= ple else ('LE', le)
                tail = buf[i + 28:i + 30]
                handlers = [n for n, mg, tl in UNBLOB if mg == m and tl == tail]
                bytes_used_field = f['bytes_used']
                shifted = False
                out.append({
                    'offset': i,
                    'handler_candidates': handlers,
                    'endian': endian,
                    'plausibility': pbe if endian == 'BE' else ple,
                    'sb': f,
                    'bytes_used_field_shifted': shifted,
                    'bytes_used': bytes_used_field,
                    'carve_len': min(len(buf) - i, bytes_used_field) if bytes_used_field else len(buf) - i,
                    'chunk_end': unblob_chunk_end(buf, i, bytes_used_field)[0] if bytes_used_field else None,
                    'chunk_end_rule': unblob_chunk_end(buf, i, bytes_used_field)[1] if bytes_used_field else None,
                })
            i += 1
    return out


def landmarks(buf):
    out = {}
    for lm in LANDMARKS:
        pos = []
        i = 0
        while len(pos) < 4:
            i = buf.find(lm, i)
            if i < 0:
                break
            pos.append(i)
            i += 1
        if pos:
            out[lm.decode('latin-1')] = pos
    return out


UNSQ_TYPE = re.compile(r'^(s|d|b|c|p|l|w|-)')
UNSQ_LINE = re.compile(r'^(?P<type>\S+)\s+(?P<mode>\S+)\s+(?P<uid>\d+)/(?P<gid>\d+)\s+'
                       r'(?P<size>\d+)\s+(?P<date>\S+ \S+)\s+(?P<path>.*)$')


def unsquashfs_entries(carve):
    """(rc, entries[{path,type,size}], stderr) from `unsquashfs -lls`."""
    rc, out, err = run(['unsquashfs', '-lls', carve])
    entries = []
    for line in out.decode('utf-8', 'replace').splitlines():
        m = UNSQ_LINE.match(line)
        if m:
            t = m.group('type')[:1]
        entries.append({'path': m.group('path'), 'type': 'f' if t == '-' else t,
                        'size': int(m.group('size'))})
    return rc, entries, err.decode('utf-8', 'replace')


def sevenzip_entries(carve):
    """(rc, entries[{path,type,size}], head_lines) from `7z l -slt`."""
    rc, out, err = run(['7z', 'l', '-slt', carve])
    text = out.decode('utf-8', 'replace')
    entries = []
    cur = {}
    for line in text.splitlines():
        if line.startswith('Path = '):
            if cur.get('path') is not None:
                entries.append(cur)
            cur = {'path': line[7:]}
        elif line.startswith('Size = ') and 'size' not in cur:
            v = line[7:].strip()
            cur['size'] = int(v) if v.isdigit() else 0
        elif line.startswith('Folder = '):
            cur['folder'] = line[9:].strip()
        elif line.startswith('Mode = '):
            cur['type'] = line[7:7 + 1]
    if cur.get('path') is not None:
        entries.append(cur)
    out_entries = []
    for e in entries:
        if e['path'].endswith('.sqfs') or not e['path']:
            continue
        t = e.get('type') or ('d' if e.get('folder') == '+' else '-')
        if t == '-':
            t = 'f'
        out_entries.append({'path': e['path'], 'type': t, 'size': e.get('size', 0)})
    head = text.splitlines()[:16]
    return rc, out_entries, head


def sevenzip_meta(carve):
    rc, out, err = run(['7z', 'l', '-slt', carve])
    text = out.decode('utf-8', 'replace')
    keep = {}
    for line in text.splitlines()[:30]:
        if '=' in line:
            k, v = [x.strip() for x in line.split('=', 1)]
            if k in ('Type', 'Physical Size', 'Headers Size', 'Tail Size', 'File System',
                     'Method', 'Cluster Size', 'Big-endian', 'Created', 'Characteristics',
                     'Blocks', 'Code Page'):
                keep[k] = v
    return keep


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('image')
    ap.add_argument('--offset', type=lambda s: int(s, 0), default=None)
    ap.add_argument('--carve-dir', default='.')
    ap.add_argument('--tag', default=None)
    ap.add_argument('--kind', default=None,
                    help='backhand kind for a listing count, e.g. be_v3_0_lzma')
    args = ap.parse_args(argv)

    buf = open(args.image, 'rb').read()
    res = {'image': os.path.abspath(args.image), 'bytes': len(buf), 'sha256': sha(buf),
           'landmarks': landmarks(buf), 'superblocks': scan_superblocks(buf)}
    res['image_head_hex'] = buf[:64].hex()

    pick = None
    if args.offset is not None:
        pick = next((s for s in res['superblocks'] if s['offset'] == args.offset), None)
        if pick is None:
            print(json.dumps({'error': 'no superblock at offset', 'offset': args.offset,
                              'hits': [s['offset'] for s in res['superblocks']]}, indent=1))
            return 2
    elif res['superblocks']:
        pick = max(res['superblocks'], key=lambda s: (s['plausibility'], s['offset']))

    if pick is None:
        res['readers'] = None
        print(json.dumps(res, indent=1))
        return 0

    tag = args.tag or os.path.basename(args.image)
    carve = os.path.join(args.carve_dir, re.sub(r'[^A-Za-z0-9_.-]', '_', tag) + '.' + str(pick['offset']) + '.sqfs')
    carve_end = pick.get('chunk_end') or (pick['offset'] + pick['carve_len'])
    data = buf[pick['offset']:carve_end]
    with open(carve, 'wb') as f:
        f.write(data)
    res['carve'] = {'path': carve, 'bytes': len(data), 'sha256': sha(data),
                    'range': [pick['offset'], pick['offset'] + len(data)]}

    readers = {}
    rc, out, err = run(['unsquashfs', '-s', carve])
    readers['unsquashfs_s'] = {'rc': rc, 'stdout': out.decode('utf-8', 'replace'),
                               'stderr': err.decode('utf-8', 'replace')}
    rc, entries, err = unsquashfs_entries(carve)
    readers['unsquashfs_lls'] = {
        'rc': rc, 'stderr_tail': err.strip().splitlines()[-3:] if err.strip() else [],
        'entries': len(entries),
        'counts': {t: sum(1 for e in entries if e['type'] == t)
                   for t in sorted({e['type'] for e in entries})},
        'regular': sorted(e['path'] for e in entries if e['type'] == 'f'),
        'nonregular': sorted((e['path'], e['type']) for e in entries if e['type'] != 'f'),
    }
    rc, entries7, head7 = sevenzip_entries(carve)
    seen = set()
    uniq = []
    for e in entries7:
        p = e.get('path')
        if p in seen or p is None:
            continue
        seen.add(p)
        uniq.append(e)
    readers['7z'] = {
        'rc': rc, 'meta': sevenzip_meta(carve),
        'entries': len(uniq),
        'counts': {t: sum(1 for e in uniq if e.get('type') == t)
                   for t in sorted({e.get('type') for e in uniq if e.get('type')})},
        'regular': sorted(e['path'] for e in uniq if e.get('type') == 'f'),
        'nonregular': sorted((e['path'], e.get('type')) for e in uniq if e.get('type') != 'f'),
    }
    if args.kind:
        rc, out, err = run([BACKHAND, '-l', '-k', args.kind, carve])
        lines = [l for l in out.decode('utf-8', 'replace').splitlines() if l.strip()]
        readers['backhand'] = {
            'kind': args.kind, 'rc': rc, 'entries': len(lines),
            'stderr_tail': err.decode('utf-8', 'replace').strip().splitlines()[-3:],
            'head': lines[:6],
        }
    a, b = readers['unsquashfs_lls']['regular'], readers['7z']['regular']
    res['readers'] = readers
    res['path_set_compare'] = {
        'unsquashfs_regular': len(a), '7z_regular': len(b),
        'only_unsquashfs': sorted(set(a) - set(b))[:20],
        'only_7z': sorted(set(b) - set(a))[:20],
        'agree': set(a) == set(b),
    }
    print(json.dumps(res, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
