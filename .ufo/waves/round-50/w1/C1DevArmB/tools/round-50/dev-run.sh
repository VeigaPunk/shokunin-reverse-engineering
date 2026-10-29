#!/usr/bin/env bash
# C1DevArmB dev-arm run: REA 6.5.0 extract-firmware as tools/round-41/c1-run.sh arm `after` (argv identical), LE carriers.
# usage: dev-run.sh CARRIER RUNDIR   (RUNDIR under /fast/scratch/hyaku/kaidoku-r50/)
set -uo pipefail
carrier=$1; run=$2
mkdir -p "$run/cwd"; export TMPDIR=$run/cwd
export REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob
argv=(npx -y rea-agents@6.5.0 extract-firmware --format json --full-output --max-depth 1 "$carrier" "$run/extract")
printf '%s\n' "${argv[@]}" > "$run/argv.txt"
start=$(date -u +%FT%TZ); s=$(date +%s%3N)
( cd "$run/cwd" && timeout 900 "${argv[@]}" ) > "$run/envelope.json" 2> "$run/rea.err"
rc=$?
e=$(date +%s%3N); end=$(date -u +%FT%TZ)
printf '{"exit":%s,"start_utc":"%s","end_utc":"%s","duration_ms":%s}\n' $rc $start $end $((e-s)) > "$run/run.json"
echo "$run rc=$rc dur_ms=$((e-s))"
