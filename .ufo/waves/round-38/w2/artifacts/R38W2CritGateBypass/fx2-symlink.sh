#!/bin/bash
# fx2: the same rule surfaces reached through a SYMLINK committed in the freeze.
# Does freeze-drift.py (and the proposed pin-gate) see a rule change that is an
# edit to the link target rather than to the linked path?
set -u
S=/fast/scratch/hyaku/kaidoku-r38/R38W2CritGateBypass
GD=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-38/freeze-drift.py
PG=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-38/w2/artifacts/R38W2CritGateBypass/pin-gate.py
D=$(mktemp -d "$S/fx2.XXXX") || exit 9
export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@invalid \
       GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@invalid
git -C "$D" init -q || exit 9
TOP=$(git -C "$D" rev-parse --show-toplevel)
[ "$(realpath "$TOP")" = "$(realpath "$D")" ] || { echo "TOPLEVEL MISMATCH"; exit 9; }
w() { mkdir -p "$(dirname "$D/$1")"; printf '%s' "$2" > "$D/$1"; }
w plans/round-38-claims.md '# claims v1: four carriers, four oracles
'
w corpus/evidence/round-38/c1/carriers.real.json '{"carriers":[{"id":"K1"},{"id":"K2"},{"id":"K3"},{"id":"K4"}]}'
w corpus/evidence/round-37/c1/K1/oracle.real.tsv 'f	aaaa	3
'
ln -s ../../round-38/c1/carriers.real.json "$D/.ufo/waves/round-38/c1/carriers.json" 2>/dev/null || { mkdir -p "$D/.ufo/waves/round-38/c1"; ln -s ../../../corpus/evidence/round-38/c1/carriers.real.json "$D/.ufo/waves/round-38/c1/carriers.json"; }
mkdir -p "$D/corpus/evidence/round-37/c1/K1"
ln -sf ../../../round-38/c1/oracle.real.tsv "$D/corpus/evidence/round-37/c1/K1/oracle.tsv" 2>/dev/null
w corpus/evidence/round-37/c1/K1/oracle.real.tsv 'f	aaaa	3
'
w tools/round-38/c1-counter.py 'print("v1")
'
w tools/round-38/c2-counter.py 'print("v1")
'
git -C "$D" add -A && git -C "$D" commit -qm 'freeze with target-linked rule surfaces' || exit 9
F=$(git -C "$D" rev-parse HEAD)
echo "D=$D F=$F"
echo "CASE fx2-freeze-modes :: $(git -C "$D" ls-tree -r "$F" | awk '$1!="100644"{print $1,$4}' | tr '\n' ' ')"

# Amend ONLY the link targets: carriers 4 -> 1, oracle rows dropped.
w corpus/evidence/round-38/c1/carriers.real.json '{"carriers":[{"id":"K1"}]}'
w corpus/evidence/round-37/c1/K1/oracle.real.tsv 'f	bbbb	9
'
git -C "$D" add -A && git -C "$D" commit -qm 'rule weakened through the link target' ; A=$(git -C "$D" rev-parse HEAD)

out=$(python3 -I -B "$GD" --root "$D" --freeze "$F" --rev "$A" 2>&1); rc=$?
echo "CASE fx2-freeze-drift-default :: exit=$rc verdict=$(printf '%s' "$out" | python3 -c 'import json,sys;print(json.load(sys.stdin)["verdict"])')"
out=$(python3 -I -B "$GD" --root "$D" --freeze "$F" --rev "$A" '.ufo/waves/round-38/c1/carriers.json' ':(glob)corpus/evidence/round-37/c1/*/oracle.tsv' 2>&1); rc=$?
echo "CASE fx2-freeze-drift-explicit-paths :: exit=$rc verdict=$(printf '%s' "$out" | python3 -c 'import json,sys;print(json.load(sys.stdin)["verdict"])')"
echo "CASE fx2-diff-of-listed-paths :: $(git -C "$D" diff --name-only "$F" "$A" -- .ufo/waves/round-38/c1/carriers.json 'corpus/evidence/round-37/c1/K1/oracle.tsv' | tr '\n' ' ')(empty = identical)"
echo "CASE fx2-carriers-blob :: $(git -C "$D" show "$F:.ufo/waves/round-38/c1/carriers.json")"
echo "CASE fx2-carriers-json-loads :: $(python3 -I -B -c "
import json,subprocess
raw=subprocess.run(['git','-C','$D','show','$A:.ufo/waves/round-38/c1/carriers.json'],capture_output=True).stdout
try:
    json.loads(raw); print('parses as JSON (would be usable as a spec)')
except Exception as e:
    print('json.loads FAILS ->', type(e).__name__, '(counter exits 2: unevaluable)')
")"
co=$(cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && python3 -I -B tools/round-38/c1-counter.py --root "$D" --rev "$A" --freeze "$F" --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents 2>&1); crc=$?
echo "CASE fx2-real-counter :: exit=$crc last_stderr=$(printf '%s' "$co" | tail -1 | cut -c1-90)"
python3 - "$S/r-fx2.json" "$A" "$F" <<'EOF'
import json,sys
json.dump({'revision':sys.argv[2],'freeze':sys.argv[3],'argv':['tools/round-38/c1-counter.py']},open(sys.argv[1],'w'))
EOF
out=$(python3 -I -B "$PG" --root "$D" --rev "$A" --receipt "$S/r-fx2.json" 2>&1); rc=$?
echo "CASE fx2-pin-gate :: exit=$rc $(printf '%s' "$out" | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d["verdict"],[ (f["check"],f["detail"]) for f in d["fails"]])')"
rm -rf -- "$D"
