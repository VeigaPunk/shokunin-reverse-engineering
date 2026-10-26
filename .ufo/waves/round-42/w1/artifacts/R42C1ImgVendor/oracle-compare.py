#!/usr/bin/env python3
"""Two-producer oracle compare for a SquashFS v3 carrier carve.

Producer A: backhand `unsquashfs-backhand` (`-k <kind> -d DIR`), the L1-built
v3/LZMA-capable tool (0.25.5, features v3,gzip,lzma,xz).
Producer B: 7-Zip 26.04 (`7z x -oDIR`, `7z l -slt`).

Both trees are extracted into scratch and walked without following links; the
report compares, per path: kind (regular / symlink / dir) and sha256 of regular
file contents, plus symlink targets.

Usage: oracle-compare.py <carve.sqfs> <kind> <workdir>
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

BACKHAND = '/home/vgpnk/.local/opt/backhand-0.25.5-v3/bin/unsquashfs-backhand'


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def walk(root):
    """{rel: {kind, sha256?|target?}} for a extracted tree (no link following)."""
    out = {}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        for name in dirnames + filenames:
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)
            if os.path.islink(full):
                out[rel] = {'kind': 'link', 'target': os.readlink(full)}
            elif os.path.isdir(full):
                out[rel] = {'kind': 'dir'}
            elif os.path.isfile(full):
                out[rel] = {'kind': 'file', 'sha256': sha_file(full), 'size': os.path.getsize(full)}
            else:
                out[rel] = {'kind': 'other'}
    return out


def main(argv):
    carve, kind, work = argv[1], argv[2], argv[3]
    a_dir = os.path.join(work, 'bh')
    b_dir = os.path.join(work, '7z')
    shutil.rmtree(a_dir, ignore_errors=True)
    shutil.rmtree(b_dir, ignore_errors=True)
    ra = subprocess.run([BACKHAND, '-k', kind, '-d', a_dir, '-f', carve],
                        capture_output=True)
    rb = subprocess.run(['7z', 'x', '-bd', '-y', '-o' + b_dir, carve], capture_output=True)
    A, B = walk(a_dir), walk(b_dir)
    a_files = {k: v for k, v in A.items() if v['kind'] == 'file'}
    b_files = {k: v for k, v in B.items() if v['kind'] == 'file'}
    agree = [p for p in a_files if p in b_files and a_files[p]['sha256'] == b_files[p]['sha256']]
    mismatch = [p for p in a_files if p in b_files and a_files[p]['sha256'] != b_files[p]['sha256']]
    a_links = {k: v['target'] for k, v in A.items() if v['kind'] == 'link'}
    b_links = {k: v['target'] for k, v in B.items() if v['kind'] == 'link'}
    res = {
        'carve': carve, 'kind': kind,
        'backhand': {'rc': ra.returncode, 'stderr_tail':
                     ra.stderr.decode('utf-8', 'replace').strip().splitlines()[-4:]},
        '7z': {'rc': rb.returncode, 'stderr_tail':
               rb.stderr.decode('utf-8', 'replace').strip().splitlines()[-4:]},
        'counts': {
            'backhand': {k: sum(1 for v in A.values() if v['kind'] == k)
                         for k in ('file', 'link', 'dir', 'other')},
            '7z': {k: sum(1 for v in B.values() if v['kind'] == k)
                   for k in ('file', 'link', 'dir', 'other')},
        },
        'regular_files': {'backhand': len(a_files), '7z': len(b_files),
                          'agree_path_sha256': len(agree),
                          'sha256_mismatch': mismatch[:20],
                          'only_backhand': sorted(set(a_files) - set(b_files))[:20],
                          'only_7z': sorted(set(b_files) - set(a_files))[:20],
                          'path_sets_equal': set(a_files) == set(b_files),
                          'all_contents_equal': len(agree) == len(a_files) == len(b_files)},
        'symlinks': {'backhand': len(a_links), '7z': len(b_links),
                     'targets_equal': a_links == b_links,
                     'only_backhand': sorted(set(a_links) - set(b_links))[:20],
                     'only_7z': sorted(set(b_links) - set(a_links))[:20]},
    }
    print(json.dumps(res, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
