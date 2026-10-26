#!/usr/bin/env python3
"""Compare sasquatch-v4be (no -be) extraction and REA publication with the frozen oracle tables."""
import hashlib
import json
import os
import stat
import struct
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
S = '/fast/scratch/hyaku/kaidoku-r40/R40W2ReproL'


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def read_tsv(p):
    rows = []
    with open(p) as fh:
        for line in fh:
            line = line.rstrip('\n')
            if not line:
                continue
            rows.append(line.split('\t'))
    return rows


def tree_scan(root):
    files, links, dirs, other = {}, {}, {}, {}
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root)
        for d in dirnames:
            rel = d if rel_dir == '.' else rel_dir + '/' + d
            dirs[rel] = True
        for f in filenames:
            p = os.path.join(dirpath, f)
            rel = f if rel_dir == '.' else rel_dir + '/' + f
            st = os.lstat(p)
            if stat.S_ISLNK(st.st_mode):
                links[rel] = os.readlink(p)
            elif stat.S_ISREG(st.st_mode):
                files[rel] = (sha256_file(p), st.st_size)
            else:
                other[rel] = oct(st.st_mode)
    return files, links, dirs, other


def rel_suffix(path):
    if path is None:
        return None
    parts = [p for p in path.split('/') if p not in ('', '.')]
    for i, part in enumerate(parts):
        if part.endswith('_extract') and i + 1 < len(parts):
            return '/'.join(parts[i + 1:])
    return '/'.join(parts)


for cid in ('L1', 'L2'):
    print('=' * 72)
    print('CARRIER', cid)
    base = os.path.join(LANE, 'corpus/evidence/round-40/c1', cid)
    oracle = read_tsv(os.path.join(base, 'oracle.tsv'))
    nonreg = read_tsv(os.path.join(base, 'nonregular.tsv'))
    o_map = {r[0]: (r[1], int(r[2])) for r in oracle}
    n_map = {r[0]: (r[1], r[2] if len(r) > 2 else '') for r in nonreg}
    print('oracle rows=%d nonregular rows=%d' % (len(o_map), len(n_map)))

    # 1) sasquatch-v4be (no -be) extraction
    root = os.path.join(S, 'sq', cid + '-nobe', 'root')
    files, links, dirs, other = tree_scan(root)
    print('-- sasquatch(no -be): regular=%d symlinks=%d dirs=%d other=%d'
          % (len(files), len(links), len(dirs), len(other)))
    print('   files == oracle.tsv :', files == o_map,
          '| only_oracle:', sorted(set(o_map) - set(files)),
          '| only_extract:', sorted(set(files) - set(o_map)),
          '| hash/size mismatches:', sorted(k for k in set(files) & set(o_map) if files[k] != o_map[k]))
    nr_extract = dict(n_map)
    for rel in dirs:
        if rel not in nr_extract:
            nr_extract[rel] = ('dir', '')
    link_norm = {}
    for rel, target in links.items():
        link_norm[rel] = target
    # absolute targets are re-rooted by unsquashfs -d; compare on either raw or re-rooted form
    mism = []
    for rel, tgt in link_norm.items():
        exp = nr_extract.get(rel)
        if not exp or exp[0] != 'symlink':
            mism.append((rel, 'missing-or-kind', tgt, exp))
        elif tgt != exp[1] and not (exp[1].startswith('/') and tgt.lstrip('./') == exp[1].lstrip('/')):
            mism.append((rel, 'target', tgt, exp[1]))
    extra = sorted(set(nr_extract) - set(link_norm) - set(dirs))
    print('   nonregular cross-check mismatches:', mism, '| table-only entries:', extra)
    print('   nonregular: dirs_table=%d links_table=%d; extract dirs=%d links=%d'
          % (sum(1 for v in n_map.values() if v[0] == 'dir'),
             sum(1 for v in n_map.values() if v[0] == 'symlink'), len(dirs), len(links)))

    # 2) REA publication vs oracle
    nr = json.load(open(os.path.join(S, 'rea-%s/stdout.json' % cid)))['data']['normalized_result']
    pub = {}
    for e in nr.get('files') or []:
        pub[rel_suffix(e.get('relative_path'))] = (e.get('sha256'), e.get('size'))
    print('-- REA published files=%d; == oracle.tsv: %s; only_oracle=%s only_pub=%s mismatches=%s'
          % (len(pub), pub == o_map, sorted(set(o_map) - set(pub)),
             sorted(set(pub) - set(o_map)),
             sorted(k for k in set(pub) & set(o_map) if pub[k] != o_map[k])))

    # 3) superblock, independent BE read + AVM marker + metadata block-length endianness
    p = os.path.join(base, 'carrier.sqsh')
    with open(p, 'rb') as fh:
        sb = fh.read(96)
    (magic, inodes, mkfs, block_size, frags, comp, block_log, flags, no_ids, s_major,
     s_minor, root_inode, bytes_used, id_start, xattr_start, inode_start, dir_start,
     frag_start, lookup_start) = struct.unpack('>IIIIIHHHHHHQQQQQQQQ', sb)
    print('-- superblock: magic=%r inodes=%d mkfs_time=%d bytes_used=%d avm_marker=%s s=%d.%d comp=%d'
          % (struct.pack('>I', magic), inodes, mkfs, bytes_used, mkfs == bytes_used,
             s_major, s_minor, comp))
    with open(p, 'rb') as fh:
        fh.seek(inode_start)
        hdr = fh.read(2)
    le = struct.unpack('<H', hdr)[0]
    be = struct.unpack('>H', hdr)[0]
    le_sz, be_sz = le & 0x7FFF, be & 0x7FFF
    print('-- metadata block header at inode_table_start=%d: bytes=%s | LE raw=%d (uncompressed=%s, size=%d) '
          '| BE raw=%d (uncompressed=%s, size=%d) | size<=8192: LE=%s BE=%s (decisive test: cmp3.py)'
          % (inode_start, hdr.hex(), le, bool(le & 0x8000), le_sz, be, bool(be & 0x8000), be_sz,
             le_sz <= 8192, be_sz <= 8192))
