#!/bin/sh
# C1FreezeWindow probe 2: two-parent merge where only the merge-vs-second-parent diff
# names a frozen path (no plain commit in the window touched it). This is the fixture
# where `-m --diff-merges=first-parent` and `--diff-merges=first-parent -m` differ in the
# SET of paths, not merely in output multiplicity, and where the reversed order turns a
# net-identical path into gate.py's `restored` violation.
set -u
S=/fast/scratch/hyaku/kaidoku-r47/C1FreezeWindow
export TMPDIR="$S" HYAKU_SCRATCH="$S"
cd "$S" || exit 9
D="$S/merge-fx2"
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
printf 'claims\n' > "$D/plans/round-47-claims.md"
git -C "$D" add -A && git -C "$D" commit -q -m c1
C1=$(git -C "$D" rev-parse HEAD)

git -C "$D" checkout -q -b side
printf 'SIDE\n' > "$D/tools/round-47/frozen.txt"
git -C "$D" commit -q -am s1
printf 'side marker\n' > "$D/side.txt"
git -C "$D" add -A && git -C "$D" commit -q -m s2
B=$(git -C "$D" rev-parse HEAD)          # window BASE = side tip

git -C "$D" checkout -q "$MAIN"
printf 'OTHER\n' > "$D/other.txt"
git -C "$D" add -A && git -C "$D" commit -q -m m2
P2=$(git -C "$D" rev-parse HEAD)         # second parent: frozen.txt = V1

git -C "$D" checkout -q side
git -C "$D" merge -q --no-ff --no-commit "$P2" >/dev/null 2>&1
git -C "$D" checkout HEAD -- tools/round-47/frozen.txt   # resolve to side's SIDE bytes
git -C "$D" add -A
git -C "$D" commit -q -m "merge main into side, frozen path resolved to side bytes"
M=$(git -C "$D" rev-parse HEAD)

echo "BASE=$B"; echo "P1=$B"; echo "P2=$P2"; echo "TIP=$M"
echo "parents=$(git -C "$D" rev-list --parents -n1 "$M")"
echo "blob@BASE=$(git -C "$D" rev-parse "$B:tools/round-47/frozen.txt") blob@TIP=$(git -C "$D" rev-parse "$M:tools/round-47/frozen.txt") blob@P2=$(git -C "$D" rev-parse "$P2:tools/round-47/frozen.txt")"
echo "commits-in-window=$(git -C "$D" rev-list "$B..$M" | tr '\n' ' ')"
echo "net-diff-BASE..TIP -- tools/round-47 plans/round-47-claims.md:"
git -C "$D" diff --name-status "$B" "$M" -- tools/round-47 plans/round-47-claims.md
echo "plain-commit-touches-in-window:"
git -C "$D" log --name-status --format='%h' "$B..$M" -- tools/round-47 plans/round-47-claims.md | sed 's/^/  /'

P="tools/round-47 plans/round-47-claims.md"
run() {
  label=$1; shift
  out="$S/fx2-$label.out"
  git -C "$D" log "$@" "$B..$M" -- $P > "$out" 2>"$S/fx2-$label.err"
  rc=$?
  echo "== $label rc=$rc bytes=$(wc -c < "$out") sha256=$(sha256sum < "$out" | cut -d' ' -f1)"
  echo "   argv: git -C \$D log $* \$BASE..\$TIP -- $P"
  sed 's/^/   | /' "$out"
  [ -s "$S/fx2-$label.err" ] && sed 's/^/   ! /' "$S/fx2-$label.err"
  :
}
run frozen-order   --name-status --format= -m --diff-merges=first-parent
run reversed-order --name-status --format= --diff-merges=first-parent -m
run trailing-m     --name-status --format= -m --diff-merges=first-parent -m
run trailing-sep   --name-status --format= -m --diff-merges=first-parent --diff-merges=separate

echo "$B" > "$S/fx2-base.txt"; echo "$M" > "$S/fx2-tip.txt"
echo "UTC=$(date -u +%FT%TZ)"
