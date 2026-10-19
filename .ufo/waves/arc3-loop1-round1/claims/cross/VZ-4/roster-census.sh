#!/bin/bash
# VZ-4 roster census: delivered/64 vs the frozen roster (claims-frozen.md:90-95)
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
W=.ufo/waves/arc3-loop1-round1
C1="PL-1 $(seq -f 'EX-%02g' 1 15 | tr '\n' ' ')SC-1 SC-2 SC-3 RV-1 RV-2 RV-3 RV-4 CR-1 CR-2 VZ-1"
C2="PL-2 $(seq -f 'EX-%02g' 16 25 | tr '\n' ' ')SC-4 SC-5 RV-5 RV-6 RV-7 RV-8 CR-3 CR-4 VZ-2"
C3="PL-3 $(seq -f 'EX-%02g' 26 31 | tr '\n' ' ')SC-6 SC-7 RV-9 RV-10 RV-11 CR-5 VZ-3"
CX="CN-1 CN-2 CU-1 VZ-4"
ALL="$C1 $C2 $C3 $CX"
echo "== roster size: $(echo $ALL | wc -w) =="
echo "== delivered: $(ls $W/seats/*.md 2>/dev/null | wc -l) =="
for chain in "C1:$C1" "C2:$C2" "C3:$C3" "CX:$CX"; do
  name=${chain%%:*}; seats=${chain#*:}
  tot=0; got=0; miss=""
  for s in $seats; do tot=$((tot+1)); if [ -f "$W/seats/$s.md" ]; then got=$((got+1)); else miss="$miss $s"; fi; done
  echo "$name: $got/$tot missing:$miss"
done
echo "== stray seat files not in roster =="
for f in $W/seats/*.md; do [ -e "$f" ] || continue; s=$(basename "$f" .md); echo "$ALL" | grep -qw "$s" || echo "  STRAY: $s"; done
