#!/bin/bash
S=/fast/scratch/hyaku/kaidoku-r50/C2CounterBuild; export TMPDIR=$S HYAKU_SCRATCH=/fast/scratch/hyaku
D=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-50/w1/C2CounterBuild
R=$D/receipts; mkdir -p $R; rm -f $R/*
cd $S && rm -rf green w && git clone -q --shared /home/vgpnk/Projects/shokunin/kaidoku-shokunin $S/green && [ "$(git -C $S/green rev-parse --show-toplevel)" = "$S/green" ] && python3 -B $D/make-green.py --clone $S/green > $R/fixture-commits.json
F=$(python3 -c "import json;print(json.load(open('$R/fixture-commits.json'))['freeze'])"); G=$(python3 -c "import json;print(json.load(open('$R/fixture-commits.json'))['green'])")
CNT=green/tools/round-50/c2-record.py
rec() { # name, then command...
  n=$1; shift
  t=$(date -u +%FT%TZ)
  "$@" > $R/$n.stdout 2> $R/$n.stderr; e=$?
  printf '%s\t%s\texit=%s\tsha256=%s\t%s\n' "$n" "$t" "$e" "$(sha256sum < $R/$n.stdout | cut -d' ' -f1)" "$*" >> $R/index.tsv
}
rec freeze-plain     python3 -I -B $CNT --root green --rev $F --freeze $F --work $S/w --json-out $R/freeze-plain.json
rec green-plain      python3 -I -B $CNT --root green --rev $G --freeze $F --work $S/w --json-out $R/green-plain.json
rec green-battery    python3 -I -B $CNT --root green --rev $G --freeze $F --work $S/w --battery --json-out $R/green-battery.json
rec selftest         python3 -I -B $CNT --selftest --root green --work $S/w --json-out $R/selftest.json
rec attacks          python3 -B $D/attacks.py green $G $S/w
rec r49-selftest     python3 -I -B green/tools/round-50/selftest-r49-c2.py --root $S/green --work $S/w --json-out $R/r49-selftest.json
rec bad-freeze       python3 -I -B $CNT --root green --rev $F --freeze $G --work $S/w
rec no-scratch       env -u TMPDIR python3 -I -B $CNT --root green --rev $G --freeze $F
sha256sum $D/tools/round-50/* $D/make-green.py $D/attacks.py > $R/SHA256SUMS-seat-files.txt
cat $R/index.tsv | cut -c1-220
