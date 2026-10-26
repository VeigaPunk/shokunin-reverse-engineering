#!/usr/bin/env python3
"""Build a SquashFS fixture whose name census matches V4's shape.

Usage: build-budget-fixture.py <tree-root> <out.squashfs> [--dirs N]
       [--files N] [--symlinks N] [--files-per-dir N]

The tree is flat-under-known-dirs: every non-root name lives exactly one
directory below the root plus the per-dir fan-out, so the census is exact and
countable without walking the image:

  names = dirs + files + symlinks
  staging entries REA sees at --max-depth 1 = names + 1 (unblob's
  `firmware.bin_extract` chunk directory)

Sizes are deterministic and tiny; compression choice does not change entry
counts.  No device nodes, fifos or sockets are written (the round-40 writer
emits none), so a special-file census cannot be exercised from this fixture.
"""
import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WRITER = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-40/gen-squashfs.py"

ap = argparse.ArgumentParser()
ap.add_argument("tree")
ap.add_argument("out")
ap.add_argument("--dirs", type=int, default=401)
ap.add_argument("--files", type=int, default=6349)
ap.add_argument("--symlinks", type=int, default=615)
ap.add_argument("--files-per-dir", type=int, default=16)
ap.add_argument("--endian", default="le")
ap.add_argument("--comp", default="gzip")
args = ap.parse_args()

tree = os.path.abspath(args.tree)
out = os.path.abspath(args.out)
os.makedirs(tree, exist_ok=True)

dirs = []
for i in range(args.dirs):
    d = os.path.join(tree, "d%04d" % i)
    os.makedirs(d, exist_ok=True)
    dirs.append(d)

files = 0
per = args.files_per_dir
for i in range(args.files):
    d = dirs[i % len(dirs)]
    name = os.path.join(d, "f%05d" % i)
    with open(name, "wb") as fh:
        fh.write(b"payload%05d\n" % i)
    files += 1

links = 0
for i in range(args.symlinks):
    d = dirs[i % len(dirs)]
    target = "f%05d" % (i % max(files, 1))
    name = os.path.join(d, "l%05d" % i)
    if os.path.lexists(name):
        os.unlink(name)
    os.symlink(target, name)
    links += 1

names = len(dirs) + files + links
print("census names=%d (dirs=%d files=%d symlinks=%d) staging_entries_at_depth1=%d"
      % (names, len(dirs), files, links, names + 1))

cmd = [sys.executable, "-I", "-B", WRITER, "--endian", args.endian,
       "--comp", args.comp, tree, out]
sys.exit(subprocess.call(cmd))
