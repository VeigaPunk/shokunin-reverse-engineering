#!/bin/bash
# Round 13, target 2 (part 2): isolate why the round-12 build produced a
# non-AVM image under -DTARGET_FORMAT=AVM_LE, and complete the unblob run.
W=/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round13/work
cd "$W/sq43/squashfs4.3/squashfs-tools" || { echo NO_TREE; exit 1; }

measure () {
python3 -c "
import struct,sys
p=sys.argv[1]
d=open(p,'rb').read()
be = d[:4]==b'sqsh'
e = '>' if be else '<'
mt=struct.unpack(e+'I',d[8:12])[0]; bu=struct.unpack(e+'Q',d[40:48])[0]
print('  %-34s bytes=%d magic=%s(%s) comp=%d mkfs_time=%d bytes_used=%d -> %s' % (
  p.split('/')[-1], len(d), d[:4].decode(), 'BE' if be else 'LE',
  struct.unpack(e+'H',d[20:22])[0], mt, bu,
  'AVM MARKER SET (equal)' if mt==bu else 'NOT AVM (timestamp)'))
" "$1"
}

BUILD="make -j4 CC=gcc LEGACY_FORMATS_SUPPORT=1 GZIP_SUPPORT=1 LZMA_XZ_SUPPORT=1 XZ_SUPPORT=1 COMP_DEFAULT=xz XATTR_SUPPORT=0 XATTR_DEFAULT=0 mksquashfs unsquashfs"

echo "=== A: the binary identity right now ==="
sha256sum mksquashfs | cut -c1-32

echo "=== B: re-run make with a DIFFERENT define and NO clean (the round-12 move) ==="
$BUILD EXTRA_CFLAGS="-fcommon -DTARGET_FORMAT=AVM_LE -std=gnu89" 2>&1 | tail -3
echo "--- binary identity after the no-clean rebuild ---"
sha256sum mksquashfs | cut -c1-32

echo "=== C: CLEAN rebuild, plain Freetz 550 only, -DTARGET_FORMAT=AVM_LE, image WITHOUT -no-mkfs-time ==="
make clean >/dev/null 2>&1
$BUILD EXTRA_CFLAGS="-fcommon -DTARGET_FORMAT=AVM_LE -std=gnu89" > "$W/build-c.log" 2>&1
echo "  make exit=$?  binary=$(sha256sum mksquashfs | cut -c1-32)"
./mksquashfs "$W/avmlsrc" "$W/avm-le-plain550.squashfs" -comp xz -all-root -no-progress -no-exports -no-sparse -b 65536 >/dev/null 2>&1
measure "$W/avm-le-plain550.squashfs"

echo "=== D: CLEAN rebuild with AVM_FORMAT_AS_OPTION, image WITHOUT -no-mkfs-time ==="
make clean >/dev/null 2>&1
$BUILD EXTRA_CFLAGS="-fcommon -DTARGET_FORMAT=AVM_LE -DAVM_FORMAT_AS_OPTION -std=gnu89" > "$W/build-d.log" 2>&1
echo "  make exit=$?  binary=$(sha256sum mksquashfs | cut -c1-32)"
./mksquashfs "$W/avmlsrc" "$W/avm-le-standard-time.squashfs" -comp xz -all-root -no-progress -no-exports -no-sparse -b 65536 >/dev/null 2>&1
measure "$W/avm-le-standard-time.squashfs"

echo "=== E: CLEAN rebuild with AVM_FORMAT_AS_OPTION, image WITH -no-mkfs-time (the genuine AVM_LE) ==="
./mksquashfs "$W/avmlsrc" "$W/avm-le-genuine.squashfs" -comp xz -no-mkfs-time -all-root -no-progress -no-exports -no-sparse -b 65536 >/dev/null 2>&1
measure "$W/avm-le-genuine.squashfs"
echo "--- upstream's own unsquashfs -stat interpretation ---"
./unsquashfs -stat "$W/avm-le-genuine.squashfs" 2>&1 | head -4
echo "--- and of the plain-550 image, for contrast ---"
./unsquashfs -stat "$W/avm-le-plain550.squashfs" 2>&1 | head -3

echo "=== F: locate sasquatch ==="
ls -d /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round12/work/sasq/usr/bin 2>/dev/null
ls /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round12/work/sasq/usr/bin 2>/dev/null | head
which sasquatch sasquatch-v4be 2>/dev/null

echo "=== G: unblob on the GENUINE AVM_LE image (correct PATH) ==="
PATH="/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round12/work/sasq/usr/bin:$PATH" \
  /home/vgpnk/.local/bin/unblob -v "$W/avm-le-genuine.squashfs" -e /tmp/r13-avml2 2>&1 | \
  grep -oE "command='[^']*'|handler=[a-z0-9_]*|Can't run extract command|dependencies=\[[^]]*\]" | head -5
echo "--- extracted ---"
find /tmp/r13-avml2 -type f 2>/dev/null | head -6
cat /tmp/r13-avml2/*/apple1.txt 2>/dev/null | head -2
echo "=== H: the BE extractor on the same image ==="
PATH="/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round12/work/sasq/usr/bin:$PATH" \
  sasquatch-v4be -no-exit-code -f -d /tmp/r13-avml3 "$W/avm-le-genuine.squashfs" 2>&1 | tail -4
echo "AVMLE13B_DONE"
