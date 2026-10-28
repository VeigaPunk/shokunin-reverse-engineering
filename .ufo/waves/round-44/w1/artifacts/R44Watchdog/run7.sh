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
rec W50-reflog-dated   git -C "$L" reflog -8 --date=iso --format='%gd %gs | %cd'
rec W51-jj-oplog-list  bash -c "ls -la $L/.jj/repo/op_store 2>/dev/null | head -3; ls $L/.jj/repo/op_heads/heads 2>/dev/null | wc -l"
rec W52-tracked-deletions bash -c "git -C $L status --porcelain=v1 | grep -E '^ ?D'"
