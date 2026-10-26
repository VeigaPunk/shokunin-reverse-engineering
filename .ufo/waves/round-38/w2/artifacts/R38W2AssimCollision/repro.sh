#!/usr/bin/env bash
# Reproduces the round-38 wave-2 id-collision measurement. Read-only w.r.t. the lane.
set -eu
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
ST=/home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md
OUT=${1:?usage: repro.sh OUTDIR}
mkdir -p "$OUT"
P='^ {0,3}\|[[:space:]]*S[0-9]{3,}'
grep -oE "$P" "$ST" | grep -oE 'S[0-9]+' | sort > "$OUT/staged-ids.txt"
for rev in e059ca93 3b960fe5 0fc61133 HEAD; do
  git -C "$L" show "$rev:corpus/SOURCES.md" > "$OUT/reg-$rev.md"
  grep -oE "$P" "$OUT/reg-$rev.md" | grep -oE 'S[0-9]+' | sort > "$OUT/reg-ids-$rev.txt"
  comm -12 "$OUT/reg-ids-$rev.txt" "$OUT/staged-ids.txt" > "$OUT/collisions-$rev.txt"
  printf '%s rows=%s collisions=%s\n' "$rev" \
    "$(wc -l < "$OUT/reg-ids-$rev.txt")" "$(wc -l < "$OUT/collisions-$rev.txt")"
done
