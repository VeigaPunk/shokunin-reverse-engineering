#!/usr/bin/env bash
# RV-6 stability poll for EX-16's landing: exits when the gate file hash is
# unchanged across two consecutive 45 s checks, or when EX-16's seat report
# lands, or after 20 checks. Prints the observe log.
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
LOG=/var/tmp/rv6-round2/stability-ex16.log
cd "$REPO" || exit 2
prev=""
for i in $(seq 1 20); do
  H=$(sha256sum .ufo/gates/c1-census-v10.py | cut -d' ' -f1)
  S=$(test -f .ufo/waves/arc3-loop1-round2/seats/EX-16.md && echo 1 || echo 0)
  echo "$(date -u +%H:%M:%SZ) check=$i sha256=$H report=$S" >> "$LOG"
  echo "$(date -u +%H:%M:%SZ) check=$i sha256=${H:0:16} report=$S"
  if [ "$H" = "$prev" ]; then
    echo "STABLE at check=$i sha256=$H report=$S"
    exit 0
  fi
  prev=$H
  [ "$i" -lt 20 ] && sleep 45
done
echo "UNSTABLE after 20 checks last_sha256=$prev"
exit 1
