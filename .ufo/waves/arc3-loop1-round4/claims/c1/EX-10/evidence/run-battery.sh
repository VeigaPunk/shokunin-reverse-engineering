#!/bin/bash
# EX-10 / arc3-loop1-round4 — id-stability rerun battery (scratch; no repo writes)
# Repeat EX-06's r3 exact invocation twice + path/encoding variants. Log verbatim.
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
OUT=/var/tmp/ex10-r4/out
LOG=/var/tmp/ex10-r4/battery-log.txt
T1=/var/tmp/ex10-r4/tmpdir
T2=/var/tmp/ex10-r4/tmpdir2
CARRIER=.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.runtime.hex
CARRIER_ABS=$REPO/$CARRIER

: > "$LOG"

run() { # $1=leg-name  $2=TMPDIR  $3...=argv after "inspect-evm-interface"
  local leg="$1"; shift
  local tdir="$1"; shift
  local cmd="TMPDIR=$tdir npx -y rea-agents@6.4.0 inspect-evm-interface $*"
  local ts; ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  local t0; t0=$(date +%s.%N)
  ( cd "$REPO" && TMPDIR="$tdir" npx -y rea-agents@6.4.0 inspect-evm-interface "$@" ) \
      > "$OUT/$leg.json" 2> "$OUT/$leg.err"
  local rc=$?
  local t1; t1=$(date +%s.%N)
  local bytes; bytes=$(stat -c %s "$OUT/$leg.json")
  local sha; sha=$(sha256sum "$OUT/$leg.json" | cut -d' ' -f1)
  local eid; eid=$(python3 -c "import json,sys;print(json.load(open('$OUT/$leg.json')).get('evidence_id',''))" 2>/dev/null)
  local dur; dur=$(python3 -c "print(f'{$t1-$t0:.1f}')")
  printf '%s | leg=%s | cmd: %s\n  exit=%s bytes=%s dur=%ss sha256=%s\n  evidence_id=%s\n' \
    "$ts" "$leg" "$cmd" "$rc" "$bytes" "$dur" "$sha" "$eid" >> "$LOG"
}

# --- the two exact repeats of EX-06's r3 invocation (same TMPDIR, cwd=repo root, rel path) ---
run exact-r1 "$T1" "$CARRIER" hex --format json
sleep 3
run exact-r2 "$T1" "$CARRIER" hex --format json

# --- controls: TMPDIR variant (EX-06's own tmpdir path), second tmpdir, abs-path argv, cwd/abs ---
run var-ex06tmpdir /var/tmp/ex06-r3/tmpdir "$CARRIER" hex --format json
run var-tmpdir2 "$T2" "$CARRIER" hex --format json
run var-abspath "$T1" "$CARRIER_ABS" hex --format json
run var-abs-cwdroot "$T1" "$CARRIER_ABS" hex --format json
run var-cwd-abs-from-tmp "$T1" "$CARRIER_ABS" hex --format json
echo "BATTERY-DONE rc=$?" >> "$LOG"
