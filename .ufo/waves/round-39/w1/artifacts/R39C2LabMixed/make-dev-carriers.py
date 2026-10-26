#!/usr/bin/env python3
"""Author three development standard-BE SquashFS v4 gzip trees in scratch and
build them with the lane generator (tools/round-37/gen-squashfs.py).

Never touches K1-K6. Usage: make-dev-carriers.py <lane-root> <scratch-dir>
"""
import os, shutil, subprocess, sys

LANE = sys.argv[1]
S = sys.argv[2]
GEN = os.path.join(LANE, 'tools/round-37/gen-squashfs.py')
TREES = os.path.join(S, 'trees')
IMGS = os.path.join(S, 'images')

# name -> (files{dict}, symlinks{path: target})
SPECS = {
    # D1: in-tree link sorts BEFORE the escaping link (a_ < z_)
    'D1-in-first': (
        {'hello.txt': b'dev1 hello\n', 'bin/run': b'#!/bin/sh\necho hi\n'},
        {'a_in': 'hello.txt', 'z_out': '../outside-d1.txt'},
    ),
    # D2: same logical content, escaping link sorts BEFORE the in-tree link
    'D2-out-first': (
        {'hello.txt': b'dev1 hello\n', 'bin/run': b'#!/bin/sh\necho hi\n'},
        {'a_out': '../outside-d2.txt', 'z_in': 'hello.txt'},
    ),
    # D3: nested, TWO in-tree links + one escaping link (gap multiplicity)
    'D3-nested-multi': (
        {'hello.txt': b'dev3 hello\n'},
        {'deep/up_in': '../hello.txt',
         'deep/b_in2': '../hello.txt',
         'deep/out_up': '../../outside-d3.txt'},
    ),
    # D4 (supplementary order probe): chase link sorts BEFORE its escaping target
    'D4-chase-first': (
        {'hello.txt': b'dev4 hello\n'},
        {'a_chase': 'b_escape', 'b_escape': '../outside-d4.txt'},
    ),
    # D5 (supplementary order probe): escaping target sorts BEFORE the chase link
    'D5-escape-first': (
        {'hello.txt': b'dev5 hello\n'},
        {'a_escape': '../outside-d5.txt', 'z_chase': 'a_escape'},
    ),
    # D6: TWO escaping links + one in-tree link -> diagnostic multiplicity
    'D6-two-escaping': (
        {'hello.txt': b'dev6 hello\n'},
        {'in_link': 'hello.txt',
         'out_a': '../outside-d6a.txt',
         'out_b': '../outside-d6b.txt'},
    ),
    # C1 (order probe, chain): alphabetical order puts the ESCAPING target first
    'C1-target-first': (
        {'hello.txt': b'chain1 hello\n'},
        {'a_target': '../outside-c1.txt', 'z_link': 'a_target'},
    ),
    # C2 (order probe, chain): alphabetical order puts the CHASING link first
    'C2-chase-first': (
        {'hello.txt': b'chain2 hello\n'},
        {'a_chase': 'z_target', 'z_target': '../outside-c2.txt'},
    ),
    # C3 (order probe, cross-directory): escaping link in root, chase link nested
    'C3-root-escape': (
        {'hello.txt': b'chain3 hello\n'},
        {'a_target': '../outside-c3.txt', 'deep/z_link': '../a_target'},
    ),
    # C4 (order probe, cross-directory): chase link in root, escaping link nested
    'C4-root-chase': (
        {'hello.txt': b'chain4 hello\n'},
        {'a_chase': 'deep/z_target', 'deep/z_target': '../../outside-c4.txt'},
    ),
    # D8: directory symlinks -- one in-tree (d_in -> docs), one escaping
    'D8-dir-links': (
        {'hello.txt': b'dev8 hello\n', 'docs/a.txt': b'doc a\n'},
        {'d_in': 'docs', 'd_out': '../outside-d8'},
    ),
}


def main():
    for name in ('D1-in-first', 'D2-out-first', 'D3-nested-multi',
                 'D4-chase-first', 'D5-escape-first', 'D6-two-escaping',
                 'C1-target-first', 'C2-chase-first',
                 'C3-root-escape', 'C4-root-chase', 'D8-dir-links'):
        files, links = SPECS[name]
        t = os.path.join(TREES, name)
        if os.path.exists(t):
            shutil.rmtree(t)
        os.makedirs(t)
        for rel, data in sorted(files.items()):
            p = os.path.join(t, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True) if os.path.dirname(p) else None
            with open(p, 'wb') as f:
                f.write(data)
        for rel, target in sorted(links.items()):
            p = os.path.join(t, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True) if os.path.dirname(p) else None
            os.symlink(target, p)
        out = os.path.join(IMGS, name + '.sqsh')
        os.makedirs(IMGS, exist_ok=True)
        # intentionally no chmod pass: generator writes mode 0644/0755 by type
        subprocess.run([sys.executable, GEN, t, out, '--endian', 'be',
                        '--comp', 'gzip'], check=True)


if __name__ == '__main__':
    main()
