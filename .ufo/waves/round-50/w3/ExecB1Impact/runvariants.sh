#!/usr/bin/env bash
# ExecB1Impact: run the frozen C2 counter against each fixture clone; write receipts.
# Usage: runvariants.sh <SCRATCH> <variant-name>
set -u
S="$1"; name="$2"
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
export TMPDIR="$S"
clone="$S/$name"
rev=$(git -C "$clone" rev-parse HEAD)
mkdir -p "$S/receipts"
extra=""
[ "${name}" = "v6-outside-beforecorr" ] && extra="--battery"
out="$S/receipts/$name.json"
start=$(date -u +%Y-%m-%dT%H:%M:%SZ)
( cd "$clone" && python3 -I -B tools/round-50/c2-record.py --root "$clone" --rev "$rev" \
    --freeze "$rev" $extra --work "$S/w-$name" --json-out "$out" ) >"$S/receipts/$name.out" 2>"$S/receipts/$name.err"
ec=$?
end=$(date -u +%Y-%m-%dT%H:%M:%SZ)
printf '%s\n' \
  "name=$name" "rev=$rev" \
  "cmd=( cd $clone && python3 -I -B tools/round-50/c2-record.py --root $clone --rev $rev --freeze $rev $extra --work $S/w-$name --json-out $out )" \
  "exit=$ec" "utc_start=$start" "utc_end=$end" \
  "stdout_sha256=$(sha256sum "$S/receipts/$name.out" | cut -d' ' -f1)" \
  "json_sha256=$(sha256sum "$out" 2>/dev/null | cut -d' ' -f1)" \
  "stderr_sha256=$(sha256sum "$S/receipts/$name.err" | cut -d' ' -f1)" \
  "stderr_bytes=$(wc -c < "$S/receipts/$name.err")" > "$S/receipts/$name.txt"
echo "done $name exit=$ec"
