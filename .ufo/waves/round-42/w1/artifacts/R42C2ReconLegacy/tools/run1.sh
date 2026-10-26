#!/usr/bin/env bash
# Run REA extract-firmware over the unblob v1-v3 fixtures, two depths each.
set -uo pipefail
S=/fast/scratch/hyaku/kaidoku-r42/R42C2ReconLegacy
cd "$S" || exit 1
export TMPDIR="$S"
REA=npx
PIN=rea-agents@6.5.0
UNB=$HOME/.local/bin/unblob

run() { # name input depth extra_env
  local name=$1 input=$2 depth=$3
  local w="$S/runs/$name"
  mkdir -p "$w"
  ( cd "$w" || exit 1
    set -a; local args=()
    if [ "$depth" = "1" ]; then args=(--max-depth 1); fi
    REA_UNBLOB_COMMAND=$UNB timeout 600 "$REA" -y "$PIN" extract-firmware --format json --full-output "${args[@]}" "$input" "$w/out" \
      > "$w/envelope.json" 2> "$w/rea.err"
    echo "$name rc=$?" > "$w/rc.txt"
  )
}

export -f run
export S REA PIN UNB

jobs=()
add() { jobs+=("$1|$2|$3"); }

for fam in squashfs_v1 squashfs_v2 squashfs_v2_nonstandard squashfs_v3 squashfs_v3_ddwrt squashfs_v3_broadcom squashfs_v3_nonstandard squashfs_v3_adaptive; do
  for f in "$S/fx/$fam"/*.bin; do
    b=$(basename "$f" .bin)
    for d in default 1; do
      add "${fam}_${b}_d${d}" "$f" "$d"
    done
  done
done

printf '%s\n' "${jobs[@]}" | xargs -P 4 -I{} bash -c 'IFS="|" read -r n i d <<< "{}"; run "$n" "$i" "$d"'
echo DONE
