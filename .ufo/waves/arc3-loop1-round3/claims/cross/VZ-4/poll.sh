#!/bin/bash
# VZ-4 standing poller — 30 checks at 60 s, seat-report census each check.
# Runs against the wave dir; scratch/log file inside this seat's artifact dir.
W=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round3
OUT=$W/claims/cross/VZ-4/poll-log.txt
: > "$OUT"
for i in $(seq 1 30); do
  ts=$(date -u +%FT%TZ)
  n=$(ls "$W/seats/" 2>/dev/null | grep -c '\.md$')
  names=$(ls "$W/seats/" 2>/dev/null | sed 's/\.md$//' | sort | tr '\n' ',')
  printf '%s check=%02d seats=%d :: %s\n' "$ts" "$i" "$n" "$names" >> "$OUT"
  [ "$i" -lt 30 ] && sleep 60
done
printf '%s poller=done\n' "$(date -u +%FT%TZ)" >> "$OUT"