#!/bin/sh
# Rebuild carrier K5 (standard big-endian SquashFS v4, gzip, 4096-byte blocks)
# byte-identically. Idempotent: rewrites src/, carrier.sqsh, carrier.sqsh.sha256.
#
#   ./build.sh
#
# Requires only python3. Determinism: the tree is a pure function of make-tree.py
# (SHA-256 counter-mode PRNG, fixed content, no timestamps), and gen-squashfs.py
# pins mtime/uid/gid and sorts every directory and inode list, so no host path,
# clock or locale reaches the image.
#
# gen-squashfs.py here is tools/round-37/gen-squashfs.py plus a one-line fix:
# the directory-entry name_size field must count UTF-8 BYTES, not characters
# (stock == this file for every ASCII tree; see gen-squashfs.py --diff note).
set -eu
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

python3 "$here/make-tree.py" "$here/src"
python3 "$here/gen-squashfs.py" "$here/src" "$here/carrier.sqsh" --endian be --comp gzip
python3 "$here/make-oracle.py" "$here/src" "$here"

cd "$here"
sha256sum carrier.sqsh | tee carrier.sqsh.sha256
