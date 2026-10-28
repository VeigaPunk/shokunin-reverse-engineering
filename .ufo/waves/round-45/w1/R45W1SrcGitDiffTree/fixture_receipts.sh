#!/bin/sh
# S141 semantic receipt: does the documented --name-status + -z framing hold?
set -u
S="$1"
export TMPDIR="$S"
R=$(mktemp -d -p "$S" receipt.XXXX) || exit 2
git -C "$R" init -q || exit 2
[ "$(git -C "$R" rev-parse --show-toplevel)" = "$R" ] || { echo "TOPLEVEL MISMATCH" >&2; exit 2; }
git -C "$R" config user.email r45@example.invalid
git -C "$R" config user.name r45
cd "$R" || exit 2
printf 'x\n' > 'é.txt'
printf 'y\n' > "$(printf 'tab\there.txt')"
printf 'a\nb\nc\nd\ne\nf\ng\nh\n' > old.txt
git -C "$R" add -A && git -C "$R" commit -qm one || exit 2
printf 'x2\n' > 'é.txt'
printf 'y2\n' > "$(printf 'tab\there.txt')"
git -C "$R" mv old.txt new.txt
git -C "$R" add -A && git -C "$R" commit -qm two || exit 2
C=$(git -C "$R" rev-parse HEAD)
echo "== fixture=$R commit=$C git=$(git --version) =="
echo "-- A: --name-status WITHOUT -z (quoted/munged?) --"
git -C "$R" diff-tree -r -M --name-status --no-commit-id "$C"
echo "-- B: --name-status WITH -z (od -c) --"
git -C "$R" diff-tree -r -M --name-status --no-commit-id -z "$C" | od -c
echo "-- C: NUL-field count in B for a 2-path rename record --"
git -C "$R" diff-tree -r -M --name-status --no-commit-id -z "$C" | tr -cd '\000' | wc -c
