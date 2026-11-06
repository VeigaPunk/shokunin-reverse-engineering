#!/bin/bash
# ExecReproC1: sequential frozen R100-C1 battery runs (5 configs), own clone only.
set -u
S=/fast/scratch/hyaku/kaidoku-r100/ExecReproC1
C=$S/clone
F=8e24c29a37ca81a0bd1ff5ec73c96a949885322e
A1=a610671d7a01e1d762eb7103e6ee9f8a2be287ed
TIP=$(git -C "$C" rev-parse origin/main 2>/dev/null || git -C "$C" rev-parse main)
echo "tip=$TIP" >> "$S/logs/runs.log"

run_one() {
  name=$1; rev=$2; repair=$3
  if ! git -C "$C" checkout --detach --quiet "$rev"; then
    echo "$name CHECKOUT-FAIL" >> "$S/logs/runs.log"; return
  fi
  top=$(git -C "$C" rev-parse --show-toplevel)
  if [ "$top" != "$C" ]; then echo "$name TOPLEVEL-MISMATCH:$top" >> "$S/logs/runs.log"; return; fi
  echo "== $name rev=$rev repair=$repair start=$(date -u +%H:%M:%S)" >> "$S/logs/runs.log"
  ( cd "$C" && TMPDIR="$S/tmp" python3 -I -B tools/round-100/pe-upx-corrupt-battery.py \
      --root "$C" --repair "$repair" --rev "$rev" \
      --work "$S/work-$name" --json-out "$S/receipts/$name.json" \
      > "$S/logs/$name.log" 2>&1 )
  echo "$name rc=$?" >> "$S/logs/runs.log"
  tail -1 "$S/logs/$name.log" >> "$S/logs/runs.log"
}

run_one a1  "$A1" tools/round-100/upx-pe-repair.py
run_one tip "$TIP" tools/round-100/upx-pe-repair.py
run_one r99 "$F"  tools/round-99/upx-pe-repair.py
run_one h4  "$F"  tools/round-100/forgeries/h4-oracle-alias.py
run_one h6  "$F"  tools/round-100/forgeries/h6-exec-only.py
echo "ALL-DONE $(date -u +%H:%M:%S)" >> "$S/logs/runs.log"
