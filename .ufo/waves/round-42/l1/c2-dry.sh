#!/usr/bin/env bash
# QUALITY 84 pre-freeze dry run of the frozen C2 counter (L1 KaidokuR42).
set -euo pipefail
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
S=/fast/scratch/hyaku/kaidoku-r42/l1-dry/c2
rm -rf "$S"; mkdir -p "$S/tmp"; export TMPDIR="$S/tmp"
D="$S/lane"
git clone -q --shared "$LANE" "$D"
[[ $(git -C "$D" rev-parse --show-toplevel) == "$D" ]]
# copy the uncommitted freeze material
for p in SKILL.md plans/round-42-claims.md tools/round-42 corpus/evidence/round-42/c2 .ufo/waves/round-42/controls corpus/knowledge/2026-10-26-r42-sqfs-triage-v4.md; do
  [[ -e $LANE/$p ]] || continue
  mkdir -p "$D/$(dirname "$p")"; rm -rf "${D:?}/$p"; cp -a "$LANE/$p" "$D/$p"
done
git -C "$D" add -A
git -C "$D" -c user.name=fx -c user.email=fx@fx commit -q -m "fx freeze-like"
F=$(git -C "$D" rev-parse HEAD); echo "freeze-like $F"
cd "$S"
python3 -I -B "$D/tools/round-42/heldout-gen-v4.py" --seed "$F" --out "$D/corpus/evidence/round-42/c2/heldout" --run --scratch "$S/gen" > "$S/gen.log" 2>&1; echo "gen rc=$?"
git -C "$D" add -A
git -C "$D" -c user.name=fx -c user.email=fx@fx commit -q -m "fx held-out data"
R=$(git -C "$D" rev-parse HEAD); echo "data $R"
cd "$S"
set +e
python3 -I -B "$D/tools/round-42/c2-counter.py" --root "$D" --rev "$R" --freeze "$F" --json-out "$S/c2-dry.json" > "$S/counter.log" 2>&1
echo "counter rc=$?"
set -e
cp "$S/c2-dry.json" "$LANE/.ufo/waves/round-42/l1/dryrun-c2.json" 2>/dev/null || true
jq -c '{exit_code, matched, n, met_target, false_bindings: [.bindings|to_entries[]|select(.value==false)|.key]}' "$S/c2-dry.json"
