#!/usr/bin/env python3
"""Check the R41-C1Collide hypothesis on the fresh AVM-genuine dev carriers.

For each carrier it asserts, from the REA receipt and the source-tree manifest:

  H1  the depth-0 chunk is `squashfs_v4_*` and no chunk carries
      `extraction_failed`
  H2  every published file path is EXACTLY `<chunk>_extract/<rel>` where <rel>
      is a ground-truth regular file of the source tree (set equality of the
      extract-root-relative sets, both directions)
  H3  no published file path is any ground-truth non-regular path (no symlink,
      device, fifo or socket is ever materialised), and every regular file is
      published
  H4  the superblock is the genuine AVM layout: `sqsh`, v4.0,
      `mkfs_time == bytes_used`, and the first metadata block-length header is
      little-endian (a big-endian read is not a sane block length)

Usage: verify-publish.py --lane LANE --carriers DIR [--receipts ...]
Exit 0 when every carrier holds H1..H4, 1 otherwise, 2 usage.
"""
import argparse
import json
import os
import struct
import sys

# The extract root is the chunk's own staging directory: `<...>_extract`.  See
# score-matchers.py:carrier_root for the receipt evidence that fixes this.


def load_env(path):
    d = json.load(open(path))
    if isinstance(d, dict) and 'data' in d and 'normalized_result' not in d:
        return d['data']
    return d


def manifest_rows(path):
    files, nonreg = set(), set()
    for line in open(path):
        if not line.strip():
            continue
        kind, rel = line.rstrip('\n').split('\t')[:2]
        (files if kind == 'file' else nonreg).add(rel)
    return files, nonreg


def layout(img):
    b = open(img, 'rb').read()
    (mkfs,) = struct.unpack_from('>I', b, 8)
    (bytes_used,) = struct.unpack_from('>Q', b, 40)
    (maj, minr) = struct.unpack_from('>HH', b, 28)
    (itab,) = struct.unpack_from('>Q', b, 64)
    (dtab,) = struct.unpack_from('>Q', b, 72)
    hdr_le, = struct.unpack_from('<H', b, itab)
    hdr_be, = struct.unpack_from('>H', b, itab)
    # the format test c1-counter.py layout_probe uses: the first metadata
    # block's length must land exactly on the next table (identity), which a
    # wrong-endian read almost never does
    return {
        'le_identity': itab + 2 + (hdr_le & ~0x8000) == dtab,
        'be_identity': itab + 2 + (hdr_be & ~0x8000) == dtab,
        'magic': b[:4],
        'version': '%d.%d' % (maj, minr),
        'mkfs_time': mkfs,
        'bytes_used': bytes_used,
        'marker_ok': mkfs == bytes_used,
        'meta_header_le': '0x%04x' % hdr_le,
        'meta_header_be': '0x%04x' % hdr_be,
        'meta_len_le': hdr_le & ~0x8000,
        'meta_len_be': hdr_be & ~0x8000,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--carriers', required=True)
    args = ap.parse_args()
    idx = json.load(open(os.path.join(args.carriers, 'index.json')))
    here = os.path.dirname(os.path.abspath(args.carriers))
    ok_all = True
    for cid, meta in sorted(idx['carriers'].items()):
        rec = os.path.join(here, 'rea-%s.log' % cid)
        if not os.path.exists(rec):
            print('%s: no receipt at %s' % (cid, rec))
            ok_all = False
            continue
        env = load_env(rec)
        nr = env.get('normalized_result') or {}
        files, nonreg = manifest_rows(meta['manifest'])
        chunks = nr.get('chunks') or []
        depth0 = [c for c in chunks
                  if c.get('input_path') == '$input'
                  and str(c.get('handler') or '').startswith('squashfs_v4')]
        h1 = bool(depth0) and not any(c.get('extraction_failed') for c in chunks)
        paths = [f['relative_path'] for f in (nr.get('files') or [])]
        roots = {p.split('/')[0] for p in paths}
        root = roots.pop() if len(roots) == 1 else None
        rels = {p.split('/', 1)[1] for p in paths if root and p.startswith(root + '/')}
        h2 = (root is not None and root.endswith('_extract')
              and len(rels) == len(paths) and rels == files)
        leaked = sorted(rels & nonreg)
        h3 = not leaked and not (files - rels)
        lay = layout(meta['path'])
        h4 = (lay['magic'] == b'sqsh' and lay['version'] == '4.0'
              and lay['marker_ok'] and lay['le_identity']
              and not lay['be_identity'])
        verdict = h1 and h2 and h3 and h4
        ok_all = ok_all and verdict
        print('%s\t%s\troot=%s published=%d truth_files=%d truth_nonreg=%d '
              'leaked=%r handler=%r layout=%s'
              % (cid, 'HOLDS' if verdict else 'BROKEN', root, len(paths),
                 len(files), len(nonreg), leaked,
                 [c.get('handler') for c in chunks],
                 'sqsh/v%s/marker=%s/le_len=%d(identity=%s)/be_len=%d(identity=%s)'
                 % (lay['version'], lay['marker_ok'], lay['meta_len_le'],
                    lay['le_identity'], lay['meta_len_be'], lay['be_identity'])))
        for name, cond in (('H1 depth0 squashfs, no failure', h1),
                           ('H2 exact root+rel set equality', h2),
                           ('H3 no non-regular published, no missing file', h3),
                           ('H4 AVM marker + LE metadata header', h4)):
            print('    %-48s %s' % (name, 'ok' if cond else 'FAIL'))
        if rels != files:
            print('    only in receipt: %r' % sorted(rels - files)[:5])
            print('    only in tree   : %r' % sorted(files - rels)[:5])
    return 0 if ok_all else 1


if __name__ == '__main__':
    sys.exit(main())
