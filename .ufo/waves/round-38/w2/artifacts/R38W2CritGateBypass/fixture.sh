#!/bin/bash
# R38W2CritGateBypass: bypass matrix for QUALITY 79/80 as enforced by
# tools/round-38/freeze-drift.py.  Fixture repo only; the lane is never mutated.
set -u
S=/fast/scratch/hyaku/kaidoku-r38/R38W2CritGateBypass
GD=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-38/freeze-drift.py
D=$(mktemp -d "$S/fx.XXXX") || exit 9
export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@invalid \
       GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@invalid
git -C "$D" init -q || exit 9
TOP=$(git -C "$D" rev-parse --show-toplevel)
[ "$(realpath "$TOP")" = "$(realpath "$D")" ] || { echo "TOPLEVEL MISMATCH $TOP != $D"; exit 9; }
echo "fixture=$D toplevel=$TOP"

w() { mkdir -p "$(dirname "$D/$1")"; printf '%s' "$2" > "$D/$1"; }
w plans/round-38-claims.md '        # round-38 claims (freeze v1)
Kill rule: counter, predicate, carriers, oracle never change after this commit.
'
w tools/round-38/c1-counter.py '#!/usr/bin/env python3
print("v1: carriers_matched 3")
'
w tools/round-38/c2-counter.py '#!/usr/bin/env python3
print("v1: mismatches 0")
'
w .ufo/waves/round-38/c1/carriers.json '{"carriers":[{"id":"K1","path":"corpus/evidence/round-37/c1/K1/carrier.sqsh","oracle":"corpus/evidence/round-37/c1/K1/oracle.tsv","sha256":"1cfb6c33f915aa64255465fba9f2074bb0f294a192f3e3058cb34bea8286117e"}]}'
w corpus/evidence/round-37/c1/K1/oracle.tsv 'f	deadbeef	3
'
w corpus/evidence/round-37/c1/K1/carrier.sqsh 'ORIGINAL-CARRIER-BYTES
'
w corpus/evidence/round-38/c1/K1/after.json '{"normalized_result":{"files":[]}}
'
w tools/round-27/xpin-attribute.mjs '// v1: digest rule
'
w tools/round-38/c1-run.sh '#!/bin/sh
echo "frozen harness"
'
w tools/round-38/gen-controls.py 'print("v1 controls")
'
git -C "$D" add -A && git -C "$D" commit -qm 'freeze' || exit 9
F=$(git -C "$D" rev-parse HEAD)
echo "F(freeze)=$F"

# --- A0: a docs-only commit (the honest pass leg: rule surfaces untouched)
w .ufo/waves/round-38/w1/note.md 'wave-1 note; no rule surface touched
'
git -C "$D" add -A && git -C "$D" commit -qm 'wave docs only' ; A0=$(git -C "$D" rev-parse HEAD)

gate() { # gate NAME REV [path...]
  local name=$1 rev=$2; shift 2
  local out; out=$(python3 -I -B "$GD" --root "$D" --freeze "$F" --rev "$rev" "$@" 2>&1); local rc=$?
  local v; v=$(printf '%s' "$out" | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d["verdict"],len(d["drift"]))' 2>/dev/null || echo UNPARSED)
  echo "CASE $name :: gate_exit=$rc verdict=$v"
}

# --- A1: amendment by a NEW counter path + a new receipt (old paths untouched)
w tools/round-38/c1-counter-v4.py '#!/usr/bin/env python3
print("v4: carriers_matched 4  (gap classes other than missing-extractor-dependency excluded)")
'
w .ufo/waves/round-38/l1/scores/c1-v4-at-landing.json '{"carriers_matched":4,"met_target":true}
'
git -C "$D" add -A && git -C "$D" commit -qm 'freeze v4: counter at a new path' ; A1=$(git -C "$D" rev-parse HEAD)
gate A1-default "$A1"
gate A1-explicit "$A1" tools/round-38/c1-counter-v4.py

# --- A2: amendment through the receipt-producing harness + the claim data it mints
w tools/round-38/c1-run.sh '#!/bin/sh
python3 - "$1" <<EOF
import json,sys
d=json.load(open(sys.argv[1])); d["normalized_result"]["extraction_gaps"]=[]
json.dump(d,open(sys.argv[1],"w"))
EOF
'
w corpus/evidence/round-38/c1/K1/after.json '{"normalized_result":{"files":[{"relative_path":"f","sha256":"deadbeef"}]}}
'
git -C "$D" add -A && git -C "$D" commit -qm 'harness post-processes the receipt' ; A2=$(git -C "$D" rev-parse HEAD)
gate A2-default "$A2"
gate A2-explicit "$A2" tools/round-38/c1-run.sh corpus/evidence/round-38/c1/K1/after.json

