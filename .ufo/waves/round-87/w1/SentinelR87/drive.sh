#!/usr/bin/env bash
# SentinelR87 driver: run the repair on every crafted input with a timeout and /usr/bin/time -v.
set -u
S=/fast/scratch/hyaku/kaidoku-r87/SentinelR87
T=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-87/upx-magic-repair.py
TO=${TO:-300}
cd "$S"
export TMPDIR="$S/tmp"; mkdir -p "$TMPDIR" "$S/out"
printf '%-28s %5s %9s %10s %s\n' input rc wall_s maxrss_kb msg
for f in "$@"; do
  b=$(basename "$f")
  timeout -s KILL "$TO" /usr/bin/time -v -o "$S/out/$b.time" \
    env -i PATH=/usr/bin LANG=C HOME="$S/home" TMPDIR="$TMPDIR" \
    python3 -I -B "$T" --in "$f" --out "$S/out/$b.out" >"$S/out/$b.stdout" 2>"$S/out/$b.stderr"
  rc=$?
  wall=$(awk -F': ' '/Elapsed \(wall/{print $2}' "$S/out/$b.time" 2>/dev/null)
  rss=$(awk -F': ' '/Maximum resident/{print $2}' "$S/out/$b.time" 2>/dev/null)
  msg=$(cat "$S/out/$b.stdout" "$S/out/$b.stderr" | grep -v '^Command' | tail -n1 | cut -c1-90)
  printf '%-28s %5s %9s %10s %s\n' "$b" "$rc" "${wall:-KILLED}" "${rss:--}" "$msg"
done
