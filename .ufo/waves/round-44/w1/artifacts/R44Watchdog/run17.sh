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
rec W88-inventory-total bash -c "date -Is; git -C $L status --porcelain=v1 -uall | wc -l; git -C $L status --porcelain=v1 -uall | grep -c '^??' || true; git -C $L status --porcelain=v1 | grep -vc '^??' || true"
rec W89-r44-line-total bash -c "grep -cE 'round=44' $WL; grep -E 'round=44' $WL | grep -oE '(launch|complete|lane-dead-no-report) [a-z0-9-]+ round=44' | awk '{print \$2}' | sort -u | tr '\\n' ' '"
rec W90-claims-rev-cite bash -c "git -C $L rev-parse HEAD; sha256sum $L/plans/round-44-claims.md; git -C $L show HEAD:plans/round-44-claims.md | sha256sum"
