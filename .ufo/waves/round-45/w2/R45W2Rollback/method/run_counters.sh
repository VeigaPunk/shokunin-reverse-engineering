#!/bin/bash
# Counter + command-A receipts over baselines and mutants.
set -u
S=/fast/scratch/hyaku/kaidoku-r45/R45W2Rollback
export TMPDIR="$S" HYAKU_SCRATCH="$S/counterscratch"
mkdir -p "$S/receipts" "$S/counterscratch"
C="$S/clone"; cd "$C" || exit 9
[ "$(git rev-parse --show-toplevel)" = "$C" ] || { echo REFUSING; exit 9; }
FREEZE=f762b7273e3f6ca3c710bb37d5de92a4a4417aec
LAND=e715263cb51b713c342ab992d527fe9d61d6f8ff
A1=1f4b27f82353d6544dc0c8048b3cfdadd8525d12
TIP=0ee50aaff516571aa607769bbbdf19a3db90dfa5
mapfile -t M <"$S/mutants.txt"
M1=${M[0]}; M2=${M[1]}; M3=${M[2]}

receipt() {
  local name=$1; shift
  local out="$S/receipts/$name.out" err="$S/receipts/$name.err"
  local utc; utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  "$@" >"$out" 2>"$err"; local rc=$?
  printf 'name=%s\nutc=%s\ncmd=' "$name" "$utc" >"$S/receipts/$name.receipt"
  printf '%q ' "$@" >>"$S/receipts/$name.receipt"
  printf '\nexit=%s\nstdout_sha256=%s\nstderr_sha256=%s\nstdout_bytes=%s\n' \
    "$rc" "$(sha256sum "$out" | cut -d' ' -f1)" "$(sha256sum "$err" | cut -d' ' -f1)" \
    "$(wc -c <"$out")" >>"$S/receipts/$name.receipt"
  echo "[$name] exit=$rc"
}

for pair in "land:$LAND" "a1:$A1" "tip:$TIP" "m1:$M1" "m2:$M2" "m3:$M3"; do
  tag=${pair%%:*}; rev=${pair#*:}
  receipt "cmdA-$tag" python3 -B "$S/measure.py" "$rev"
  receipt "c1-$tag" python3 -I -B tools/round-45/c1-counter.py --root "$C" --freeze "$FREEZE" --rev "$rev" --json-out "$S/receipts/c1-$tag.json"
  receipt "c2-$tag" python3 -I -B tools/round-45/c2-counter.py --root "$C" --freeze "$FREEZE" --rev "$rev" --json-out "$S/receipts/c2-$tag.json"
done
