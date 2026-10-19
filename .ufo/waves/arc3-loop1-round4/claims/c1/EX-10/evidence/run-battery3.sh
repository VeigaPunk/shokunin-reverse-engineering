#!/bin/bash
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
OUT=/var/tmp/ex10-r4/out
LOG=/var/tmp/ex10-r4/battery3-log.txt
T1=/var/tmp/ex10-r4/tmpdir
CARRIER=.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.runtime.hex
: > "$LOG"
run() { local leg="$1"; shift; local pin="$1"; shift
  local ts; ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  ( cd "$REPO" && TMPDIR="$T1" npx -y "rea-agents@$pin" inspect-evm-interface "$@" ) > "$OUT/$leg.json" 2> "$OUT/$leg.err"
  local rc=$?; local bytes; bytes=$(stat -c %s "$OUT/$leg.json"); local sha; sha=$(sha256sum "$OUT/$leg.json"|cut -d' ' -f1)
  local eid; eid=$(python3 -c "import json;print(json.load(open('$OUT/$leg.json')).get('evidence_id',''))" 2>/dev/null)
  printf '%s | leg=%s | pin=%s | cmd: TMPDIR=%s npx -y rea-agents@%s inspect-evm-interface %s hex --format json\n  exit=%s bytes=%s sha256=%s id=%s\n' "$ts" "$leg" "$pin" "$T1" "$pin" "$CARRIER" "$rc" "$bytes" "$sha" "$eid" >> "$LOG"
}
run pin-6.7.0-r1 6.7.0 "$CARRIER" hex --format json
sleep 2
run pin-6.7.0-r2 6.7.0 "$CARRIER" hex --format json
echo "BATTERY3-DONE" >> "$LOG"
