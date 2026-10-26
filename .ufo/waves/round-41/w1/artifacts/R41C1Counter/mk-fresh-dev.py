#!/usr/bin/env python3
"""Build one FRESH AVM-genuine dev carrier plus its independent oracle.

The round-41 C1 dry run cannot use the round-40 carriers as "new coverage": the
counter's `carrier_fresh_ok` clause refuses a pin a previous freeze scored (that
is the claim's relabel kill rule). This builds a small deterministic tree, writes
it as an AVM-genuine SquashFS v4 image with the lane writer, and derives the
oracle independently of that writer with sasquatch-v4be - the same two-tool
discipline the claim uses.

Usage:
  mk-fresh-dev.py --gen <tools/round-40/gen-squashfs.py> --out DIR
                  [--sasquatch ~/.local/bin/sasquatch-v4be] [--comp xz|gzip]
Prints one JSON object: carrier sha256/size, oracle.tsv and nonregular.tsv paths
and row counts. Writes only inside --out.
"""
import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys

# Deterministic payloads: a text file, a binary blob and a library-sized blob, so
# the oracle is not the degenerate all-zeros digest of a scrubber.
TREE = {
    'etc/version': (b'FRITZ!OS 07.90-000000\n' * 4, None),
    'usr/bin/tool': (bytes((i * 37 + 11) & 0xff for i in range(3000)), None),
    'var/lib/data': (bytes((i * 91 + 7) & 0xff for i in range(5000)), None),
    'bin/tool': (None, '../usr/bin/tool'),
}


def build_tree(root):
    for rel, (data, target) in sorted(TREE.items()):
        full = os.path.join(root, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        if target is not None:
            os.symlink(target, full)
        else:
            with open(full, 'wb') as fh:
                fh.write(data)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--gen', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--sasquatch', default=os.path.expanduser('~/.local/bin/sasquatch-v4be'))
    ap.add_argument('--comp', default='xz', choices=('xz', 'gzip'))
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    tree = os.path.join(a.out, 'tree')
    build_tree(tree)
    image = os.path.join(a.out, 'dev-avm-be.sqsh')
    p = subprocess.run([sys.executable, '-I', '-B', a.gen, tree, image,
                        '--endian', 'avm-genuine', '--comp', a.comp],
                       capture_output=True)
    if p.returncode != 0:
        raise SystemExit('gen-squashfs failed: ' + p.stderr.decode()[:400])
    raw = open(image, 'rb').read()
    # independent oracle
    oracle_dir = os.path.join(a.out, 'oracle')
    os.makedirs(oracle_dir, exist_ok=True)
    q = subprocess.run([a.sasquatch, '-f', '-d', oracle_dir, image], capture_output=True)
    if q.returncode != 0:
        raise SystemExit('sasquatch failed: ' + q.stderr.decode()[:400])
    files, nonreg = [], []
    for dirpath, _dirs, names in os.walk(oracle_dir):
        for name in sorted(names):
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, oracle_dir).replace(os.sep, '/')
            st = os.lstat(full)
            if stat.S_ISLNK(st.st_mode):
                nonreg.append((rel, 'symlink', os.readlink(full)))
            elif stat.S_ISREG(st.st_mode):
                data = open(full, 'rb').read()
                files.append((rel, hashlib.sha256(data).hexdigest(), len(data)))
            elif stat.S_ISDIR(st.st_mode):
                nonreg.append((rel, 'dir', ''))
    files.sort()
    nonreg.sort()
    oracle_tsv = os.path.join(a.out, 'oracle.tsv')
    nonreg_tsv = os.path.join(a.out, 'nonregular.tsv')
    with open(oracle_tsv, 'w') as fh:
        for rel, sha, size in files:
            fh.write('%s\t%s\t%d\n' % (rel, sha, size))
    with open(nonreg_tsv, 'w') as fh:
        for rel, kind, detail in nonreg:
            fh.write('%s\t%s\t%s\n' % (rel, kind, detail))
    print(json.dumps({'carrier': image,
                      'sha256': hashlib.sha256(raw).hexdigest(),
                      'size': len(raw),
                      'compression': a.comp,
                      'oracle': oracle_tsv, 'oracle_rows': len(files),
                      'nonregular': nonreg_tsv, 'nonregular_rows': len(nonreg),
                      'sasquatch_rc': q.returncode}, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
