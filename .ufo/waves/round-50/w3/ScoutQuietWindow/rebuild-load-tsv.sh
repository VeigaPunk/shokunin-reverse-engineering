#!/bin/bash
# Rebuild load-samples.tsv for seat ScoutQuietWindow (round-50 w3).
#
# sample.sh wrote the original TSV with unbraced positional refs ($14..$17).
# bash expands $14 as "${1}4" (positional params >=10 require braces), so the
# original cpu columns are garbage ("394,395,396,397" = "$1"+"4/5/6/7").
# The load columns (from /proc/loadavg) and the timestamps were correct.
# vmstat-raw.txt holds every full `vmstat 5 5` output; this script re-derives
# the cpu columns from the LAST numeric line of each sample's capture.
# vmstat here emits 18 columns (us sy id wa st gu at the end):
#   1=r 2=b ... 13=us 14=sy 15=id 16=wa.
set -euo pipefail
SEAT=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-50/w3/ScoutQuietWindow
awk '
  FNR==NR {
    if ($0 ~ /^utc/) next
    n++; ts[n]=$1; load[n]=$2 SUBSEP $3 SUBSEP $4 SUBSEP $5 SUBSEP $6
    next
  }
  /^# / { next }
  /^== sample / { idx++; next }
  NF>=17 { last[idx]=$0; next }
  END {
    printf "utc\tload1\tload5\tload15\tr\tb\tus\tsy\tid\twa\n"
    for (i=1;i<=n;i++) {
      split(load[i], L, SUBSEP)
      delete F; m=split(last[i], F, " +")
      if (m < 16) { printf "ERR sample %s: only %d fields\n", ts[i], m > "/dev/stderr"; exit 2 }
      printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", ts[i], L[1],L[2],L[3],L[4],L[5], F[13],F[14],F[15],F[16]
    }
  }
' "$SEAT/load-samples.tsv" "$SEAT/vmstat-raw.txt" > "$SEAT/load-samples.tsv.new"
mv "$SEAT/load-samples.tsv.new" "$SEAT/load-samples.tsv"
sha256sum "$SEAT/load-samples.tsv"
cat "$SEAT/load-samples.tsv"
