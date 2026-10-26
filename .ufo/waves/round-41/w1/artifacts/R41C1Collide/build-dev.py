#!/usr/bin/env python3
"""Build fresh AVM-genuine dev carriers for R41-C1Collide (NOT the reserved L3/L4).

Four carriers, all written by tools/round-40/gen-squashfs.py --endian avm-genuine:

  A-xz   regular usr/bin/busy  + symlink bin/busy -> ../usr/bin/busy
         (regular path is DEEPER than the symlink path: symlink path is a suffix
          of the regular path -- the R40-CL1 direction)
  A-gz   the same tree, gzip, to show the compressor does not change publication
  B-xz   symlink usr/sbin/tool -> /sbin/tool + regular sbin/tool
         (symlink path is DEEPER than the regular path: reverse direction)
  C-xz   regular opt/x/etc/conf + regular etc/conf, SAME bytes
         (two regular files, one path a suffix of the other, identical sha:
          the oracle-shadow direction)

Contents are sha256 counter streams of a fixed label (no clock, no urandom), so
every image is byte-identical on rebuild.  The manifest records the ground truth
(kind, path, sha256, size, link target) that the oracle/non-regular tables are
derived from -- derived from the SOURCE TREE, never from a receipt.

Usage: build-dev.py OUTDIR WRITER
Exit 0 ok, 2 usage, 3 writer failure.
"""
import hashlib
import json
import os
import subprocess
import sys


def stream(label, n):
    out = bytearray()
    i = 0
    while len(out) < n:
        out += hashlib.sha256(('%s/%d' % (label, i)).encode()).digest()
        i += 1
    return bytes(out[:n])


CARRIERS = {
    'A-xz': {
        'comp': 'xz',
        'files': {
            'etc/version': b'kaidoku r41 A avm-genuine xz\n',
            'usr/bin/busy': stream('A/busy', 40000),
            'usr/lib/libavm.so': stream('A/libavm', 30000),
        },
        'links': {
            'bin/busy': '../usr/bin/busy',
        },
    },
    'A-gz': {
        'comp': 'gzip',
        'files': {
            'etc/version': b'kaidoku r41 A avm-genuine xz\n',
            'usr/bin/busy': stream('A/busy', 40000),
            'usr/lib/libavm.so': stream('A/libavm', 30000),
        },
        'links': {
            'bin/busy': '../usr/bin/busy',
        },
    },
    'B-xz': {
        'comp': 'xz',
        'files': {
            'etc/version': b'kaidoku r41 B avm-genuine xz\n',
            'sbin/tool': stream('B/tool', 50000),
            'usr/lib/libavm.so': stream('B/libavm', 20000),
        },
        'links': {
            'usr/sbin/tool': '/sbin/tool',
        },
    },
    'C-xz': {
        'comp': 'xz',
        'files': {
            'etc/conf': stream('C/conf', 7000),
            'opt/x/etc/conf': stream('C/conf', 7000),   # identical bytes
            'etc/version': b'kaidoku r41 C avm-genuine xz\n',
        },
        'links': {},
    },
    # Reverse-direction GAP ambiguity: two symlink entries whose paths are a
    # suffix of one another.  A gap on the deeper one resolves to two entries
    # under a suffix rule, so `gaps_ok` (exactly one entry) fails.
    'D-xz': {
        'comp': 'xz',
        'files': {
            'etc/version': b'kaidoku r41 D avm-genuine xz\n',
            'usr/bin/tool': stream('D/tool', 30000),
        },
        'links': {
            'sbin/tool': '../usr/bin/tool',
            'usr/sbin/tool': '/usr/bin/tool',
        },
    },
    # Nested extraction probe: the carrier also holds an inner AVM-genuine image
    # as a regular file, so a run above depth 1 extracts a second chunk INSIDE
    # the first extract root.  Published paths then carry two `_extract`
    # components: `<outer>_extract/var/inner.squashfs_extract/<rel>`.
    'E-xz': {
        'comp': 'xz',
        'files': {
            'etc/version': b'kaidoku r41 E avm-genuine xz\n',
            'usr/bin/busy': stream('A/busy', 40000),
        },
        'links': {
            'bin/busy': '../usr/bin/busy',
        },
        'nested': {'rel': 'var/filesystem_core.squashfs', 'comp': 'xz',
                   'files': {'inner/only.txt': b'inner payload only\n'}},
    },
}


def build_tree(root, spec):
    for rel, data in sorted(spec['files'].items()):
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'wb') as fh:
            fh.write(data)
    for rel, target in sorted(spec['links'].items()):
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        os.symlink(target, p)


