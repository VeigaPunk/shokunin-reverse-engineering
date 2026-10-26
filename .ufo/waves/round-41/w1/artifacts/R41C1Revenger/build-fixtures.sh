#!/bin/bash
# R41C1Revenger: rebuild the six development fixtures used for the exact-path study.
# Regenerates byte-identical images from tools/round-40/gen-squashfs.py (read-only use).
# Usage: build-fixtures.sh OUTDIR
set -eu
OUT=${1:?usage: build-fixtures.sh OUTDIR}
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
GEN=$LANE/tools/round-40/gen-squashfs.py
mkdir -p "$OUT"
cd "$OUT"

mk_t1() {
  rm -rf t1 && mkdir -p t1/etc t1/usr/bin t1/usr/share/doc t1/lib/firmware_extract t1/var/tmp t1/sbin t1/bin
  printf 'hello r41\n' > t1/etc/a.txt
  python3 -c "import sys;sys.stdout.buffer.write(b'A'*40000)" > t1/usr/bin/busy
  printf 'inside a dir named firmware_extract\n' > t1/lib/firmware_extract/marker.bin
  printf 'nested-name collision: regular file whose path ends with a dir name\n' > t1/var/tmp/keep.txt
  python3 -c "import sys;sys.stdout.buffer.write(b'T'*5000)" > t1/sbin/tool
  ln -s busy t1/usr/bin/ls
  ln -s /usr/bin/busy t1/bin/busy
  ln -s /usr/bin/busy t1/bin_busy_abs_placeholder
  ln -s ../sbin/tool t1/etc/link_tool
}

mk_t1
python3 -I -B "$GEN" t1 F1.sqsh --endian avm-genuine --comp xz

# F2: 4096 bytes of zero padding before the image -> squashfs at a nonzero carve offset
python3 -c "open('F2.bin','wb').write(b'\x00'*4096 + open('F1.sqsh','rb').read())"

# F3: outer squashfs holding F1 as nested/inner.squashfs -> a second chunk root at depth 2
rm -rf t3 && mkdir -p t3/nested t3/etc
cp F1.sqsh t3/nested/inner.squashfs
printf 'outer marker\n' > t3/etc/outer.txt
python3 -I -B "$GEN" t3 F3.sqsh --endian avm-genuine --comp gzip

# F4: escaping + absolute + in-tree relative symlinks
rm -rf t4 && mkdir -p t4/etc t4/sbin
printf 'x\n' > t4/etc/f.txt
python3 -c "import sys;sys.stdout.buffer.write(b'S'*3000)" > t4/sbin/tool
ln -s ../../../../etc/passwd t4/etc/esc
ln -s /etc/passwd t4/etc/abs_passwd
ln -s ../sbin/tool t4/etc/rel_ok
python3 -I -B "$GEN" t4 F4.sqsh --endian avm-genuine --comp xz

# F6: two concatenated squashfs chunks -> two sibling chunk roots at depth 0
cat F1.sqsh F4.sqsh > F6.bin

sha256sum F1.sqsh F2.bin F3.sqsh F4.sqsh F6.bin
