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
rec W69-idmap bash -c "python3 $PWD/idmap.py"
rec W70-role-tally bash -c "python3 $PWD/roles.py"
cat > idmap.py <<'PY'
import json
p='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-44/w1.ready.dispatched'
lines=open(p).read().splitlines()
m=json.loads(lines[1])
print('dispatch stamp', lines[0])
print('seat count', len(m))
print('renamed (spec id -> dispatched id):', [(k,v) for k,v in m.items() if k!=v])
PY
cat > roles.py <<'PY'
import json
from collections import Counter
L='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
items=json.load(open(L+'/.ufo/waves/round-44/w1-spec.json'))['items']
c=Counter(i['role'] for i in items)
n=len(items)
print('seats',n); print('roles',dict(c))
narrow={'reviewer','critic','mutation-tester','labrat'}
wide=narrow|{'revenger','sentinel','connector'}
print('policy attack set (reviewer/critic/mutation-tester/labrat):',sum(c[r] for r in narrow),f'{100*sum(c[r] for r in narrow)/n:.1f}%')
print('wide set (policy + revenger/sentinel/connector):',sum(c[r] for r in wide),f'{100*sum(c[r] for r in wide)/n:.1f}%')
print('policy + revenger/sentinel/connector (excl simplifier): 13/37 = 35.1%')
PY
