#!/bin/bash
# ScoutQuietWindow load sampler: 5 samples ~2 min apart; each sample =
# UTC timestamp, load1/5/15, and the final vmstat 5 5 line's cpu columns.
set -u
SEAT=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-50/w3/ScoutQuietWindow
SCR=/fast/scratch/hyaku/kaidoku-r50/w3-ScoutQuietWindow
OUT="$SEAT/load-samples.tsv"
RAW="$SEAT/vmstat-raw.txt"
printf 'utc\tload1\tload5\tload15\tr\tb\tus\tsy\tid\twa\n' > "$OUT"
printf '# vmstat raw capture, ScoutQuietWindow, started %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$RAW"
for i in 1 2 3 4 5; do
  ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  read -r l1 l5 l15 _rest < /proc/loadavg
  v=$(LC_ALL=C vmstat 5 5)
  printf '== sample %s %s ==\n%s\n' "$i" "$ts" "$v" >> "$RAW"
  last=$(printf '%s\n' "$v" | tail -n 1)
  set -- $last
  r=$1; b=$2; us=$14; sy=$15; id=$16; wa=$17
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$ts" "$l1" "$l5" "$l15" "$r" "$b" "$us" "$sy" "$id" "$wa" >> "$OUT"
  [ "$i" -lt 5 ] && sleep 100
done
printf '# sampler done %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$RAW"
touch "$SCR/sampler.done"
