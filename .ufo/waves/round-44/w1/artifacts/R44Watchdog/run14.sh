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
rec W72-final-state bash -c "date -Is; git -C $L rev-parse HEAD; git -C $L symbolic-ref -q HEAD || echo DETACHED; git -C $L rev-list --count origin/main..HEAD; git -C $L status --porcelain=v1 -uall | wc -l; git -C $L status --porcelain=v1 -uall | grep -c '^??'"
rec W73-final-wd bash -c "grep -cE 'kaidoku round=44' $WL; grep -nE '(complete|lane-dead-no-report) kaidoku round=44' $WL || true"
rec W74-l1-now bash -c "find $L/.ufo/waves/round-44/l1 -type f | sort; echo '---'; find $L/.ufo/waves/round-44/l1 -type f -exec stat -c '%s %n' {} \\;"
rec W75-dirty-list-now bash -c "git -C $L status --porcelain=v1 | grep -v '^??'"
rec W76-dispatch-caprefusals bash -c "grep -cE 'spawn-cap .*kaidoku-shokunin/.ufo/waves/round-44/w1.ready' /home/vgpnk/Projects/shokunin/.ufo/state/inline-dispatcher.log"
