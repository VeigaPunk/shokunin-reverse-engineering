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
rec W83-offbranch-gate bash -c "echo 'ls-remote:'; git -C $L ls-remote origin refs/heads/main; echo 'HEAD:'; git -C $L rev-parse HEAD; echo 'ahead-of-origin:'; git -C $L rev-list --count origin/main..HEAD"
rec W84-jj-bookmark-main bash -c "jj -R $L log -r main --no-graph -T 'commit_id ++ \"\\n\"' | tail -1"
rec W85-rea-absence bash -c "find $L/corpus/evidence/round-44/c1 -type f | wc -l; find /fast/scratch/hyaku/kaidoku-r44 -path '*clone*' -prune -o -name 'run.json' -newermt '2026-10-28 00:00' -print | head -3"
rec W86-l1-citation bash -c "sed -n '22,26p' $L/plans/round-44-claims.md"
rec W87-sasquatch-identity bash -c "command -v sasquatch; sasquatch -version | head -1; command -v unsquashfs; /usr/bin/unsquashfs -version | head -1"
