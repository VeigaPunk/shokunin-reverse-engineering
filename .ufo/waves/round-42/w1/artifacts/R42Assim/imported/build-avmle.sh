#!/bin/bash
# Round 13, target 2: build the AVM_FORMAT_AS_OPTION variant of the Freetz
# squashfs4.3 toolchain and produce a GENUINE AVM_LE image
# (little-endian SquashFS whose mkfs_time field equals bytes_used).
W=/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round13/work
cd "$W/sq43/squashfs4.3/squashfs-tools" || { echo NO_TREE; exit 1; }

echo "=== DIAG 1: does mksquashfs.c include _endian.h? ==="
grep -n '_endian.h' mksquashfs.c | head -3
echo "=== DIAG 2: the two mkfs_time assignments and their enclosing functions ==="
grep -n 'mkfs_time' mksquashfs.c
echo "--- function containing the AVM assignment (searching backwards) ---"
awk 'NR<=4474 && /^[a-zA-Z_].*\(.*\)$|^static .*\(|^void / {f=NR": "$0} END{print f}' mksquashfs.c
echo "--- function containing the time(NULL) assignment ---"
awk 'NR<=5312 && /^[a-zA-Z_].*\(.*\)$|^static .*\(|^void / {f=NR": "$0} END{print f}' mksquashfs.c
echo "=== DIAG 3: context around line 5312 ==="
sed -n '5300,5320p' mksquashfs.c
echo "=== DIAG 4: context around 4460-4480 ==="
sed -n '4455,4480p' mksquashfs.c

echo "=== BUILD with TARGET_FORMAT=AVM_LE + AVM_FORMAT_AS_OPTION ==="
make -j4 CC=gcc EXTRA_CFLAGS="-fcommon -DTARGET_FORMAT=AVM_LE -DAVM_FORMAT_AS_OPTION -std=gnu89" \
     LEGACY_FORMATS_SUPPORT=1 GZIP_SUPPORT=1 LZMA_XZ_SUPPORT=1 XZ_SUPPORT=1 \
     COMP_DEFAULT=xz XATTR_SUPPORT=0 XATTR_DEFAULT=0 mksquashfs unsquashfs > "$W/build-avmle.log" 2>&1
echo "make exit=$?"
grep -E 'error:|Error' "$W/build-avmle.log" | head -5
ls -la mksquashfs unsquashfs 2>/dev/null | head -3
echo "=== VERIFY the preprocessor actually took the AVM branch ==="
gcc -E -I. -DTARGET_FORMAT=AVM_LE -DAVM_FORMAT_AS_OPTION mksquashfs.c 2>/dev/null | grep -n -A 2 'bytes_used = bytes' | head -8

if [ -x mksquashfs ]; then
  rm -rf "$W/avmlsrc"; mkdir -p "$W/avmlsrc"
  printf 'apple\n' > "$W/avmlsrc/apple1.txt"; printf 'banana\n' > "$W/avmlsrc/apple2.txt"
  printf 'cherry\n' > "$W/avmlsrc/apple3.txt"; printf 'date\n' > "$W/avmlsrc/apple4.txt"
  echo "=== CREATE the image with -no-mkfs-time (strict AVM format) ==="
  ./mksquashfs "$W/avmlsrc" "$W/avm-le-genuine.squashfs" -comp xz -no-mkfs-time \
      -all-root -no-progress -no-exports -no-sparse -b 65536 2>&1 | tail -4
  echo "=== MEASURE the superblock ==="
  python3 -c "
import struct,os
p='$W/avm-le-genuine.squashfs'
d=open(p,'rb').read()
be = d[:4]==b'sqsh'
e = '>' if be else '<'
mt=struct.unpack(e+'I',d[8:12])[0]; bu=struct.unpack(e+'Q',d[40:48])[0]
print('  bytes',len(d),'magic',d[:4],'(sqsh=BE, hsqs=LE)','compression',struct.unpack(e+'H',d[20:22])[0],'(4=xz)')
print('  mkfs_time',mt,'bytes_used',bu,'->','AVM MARKER SET (equal)' if mt==bu else 'NOT AVM')
print('  little_endian' if not be else '  big_endian')"
  echo "=== the patched unsquashfs -stat on it (upstream's own AVM interpretation) ==="
  ./unsquashfs -stat "$W/avm-le-genuine.squashfs" 2>&1 | head -8
  echo "=== unblob on the GENUINE AVM_LE image ==="
  PATH="$W/sasq/usr/bin:$PATH" /home/vgpnk/.local/bin/unblob -v "$W/avm-le-genuine.squashfs" -e /tmp/r13-avml 2>&1 | \
    grep -oE "command='[^']*'|handler=[a-z0-9_]*|Can't run extract command|dependencies=\[[^]]*\]" | head -5
  echo "--- extracted files ---"
  find /tmp/r13-avml -type f 2>/dev/null | head -6
  echo "--- content check ---"
  cat /tmp/r13-avml/*/apple1.txt 2>/dev/null | head -2
  echo "=== direct sasquatch-v4be on it (the BE extractor) ==="
  PATH="$W/sasq/usr/bin:$PATH" sasquatch-v4be -no-exit-code -f -d /tmp/r13-avmld "$W/avm-le-genuine.squashfs" 2>&1 | tail -4
fi
echo "AVMLE13_DONE"
