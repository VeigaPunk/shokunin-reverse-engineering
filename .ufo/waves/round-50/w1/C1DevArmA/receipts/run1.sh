#!/usr/bin/env bash
# usage: run1.sh m tag [extra args...]
m=$1; tag=$2; shift 2
B=/fast/scratch/hyaku/kaidoku-r50/C1DevArmA
d=$B/run-$m-$tag; mkdir -p $d; cd $d
export TMPDIR=$d HYAKU_SCRATCH=/fast/scratch/hyaku REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob
s=$(date +%s%3N); st=$(date -u +%FT%TZ)
timeout 900 npx -y rea-agents@6.5.0 extract-firmware --format json --full-output --max-depth 1 "$@" $B/car-$m/filesystem.image $B/kaidoku-r50/ex-$m-$tag > envelope.json 2> rea.err
rc=$?; e=$(date +%s%3N)
echo "$rc" > rc; echo "$((e-s))" > ms; echo "$st" > start
