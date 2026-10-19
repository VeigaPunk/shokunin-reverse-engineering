#!/usr/bin/env bash
# RV-6 poll for EX-16's landing (arc3-loop1-round2). One check every 60 s, max 25.
# Landing signal: gate file sha256 moves off the recorded baseline, or EX-16's
# after-receipts / seat report appear. Exits 0 on landing, 1 on 25 checks without.
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
BASE=6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b
LOG=/var/tmp/rv6-round2/poll-ex16.log
cd "$REPO" || exit 2
for i in $(seq 1 25); do
  H=$(sha256sum .ufo/gates/c1-census-v10.py | cut -d' ' -f1)
  A=$(find .ufo/waves/arc3-loop1-round2/claims/c2/EX-16/receipts -name 'after*' 2>/dev/null | wc -l)
  S=$(test -f .ufo/waves/arc3-loop1-round2/seats/EX-16.md && echo 1 || echo 0)
  R=$(ls .ufo/waves/arc3-loop1-round2/seats/ 2>/dev/null | wc -l)
  echo "$(date -u +%H:%M:%SZ) check=$i gate_sha256=${H:0:16} ex16_after_receipts=$A ex16_report=$S seats_present=$R" >> "$LOG"
  if [ "$H" != "$BASE" ] || [ "$A" -gt 0 ] || [ "$S" = 1 ]; then
    echo "LANDED at check=$i gate_sha256=${H:0:16} after_receipts=$A report=$S"
    exit 0
  fi
  [ "$i" -lt 25 ] && sleep 60
done
echo "NO-LANDING after 25 checks"
exit 1
