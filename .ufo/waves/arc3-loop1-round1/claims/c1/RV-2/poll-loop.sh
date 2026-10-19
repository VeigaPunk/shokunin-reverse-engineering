#!/usr/bin/env bash
# RV-2 poller: watch for EX-05 / EX-07 artifacts + seat reports; max 25 checks x 60s
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1
LOG=claims/c1/RV-2/poll-log.txt
: > "$LOG"
for i in $(seq 1 25); do
  TS=$(date -u +%H:%M:%S)
  EX05=$(find claims/c1/EX-05 -type f 2>/dev/null | wc -l)
  EX07=$(find claims/c1/EX-07 -type f 2>/dev/null | wc -l)
  S05=$([ -f seats/EX-05.md ] && echo yes || echo no)
  S07=$([ -f seats/EX-07.md ] && echo yes || echo no)
  echo "$TS check=$i EX-05-files=$EX05 seat=$S05 | EX-07-files=$EX07 seat=$S07" >> "$LOG"
  if [ "$EX05" -gt 0 ] && [ "$S05" = yes ] && [ "$EX07" -gt 0 ]; then
    echo "$TS STOPPING: EX-05 artifacts + report landed" >> "$LOG"; break
  fi
  sleep 60
done
echo "$(date -u +%H:%M:%S) poller exit" >> "$LOG"
