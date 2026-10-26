#!/usr/bin/env python3
"""TEST DOUBLE, not the oracle. Stands in for the round-40 reader while
R40C1Reader's sqfs-list.py is still being written, so the harness arms
(argument contract, table grammar, cross-check comparison, run.json) can be
exercised now. It derives both tables from `sasquatch-v4be -f` (NO -be)
extraction, i.e. from the same extractor the harness cross-check uses: the
comparison is therefore trivially equal and proves nothing about AVM-layout
decoding. It must never be frozen or cited as an independent oracle.

Contract copied from R40C1Reader: --layout {auto,le,be,avm} (required),
--files OUT, --nonregular OUT, --inspect, IMAGE positional; exit 0 ok,
2 unreadable/unsupported.
"""
import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def main(argv):
    ap = argparse.ArgumentParser(
        description='TEST DOUBLE reader (sasquatch-backed); --layout, --files, '
                    '--nonregular, --inspect')
    ap.add_argument('--layout', choices=('auto', 'le', 'be', 'avm'), required=True)
    ap.add_argument('--files', required=True)
    ap.add_argument('--nonregular')
    ap.add_argument('--inspect', action='store_true')
    ap.add_argument('image')
    a = ap.parse_args(argv)

    if a.layout != 'avm':
        print('test-double: only --layout avm is implemented, got %r' % a.layout,
              file=sys.stderr)
        return 2
    sq = shutil.which('sasquatch-v4be')
    if not sq:
        print('test-double: sasquatch-v4be not on PATH', file=sys.stderr)
        return 2

    tmp = tempfile.mkdtemp(prefix='td-reader.')
    root = os.path.join(tmp, 'root')
    os.mkdir(root)
    try:
        p = subprocess.run([sq, '-f', '-no-exit-code', '-n', '-d', root, a.image],
                           cwd=tmp, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if p.returncode != 0:
            sys.stderr.write(p.stderr.decode('utf-8', 'replace')[:800])
            print('test-double: sasquatch-v4be exited %d' % p.returncode, file=sys.stderr)
            return 2
        files, nonreg = [], []
        for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
            for name in dirnames + filenames:
                path = os.path.join(dirpath, name)
                rel = os.path.relpath(path, root).replace(os.sep, '/')
                st = os.lstat(path)
                if stat.S_ISLNK(st.st_mode):
                    nonreg.append((rel, 'symlink', os.readlink(path)))
                elif stat.S_ISDIR(st.st_mode):
                    nonreg.append((rel, 'dir', ''))
                elif stat.S_ISREG(st.st_mode):
                    files.append((rel, sha256(path), str(st.st_size)))
                elif stat.S_ISFIFO(st.st_mode):
                    nonreg.append((rel, 'fifo', ''))
                elif stat.S_ISSOCK(st.st_mode):
                    nonreg.append((rel, 'socket', ''))
                elif stat.S_ISCHR(st.st_mode):
                    nonreg.append((rel, 'char-device',
                                   '%d:%d' % (os.major(st.st_rdev), os.minor(st.st_rdev))))
                elif stat.S_ISBLK(st.st_mode):
                    nonreg.append((rel, 'block-device',
                                   '%d:%d' % (os.major(st.st_rdev), os.minor(st.st_rdev))))
        key = lambda r: r[0].encode('utf-8', 'surrogateescape')
        files.sort(key=key)
        nonreg.sort(key=key)
        with open(a.files, 'w', encoding='utf-8', newline='\n') as fh:
            for rel, digest, size in files:
                fh.write('%s\t%s\t%s\n' % (rel, digest, size))
        if a.nonregular:
            with open(a.nonregular, 'w', encoding='utf-8', newline='\n') as fh:
                for rel, kind, detail in nonreg:
                    fh.write('%s\t%s\t%s\n' % (rel, kind, detail))
        if a.inspect:
            json.dump({'layout': 'avm', 'test_double': True,
                       'extractor': sq, 'regular_files': len(files),
                       'nonregular_entries': len(nonreg)}, sys.stdout, indent=1)
            sys.stdout.write('\n')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
