#!/bin/bash
# CR-3 poll: watch for EX-14 map, EX-16 gate landing, other c2/c3 seat reports.
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
LOG=/var/tmp/cr3/receipts/poll-log.txt
for i in $(seq 1 25); do
  ts=$(date -u +%H:%M:%SZ)
  gate_sha=$(sha256sum .ufo/gates/c1-census-v10.py | cut -c1-16)
  ex14=$(find .ufo/waves/arc3-loop1-round2/claims/c2/EX-14 -type f 2>/dev/null | wc -l)
  seats=$(ls .ufo/waves/arc3-loop1-round2/seats/ 2>/dev/null | tr '\n' ' ')
  g20=$(grep -c "g20\|G20" .ufo/gates/c1-census-v10.py)
  echo "$ts check=$i gate_sha=$gate_sha g20_lines=$g20 ex14_files=$ex14 seats=[$seats]" >> $LOG
  if [ "$ex14" -gt 0 ] && [ "$g20" -gt 0 ]; then echo "CONDITION-MET at check $i" >> $LOG; fi
  sleep 60
done
