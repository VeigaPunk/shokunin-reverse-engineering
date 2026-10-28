#!/usr/bin/env bash
set -u
SEAT=R44Watchdog; OUT=out
rec() { local id="$1"; shift; local f="$OUT/$id.stdout.txt" e="$OUT/$id.stderr.txt" t0 t1 rc sha wall bytes
  t0=$(date +%s.%N); "$@" >"$f" 2>"$e"; rc=$?; t1=$(date +%s.%N)
  wall=$(awk -v a="$t0" -v b="$t1" 'BEGIN{printf "%.3f", b-a}')
  sha=$(sha256sum "$f"|cut -d' ' -f1); bytes=$(stat -c%s "$f")
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$SEAT" "$id" "$rc" "$sha" "$wall" "$bytes" "$*" >> receipts.tsv
  echo "[$id] rc=$rc wall=${wall}s sha256=$sha bytes=$bytes"; return 0; }
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
rec W26-claims-HEAD-target   bash -c "git -C $LANE show HEAD:plans/round-44-claims.md | grep -nE 'carriers_matched|six carriers|These four'"
rec W27-claims-diff-stat     git -C "$LANE" diff --stat -- plans/round-44-claims.md
rec W28-claims-diff-brief    git -C "$LANE" diff -U0 -- plans/round-44-claims.md
rec W29-claims-HEAD-sha      bash -c "git -C $LANE show HEAD:plans/round-44-claims.md | sha256sum"
rec W30-carriers-diff        git -C "$LANE" diff --stat -- tools/round-44/carriers.json
rec W31-dirty-tracked-list   bash -c "git -C $LANE status --porcelain=v1 | grep -v '^??'"
rec W32-unblob-sasquatch-id  bash -c 'sasquatch -version | head -1'
rec W33-revenger-extractline bash -c "grep -nE 'no-extract|-s ,|skip-extraction|extraction_reports|empty' $LANE/.ufo/waves/round-44/w1/R44C1Revenger.md | head -12"
