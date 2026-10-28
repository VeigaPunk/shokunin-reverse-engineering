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
rec W40-tools44-HEAD-now   git -C "$L" ls-tree -r --name-only HEAD -- tools/round-44/
rec W41-untracked-count    bash -c "git -C $L status --porcelain=v1 -uall | grep -c '^??'"
rec W42-dirty-total        bash -c "git -C $L status --porcelain=v1 -uall | wc -l"
rec W43-head-now           bash -c "git -C $L rev-parse HEAD; git -C $L rev-list --count origin/main..HEAD"
rec W44-partial-marker     bash -c "git -C $L status --porcelain=v1 -- .ufo/waves/round-44/w1.ready.partial .ufo/waves/round-44/w1.ready .ufo/waves/round-44/w1.ready.dispatched"
rec W45-unblob-sha-vs-head bash -c "cd $L && sha256sum unblob.log | cut -d' ' -f1; git cat-file -p HEAD:unblob.log | sha256sum | cut -d' ' -f1"
rec W46-jj-disclosure      bash -c "cat $L/.jj/repo/store/git_target 2>/dev/null; ls -la $L/.jj/working_copy/info 2>/dev/null | head -3"
