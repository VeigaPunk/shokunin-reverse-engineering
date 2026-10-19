#!/bin/bash
# RV-4 background poller: watch for EX-16's landed census edit / seat report.
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
LOG=/var/tmp/rv4-mutation/poll-ex16.log
: > "$LOG"
for i in $(seq 1 25); do
  ts=$(date -u +%H:%M:%S)
  sha=$(sha256sum "$R/.ufo/gates/c1-census-v10.py" | cut -d' ' -f1)
  ex16=$(ls -1 "$R/.ufo/waves/arc3-loop1-round2/claims/c2/EX-16/" 2>/dev/null | tr '\n' ',')
  seats=$(ls -1 "$R/.ufo/waves/arc3-loop1-round2/seats/" 2>/dev/null | wc -l)
  echo "$ts check=$i census=$sha ex16=[$ex16] seats=$seats" >> "$LOG"
  if [ "$sha" != "6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b" ]; then
    echo "$ts LANDED: census sha changed -> $sha" >> "$LOG"; break
  fi
  sleep 60
done
echo "$(date -u +%H:%M:%S) poller done" >> "$LOG"
