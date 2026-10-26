#!/bin/sh
# Dev probe (NOT the carrier, NOT REA): confirm how unblob 26.6.4 treats the exact
# symlink shapes carrier K5 uses, on a scratch tree built with the same generator.
#
#   S=/fast/scratch/... ./dev-probe.sh
#
# Tree D5C mirrors K5's link geometry only -- 3-component link directory, one
# in-tree same-directory link, one in-tree `..` link into a sibling directory, one
# 4-`..` escaping link, plus a non-ASCII name -- with different file contents, so it
# is not K5. Expected: the escaping link is removed (MaliciousSymlinkRemoved), the two
# in-tree links survive with their targets unchanged, and the non-ASCII file is
# published with its source sha256. D5D is the boundary: a 4-component directory with
# the same 4 `..` resolves to /etc/shadow INSIDE the extraction root, so it is kept --
# the split is the `..` count relative to the image root, exactly what make-oracle.py's
# stack rule computes.
set -eu
S=${S:?set S to a scratch dir}
A=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
export TMPDIR="$S" HYAKU_SCRATCH=${HYAKU_SCRATCH:-/fast/scratch/hyaku}
cd "$S"

mk() {
  rm -rf "$1"; mkdir -p "$1/deep/a/b" "$1/deep/a/side" \
      "$1/deeper/a/b/c" "$1/deeper/a/side"
  printf 'probe side target\n' > "$1/deep/a/side/target.bin"
  printf 'probe unicode body\n' > "$1/deep/a/b/Überblick-設計.txt"
  ln -s Überblick-設計.txt "$1/deep/a/b/same-dir"
  ln -s ../side/target.bin "$1/deep/a/b/via-dotdot"
  ln -s ../../../../etc/shadow "$1/deep/a/b/escape"
  printf 'deep side target\n' > "$1/deeper/a/side/target.bin"
  ln -s ../../../../etc/shadow "$1/deeper/a/b/c/inside"
}

for name in D5C D5D; do
  mk "tree-$name"
  python3 "$A/gen-squashfs.py" "tree-$name" "probe-$name.sqsh" --endian be --comp gzip
  rm -rf "out-$name"
  ~/.local/bin/unblob -e "$S/out-$name" -f "$S/probe-$name.sqsh" \
      > "probe-$name.stdout" 2> "probe-$name.stderr"
  echo "== $name unblob_exit=0"
  find "$S/out-$name" -type l -printf '   link %P -> %l\n' | LC_ALL=C sort
  find "$S/out-$name" -type f -printf '   file %P %s\n' | LC_ALL=C sort
done
echo '== traversal removals recorded in unblob.log (cwd)'
grep -a 'Path traversal' unblob.log || echo '   (none)'
