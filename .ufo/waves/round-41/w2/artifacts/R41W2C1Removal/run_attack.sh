#!/bin/bash
set -u
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
S=/fast/scratch/hyaku/kaidoku-r41/R41W2C1Removal
CAR=$1; ATT=$2
D=$(mktemp -d "$S/fx.XXXX")
git clone -q --shared "$L" "$D/lane" || { echo CLONEFAIL; exit 9; }
git -C "$D/lane" checkout -q e9a24d07256d1606f01aa4d2d65f74e649c5f3d4
TOP=$(git -C "$D/lane" rev-parse --show-toplevel)
if [ "$TOP" != "$D/lane" ]; then echo BADTOP "$TOP"; exit 9; fi
python3 "$S/mutate.py" "$D/lane" "$CAR" "$ATT" "$D/lane/corpus/evidence/round-41/c1/$CAR/after.json" || { echo MUTATEFAIL; exit 9; }
git -C "$D/lane" add corpus/evidence/round-41/c1/$CAR/after.json
git -C "$D/lane" -c user.name=fx -c user.email=fx@fx commit -q -m "fx $CAR $ATT" || { echo COMMITFAIL; exit 9; }
H=$(git -C "$D/lane" rev-parse HEAD)
cd "$S"
export TMPDIR="$S" HYAKU_SCRATCH=/fast/scratch/hyaku
python3 -I -B "$L/tools/round-41/c1-counter.py" --root "$D/lane" --rev "$H" --freeze d764389e9cbe61b9d1b07538ff3bff02d50bb34f --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --carrier-cache "$S/cache" --json-out "$S/out/${CAR}-${ATT}.json"
RC=$?
python3 - "$S/out/${CAR}-${ATT}.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
print('RESULT', d.get('revision','')[:8], 'matched', d.get('carriers_matched'), 'met_target', d.get('met_target'), 'exit_code', d.get('exit_code'))
for k,v in d.get('carriers',{}).items():
    print(' ', k, 'matched=',v.get('matched'), 'gaps_ok=',v.get('gaps_ok'), 'proj_ok=',v.get('projection_ok'), 'proj_diff=',v.get('projection_diff'), 'note=',str(v.get('gaps_note'))[:200])
PY
echo "MUTATION $CAR-$ATT steer=$RC"
