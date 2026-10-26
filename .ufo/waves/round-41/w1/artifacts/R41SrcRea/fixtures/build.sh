#!/bin/bash
# Rebuild the three lane-built fixtures from nothing. No vendor bytes are involved.
# Writes into $1 (default: ./rebuild). Requires mksquashfs (squashfs-tools) and
# tools/round-40/gen-squashfs.py from the lane at the base revision.
set -euo pipefail
OUT=${1:-./rebuild}
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
BASE=49096c7e6f226af0c750c4b003be58883cb6049f
mkdir -p "$OUT"
cd "$OUT"

# 1. outer.sqfs — LE v4 (gzip) holding a nested LE v4 image; build 4096 B, sha256 91a530e2…
mkdir -p inner-src outer-src
printf 'hello\n' > inner-src/hello.txt
mksquashfs inner-src inner.sqfs -comp gzip -noappend -quiet -all-root
cp inner.sqfs outer-src/
mksquashfs outer-src outer.sqfs -comp gzip -noappend -quiet -all-root

# 2. avm-pad.sqfs — genuine AVM layout writer (BE superblock, LE block-length headers),
#    marker mkfs_time == bytes_used, zero-padded to 4096 B; sha256 319a0239…
git -C "$LANE" show "$BASE":tools/round-40/gen-squashfs.py > gen-squashfs.py
mkdir -p avmtree/sub
printf 'alpha\n' > avmtree/a.txt
printf 'beta\n' > avmtree/sub/b.txt
python3 -I -B gen-squashfs.py --endian avm-genuine avmtree avm.sqfs
cp avm.sqfs avm-pad.sqfs
truncate -s 4096 avm-pad.sqfs

# 3. lebig-corrupt2.sqfs — LE v4 (gzip), 300 zero bytes at 4000..4300 of an 8192 B image,
#    which lands in the fragment table and makes sasquatch exit 1 "FATAL ERROR";
#    sha256 853fb41a…
python3 - <<'PY'
import os
os.makedirs('lebig', exist_ok=True)
for i in range(8):
    open('lebig/f%d.bin' % i, 'wb').write(os.urandom(500))
open('lebig/keep.txt', 'w').write('keep\n')
PY
mksquashfs lebig lebig.sqfs -comp gzip -noappend -quiet -all-root
python3 - <<'PY'
b = bytearray(open('lebig.sqfs', 'rb').read())
b[4000:4300] = b'\x00' * 300
open('lebig-corrupt2.sqfs', 'wb').write(bytes(b))
PY
sha256sum outer.sqfs avm-pad.sqfs lebig-corrupt2.sqfs
