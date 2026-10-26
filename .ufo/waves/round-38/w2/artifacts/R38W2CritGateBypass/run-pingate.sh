#!/bin/bash
# Run the proposed pin-gate over the kept fixture from fixture.sh (KEEP=1).
set -u
S=/fast/scratch/hyaku/kaidoku-r38/R38W2CritGateBypass
PG=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-38/w2/artifacts/R38W2CritGateBypass/pin-gate.py
export TMPDIR="$S" HYAKU_SCRATCH=/fast/scratch/hyaku KEEP=1
out=$(bash "$S/fixture.sh" 2>&1)
printf '%s\n' "$out"
D=$(printf '%s\n' "$out" | sed -n 's/^fixture=\([^ ]*\) .*/\1/p')
eval "$(printf '%s\n' "$out" | grep '^REVS ' | cut -d' ' -f2-)"
echo "KEPT=$D"

mk() { python3 - "$@" <<'EOF'
import json,sys
out,rev,fz,tool=sys.argv[1:5]
json.dump({'revision':rev,'freeze':fz,'carriers_matched':4,'met_target':True,
           'argv':[tool,'--rev',rev]},open(out,'w'))
EOF
}
pg() { local name=$1; shift; local rc; local o; o=$(python3 -I -B "$PG" "$@" 2>&1); rc=$?
  printf 'PINGATE %-36s exit=%s %s\n' "$name" "$rc" "$(printf '%s' "$o" | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d["verdict"],[f["check"] for f in d["fails"]])' 2>/dev/null || echo UNPARSE)"; }

mk "$S/r-a0.json" "$A0" "$F" "$D/tools/round-38/c1-counter.py"
mk "$S/r-a1.json" "$A1" "$F" "$D/tools/round-38/c1-counter-v4.py"
mk "$S/r-a2.json" "$A2" "$F" "$D/tools/round-38/c1-counter.py"
mk "$S/r-a3.json" "$A3" "$F" "$D/tools/round-38/c1-counter.py"
mk "$S/r-a4.json" "$A4" "$F" "$D/tools/round-38/c1-counter.py"
mk "$S/r-a5.json" "$A5" "$F" "$D/tools/round-38/c1-counter.py"
mk "$S/r-a6.json" "$A6" "$F" "$D/tools/round-38/c1-counter.py"
mk "$S/r-stale.json" "$A4" "$F" "$D/tools/round-38/c1-counter.py"

pg "F..A0 docs-only (pass leg)"  --root "$D" --rev "$A0" --receipt "$S/r-a0.json"
pg "F..A1 new counter path"      --root "$D" --rev "$A1" --receipt "$S/r-a1.json"
pg "F..A2 harness+after receipt" --root "$D" --rev "$A2" --receipt "$S/r-a2.json"
pg "F..A3 xpin helper"           --root "$D" --rev "$A3" --receipt "$S/r-a3.json"
pg "F..A4 carrier bytes"         --root "$D" --rev "$A4" --receipt "$S/r-a4.json"
pg "F..A5 carriers.json symlink" --root "$D" --rev "$A5" --receipt "$S/r-a5.json"
pg "F..A6 counter amended"       --root "$D" --rev "$A6" --receipt "$S/r-a6.json"
pg "A6 offered as 1st freeze"    --root "$D" --rev "$A6" --freeze "$A6" --receipt "$S/r-a6.json"
pg "receipt rev != measured rev" --root "$D" --rev "$A0" --receipt "$S/r-stale.json"
rm -rf -- "$D"
