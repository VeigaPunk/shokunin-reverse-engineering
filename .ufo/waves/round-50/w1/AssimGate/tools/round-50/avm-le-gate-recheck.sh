#!/bin/bash
# avm-le-gate-recheck.sh IMAGE [EXPECTED_SHA256]
# Draft recheck for the AVM-LE assimilation entry (round 50, seat AssimGate).
# Re-measures the facts the entry states on one 4096-byte little-endian image:
#   C1 identity    : sha256 == EXPECTED (default 18d3ad05...afaee4), size 4096
#   C2 superblock  : magic hsqs, compression 4 (xz), mkfs_time == bytes_used
#   C3 unblob      : unblob 26.6.4 selects SQUASHFS_V4_LE and publishes 4 regular files
#   C4 sasquatch   : `sasquatch -le` extracts 4 files, apple1.txt == "apple"
#   C5 BE refusal  : `sasquatch-v4be` (no flag) exits nonzero, "Block size too small", 0 files
# Exit: 0 all clauses met; 1 at least one clause not met; 2 could not evaluate.
# Scratch: requires TMPDIR (never /tmp). No network. Removes its own work directory.
set -u
img="${1-}"
want="${2-18d3ad0563cce852a438fe414d881909a6097fc30a38ca523372931cfcafaee4}"
if [ -z "$img" ] || [ ! -r "$img" ]; then echo "UNEVALUABLE: image not readable: ${img:-<none>}"; exit 2; fi
if [ -z "${TMPDIR-}" ]; then echo "UNEVALUABLE: TMPDIR unset (scratch must not be /tmp)"; exit 2; fi
for t in sasquatch sasquatch-v4be unsquashfs unblob python3 sha256sum; do
  command -v "$t" >/dev/null 2>&1 || { echo "UNEVALUABLE: missing $t"; exit 2; }
done
w=$(mktemp -d "$TMPDIR/avmle-recheck.XXXXXX") || { echo "UNEVALUABLE: mktemp"; exit 2; }
trap 'rm -rf "$w"' EXIT
cp -- "$img" "$w/img.squashfs" || { echo "UNEVALUABLE: copy"; exit 2; }
fail=0

sha=$(sha256sum "$w/img.squashfs" | cut -d' ' -f1)
size=$(stat -c %s "$w/img.squashfs")
if [ "$sha" = "$want" ] && [ "$size" = 4096 ]; then echo "C1 identity PASS sha=$sha size=$size"; else echo "C1 identity FAIL sha=$sha size=$size"; fail=1; fi

sb=$(python3 - "$w/img.squashfs" <<'EOF'
import struct, sys
b = open(sys.argv[1], "rb").read()
magic, _inodes, mkfs = struct.unpack_from("<4sII", b, 0)
comp = struct.unpack_from("<H", b, 20)[0]
used = struct.unpack_from("<Q", b, 40)[0]
print(magic.decode("latin1"), comp, mkfs, used)
EOF
) || { echo "UNEVALUABLE: superblock parse"; exit 2; }
set -- $sb
if [ "$1" = hsqs ] && [ "$2" = 4 ] && [ "$3" = "$4" ]; then echo "C2 superblock PASS magic=$1 comp=$2 mkfs_time=$3 bytes_used=$4"; else echo "C2 superblock FAIL magic=$1 comp=$2 mkfs_time=$3 bytes_used=$4"; fail=1; fi

mkdir -p "$w/ub" "$w/le" "$w/be"
timeout 300 unblob --extract-dir "$w/ub" "$w/img.squashfs" >"$w/unblob.log" 2>&1
ub_n=$(find "$w/ub" -type f -name 'apple*.txt' | wc -l)
if grep -q 'SQUASHFS_V4_LE' "$w/unblob.log" && [ "$ub_n" = 4 ]; then echo "C3 unblob PASS handler=SQUASHFS_V4_LE files=4"; else echo "C3 unblob FAIL files=$ub_n"; fail=1; fi

sasquatch -le -no-exit-code -f -d "$w/le" "$w/img.squashfs" >/dev/null 2>&1
le_n=$(find "$w/le" -type f | wc -l)
le_apple=$(cat "$w/le/apple1.txt" 2>/dev/null | tr -d '\n')
if [ "$le_n" = 4 ] && [ "$le_apple" = apple ]; then echo "C4 sasquatch-le PASS files=$le_n apple1=$le_apple"; else echo "C4 sasquatch-le FAIL files=$le_n apple1=$le_apple"; fail=1; fi

sasquatch-v4be -no-exit-code -f -d "$w/be" "$w/img.squashfs" >"$w/be.out" 2>"$w/be.err"
be_n=$(find "$w/be" -type f | wc -l)
if grep -q 'Block size too small' "$w/be.err" "$w/be.out" && [ "$be_n" = 0 ]; then echo "C5 v4be-refusal PASS files=$be_n"; else echo "C5 v4be-refusal FAIL files=$be_n"; fail=1; fi

if [ "$fail" = 0 ]; then echo "VERDICT met (5/5 clauses)"; exit 0; fi
echo "VERDICT not met"; exit 1
