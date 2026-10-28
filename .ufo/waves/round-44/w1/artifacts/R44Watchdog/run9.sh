#!/usr/bin/env bash
set -u
SEAT=R44Watchdog; OUT=out
rec() { local id="$1"; shift; local f="$OUT/$id.stdout.txt" e="$OUT/$id.stderr.txt" t0 t1 rc sha wall bytes
  t0=$(date +%s.%N); "$@" >"$f" 2>"$e"; rc=$?; t1=$(date +%s.%N)
  wall=$(awk -v a="$t0" -v b="$t1" 'BEGIN{printf "%.3f", b-a}')
  sha=$(sha256sum "$f"|cut -d' ' -f1); bytes=$(stat -c%s "$f")
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$SEAT" "$id" "$rc" "$sha" "$wall" "$bytes" "$*" >> receipts.tsv
  echo "[$id] rc=$rc wall=${wall}s sha256=$sha bytes=$bytes"; return 0; }
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin; WL=/home/vgpnk/Projects/shokunin/.ufo/watchdog.log
rec W57-snapshot2 bash -c "date -Is; git -C $L rev-parse HEAD; git -C $L rev-list --count origin/main..HEAD; git -C $L status --porcelain=v1 -uall | wc -l; git -C $L status --porcelain=v1 -uall | grep -c '^??'"
rec W58-watchdog-r44-again grep -nE "(launch|complete|lane-dead-no-report) kaidoku round=44" "$WL"
rec W59-jj-log-now bash -c "jj -R $L log --no-graph -r 'all()' --limit 4 2>/dev/null | cut -c1-110"
