#!/usr/bin/env bash
# RV-13 field-isolation battery — which stat/hash field is the sole discriminator
# for a same-content rewrite?  All work in /var/tmp (never /tmp, never a real
# custody path).  Each case: fresh dir, byte copy of the stand-in subject,
# v2 receipt captured, mutation applied, three verifiers run (v1 sha-only,
# v2-seconds granularity, v2+ns).
set -u
W=/var/tmp/rv13
PROTO="$W/custody_v2_proto.py"
BASE="$W/scratch"
PRISTINE="$W/pristine.conf"
OUT="$W/battery-report.txt"

rm -rf "$BASE"; mkdir -p "$BASE"
: > "$OUT"

case_report() {  # $1 = case name
  local C="$1"; local S="$BASE/$C/subject.conf"
  echo "=== $C ===" >> "$OUT"
  echo "-- post state: $(stat -c 'size=%s inode=%i mtime=%Y mtime_ns=%y ctime=%Z ctime_ns=%z mode=%a' "$S")" >> "$OUT"
  echo "-- sha256: $(sha256sum "$S" | cut -d' ' -f1)" >> "$OUT"
  for mode in verify-shasum-only verify-seconds verify; do
    local out; out=$(python3 "$PROTO" "$mode" "$BASE/$C/pre.receipt" "$S" 2>&1); local rc=$?
    printf -- "-- %-18s exit=%s\n%s\n" "$mode" "$rc" "$(echo "$out" | sed 's/^/     /')" >> "$OUT"
  done
  echo >> "$OUT"
}

new_case() { local C="$1"; mkdir -p "$BASE/$C"; cp -p "$PRISTINE" "$BASE/$C/subject.conf";
             python3 "$PROTO" emit "$BASE/$C/subject.conf" > "$BASE/$C/pre.receipt"; }

# stand-in subject (synthesized; no custody bytes involved)
[ -f "$PRISTINE" ] || { printf 'custody-stand-in\n' > "$PRISTINE"; head -c 4100 /dev/urandom >> "$PRISTINE"; }

echo "# RV-13 field-isolation battery  $(date -u '+%Y-%m-%dT%H:%M:%SZ')" >> "$OUT"
echo "# subject stand-in sha256: $(sha256sum "$PRISTINE" | cut -d' ' -f1)" >> "$OUT"
echo "# verifier: $PROTO" >> "$OUT"
echo >> "$OUT"

# F0a untouched control
new_case F0a-untouched
case_report F0a-untouched

# F0b atime-only perturbation
new_case F0b-atime-only
cat "$BASE/F0b-atime-only/subject.conf" > /dev/null
case_report F0b-atime-only

# F1 in-place same-content rewrite (inode preserved, mtime moves, ctime moves)
new_case F1-inplace-same-content
PRE_MTIME=$(stat -c %Y "$BASE/F1-inplace-same-content/subject.conf")
dd if="$PRISTINE" of="$BASE/F1-inplace-same-content/subject.conf" bs=4096 conv=notrunc status=none
echo "-- pre_mtime=$PRE_MTIME (unchanged by design in F1)" >> "$OUT"
case_report F1-inplace-same-content

# F2 in-place same-content rewrite + mtime restored to the exact pre epoch
#    -> size/sha256/inode/mtime(seconds) all equal; only ctime (and mtime_ns) move
new_case F2-inplace-mtime-restored
PRE_MTIME=$(stat -c %Y "$BASE/F2-inplace-mtime-restored/subject.conf")
dd if="$PRISTINE" of="$BASE/F2-inplace-mtime-restored/subject.conf" bs=4096 conv=notrunc status=none
touch -d "@$PRE_MTIME" "$BASE/F2-inplace-mtime-restored/subject.conf"
echo "-- restored mtime epoch $PRE_MTIME; pre-receipt mtime_epoch = $(grep '^MTIME_EPOCH' "$BASE/F2-inplace-mtime-restored/pre.receipt")" >> "$OUT"
case_report F2-inplace-mtime-restored

# F3 replace-by-new-file, same content, mtime+mode restored (inode changes)
new_case F3-replace-new-inode
PRE_MTIME=$(stat -c %Y "$BASE/F3-replace-new-inode/subject.conf")
PRE_INODE=$(stat -c %i "$BASE/F3-replace-new-inode/subject.conf")
cp "$PRISTINE" "$BASE/F3-replace-new-inode/subject.new"
touch -r "$BASE/F3-replace-new-inode/subject.conf" "$BASE/F3-replace-new-inode/subject.new"
mv -f "$BASE/F3-replace-new-inode/subject.new" "$BASE/F3-replace-new-inode/subject.conf"
echo "-- pre inode=$PRE_INODE mtime=$PRE_MTIME" >> "$OUT"
case_report F3-replace-new-inode

# F4 content change (1 byte) with mtime restored, same inode
#    -> sha256/size must be load-bearing too
new_case F4-content-change
PRE_MTIME=$(stat -c %Y "$BASE/F4-content-change/subject.conf")
printf 'X' >> "$BASE/F4-content-change/subject.conf"
touch -d "@$PRE_MTIME" "$BASE/F4-content-change/subject.conf"
echo "-- content appended 1 byte, mtime restored to $PRE_MTIME" >> "$OUT"
case_report F4-content-change

# F5 no-op metadata touch: chmod to the SAME mode (0o644 -> 0o644)
new_case F5-noop-chmod
chmod 644 "$BASE/F5-noop-chmod/subject.conf"
echo "-- chmod 644 on an already-0o644 file" >> "$OUT"
case_report F5-noop-chmod

# F6 hardlink swap of a second identical-content file with mtime restored
#    (inode DIFFERENT but size/sha256/mtime/mode equal)
new_case F6-hardlink-swap
PRE_MTIME=$(stat -c %Y "$BASE/F6-hardlink-swap/subject.conf")
cp "$PRISTINE" "$BASE/F6-hardlink-swap/other.conf"
touch -d "@$PRE_MTIME" "$BASE/F6-hardlink-swap/other.conf"
mv -f "$BASE/F6-hardlink-swap/other.conf" "$BASE/F6-hardlink-swap/subject.conf"
case_report F6-hardlink-swap

cat "$OUT"
echo "REPORT: $OUT"
