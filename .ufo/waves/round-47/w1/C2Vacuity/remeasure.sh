#!/bin/bash
# Re-measure every attack card against the counter bytes now in the lane worktree.
S=/fast/scratch/hyaku/kaidoku-r47/C2Vacuity
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
OUT=$L/.ufo/waves/round-47/w1/C2Vacuity
F=$S/fix
export TMPDIR="$S" HYAKU_SCRATCH="$S"
mkdir -p "$S"
git clone -q --shared "$L" "$F" || exit 1
[ "$(git -C "$F" rev-parse --show-toplevel)" = "$F" ] || { echo TOPLEVEL-MISMATCH; exit 1; }
git -C "$F" config user.email r47@c2vacuity.local
git -C "$F" config user.name "c2 vacuity"
# the non-ancestor measurement point the rev-exemption cards cite
git -C "$F" checkout -q --detach 13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5
git -C "$F" commit -q --allow-empty -m "side measurement point (empty)"
SIDE=$(git -C "$F" rev-parse HEAD); SIDE8=${SIDE:0:8}
cd "$L" || exit 1
BLOB=$(git hash-object tools/round-47/record.py)
SUM=$(sha256sum tools/round-47/record.py | cut -d' ' -f1)
: > "$OUT/exits.txt"
echo "# $(date -u +%FT%TZ) record.py git-blob=$BLOB sha256=$SUM lane-HEAD=$(git -C "$L" rev-parse HEAD)" >> "$OUT/exits.txt"
for card in "$OUT"/cards/*.md; do
  A=$(basename "$card" .md)
  git -C "$F" checkout -q --detach 13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5
  sed "s/SIDESHA/$SIDE8/g" "$card" > "$F/SCORECARD.md"
  git -C "$F" add SCORECARD.md && git -C "$F" commit -q -m "attack $A"
  REV=$(git -C "$F" rev-parse HEAD)
  J="$F/r47-$A.json"
  python3 -I -B tools/round-47/record.py --root "$F" --rev "$REV" --json-out "$J" > "$OUT/attack-$A.stdout.json" 2>"$S/$A.err"
  code=$?
  cp "$J" "$OUT/attack-$A.json"
  met=$(python3 -c "import json;print(json.load(open('$J')).get('met_target'))")
  fail=$(python3 -c "import json;d=json.load(open('$J'));print('; '.join(d.get('failing') or [d.get('reason','')]))")
  printf '%-34s exit=%s met=%s failing=%s rev=%s\n' "$A" "$code" "$met" "$fail" "$REV" >> "$OUT/exits.txt"
  echo "$A exit=$code met=$met $fail"
done
# mutation demo against the same bytes
mkdir -p "$S/mut/tools/round-47" "$S/mut/tools/round-46"
cp tools/round-47/record.py "$S/mut/tools/round-47/record.orig.py"
cp tools/round-46/gate.py "$S/mut/tools/round-46/"
sed 's/^EXEMPT_MAX = 3$/EXEMPT_MAX = 99/' tools/round-47/record.py > "$S/mut/tools/round-47/record.weak.py"
git -C "$F" checkout -q --detach 13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5
sed "s/SIDESHA/$SIDE8/g" "$OUT/cards/A11-exempt-cap.md" > "$F/SCORECARD.md"
git -C "$F" add SCORECARD.md && git -C "$F" commit -q -m "cap demo"
REV=$(git -C "$F" rev-parse HEAD)
for tag in orig weak; do
  J="$F/r47-mut-$tag.json"
  python3 -I -B "$S/mut/tools/round-47/record.$tag.py" --root "$F" --rev "$REV" --json-out "$J" > "$OUT/attack-mut-$tag.stdout.txt" 2>&1
  code=$?
  cp "$J" "$OUT/attack-mut-$tag.json"
  echo "mut-$tag exit=$code met=$(python3 -c "import json;print(json.load(open('$J')).get('met_target'))")"
done
cp "$S/mut/tools/round-47/record.orig.py" "$OUT/record.orig.py"
cp "$S/mut/tools/round-47/record.weak.py" "$OUT/record.weak.py"
echo "SIDE=$SIDE (not an ancestor of any measured rev; empty commit on the base)" >> "$OUT/exits.txt"
echo "MUTREV=$REV" >> "$OUT/exits.txt"
