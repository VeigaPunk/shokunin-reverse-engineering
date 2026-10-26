#!/usr/bin/env python3
"""make-dev-images.py -- build the round-40 development AVM-genuine images with
gen-squashfs.py (same directory), verify each with sasquatch-v4be without
`-be`, and emit a manifest of image sha256s.

These are DEVELOPMENT images. They are not C1 carriers (no REA or unblob run
was made on any of them except the two throwaway dev checks recorded in the
seat report, which used copies built here).

Usage:
  python3 make-dev-images.py --work DIR --out DIR [--sasquatch PATH]

--work is where the trees and sasquatch outputs live (honours TMPDIR when
omitted); --out receives the .sqsh images and manifest.tsv. Exit 0 iff every
image extracts to files whose sha256s equal the source tree.
"""
import argparse
import hashlib
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile


def load_writer():
    here = os.path.dirname(os.path.abspath(__file__))
    p = os.path.join(here, 'gen-squashfs.py')
    spec = importlib.util.spec_from_file_location('gen_squashfs', p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def files_of(tree):
    out = {}
    for root, _d, fns in os.walk(tree):
        for fn in fns:
            p = os.path.join(root, fn)
            if not os.path.islink(p):
                out[os.path.relpath(p, tree)] = sha(p)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work')
    ap.add_argument('--out', required=True)
    ap.add_argument('--sasquatch', default='sasquatch-v4be')
    a = ap.parse_args()
    g = load_writer()
    work = a.work or tempfile.mkdtemp(prefix='sqfs-dev-',
                                      dir=os.environ.get('TMPDIR'))
    os.makedirs(work, exist_ok=True)
    os.makedirs(a.out, exist_ok=True)
    rows = []
    tree_manifest = []
    ok_all = True
    for tname, entries in g._tree_specs().items():
        tree = os.path.join(work, 'tree-' + tname)
        shutil.rmtree(tree, ignore_errors=True)
        os.makedirs(tree)
        g._populate(tree, entries)
        want = files_of(tree)
        for rel, h in sorted(want.items()):
            tree_manifest.append(f'{tname}\t{rel}\t{h}')
        for comp in ('gzip', 'xz'):
            name = f'{tname}-{comp}-avm-genuine.sqsh'
            img = os.path.join(a.out, name)
            g.build_image(tree, img, 'avm-genuine', comp)
            ex = os.path.join(work, 'ex-' + name)
            shutil.rmtree(ex, ignore_errors=True)
            r = subprocess.run([a.sasquatch, '-f', '-d', ex, img],
                               cwd=work, capture_output=True, text=True)
            got = files_of(ex) if os.path.isdir(ex) else {}
            ok = r.returncode == 0 and got == want
            ok_all = ok_all and ok
            b = open(img, 'rb').read()
            import struct
            mkfs = struct.unpack_from('>I', b, 8)[0]
            used = struct.unpack_from('>Q', b, 40)[0]
            itab = struct.unpack_from('>Q', b, 64)[0]
            dtab = struct.unpack_from('>Q', b, 72)[0]
            hdr = struct.unpack_from('<H', b, itab)[0]
            le_end = g._walk_meta(b, itab, dtab, 'le')
            be_end = g._walk_meta(b, itab, dtab, 'be')
            rows.append(dict(image=name, bytes=len(b), sha256=sha(img),
                             comp=comp, mode='avm-genuine', tree=tname,
                             files=len(want), sasquatch_exit=r.returncode,
                             extract_ok=ok, mkfs_time=mkfs,
                             bytes_used=used,
                             marker=mkfs == used,
                             inode_table=itab, dir_table=dtab,
                             first_hdr_le=hdr & 0x7fff,
                             le_walk_end=le_end, le_walk_lands=le_end == dtab,
                             be_walk_end=be_end, be_walk_lands=be_end == dtab,
                             hdr_uncompressed=bool(hdr & 0x8000)))
            print(f'{"OK  " if ok else "FAIL"} {name} {len(b)} B '
                  f'sha256 {rows[-1]["sha256"]} files {len(got)}/{len(want)} '
                  f'sasquatch exit {r.returncode}')
    with open(os.path.join(a.out, 'manifest.tsv'), 'w') as f:
        cols = list(rows[0])
        f.write('\t'.join(cols) + '\n')
        for row in rows:
            f.write('\t'.join(str(row[c]) for c in cols) + '\n')
    with open(os.path.join(a.out, 'tree-files.tsv'), 'w') as f:
        f.write('tree\tpath\tsha256\n')
        f.write('\n'.join(tree_manifest) + '\n')
    print('manifest.tsv and tree-files.tsv written to', a.out)
    return 0 if ok_all else 1


if __name__ == '__main__':
    sys.exit(main())