def walk_truth(root):
    """Ground truth from the source tree: kind, rel, sha256, size, link target."""
    rows = []
    for dirpath, dnames, fnames in os.walk(root):
        dnames.sort()
        rel_dir = os.path.relpath(dirpath, root)
        for dn in list(dnames):
            p = os.path.join(dirpath, dn)
            if os.path.islink(p):
                rows.append(('symlink', os.path.relpath(p, root), '', '',
                             os.readlink(p)))
                dnames.remove(dn)
        if rel_dir != '.':
            rows.append(('dir', rel_dir, '', '', ''))
        for fn in sorted(fnames):
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, root)
            if os.path.islink(p):
                rows.append(('symlink', rel, '', '', os.readlink(p)))
                continue
            raw = open(p, 'rb').read()
            rows.append(('file', rel, hashlib.sha256(raw).hexdigest(),
                         str(len(raw)), ''))
    rows.sort(key=lambda r: (r[1], r[0]))
    return rows


def main():
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    out = os.path.abspath(sys.argv[1])
    writer = os.path.abspath(sys.argv[2])
    os.makedirs(out, exist_ok=True)
    index = {}
    for cid, spec in CARRIERS.items():
        d = os.path.join(out, cid)
        src = os.path.join(d, 'src')
        os.makedirs(d, exist_ok=False)
        build_tree(src, spec)
        nested_sha = None
        if spec.get('nested'):
            n = spec['nested']
            nsrc = os.path.join(d, 'inner-src')
            os.makedirs(nsrc)
            for rel, data in sorted(n['files'].items()):
                p = os.path.join(nsrc, rel)
                os.makedirs(os.path.dirname(p), exist_ok=True)
                with open(p, 'wb') as fh:
                    fh.write(data)
            nimg = os.path.join(d, 'inner.sqsh')
            pn = subprocess.run([sys.executable, '-I', '-B', writer, nsrc,
                                 nimg, '--endian', 'avm-genuine',
                                 '--comp', n['comp']],
                                capture_output=True, text=True)
            if pn.returncode != 0:
                print('%s: inner writer failed rc=%d\n%s'
                      % (cid, pn.returncode, pn.stderr), file=sys.stderr)
                return 3
            nested_sha = hashlib.sha256(open(nimg, 'rb').read()).hexdigest()
            dst = os.path.join(src, n['rel'])
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, 'wb') as fh:
                fh.write(open(nimg, 'rb').read())
        img = os.path.join(d, 'carrier.sqsh')
        p = subprocess.run([sys.executable, '-I', '-B', writer, src, img,
                            '--endian', 'avm-genuine', '--comp', spec['comp']],
                           capture_output=True, text=True)
        if p.returncode != 0:
            print('%s: writer failed rc=%d\n%s' % (cid, p.returncode, p.stderr),
                  file=sys.stderr)
            return 3
        raw = open(img, 'rb').read()
        sha = hashlib.sha256(raw).hexdigest()
        rows = walk_truth(src)
        with open(os.path.join(d, 'manifest.tsv'), 'w') as fh:
            for kind, rel, h, size, target in rows:
                fh.write('%s\t%s\t%s\t%s\t%s\n' % (kind, rel, h, size, target))
        with open(os.path.join(d, 'oracle.tsv'), 'w') as fh:
            for kind, rel, h, size, _t in rows:
                if kind == 'file':
                    fh.write('%s\t%s\t%s\n' % (rel, h, size))
        with open(os.path.join(d, 'nonregular.tsv'), 'w') as fh:
            for kind, rel, _h, _s, target in rows:
                if kind != 'file':
                    fh.write('%s\t%s\t%s\n' % (rel, kind, target))
        index[cid] = {'path': img, 'sha256': sha, 'size': len(raw),
                      'comp': spec['comp'],
                      'nested': ({'rel': spec['nested']['rel'],
                                  'sha256': nested_sha,
                                  'files': sorted(spec['nested']['files'])}
                                 if spec.get('nested') else None),
                      'oracle': os.path.join(d, 'oracle.tsv'),
                      'nonregular': os.path.join(d, 'nonregular.tsv'),
                      'manifest': os.path.join(d, 'manifest.tsv')}
        print('%s\t%s\t%s' % (cid, sha, len(raw)))
    with open(os.path.join(out, 'index.json'), 'w') as fh:
        json.dump({'claim': 'R41-C1Collide', 'writer': writer,
                   'endian': 'avm-genuine', 'carriers': index}, fh, indent=1)
        fh.write('\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
