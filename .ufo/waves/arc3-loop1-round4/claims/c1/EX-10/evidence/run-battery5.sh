#!/bin/bash
# EX-10 battery 5: EX-06's probe-log.txt invocation VERBATIM (TMPDIR included), twice
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
OUT=/var/tmp/ex10-r4/out
LOG=/var/tmp/ex10-r4/battery5-log.txt
: > "$LOG"
for i in 1 2; do
  leg="exact-verbatim-r$i"
  ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  ( cd "$REPO" && TMPDIR=/var/tmp/ex06-r3/tmpdir npx -y rea-agents@6.4.0 inspect-evm-interface .ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.runtime.hex hex --format json ) > "$OUT/$leg.json" 2> "$OUT/$leg.err"
  rc=$?
  sha=$(sha256sum "$OUT/$leg.json"|cut -d' ' -f1)
  eid=$(python3 -c "import json;print(json.load(open('$OUT/$leg.json')).get('evidence_id',''))" 2>/dev/null)
  printf '%s | %s | VERBATIM probe-log.txt line 2 (TMPDIR=/var/tmp/ex06-r3/tmpdir)\n  exit=%s bytes=%s sha256=%s\n  id=%s\n' "$ts" "$leg" "$rc" "$(stat -c %s "$OUT/$leg.json")" "$sha" "$eid" >> "$LOG"
  sleep 2
done
echo "BATTERY5-DONE" >> "$LOG"
