#!/usr/bin/env python3
"""Build the two lane-built R41-C1 carriers L3 (xz) and L4 (gzip) deterministically.

Round-41 port of tools/round-40/mk-l-carriers.py (base bytes
309c502d21dfeef9b7b2a5a9a62bfa875270fdf79eec671461070996d291042e is the writer it
calls).  Every carrier is a genuine AVM-layout big-endian SquashFS v4 image written
by that same writer in `--endian avm-genuine` mode: `sqsh` magic, big-endian
superblock / inode / directory / lookup fields, `mkfs_time == bytes_used` (the AVM
marker), and LITTLE-endian 2-byte metadata block-length headers.

Differences from the round-40 trees (fresh content; L1/L2 pins must not recur):
  * >= 12 regular files in nested directories (round 40 had 7 and 6);
  * nested-name collisions in BOTH directions, which the round-40 pair only had
    one of (R40-CL1: a suffix test read the regular `usr/bin/busy` as the symlink
    `bin/busy`):
      1. regular `usr/bin/busy` + symlink `bin/busy`   (regular path ends with
         the symlink path),
      2. symlink `usr/sbin/tool` + regular `sbin/tool` (symlink path ends with
         the regular path);
  * one deep regular file whose tail equals another regular file's full path
    (`opt/x/etc/conf` vs `etc/conf`) with DIFFERENT contents, so an anchored
    matcher cannot satisfy one row with the other;
  * exactly one relative and one absolute retained symlink, both resolving
    inside the tree, plus one extra non-colliding relative link; no escaping
    link (vendor AVM members carry none).

Determinism: file contents are fixed byte strings or sha256 counter streams of a
fixed label (no clock, no urandom); the writer stamps the fixed MKFS_TIME into
every inode and derives mkfs_time from bytes_used.  Two builds into two fresh
directories are byte-identical (checked by --builds 2, and by the caller).

Usage: mk-l-carriers.py OUTDIR [--writer PATH] [--builds N] [--lane PATH]
  OUTDIR/L3/carrier.sqsh, OUTDIR/L4/carrier.sqsh, OUTDIR/<id>/src/  (build 1)
  with --builds 2 also OUTDIR/b2/<id>/... for the byte-identity check.
Prints one TSV line per carrier: id, comp, sha256, size, files, links, dirs, path.
Exit 0 ok, 2 usage/verification failure, 3 writer failure, 4 determinism failure.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

DEFAULT_LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
WRITER_REL = 'tools/round-41/gen-squashfs.py'  # byte copy of tools/round-40/gen-squashfs.py (frozen C1 path)


def stream(label, n):
    out = bytearray()
    i = 0
    while len(out) < n:
        out += hashlib.sha256(('%s/%d' % (label, i)).encode()).digest()
        i += 1
    return bytes(out[:n])


TREES = {
    'L3': {
        'comp': 'xz',
        'files': {
            # the deep-tail pair: opt/x/etc/conf must NOT satisfy etc/conf
            'etc/conf': b'kaidoku r41 L3 top-level conf\nmode=avm-genuine\n',
            'opt/x/etc/conf': stream('L3/deepconf', 96),
            'etc/version': b'kaidoku r41 L3 avm-genuine xz\n',
            'etc/init.d/rc.S': b'#!/bin/sh\necho boot L3\n' * 60,
            'usr/bin/busy': stream('L3/busy', 48000),
            'sbin/tool': stream('L3/tool', 32000),
            'usr/lib/libcore.so': stream('L3/core', 90000),
            'usr/share/web/index.html': b'<html><body>L3</body></html>\n' * 200,
            'usr/share/doc/LICENSE': b'lane-built carrier, AVM layout, round 41\n' * 40,
            'lib/modules/kmod.ko': stream('L3/kmod', 12000),
            'var/lib/state.dat': stream('L3/state', 3000),
            'var/tmp/empty': b'',
            'opt/app/config.json': b'{"layout": "avm-genuine", "round": 41, "carrier": "L3"}\n',
        },
        'links': {
            'bin/busy': '../usr/bin/busy',            # relative, in-tree; collision 1
            'usr/sbin/tool': '/sbin/tool',            # absolute, in-tree; collision 2
            'usr/share/web/current': 'index.html',    # relative, in-tree, no collision
        },
    },
    'L4': {
        'comp': 'gzip',
        'files': {
            'etc/conf': b'kaidoku r41 L4 top-level conf\nmode=avm-genuine\n',
            'opt/x/etc/conf': stream('L4/deepconf', 120),
            'etc/hosts': b'127.0.0.1 localhost L4\n',
            'etc/fstab': b'/dev/root / squashfs ro 0 1\n',
            'usr/bin/busy': stream('L4/busy', 56000),
            'sbin/tool': stream('L4/tool', 28000),
            'usr/sbin/init': b'#!/bin/sh\nexec /sbin/tool\n' * 30,
            'usr/lib/libssl.so': stream('L4/ssl', 70000),
            'usr/share/doc/README': b'lane-built AVM-layout gzip carrier, round 41\n' * 60,
            'var/log/messages': b'kaidoku L4 boot line\n' * 200,
            'var/lib/db.bin': stream('L4/db', 5000),
            'var/tmp/empty': b'',
            'root/.profile': b'export PATH=/usr/bin:/sbin:/bin\n',
            'opt/x/data.bin': stream('L4/optdata', 8000),
        },
        'links': {
            'bin/busy': '../usr/bin/busy',            # relative, in-tree; collision 1
            'usr/sbin/tool': '/sbin/tool',            # absolute, in-tree; collision 2
            'var/log/current': 'messages',            # relative, in-tree, no collision
        },
    },
}


def inside(root, rel):
    """True when the entry at `rel` resolves inside root, as it would at extract time.

    An absolute symlink target is re-rooted at the extraction root (that is what
    an image consumer sees); a relative target is resolved against the link's
    directory.  The resolved path is then required to stay inside root.
    """
    target = os.readlink(os.path.join(root, rel))
    if target.startswith('/'):
        p = root.rstrip('/') + '/' + target.lstrip('/')
    else:
        p = os.path.join(root, os.path.dirname(rel), target)
    p = os.path.realpath(p)
    r = os.path.realpath(root)
    return p == r or p.startswith(r + os.sep)


def check_spec(cid, spec, root):
    """Structural invariants of a tree, on the built source tree."""
    files, links = spec['files'], spec['links']
    problems = []
    if len(files) < 12:
        problems.append('only %d regular files (need >= 12)' % len(files))
    # collision 1: regular usr/bin/busy whose path ends with the symlink bin/busy
    if 'usr/bin/busy' not in files or 'bin/busy' not in links:
        problems.append('missing collision 1 (usr/bin/busy file + bin/busy symlink)')
    elif not 'usr/bin/busy'.endswith('bin/busy'):
        problems.append('collision 1 does not hold as a path suffix')
    # collision 2: symlink usr/sbin/tool whose path ends with the regular sbin/tool
    if 'usr/sbin/tool' not in links or 'sbin/tool' not in files:
        problems.append('missing collision 2 (usr/sbin/tool symlink + sbin/tool file)')
    elif not 'usr/sbin/tool'.endswith('sbin/tool'):
        problems.append('collision 2 does not hold as a path suffix')
    # deep tail: opt/x/etc/conf ends with etc/conf, different contents
    if 'opt/x/etc/conf' not in files or 'etc/conf' not in files:
        problems.append('missing deep-tail pair (opt/x/etc/conf + etc/conf)')
    else:
        if not 'opt/x/etc/conf'.endswith('etc/conf'):
            problems.append('deep-tail pair is not a path suffix')
        if files['opt/x/etc/conf'] == files['etc/conf']:
            problems.append('deep-tail pair contents are equal')
    # link shape: exactly one absolute, the rest relative, all in-tree
    abs_links = [r for r, t in links.items() if t.startswith('/')]
    if len(abs_links) != 1:
        problems.append('%d absolute symlinks (need exactly 1)' % len(abs_links))
    rel_links = [r for r, t in links.items() if not t.startswith('/')]
    if not rel_links:
        problems.append('no relative symlink')
    for r in sorted(links):
        if not inside(root, r):
            problems.append('symlink %s escapes the tree' % r)
    for r in sorted(files):
        if '/../' in r or r.startswith('../'):
            problems.append('regular path %s leaves the tree' % r)
    # every parent directory of every entry exists as a directory
    for r in sorted(list(files) + list(links)):
        d = os.path.dirname(r)
        while d:
            p = os.path.join(root, d)
            if os.path.islink(p) or not os.path.isdir(p):
                problems.append('parent %s of %s is not a real directory' % (d, r))
                break
            d = os.path.dirname(d)
    return problems


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


def counts(root):
    nf = nl = nd = 0
    for dirpath, dnames, fnames in os.walk(root):
        dnames.sort()
        for dn in list(dnames):
            if os.path.islink(os.path.join(dirpath, dn)):
                dnames.remove(dn)
        nd += 1  # root counted too; caller subtracts nothing, informational
        for fn in fnames:
            if os.path.islink(os.path.join(dirpath, fn)):
                nl += 1
            else:
                nf += 1
    return nf, nl, nd - 1


def build(root_dir, cid, spec, writer):
    d = os.path.join(root_dir, cid)
    src = os.path.join(d, 'src')
    os.makedirs(d)
    build_tree(src, spec)
    problems = check_spec(cid, spec, src)
    if problems:
        for p in problems:
            print('%s: spec problem: %s' % (cid, p), file=sys.stderr)
        return None, problems
    img = os.path.join(d, 'carrier.sqsh')
    p = subprocess.run([sys.executable, '-I', '-B', writer, src, img,
                        '--endian', 'avm-genuine', '--comp', spec['comp']],
                       capture_output=True, text=True)
    if p.returncode != 0:
        print(p.stdout, file=sys.stderr)
        print(p.stderr, file=sys.stderr)
        return None, ['writer exit %d' % p.returncode]
    digest = hashlib.sha256(open(img, 'rb').read()).hexdigest()
    nf, nl, nd = counts(src)
    return {'id': cid, 'comp': spec['comp'], 'sha256': digest,
            'size': os.path.getsize(img), 'files': nf, 'links': nl, 'dirs': nd,
            'path': img, 'writer': '%s --endian avm-genuine --comp %s'
                                  % (WRITER_REL, spec['comp'])}, []


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument('outdir')
    ap.add_argument('--writer', default=None,
                    help='gen-squashfs.py path (default LANE/' + WRITER_REL + ')')
    ap.add_argument('--lane', default=DEFAULT_LANE)
    ap.add_argument('--builds', type=int, default=1, choices=(1, 2))
    ap.add_argument('--json', default=None, help='write the per-carrier result JSON here')
    a = ap.parse_args(argv)
    out = os.path.abspath(a.outdir)
    writer = a.writer or os.path.join(a.lane, WRITER_REL)
    if not os.path.isfile(writer):
        print('writer not found: %s' % writer, file=sys.stderr)
        return 2
    if not os.path.isdir(out):
        print('outdir must exist and be empty: %s' % out, file=sys.stderr)
        return 2
    if os.listdir(out):
        print('outdir is not empty: %s' % out, file=sys.stderr)
        return 2
    results = []
    for cid in sorted(TREES):
        r, problems = build(out, cid, TREES[cid], writer)
        if r is None:
            return 3
        results.append(r)
    if a.builds == 2:
        second = os.path.join(out, 'b2')
        os.makedirs(second)
        for cid in sorted(TREES):
            r, problems = build(second, cid, TREES[cid], writer)
            if r is None:
                return 3
            first = [x for x in results if x['id'] == cid][0]
            if r['sha256'] != first['sha256'] or r['size'] != first['size']:
                print('%s: build 2 differs (%s vs %s)' % (cid, r['sha256'], first['sha256']),
                      file=sys.stderr)
                return 4
            print('%s\tbuild2-equal\tsha256=%s' % (cid, r['sha256']), file=sys.stderr)
    for r in results:
        print('%s\t%s\t%s\t%d\t%d\t%d\t%d\t%s' % (
            r['id'], r['comp'], r['sha256'], r['size'], r['files'], r['links'],
            r['dirs'], r['path']))
    if a.json:
        with open(a.json, 'w') as fh:
            json.dump({'claim': 'R41-C1', 'writer': WRITER_REL, 'builds': a.builds,
                       'carriers': results}, fh, indent=1, sort_keys=True)
            fh.write('\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
