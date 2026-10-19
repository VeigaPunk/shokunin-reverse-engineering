#!/usr/bin/env bash
# RV-6 sampled audit trail: audit every observed revision until the gate file
# hash is unchanged across two consecutive 20 s samples (or 12 samples).
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
W=/var/tmp/rv6-round2
L="$REPO/.ufo/waves/arc3-loop1-round2/claims/c2/RV-6/logs"
TRAIL="$L/revision-audit-trail.txt"
AUDIT="$REPO/.ufo/waves/arc3-loop1-round2/claims/c2/RV-6/tools/scope-creep-audit.py"
BEFORE="$REPO/.ufo/waves/arc3-loop1-round2/claims/c2/RV-6/before/c1-census-v10.py"
mkdir -p "$W/samples"
cd "$REPO" || exit 2
prev=""
for i in $(seq 1 12); do
  H=$(sha256sum .ufo/gates/c1-census-v10.py | cut -d' ' -f1)
  cp .ufo/gates/c1-census-v10.py "$W/samples/$H.py"
  OUT=$(python3 "$AUDIT" "$BEFORE" "$W/samples/$H.py" --root . --expect-rows 20)
  ROWS=$(echo "$OUT" | grep -o 'rows_unchanged=[A-Z]*')
  KEYS=$(echo "$OUT" | grep -o 'KEYSET identical=[A-Z]*')
  FLAGS=$(echo "$OUT" | grep -o 'CREEP FLAGS ([0-9]*)')
  CANON=$(echo "$OUT" | grep -o 'after_ordered_sha256=[0-9a-f]*')
  LINES=$(wc -l < "$W/samples/$H.py")
  echo "$(date -u +%H:%M:%SZ) sample=$i sha256=$H lines=$LINES $ROWS $KEYS $CANON $FLAGS" >> "$TRAIL"
  echo "$(date -u +%H:%M:%SZ) sample=$i sha256=${H:0:16} lines=$LINES $ROWS $KEYS $FLAGS"
  if [ "$H" = "$prev" ]; then
    echo "STABLE at sample=$i sha256=$H"
    exit 0
  fi
  prev=$H
  [ "$i" -lt 12 ] && sleep 20
done
echo "STILL-CHURNING after 12 samples, last sha256=$prev"
exit 1
