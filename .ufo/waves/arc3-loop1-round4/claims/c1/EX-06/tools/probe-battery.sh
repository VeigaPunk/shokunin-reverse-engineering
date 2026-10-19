#!/usr/bin/env bash
# EX-06 (arc3-loop1-round4, c1) probe battery on the vyper runtime carrier.
# Every invocation carries a disk-backed TMPDIR under /var/tmp (standing rule).
# Usage: probe-battery.sh <carrier.hex> <tag> [carrier.bin]
set -u
CARRIER="$1"; TAG="$2"; BIN="${3:-}"
TMPDIR_R="/var/tmp/ex06-r4/tmpdir"
OUT="/var/tmp/ex06-r4/out"
LOG="/var/tmp/ex06-r4/work/battery-log.txt"
REPO="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
mkdir -p "$TMPDIR_R" "$OUT"
cd "$REPO" || exit 9

leg() {
  local pin="$1" enc="$2" path="$3" name="$4"; shift 4
  local stamp; stamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  echo "$stamp | cmd: TMPDIR=$TMPDIR_R npx -y rea-agents@$pin inspect-evm-interface $path $enc $*" >> "$LOG"
  TMPDIR="$TMPDIR_R" npx -y "rea-agents@$pin" inspect-evm-interface "$path" "$enc" "$@" \
    > "$OUT/$name.json" 2> "$OUT/$name.err"
  local rc=$?
  echo "$stamp | $name exit=$rc bytes=$(wc -c < "$OUT/$name.json")" >> "$LOG"
  echo "$name exit=$rc bytes=$(wc -c < "$OUT/$name.json") sha256=$(sha256sum "$OUT/$name.json" | cut -d' ' -f1)"
}

leg 6.4.0 hex "$CARRIER" "${TAG}-hex-6.4.0" --format json
leg 6.4.0 hex "$CARRIER" "${TAG}-hex-6.4.0-full" --format json --full-output
leg 6.4.0 hex "$CARRIER" "${TAG}-hex-6.4.0-rerun" --format json
leg 6.4.0 hex "$CARRIER" "${TAG}-hex-6.4.0-default"
leg 6.7.0 hex "$CARRIER" "${TAG}-hex-6.7.0" --format json
leg 6.7.0 hex "$CARRIER" "${TAG}-hex-6.7.0-full" --format json --full-output
if [ -n "$BIN" ] && [ -f "$BIN" ]; then
  leg 6.4.0 raw "$BIN" "${TAG}-raw-6.4.0" --format json
  leg 6.4.0 hex "$BIN" "${TAG}-trap-hex-on-bin" --format json
fi
leg 6.4.0 raw "$CARRIER" "${TAG}-trap-raw-on-hex" --format json
echo "battery done: $TAG"
