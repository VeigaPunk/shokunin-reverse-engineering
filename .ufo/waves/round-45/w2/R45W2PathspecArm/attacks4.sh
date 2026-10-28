#!/usr/bin/env bash
S=/fast/scratch/hyaku/kaidoku-r45/R45W2PathspecArm
export TMPDIR="$S"; PF="$S/preflight.py"; TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
D=$(mktemp -d -p "$S" repo.XXXXXX); git -C "$D" init -q; git -C "$D" config user.email a@b.c; git -C "$D" config user.name t
mkdir -p "$D/frozen/control-fixtures"
for i in 0 1 2 3 4 5 6 7; do printf '%s\n' "$i" > "$D/frozen/control-fixtures/c$i.json"; done
printf 'outside\n' > "$D/outside.txt"
git -C "$D" add -A; git -C "$D" commit -q -m freeze; F=$(git -C "$D" rev-parse HEAD)
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$(realpath "$D")" ] || echo TOPLEVEL_MISMATCH
for i in 0 1 2 3 4 5 6 7; do printf 'tampered\n' > "$D/frozen/control-fixtures/c$i.json"; done
run() { local n=$1 e=$2; shift 2; local o r; o=$(python3 -I -B "$PF" --root "$D" --freeze "$F" --rev "$F" "$@" 2>&1); r=$?
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$n" "$e" "$r" "$(printf '%s' "$o" | sha256sum | cut -d' ' -f1)" "$TS" "$o"; }
run X1-dirty-whole-tree 1 --check-dirty
run X2-dirty-frozen-pathspec 1 --check-dirty --pathspec frozen/
run X3-no-dirty-arm 0 --pathspec frozen/
