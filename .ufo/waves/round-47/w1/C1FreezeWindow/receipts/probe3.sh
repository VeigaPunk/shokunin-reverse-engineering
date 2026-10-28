#!/bin/sh
# C1FreezeWindow probe 3: same merge shape as probe 2, but the fixture carries a real
# `## Frozen paths (exact)` claims file so gate.freeze_state() can be run end to end on it.
set -u
S=/fast/scratch/hyaku/kaidoku-r47/C1FreezeWindow
export TMPDIR="$S" HYAKU_SCRATCH="$S"
cd "$S" || exit 9
D="$S/merge-fx3"
rm -rf "$D"
mkdir -p "$D" || exit 9
git -C "$D" init -q || exit 9
git -C "$D" config user.email fx@round47.local
git -C "$D" config user.name "round47 fixture"
TOP=$(git -C "$D" rev-parse --show-toplevel) || exit 9
if [ "$TOP" != "$D" ]; then echo "TOPLEVEL_MISMATCH got=$TOP want=$D"; exit 9; fi

MAIN=$(git -C "$D" symbolic-ref --short HEAD)
mkdir -p "$D/tools/round-47" "$D/plans"
printf 'V1\n' > "$D/tools/round-47/frozen.txt"
cat > "$D/plans/round-47-claims.md" <<'EOF'
# fixture claims

## Frozen paths (exact)

- `tools/round-47/`
- `plans/round-47-claims.md`
EOF
printf 'graded\n' > "$D/SKILL.md"
git -C "$D" add -A && git -C "$D" commit -q -m c1

git -C "$D" checkout -q -b side
printf 'SIDE\n' > "$D/tools/round-47/frozen.txt"
git -C "$D" commit -q -am s1
printf 'side marker\n' > "$D/side.txt"
git -C "$D" add -A && git -C "$D" commit -q -m s2
B=$(git -C "$D" rev-parse HEAD)

git -C "$D" checkout -q "$MAIN"
printf 'OTHER\n' > "$D/other.txt"
git -C "$D" add -A && git -C "$D" commit -q -m m2
P2=$(git -C "$D" rev-parse HEAD)

git -C "$D" checkout -q side
git -C "$D" merge -q --no-ff --no-commit "$P2" >/dev/null 2>&1
git -C "$D" checkout HEAD -- tools/round-47/frozen.txt
git -C "$D" add -A
git -C "$D" commit -q -m "merge main into side, frozen path resolved to side bytes"
M=$(git -C "$D" rev-parse HEAD)

echo "FX3=$D"; echo "BASE=$B"; echo "TIP=$M"
echo "$D" > "$S/fx3-dir.txt"; echo "$B" > "$S/fx3-base.txt"; echo "$M" > "$S/fx3-tip.txt"
echo "toplevel=$(git -C "$D" rev-parse --show-toplevel)"
echo "status=$(git -C "$D" status --porcelain | wc -l) dirty entries"
echo "UTC=$(date -u +%FT%TZ)"
