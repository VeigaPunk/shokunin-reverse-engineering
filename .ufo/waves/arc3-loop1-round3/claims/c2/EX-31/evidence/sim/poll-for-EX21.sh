#!/bin/bash
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
W=$R/.ufo/waves/arc3-loop1-round3
OUT=/var/tmp/ex31-watch.log
: > $OUT
base_cp=$(sha256sum $R/.ufo/gates/custody-pair/custody-pair.py 2>/dev/null | cut -d' ' -f1)
base_rd=$(sha256sum $R/.ufo/gates/custody-pair/README.md 2>/dev/null | cut -d' ' -f1)
base_sk=$(sha256sum $R/SKILL.md 2>/dev/null | cut -d' ' -f1)
base_sc=$(sha256sum $R/SCORECARD.md 2>/dev/null | cut -d' ' -f1)
base_pv=$(sha256sum $R/PROVINCE.md 2>/dev/null | cut -d' ' -f1)
for i in $(seq 1 25); do
  ts=$(date -Is)
  cp=$(sha256sum $R/.ufo/gates/custody-pair/custody-pair.py 2>/dev/null | cut -d' ' -f1)
  rd=$(sha256sum $R/.ufo/gates/custody-pair/README.md 2>/dev/null | cut -d' ' -f1)
  sk=$(sha256sum $R/SKILL.md 2>/dev/null | cut -d' ' -f1)
  sc=$(sha256sum $R/SCORECARD.md 2>/dev/null | cut -d' ' -f1)
  pv=$(sha256sum $R/PROVINCE.md 2>/dev/null | cut -d' ' -f1)
  seat21=$([ -f $W/seats/EX-21.md ] && echo yes || echo no)
  nseats=$(ls $W/seats/ 2>/dev/null | wc -l)
  echo "$ts check=$i cp=${cp:0:8} rd=${rd:0:8} sk=${sk:0:8} sc=${sc:0:8} pv=${pv:0:8} seat21=$seat21 seats=$nseats" >> $OUT
  if [ "$cp" != "$base_cp" ] || [ "$rd" != "$base_rd" ] || [ "$sk" != "$base_sk" ] || [ "$sc" != "$base_sc" ] || [ "$pv" != "$base_pv" ] || [ "$seat21" = yes ]; then
    echo "CHANGE-DETECTED check=$i $(date -Is)" >> $OUT
    exit 0
  fi
  sleep 60
done
echo "TIMEOUT no-change $(date -Is)" >> $OUT
