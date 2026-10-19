#!/bin/bash
# Poll for EX-16's v11 landing: hash movement on .ufo/gates/c1-census-v10.py
# plus 2 stable re-checks; also notes seats/EX-16.md and claims/c2/EX-16/.
L=/var/tmp/ex17r2
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin || exit 9
PRE=6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b
i=0; changed=0
while [ $i -lt 40 ]; do
  i=$((i+1))
  h=$(sha256sum .ufo/gates/c1-census-v10.py | cut -d' ' -f1)
  r=$( [ -f .ufo/waves/arc3-loop1-round2/seats/EX-16.md ] && echo yes || echo no )
  d=$( [ -d .ufo/waves/arc3-loop1-round2/claims/c2/EX-16 ] && echo yes || echo no )
  printf '%s check=%02d hash=%s seats/EX-16=%s claims/c2/EX-16=%s\n' \
    "$(date -u +%H:%M:%SZ)" "$i" "${h:0:12}" "$r" "$d" >> "$L/logs/poll-ex16.log"
  if [ "$h" != "$PRE" ]; then
    changed=$((changed+1))
    if [ $changed -ge 2 ]; then
      echo "$(date -u +%H:%M:%SZ) LANDED stable hash=$h report=$r artifacts=$d" >> "$L/logs/poll-ex16.log"
      exit 0
    fi
  else
    changed=0
  fi
  sleep 40
done
echo "$(date -u +%H:%M:%SZ) POLL-TIMEOUT after $i checks; hash=$h" >> "$L/logs/poll-ex16.log"
exit 3