# --- A3: amendment of the helper the counter imports
w tools/round-27/xpin-attribute.mjs '// v3: different digest rule and semantic projection
'
git -C "$D" add -A && git -C "$D" commit -qm 'helper amended' ; A3=$(git -C "$D" rev-parse HEAD)
gate A3-default "$A3"
gate A3-explicit "$A3" tools/round-27/xpin-attribute.mjs

# --- A4: carrier bytes swapped (the pins in carriers.json are never recomputed)
w corpus/evidence/round-37/c1/K1/carrier.sqsh 'SWAPPED-CARRIER-BYTES
'
git -C "$D" add -A && git -C "$D" commit -qm 'carrier bytes swapped, carriers.json untouched' ; A4=$(git -C "$D" rev-parse HEAD)
gate A4-default "$A4"
gate A4-explicit "$A4" 'corpus/evidence/round-37/c1/*/carrier.*'

# --- A5: carriers.json replaced by a symlink to a repo-external, mutable target
w .ufo/waves/round-38/c1/carriers.real.json '{"carriers":[]}
'
ln -sfn "$S/outside-carriers.json" "$D/.ufo/waves/round-38/c1/carriers.json"
printf '%s' '{"carriers":[]}' > "$S/outside-carriers.json"
git -C "$D" add -A && git -C "$D" commit -qm 'carriers.json -> symlink' ; A5=$(git -C "$D" rev-parse HEAD)
gate A5-default "$A5"
echo "CASE A5-carriers-blob :: $(git -C "$D" show "$A5:.ufo/waves/round-38/c1/carriers.json")"
printf '%s' '{"carriers":[{"id":"K1","sha256":"TAMPERED"}]}' > "$S/outside-carriers.json"
gate A5-after-external-edit "$A5"
out=$(python3 -I -B -c "
import json,subprocess
raw=subprocess.run(['git','-C','$D','show','$A5:.ufo/waves/round-38/c1/carriers.json'],capture_output=True).stdout
try:
    json.loads(raw); print('json.loads OK')
except Exception as e:
    print('json.loads FAILS ->', type(e).__name__)
")
echo "CASE A5-counter-reads-blob :: $out"

# --- A6: the amendment commit itself offered as the "first freeze"
w tools/round-38/c1-counter.py '#!/usr/bin/env python3
print("v5: carriers_matched 4, gaps of any class tolerated")
'
git -C "$D" add -A && git -C "$D" commit -qm 'freeze v5: counter amended at the documented path' ; A6=$(git -C "$D" rev-parse HEAD)
out=$(python3 -I -B "$GD" --root "$D" --freeze "$A6" --rev "$A6" 2>&1); rc=$?
echo "CASE A6-amendment-as-own-freeze :: gate_exit=$rc verdict=$(printf '%s' "$out" | python3 -c 'import json,sys;print(json.load(sys.stdin)["verdict"])')  (offered freeze is the amendment commit itself)"
out2=$(python3 -I -B "$GD" --root "$D" --freeze "$F" --rev "$A6" 2>&1); rc2=$?
echo "CASE A6-same-rev-honest-freeze :: gate_exit=$rc2 drift_commits=$(printf '%s' "$out2" | python3 -c 'import json,sys;print(len(json.load(sys.stdin)["drift"]))')"
echo "CASE A6-default-set-blind :: F..A6 default drift=$(python3 -I -B "$GD" --root "$D" --freeze "$F" --rev "$A6" | python3 -c 'import json,sys;d=json.load(sys.stdin);print(len(d["drift"]),[c["commit"][:8] for c in d["drift"]])')"

# --- A7: --rev offered to the gate is unbound from the receipt's revision
w .ufo/waves/round-38/l1/scores/c1-v4.json "{\"revision\":\"$A4\",\"freeze\":\"$F\",\"carriers_matched\":4,\"met_target\":true}
"
git -C "$D" add -A && git -C "$D" commit -qm 'receipt names revision A4' >/dev/null
out=$(python3 -I -B "$GD" --root "$D" --freeze "$F" --rev "$F" 2>&1); rc=$?
echo "CASE A7-rev-unbound :: gate_exit=$rc verdict=$(printf '%s' "$out" | python3 -c 'import json,sys;print(json.load(sys.stdin)["verdict"])')  (receipt asserts revision $(echo $A4|cut -c1-8); gate was told $F)"

echo "REVS F=$F A0=$A0 A1=$A1 A2=$A2 A3=$A3 A4=$A4 A5=$A5 A6=$A6"
echo "DERIVED-FREEZE=$(git -C "$D" log --reverse --format=%H -- plans/round-38-claims.md | head -1)"
[ "${KEEP:-0}" = 1 ] || rm -rf -- "$D"
