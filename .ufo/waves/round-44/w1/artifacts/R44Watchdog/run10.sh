#!/usr/bin/env bash
set -u
SEAT=R44Watchdog; OUT=out
rec() { local id="$1"; shift; local f="$OUT/$id.stdout.txt" e="$OUT/$id.stderr.txt" t0 t1 rc sha wall bytes
  t0=$(date +%s.%N); "$@" >"$f" 2>"$e"; rc=$?; t1=$(date +%s.%N)
  wall=$(awk -v a="$t0" -v b="$t1" 'BEGIN{printf "%.3f", b-a}')
  sha=$(sha256sum "$f"|cut -d' ' -f1); bytes=$(stat -c%s "$f")
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$SEAT" "$id" "$rc" "$sha" "$wall" "$bytes" "$*" >> receipts.tsv
  echo "[$id] rc=$rc wall=${wall}s sha256=$sha bytes=$bytes"; return 0; }
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
rec W60-claims-HEAD2 bash -c "git -C $L show HEAD:plans/round-44-claims.md | grep -nE 'carriers_matched ==|^# kaidoku'"
rec W61-tools44-HEAD2 git -C "$L" ls-tree -r --name-only HEAD -- tools/round-44/
rec W62-evidence-c1-now bash -c "find $L/corpus/evidence/round-44/c1 -type f | wc -l; ls -la $L/corpus/evidence/round-44/c1"
rec W63-seat-md-count bash -c "ls $L/.ufo/waves/round-44/w1/*.md | wc -l"
rec W64-unblob-log-provenance bash -c "git -C $L log --format='%h %cI %s' -- unblob.log | head -2"
