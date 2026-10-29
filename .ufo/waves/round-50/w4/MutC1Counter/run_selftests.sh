#!/bin/bash
S=/fast/scratch/hyaku/kaidoku-r50/w4-MutC1Counter
export TMPDIR="$S"; export HYAKU_SCRATCH="$S/hyaku"
PKG=/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
for v in pristine M1 M2; do
  R="$S/st-$v"
  echo "### $v  counter=$(sha256sum $R/tools/round-50/c1-counter.py | cut -d' ' -f1)" >&2
  python3 -I -B "$R/tools/round-50/c1-counter.py" --selftest --pkg65 "$PKG" --work "$S/work-$v" > "$S/selftest-$v.stdout" 2> "$S/selftest-$v.stderr"
  echo "EXIT=$?" >&2
  echo "$v" >> "$S/selftest-exits.txt"
done
