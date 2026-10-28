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
rec W65-l1-dir-listing bash -c "ls -la $L/.ufo/waves/round-44/l1/; find $L/.ufo/waves/round-44/l1 -type f | wc -l"
rec W66-claims-v21-probe-cite bash -c "grep -nE 'measured probe' $L/plans/round-44-claims.md; grep -nE 'REA extracts|rea-agents' $L/plans/round-44-claims.md | head -5"
rec W67-revenger-report-sha bash -c "sha256sum $L/.ufo/waves/round-44/w1/R44C1Revenger.md; grep -nE 'report sha256|unblob -s' $L/.ufo/waves/round-44/w1/R44C1Revenger.md | head -4"
rec W68-seat-coverage bash -c "python3 - <<'PY'
import json,os,glob
L='$L'
spec=[it['name'] for it in json.load(open(L+'/.ufo/waves/round-44/w1-spec.json'))['items']]
w1=L+'/.ufo/waves/round-44/w1'
have={os.path.basename(p)[:-3] for p in glob.glob(w1+'/*.md')}
print('seats',len(spec),'md',len([s for s in spec if s in have]))
print('missing',sorted(s for s in spec if s not in have))
PY"
