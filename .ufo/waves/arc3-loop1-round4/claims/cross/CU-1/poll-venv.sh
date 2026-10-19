#!/bin/bash
W=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round4
L=/dev/shm/cu1/poll-venv.log
echo "=== poller start $(date -Is) ===" >> $L
for i in $(seq 1 25); do
  ts=$(date -Is)
  seats=$(ls $W/seats/ 2>/dev/null | wc -l)
  venv="absent"; [ -e $W/tools/vyper-venv ] && venv="present"
  recv=$(ls $W/claims/c1/EX-02/ 2>/dev/null | wc -l)
  files=$(find $W/claims -type f 2>/dev/null | wc -l)
  echo "[$i] $ts seats=$seats venv=$venv EX-02-files=$recv claim-files=$files" >> $L
  ls $W/seats/ 2>/dev/null | tr '\n' ' ' >> $L; echo >> $L
  if [ "$venv" = "present" ] && [ "$recv" -gt 0 ]; then echo "  -> venv+receipt landed at $ts" >> $L; fi
  sleep 60
done
echo "=== poller end $(date -Is) ===" >> $L
