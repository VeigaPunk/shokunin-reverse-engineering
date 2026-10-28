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
rec W53-dispatch-idmap bash -c "python3 - <<'PY'
import json
d=json.load(open('$L/.ufo/waves/round-44/w1.ready.dispatched'))
m=json.loads(d[1])
suf=[(k,v) for k,v in m.items() if k!=v]
print('seats',len(m)); print('renamed',suf)
PY"
rec W54-untracked-inventory bash -c "git -C $L status --porcelain=v1 -uall | grep '^??' | sed 's/^?? //' | sort"
rec W55-v21-oracle-trees bash -c "find $L/corpus/evidence/round-44/oracle -path '*v2.1*' -name '*.txt' | sort"
rec W56-carriers-dirty-diff bash -c "git -C $L diff --stat -- tools/round-44/carriers.json; git -C $L diff -U0 -- tools/round-44/carriers.json | grep -E '^\\+' | head -20"
