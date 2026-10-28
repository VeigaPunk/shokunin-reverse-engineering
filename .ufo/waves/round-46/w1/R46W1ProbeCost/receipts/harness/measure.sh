#!/bin/bash
# $1=label $2=instrument  $3=freeze $4=rev
set -u
S=/fast/scratch/hyaku/kaidoku-r46/R46W1ProbeCost
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
label=$1; inst=$2; freeze=$3; rev=$4
W="$S/run-$label"; rm -rf -- "$W"; mkdir -p "$W/scratch"
export TMPDIR="$W/scratch" HYAKU_SCRATCH="$W/scratch"
( while :; do
    if [ -d "$W/scratch" ]; then
      b=$(du -sb -- "$W/scratch" 2>/dev/null | cut -f1)
      n=$(find "$W/scratch" -maxdepth 1 -mindepth 1 2>/dev/null | wc -l)
      f=$(find "$W/scratch" -type f 2>/dev/null | wc -l)
      echo "$(date +%s.%N) ${b:-0} $n $f" >> "$W/samples.txt"
    fi
    kill -0 $$ 2>/dev/null || break
    sleep 0.02
  done ) &
sampler=$!
cd "$W" || exit 9
/home/vgpnk/.local/bin/time -v python3 -I -B "$R/tools/round-46/$inst" --root "$R" \
  --freeze "$freeze" --rev "$rev" > "$W/stdout.json" 2> "$W/time.txt"
rc=$?
kill $sampler 2>/dev/null; wait $sampler 2>/dev/null
echo "rc=$rc" > "$W/rc.txt"
sha256sum "$W/stdout.json" | tee "$W/stdout.sha256"
echo "--- time.txt"; grep -E "Elapsed \(wall|Maximum resident|User time|System time|Exit status|Major .*page faults" "$W/time.txt"
echo "--- samples peak"; sort -k2 -n -r "$W/samples.txt" | head -3
echo "--- leftover scratch"; find "$W/scratch" -mindepth 1 | head -5; du -sb -- "$W/scratch" | cut -f1
echo "--- verdict"; python3 -c "import json;d=json.load(open('$W/stdout.json'));print({k:d.get(k) for k in ('counter','profile','spec','met_target','failing','reason','rows','block_present','marker_occurrences','rule_blocks','scope_size','unregistered','thin','absent_at_rev','frozen_path_changed')}); print('battery=',d.get('battery'))"
