#!/usr/bin/env bash
# Build a throwaway repo exercising the preflight gate's arms. Never mutates the lane.
set -u
S=/fast/scratch/hyaku/kaidoku-r44/R44W2Preflight
D="$S/fixture"
rm -rf "$D"; mkdir -p "$D"
git -C "$D" init -q
git -C "$D" config user.name "r44w2preflight"
git -C "$D" config user.email "r44w2preflight@example.invalid"
git -C "$D" config commit.gpgsign false
top=$(git -C "$D" rev-parse --show-toplevel)
[ "$top" = "$D" ] || { echo "FATAL: fixture toplevel $top != $D"; exit 9; }

mkdir -p "$D/frozen/sub" "$D/live"
printf 'frozen-A\n' > "$D/frozen/a.txt"
printf 'frozen-B\n' > "$D/frozen/sub/b.txt"
printf 'live-1\n'  > "$D/live/x.txt"
git -C "$D" add -A
git -C "$D" commit -qm "F: freeze"
F=$(git -C "$D" rev-parse HEAD)
echo "F=$F"

# --- C5: modify then restore the frozen blob (walk must be red, blob backstop clean)
printf 'frozen-A-modified\n' > "$D/frozen/a.txt"
git -C "$D" commit -qam "C5mod: modify frozen a"
C5MOD=$(git -C "$D" rev-parse HEAD)
git -C "$D" checkout -q "$F" -- frozen/a.txt
git -C "$D" commit -qam "C5restore: restore frozen a"
C5RES=$(git -C "$D" rev-parse HEAD)
echo "C5MOD=$C5MOD"; echo "C5RES=$C5RES"

# --- add a NEW file under the frozen dir
printf 'new\n' > "$D/frozen/added.txt"
git -C "$D" add -A
git -C "$D" commit -qm "CADD: add frozen/added.txt"
CADD=$(git -C "$D" rev-parse HEAD)
echo "CADD=$CADD"

# --- restore by deleting the added file, so later cases start from a clean frozen dir
git -C "$D" rm -q frozen/added.txt
git -C "$D" commit -qm "CADDRM: remove frozen/added.txt"
CADDRM=$(git -C "$D" rev-parse HEAD)
echo "CADDRM=$CADDRM"

# --- C6a: side branch edits the frozen file, merge takes the side change (normal merge)
git -C "$D" checkout -q -b side1 "$CADDRM"
printf 'frozen-B-side1\n' > "$D/frozen/sub/b.txt"
git -C "$D" commit -qam "SIDE1: edit frozen sub/b"
SIDE1=$(git -C "$D" rev-parse HEAD)
git -C "$D" checkout -q master 2>/dev/null || git -C "$D" checkout -q main
printf 'live-2\n' > "$D/live/x.txt"
git -C "$D" commit -qam "MAIN1: edit live x"
MAIN1=$(git -C "$D" rev-parse HEAD)
git -C "$D" merge -q --no-ff side1 -m "M6a: merge side1 (frozen edit arrives via merge)"
M6A=$(git -C "$D" rev-parse HEAD)
echo "SIDE1=$SIDE1"; echo "MAIN1=$MAIN1"; echo "M6A=$M6A"

# --- C6b: true evil merge: frozen edit appears in NEITHER parent
git -C "$D" checkout -q -b side2 "$M6A"
printf 'live-3\n' > "$D/live/y.txt"
git -C "$D" add -A
git -C "$D" commit -qm "SIDE2: add live/y"
SIDE2=$(git -C "$D" rev-parse HEAD)
git -C "$D" checkout -q master 2>/dev/null || git -C "$D" checkout -q main
printf 'live-4\n' > "$D/live/x.txt"
git -C "$D" commit -qam "MAIN2: edit live x again"
MAIN2=$(git -C "$D" rev-parse HEAD)
git -C "$D" merge -q --no-ff --no-commit side2 || true
printf 'frozen-A-evil\n' > "$D/frozen/a.txt"   # content in neither parent
git -C "$D" add -A
git -C "$D" commit -qm "M6b: evil merge edits frozen/a"
M6B=$(git -C "$D" rev-parse HEAD)
echo "SIDE2=$SIDE2"; echo "MAIN2=$MAIN2"; echo "M6B=$M6B"

# --- C6c: merge-only edit where the file content equals the FIRST parent but differs
#          from the second parent (tests whether -m over-reports)
git -C "$D" checkout -q -b side3 "$M6B"
printf 'frozen-B-side3\n' > "$D/frozen/sub/b.txt"
git -C "$D" commit -qam "SIDE3: edit frozen sub/b"
SIDE3=$(git -C "$D" rev-parse HEAD)
git -C "$D" checkout -q master 2>/dev/null || git -C "$D" checkout -q main
git -C "$D" merge -q --no-ff -s ours side3 -m "M6c: -s ours merge drops side3 frozen edit"
M6C=$(git -C "$D" rev-parse HEAD)
echo "SIDE3=$SIDE3"; echo "M6C=$M6C"

echo "D=$D"
