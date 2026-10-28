#!/usr/bin/env bash
set -u
SEAT=R44Watchdog; OUT=out
rec() { local id="$1"; shift; local f="$OUT/$id.stdout.txt" e="$OUT/$id.stderr.txt" t0 t1 rc sha wall bytes
  t0=$(date +%s.%N); "$@" >"$f" 2>"$e"; rc=$?; t1=$(date +%s.%N)
  wall=$(awk -v a="$t0" -v b="$t1" 'BEGIN{printf "%.3f", b-a}')
  sha=$(sha256sum "$f"|cut -d' ' -f1); bytes=$(stat -c%s "$f")
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$SEAT" "$id" "$rc" "$sha" "$wall" "$bytes" "$*" >> receipts.tsv
  echo "[$id] rc=$rc wall=${wall}s sha256=$sha bytes=$bytes"; return 0; }
P=/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Revenger
rec W34-scratch-log-census bash -c "for f in $P/ub-*/unblob.log; do printf '%s\t%s\t%s\t' \"\$(dirname \$f | xargs basename)\" \"\$(wc -l < \$f)\" \"\$(sha256sum \$f | cut -c1-16)\"; grep -oE 'Found valid chunk .*handler=[a-z0-9_]+' \$f | grep -oE 'handler=[a-z0-9_]+' | sort -u | tr '\n' ',' ; echo; done"
rec W35-no-extract-evidence  bash -c "grep -rc 'Running extract command' $P/ub-*/unblob.log | tr '\n' ' '"
rec W36-extract-dir-state    bash -c "for d in $P/ub-*/; do printf '%s %s\n' \"\$(basename \$d)\" \"\$(ls -A \$d/extract 2>/dev/null | wc -l)\"; done"
rec W37-revenger-method      bash -c "sed -n '125,145p' /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-44/w1/R44C1Revenger.md"
rec W38-w1-inventory         bash -c "cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-44/w1 && ls -1"
rec W39-report-dir-round44   bash -c "ls -la /home/vgpnk/Projects/shokunin/.ufo/reports/round-44/"
