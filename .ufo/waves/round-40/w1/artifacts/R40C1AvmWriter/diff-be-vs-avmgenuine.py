#!/usr/bin/env python3
"""diff-be-vs-avmgenuine.py -- prove that `--endian avm-genuine` differs from
`--endian be` on the same tree ONLY in (a) the superblock mkfs_time field at
bytes 8..12 (set to bytes_used, the AVM marker) and (b) the 2-byte metadata
block-length headers, which flip from big- to little-endian.

For every --selftest tree it builds both images, walks the `be` image's
metadata tables to collect every 2-byte header position (inode, directory and
id tables), and asserts:

    set(differing byte offsets) == {8,9,10,11} union {header positions}

It also prints the header raw bytes and both decodings for the first block of
each table, so the endianness flip is visible.

Usage: python3 diff-be-vs-avmgenuine.py [--json OUT]
Exit 0 iff every tree satisfies the identity above; 1 otherwise.
"""
import argparse
import importlib.util
import json
import os
import shutil
import struct
import sys
import tempfile


def load_writer():
    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(
        'gen_squashfs', os.path.join(here, 'gen-squashfs.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def header_positions(g, b):
    """All 2-byte metadata header offsets of the image, using each table's walk
    with the header endianness the image actually uses."""
    it = struct.unpack_from('>Q', b, 64)[0]
    dt = struct.unpack_from('>Q', b, 72)[0]
    id_lookup = struct.unpack_from('>Q', b, 48)[0]
    id_meta = struct.unpack_from('>Q', b, id_lookup)[0]
    # decide by walking: use the endianness that lands exactly on the table end
    e = None
    for cand in ('le', 'be'):
        if g._walk_meta(b, it, dt, cand) == dt:
            e = cand
            break
    if e is None:
        raise SystemExit('inode table headers walk past dir_table under both '
                         'endiannesses')
    starts = (g._block_starts(b, it, dt, e) +
              g._block_starts(b, dt, id_meta, e) +
              g._block_starts(b, id_meta, id_lookup, e))
    return e, starts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json')
    a = ap.parse_args()
    g = load_writer()
    work = tempfile.mkdtemp(prefix='sqfs-diff-', dir=os.environ.get('TMPDIR'))
    out = []
    ok_all = True
    try:
        for tname, entries in g._tree_specs().items():
            tree = os.path.join(work, 'tree-' + tname)
            os.makedirs(tree, exist_ok=True)
            g._populate(tree, entries)
            be_img = os.path.join(work, tname + '-be.sqsh')
            av_img = os.path.join(work, tname + '-avm-genuine.sqsh')
            g.build_image(tree, be_img, 'be', 'gzip')
            g.build_image(tree, av_img, 'avm-genuine', 'gzip')
            b = open(be_img, 'rb').read()
            v = open(av_img, 'rb').read()
            if len(b) != len(v):
                print(f'{tname}: FAIL length differs {len(b)} != {len(v)}')
                ok_all = False
                continue
            diff = {i for i in range(len(b)) if b[i] != v[i]}
            hdr_e, starts = header_positions(g, v)
            hdr_bytes = set()
            for s in starts:
                hdr_bytes.update((s, s + 1))
            expected = hdr_bytes | {8, 9, 10, 11}
            extra = diff - expected
            missing = expected - diff
            # the marker must hold and the field difference must be exactly it
            mkfs_be = struct.unpack_from('>I', b, 8)[0]
            mkfs_av = struct.unpack_from('>I', v, 8)[0]
            used = struct.unpack_from('>Q', v, 40)[0]
            row = dict(tree=tname, bytes=len(b),
                       header_endianness=hdr_e,
                       header_count=len(starts),
                       differing=len(diff),
                       diff_outside_headers_and_mkfs=sorted(extra),
                       expected_offsets_not_differing=sorted(missing),
                       mkfs_time_be=mkfs_be, mkfs_time_avm=mkfs_av,
                       bytes_used=used, marker=mkfs_av == used,
                       superblock_identical_except_mkfs=
                           b[:8] == v[:8] and b[12:96] == v[12:96],
                       headers=[dict(off=s,
                                     be_raw=b[s:s + 2].hex(),
                                     avm_raw=v[s:s + 2].hex(),
                                     be_len=struct.unpack_from('>H', b, s)[0] & 0x7FFF,
                                     avm_len=struct.unpack_from('<H', v, s)[0] & 0x7FFF)
                                for s in starts[:4]])
            ok = (not extra and not missing and row['marker'] and
                  row['superblock_identical_except_mkfs'] and hdr_e == 'le')
            ok_all = ok_all and ok
            print(f'{"PASS" if ok else "FAIL"} {tname}: bytes {len(b)}, '
                  f'headers {len(starts)} ({hdr_e}), differing {len(diff)}, '
                  f'outside header/mkfs set {len(extra)}, mkfs be={mkfs_be} '
                  f'avm={mkfs_av} bytes_used={used}')
            for h in row['headers'][:2]:
                print(f'    hdr @{h["off"]}: be raw={h["be_raw"]} '
                      f'(len {h["be_len"]}) -> avm raw={h["avm_raw"]} '
                      f'(len {h["avm_len"]})')
            out.append(row)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    if a.json:
        with open(a.json, 'w') as f:
            json.dump(out, f, indent=1)
    print(f'\n{sum(1 for r in out if True)} trees compared; '
          f'{"all" if ok_all else "NOT all"} satisfy '
          f'diff == headers + mkfs_time')
    return 0 if ok_all else 1


if __name__ == '__main__':
    sys.exit(main())
