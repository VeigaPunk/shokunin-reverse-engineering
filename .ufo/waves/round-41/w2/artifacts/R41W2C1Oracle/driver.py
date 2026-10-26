#!/usr/bin/env python3
"""R41W2C1Oracle driver: rebuild oracle tables for V3/V4/L3/L4 and cross-check.

For each carrier:
  1. frozen reader --layout avm  -> oracle.tsv / nonregular.tsv / inspect.json
  2. frozen reader --layout auto -> oracle-auto.tsv / nonregular-auto.tsv / inspect-auto.json
  3. direct sasquatch-v4be (NO -be) extraction -> root/, then list regular files
     (relpath, sha256, size) + symlink count
Outputs land under <out>/<id>/; a separate comparator diffs against the
committed tables in the lane.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

SQFS_LIST = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-41/sqfs-list.py'
SASQUATCH = os.path.expanduser('~/.local/bin/sasquatch-v4be')

CARRIERS = {
    'V3': '/fast/scratch/hyaku/kaidoku-r41/R41W2C1Oracle/cache/c4f74f54a65e861e22f5d6a47977cdbb3b5345819174f33bc86c63d3d10f872a.bin',
    'V4': '/fast/scratch/hyaku/kaidoku-r41/R41W2C1Oracle/cache/ce27ebca903a1574465ddfa0626943339ce6bc8155f31f88d04049afb570087f.bin',
    'L3': '/fast/scratch/hyaku/kaidoku-r41/R41W2C1Oracle/lcar/L3/carrier.sqsh',
    'L4': '/fast/scratch/hyaku/kaidoku-r41/R41W2C1Oracle/lcar/L4/carrier.sqsh',
}
PINS = {
    'V3': 'c4f74f54a65e861e22f5d6a47977cdbb3b5345819174f33bc86c63d3d10f872a',
    'V4': 'ce27ebca903a1574465ddfa0626943339ce6bc8155f31f88d04049afb570087f',
    'L3': '04cfb4cd6189742eaba94d0022d242d4194726a6f0684fd8381b39bc4e6c45a3',
    'L4': '4c0e545975d2993f5b3417d55990a5df5ad67fa2f21164b831119f6e85cbcfbc',
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def run(argv, cwd=None):
    p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def magic_offset(path):
    with open(path, 'rb') as fh:
        raw = fh.read(1 << 20)
    be = raw.find(b'sqsh')
    le = raw.find(b'hsqs')
    if be >= 0 and (le < 0 or be <= le):
        return 'sqsh', be
    if le >= 0:
        return 'hsqs', le
    return 'none', -1


def list_extract(root):
    """Regular files: (relpath, sha256, size); symlink count."""
    files = []
    symlinks = 0
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        for name in sorted(dirnames) + sorted(filenames):
            p = os.path.join(dirpath, name)
            rel = os.path.relpath(p, root).replace(os.sep, '/')
            if os.path.islink(p):
                symlinks += 1
                continue
            if not os.path.isfile(p):
                continue
            files.append((rel, sha256_file(p), os.path.getsize(p)))
    files.sort(key=lambda r: r[0].encode('utf-8', 'surrogateescape'))
    return files, symlinks


def write_tsv(path, rows):
    with open(path, 'w', encoding='utf-8', newline='\n') as fh:
        for row in rows:
            fh.write('\t'.join(str(x) for x in row) + '\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('outdir')
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)

    # sasquatch version pin
    rc, out, err = run([SASQUATCH, '-version'])
    sq_line = (out or err).splitlines()[0] if (out or err) else ''

    for cid, path in CARRIERS.items():
        d = os.path.join(a.outdir, cid)
        os.makedirs(d, exist_ok=True)
        rec = {'id': cid, 'carrier_path': path,
               'sha256': sha256_file(path),
               'size': os.path.getsize(path),
               'pin_matches': sha256_file(path) == PINS[cid]}
        magic, off = magic_offset(path)
        rec['magic'] = magic
        rec['magic_offset'] = off

        # 1: frozen reader --layout avm
        rc, out, err = run(['python3', '-I', '-B', SQFS_LIST, '--layout', 'avm',
                            '--files', os.path.join(d, 'oracle.tsv'),
                            '--nonregular', os.path.join(d, 'nonregular.tsv'),
                            '--inspect', path])
        rec['reader_avm_exit'] = rc
        rec['reader_avm_stderr_tail'] = err.strip().splitlines()[-3:] if err else []
        if rc == 0:
            with open(os.path.join(d, 'inspect-avm.json'), 'w') as fh:
                fh.write(out)
            rec['reader_avm_inspect'] = json.loads(out)
        # 2: frozen reader --layout auto
        rc, out, err = run(['python3', '-I', '-B', SQFS_LIST, '--layout', 'auto',
                            '--files', os.path.join(d, 'oracle-auto.tsv'),
                            '--nonregular', os.path.join(d, 'nonregular-auto.tsv'),
                            '--inspect', path])
        rec['reader_auto_exit'] = rc
        rec['reader_auto_stderr_tail'] = err.strip().splitlines()[-3:] if err else []
        if rc == 0:
            with open(os.path.join(d, 'inspect-auto.json'), 'w') as fh:
                fh.write(out)
            rec['reader_auto_inspect'] = json.loads(out)
        # 3: sasquatch-v4be direct extraction (NO -be)
        root = os.path.join(d, 'root')
        os.makedirs(root, exist_ok=True)
        sq_argv = [SASQUATCH, '-f', '-no-exit-code', '-n']
        if off != 0:
            sq_argv += ['-o', str(off)]
        sq_argv += ['-d', root, path]
        rc, out, err = run(sq_argv)
        rec['sq_argv'] = sq_argv
        rec['sq_exit'] = rc
        rec['sq_log_tail'] = (out + err).strip().splitlines()[-5:] if (out or err) else []
        if rc == 0:
            files, symlinks = list_extract(root)
            write_tsv(os.path.join(d, 'extract-files.tsv'), files)
            rec['extract_regular_files'] = len(files)
            rec['extract_symlinks'] = symlinks
        with open(os.path.join(d, 'rec.json'), 'w') as fh:
            json.dump(rec, fh, indent=1, sort_keys=True)
        print(cid, 'sha256=%s pin=%s' % (rec['sha256'], rec['pin_matches']),
              'magic=%s@%d' % (magic, off),
              'reader_avm=%d reader_auto=%d sq=%d' % (rec['reader_avm_exit'],
                                                      rec['reader_auto_exit'],
                                                      rec['sq_exit']))
    print('sq_version_line:', sq_line)
    print('sq_sha256:', sha256_file(SASQUATCH))
    return 0


if __name__ == '__main__':
    sys.exit(main())
