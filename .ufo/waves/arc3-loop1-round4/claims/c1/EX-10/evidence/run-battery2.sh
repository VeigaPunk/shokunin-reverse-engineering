#!/bin/bash
# EX-10 / arc3-loop1-round4 — battery 2: path-sensitivity / bytes-sensitivity controls
# (the r3 entry's path-sensitivity caveat, tested at round 4 on scratch copies only)
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
OUT=/var/tmp/ex10-r4/out
LOG=/var/tmp/ex10-r4/battery2-log.txt
T1=/var/tmp/ex10-r4/tmpdir
W=/var/tmp/ex10-r4/work
CARRIER=.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.runtime.hex
CARRIER_ABS=$REPO/$CARRIER

: > "$LOG"

mkdir -p "$W/alt" "$W/link" "$W/bytes"
cp "$CARRIER_ABS" "$W/alt/Rv2Token.runtime.hex"
cp "$CARRIER_ABS" "$W/bytes/Rv2Token.runtime.hex"
ln -sf "$CARRIER_ABS" "$W/link/Rv2Token.runtime.hex"
echo "scratch copies:" >> "$LOG"
sha256sum "$W/alt/Rv2Token.runtime.hex" "$W/bytes/Rv2Token.runtime.hex" "$CARRIER_ABS" >> "$LOG"
echo "symlink -> $(readlink -f "$W/link/Rv2Token.runtime.hex")" >> "$LOG"

run() { # $1=leg  $2=cwd  $3...=argv
  local leg="$1"; shift
  local cwd="$1"; shift
  local ts; ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  ( cd "$cwd" && TMPDIR="$T1" npx -y rea-agents@6.4.0 inspect-evm-interface "$@" ) \
      > "$OUT/$leg.json" 2> "$OUT/$leg.err"
  local rc=$?
  local bytes; bytes=$(stat -c %s "$OUT/$leg.json")
  local sha; sha=$(sha256sum "$OUT/$leg.json" | cut -d' ' -f1)
  local eid; eid=$(python3 -c "import json;print(json.load(open('$OUT/$leg.json')).get('evidence_id',''))" 2>/dev/null)
  local bsha; bsha=$(python3 -c "import json;print(json.load(open('$OUT/$leg.json'))['normalized_result']['bytecode']['sha256'])" 2>/dev/null)
  printf '%s | leg=%s | cwd=%s | argv0=%s | hex --format json\n  exit=%s bytes=%s envelope_sha256=%s\n  evidence_id=%s decoded_bytecode_sha256=%s\n' \
    "$ts" "$leg" "$cwd" "$1" "$rc" "$bytes" "$sha" "$eid" "$bsha" >> "$LOG"
}

# 1. cwd variant, SAME resolved path (abs argv) — does cwd leak into the id?
run b2-cwd-var "$W" "$CARRIER_ABS" hex --format json
# 2. same resolved path, different rel spelling (./ prefix) at repo root
run b2-rel-dot "$REPO" "./$CARRIER" hex --format json
# 3. symlink path -> same realpath: realpath-resolved or argv-spelled?
run b2-symlink "$REPO" "$W/link/Rv2Token.runtime.hex" hex --format json
# 4. byte-identical copy at a DIFFERENT resolved path (r3 caveat reproduction)
run b2-altpath-copy "$REPO" "$W/alt/Rv2Token.runtime.hex" hex --format json
# 5. scratch path, original bytes
run b2-bytes-a "$REPO" "$W/bytes/Rv2Token.runtime.hex" hex --format json
# 6. SAME scratch path, mutated bytes (append 0x00 to hex text; still valid hex text)
printf '00' >> "$W/bytes/Rv2Token.runtime.hex"
run b2-bytes-b "$REPO" "$W/bytes/Rv2Token.runtime.hex" hex --format json
echo "BATTERY2-DONE rc=$?" >> "$LOG"
