#!/bin/bash
# EX-29 poll: wait for the revised custody tool (sha change) — 25 checks x 60s
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
BASE=112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa
LOG=.ufo/waves/arc3-loop1-round3/claims/c2/EX-29/poll-log.txt
: > "$LOG"
for i in $(seq 1 25); do
  SHA=$(sha256sum .ufo/gates/custody-pair/custody-pair.py | cut -d' ' -f1)
  SEATS=$(ls .ufo/waves/arc3-loop1-round3/seats/ 2>/dev/null | tr '\n' ' ')
  echo "$(date -u +%FT%TZ) check=$i tool=$SHA seats=[$SEATS]" >> "$LOG"
  if [ "$SHA" != "$BASE" ]; then
    echo "TOOL-REVISED after check=$i sha=$SHA" | tee -a "$LOG"
    exit 0
  fi
  sleep 60
done
echo "POLL-EXHAUSTED tool unchanged after 25 checks sha=$SHA" | tee -a "$LOG"
exit 0
