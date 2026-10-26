#!/usr/bin/env python3
"""Author the R39-C1 carrier K5 source tree, deterministically.

Usage: make-tree.py TREE

Writes (relative to TREE), throwing the tree away first so re-runs are clean:

  README.txt
  empty.flag                             0-byte regular file
  notes with space.txt                   regular file, ASCII space in the name
  config/app.conf
  usr/share/demo/notes.txt               same-directory symlink target
  usr/share/demo/link-notes -> notes.txt                 in-tree, same dir
  usr/share/demo/link-blob  -> ../opt/blob.bin           in-tree, via `..`, sibling dir
  usr/share/demo/escape     -> ../../../../etc/shadow    escaping (4 `..` > depth 3)
  usr/share/demo/assets/manifest.json
  usr/share/demo/assets/icons/アイコン.txt                UTF-8 non-ASCII name
  usr/share/opt/blob.bin                 5000 bytes, deterministic PRNG
  var/lib/state.db                       20000 bytes, deterministic PRNG (>3 x 4096)
  var/log/last.log

Every byte is a pure function of this file: no host paths, times, random state or
locale enter the tree. The PRNG is SHA-256 counter mode, not `random`, so the output
is stable across Python versions.
"""
import hashlib
import os
import shutil
import sys

SEED = "kaidoku-r39-c1-k5"


def prng(label, n):
    out = bytearray()
    i = 0
    while len(out) < n:
        out += hashlib.sha256(f"{SEED}:{label}:{i}".encode()).digest()
        i += 1
    return bytes(out[:n])


# relative path -> bytes
FILES = {
    "README.txt": (
        "kaidoku round 39 C1 carrier K5\n"
        "standard big-endian SquashFS v4, gzip, block size 4096\n"
        "tree authored by make-tree.py; the carrier by gen-squashfs.py\n"
    ).encode(),
    "empty.flag": b"",
    "notes with space.txt": b"one ASCII space in this file name\n",
    "config/app.conf": (
        "[k5]\n"
        "endian = be\n"
        "compression = gzip\n"
        "block_size = 4096\n"
    ).encode(),
    "usr/share/demo/notes.txt": b"same-directory symlink target\n",
    "usr/share/demo/assets/manifest.json": (
        '{\n  "carrier": "K5",\n  "round": 39,\n  "claim": "R39-C1"\n}\n'
    ).encode(),
    "usr/share/demo/assets/icons/\u30a2\u30a4\u30b3\u30f3.txt": (
        "UTF-8 file name: \u30a2\u30a4\u30b3\u30f3 (icon)\n"
    ).encode(),
    "usr/share/opt/blob.bin": prng("usr/share/opt/blob.bin", 5000),
    "var/lib/state.db": prng("var/lib/state.db", 20000),
    "var/log/last.log": b"k5: last log line\n",
}

# relative path -> link target (kept relative, never absolute)
LINKS = {
    "usr/share/demo/link-notes": "notes.txt",
    "usr/share/demo/link-blob": "../opt/blob.bin",
    "usr/share/demo/escape": "../../../../etc/shadow",
}


def main(argv):
    if len(argv) != 2:
        sys.exit(f"usage: {argv[0]} TREE")
    tree = argv[1]
    if os.path.lexists(tree):
        shutil.rmtree(tree)
    os.makedirs(tree)
    for rel, data in sorted(FILES.items()):
        p = os.path.join(tree, rel)
        os.makedirs(os.path.dirname(p) or tree, exist_ok=True)
        with open(p, "wb") as f:
            f.write(data)
    for rel, target in sorted(LINKS.items()):
        p = os.path.join(tree, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        os.symlink(target, p)
    print(f"tree {tree}: {len(FILES)} files, {len(LINKS)} symlinks")


if __name__ == "__main__":
    main(sys.argv)
