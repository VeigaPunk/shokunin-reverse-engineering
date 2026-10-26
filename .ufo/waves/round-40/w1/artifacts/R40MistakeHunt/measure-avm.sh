#!/bin/sh
# Reproduce the AVM-layout measurements behind MH-5 and MH-6.
# Inputs: the retained genuine AVM-BE image in shokuknow (read-only, copied to scratch), the
# lane's round-39 writer, and this seat's patched writer. No REA and no unblob run: sasquatch-v4be
# is invoked directly on 4096-byte probe fixtures, none of which is a frozen C1 carrier.
set -u
A=$(cd "$(dirname "$0")" && pwd)
L=${LANE:-/home/vgpnk/Projects/shokunin/kaidoku-shokunin}
S=${TMPDIR:-/tmp}
W="$S/avm-measure"
rm -rf "$W"; mkdir -p "$W"
SRC=/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/avm-be.squashfs

echo "### genuine AVM-BE probe fixture (round-11 lane artifact, read-only source)"
ls -l "$SRC"
sha256sum "$SRC"
cp "$SRC" "$W/genuine.squashfs"
sha256sum "$W/genuine.squashfs"

echo
echo "### superblock fields (big-endian header) and metadata block-length decode"
python3 - "$W/genuine.squashfs" "$W/markerstripped.squashfs" <<'PY'
import struct, sys
src, dst = sys.argv[1], sys.argv[2]
b = bytearray(open(src, 'rb').read())
def dump(name, blob):
    its = int.from_bytes(blob[64:72], 'big')
    hdr = bytes(blob[its:its+2])
    print(f'{name}: magic={bytes(blob[:4])!r} mkfs_time={int.from_bytes(blob[8:12],"big")} '
          f'bytes_used={int.from_bytes(blob[40:48],"big")} comp_id={int.from_bytes(blob[20:22],"big")} '
          f'inode_table_start={its} hdr={hdr.hex()} len_LE={int.from_bytes(hdr,"little")&0x7fff} '
          f'len_BE={int.from_bytes(hdr,"big")&0x7fff}')
dump('genuine          ', b)
b[8:12] = struct.pack('>I', 1700000000)
open(dst, 'wb').write(b)
dump('marker stripped  ', b)
PY
sha256sum "$W/markerstripped.squashfs"

echo
echo "### sasquatch-v4be 4.5.1 matrix (the two directions of the marker)"
for img in genuine markerstripped; do
  for flag in noflag -be; do
    out="$W/ext-$img-$flag"; rm -rf "$out"; mkdir -p "$out"
    if [ "$flag" = noflag ]; then
      sasquatch-v4be -no-exit-code -f -d "$out" "$W/$img.squashfs" >"$out.out" 2>"$out.err"
    else
      sasquatch-v4be -be -no-exit-code -f -d "$out" "$W/$img.squashfs" >"$out.out" 2>"$out.err"
    fi
    printf '%-16s %-6s exit=%s files=%s first_stderr=%s\n' "$img" "$flag" "$?" \
      "$(find "$out" -type f | wc -l)" "$(head -1 "$out.err" | cut -c1-90)"
  done
done

echo
echo "### the writer the round-40 carrier plan needs (MH-5 green artifact)"
mkdir -p "$W/tree/etc" "$W/tree/bin"
printf 'hello avm\n' > "$W/tree/etc/a.txt"
printf '#!/bin/sh\necho hi\n' > "$W/tree/bin/run"
for comp in gzip xz; do
  python3 -I -B "$L/tools/round-39/gen-squashfs.py" "$W/tree" "$W/stock-$comp.sqsh" --endian avm --comp "$comp"
  python3 -I -B "$A/gen-squashfs-avm-mode-fixed.py" "$W/tree" "$W/fixed-$comp.sqsh" --endian avm --comp "$comp"
  for kind in stock fixed; do
    img="$W/$kind-$comp.sqsh"
    python3 - "$img" <<'PY'
import sys
b = open(sys.argv[1], 'rb').read()
its = int.from_bytes(b[64:72], 'big'); hdr = b[its:its+2]
print(f'  {sys.argv[1].split("/")[-1]}: mkfs={int.from_bytes(b[8:12],"big")} '
      f'bytes_used={int.from_bytes(b[40:48],"big")} comp_id={int.from_bytes(b[20:22],"big")} '
      f'hdr={hdr.hex()} len_LE={int.from_bytes(hdr,"little")&0x7fff} '
      f'len_BE={int.from_bytes(hdr,"big")&0x7fff}')
PY
    out="$W/ext-$kind-$comp"; rm -rf "$out"; mkdir -p "$out"
    sasquatch-v4be -no-exit-code -f -d "$out" "$img" >"$out.out" 2>"$out.err"
    printf '  %-5s %-4s noflag exit=%s files=%s\n' "$kind" "$comp" "$?" "$(find "$out" -type f | wc -l)"
    out="$W/ext-$kind-$comp-be"; rm -rf "$out"; mkdir -p "$out"
    sasquatch-v4be -be -no-exit-code -f -d "$out" "$img" >"$out.out" 2>"$out.err"
    printf '  %-5s %-4s -be    exit=%s files=%s\n' "$kind" "$comp" "$?" "$(find "$out" -type f | wc -l)"
  done
done
sha256sum "$W/fixed-gzip.sqsh" "$W/fixed-xz.sqsh"

echo
echo "### frozen interpreter labels for the three shapes the v1 table must separate"
cd "$L" || exit 2
for h in H13 H15 H01; do
  printf '%s: ' "$h"
  python3 -I -B tools/round-39/sqfs-triage.py --skill SKILL.md --json \
    "corpus/evidence/round-39/c2/heldout/$h/envelope.json" \
  | python3 -c "import json,sys; r=json.load(sys.stdin)['results'][0]; print('label=',r['label'],'rule=',r['rule'],'| cause:',r['row'][7][:110])"
done
echo
echo "### end"
