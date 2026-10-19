#!/usr/bin/env bash
# CU-1 (arc3-loop1-round3) custody drift watcher: 30 checks x 60 s.
# Read-only over custody paths; writes only this log and the poll log.
set -u
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
ART=.ufo/waves/arc3-loop1-round3/claims/cross/CU-1
LOG=$ART/watch-log.txt
POLL=$ART/poll-log.txt
PATHS=(
  "$HOME/.config/devin/mcp_config.json"
  "$HOME/.omp/agent/mcp.json"
  "$HOME/.kimi-code/config.toml"
  "$HOME/.bashrc"
  "$HOME/.profile"
)
BASE=$ART/capture-pre-indep.txt
: > "$LOG"; : > "$POLL"
for i in $(seq 1 30); do
  ts=$(date -u +%FT%TZ)
  sum=""
  for p in "${PATHS[@]}"; do
    s=$(sha256sum -- "$p" | cut -c1-12)
    i_=$(stat -c '%i' -- "$p")
    z=$(stat -c '%Z' -- "$p")
    sum="$sum $(basename "$p")=$s/$i_/$z"
  done
  echo "$ts check=$i drift-summary:$sum" >> "$LOG"
  post=$(ls "$ART"/../..//c2/receipts/*post* 2>/dev/null | head -1)
  seats=$(ls .ufo/waves/arc3-loop1-round3/seats/ 2>/dev/null | tr '\n' ' ')
  echo "$ts check=$i post-receipt=[${post:-none}] seats=[$seats]" >> "$POLL"
  sleep 60
done
echo "$(date -u +%FT%TZ) watcher-loop-complete" >> "$LOG"