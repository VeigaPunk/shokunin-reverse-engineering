#!/usr/bin/env bash
# usage: mkclone.sh <dest-dir-under-/fast/scratch/hyaku/kaidoku-r49/<seat>/>
# Builds a scratch clone of the lane at the round-49 base with the DRAFT tools/plan committed as
# a throwaway "dev freeze" (identity r49-dev, set in the clone only). Prints "DEV_FREEZE=<hash>".
set -euo pipefail
D=$1; L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin; BASE=e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9
case "$D" in /fast/scratch/hyaku/kaidoku-r49/*) ;; *) echo "dest must be under /fast/scratch/hyaku/kaidoku-r49/" >&2; exit 2;; esac
rm -rf "$D"; git clone -q --shared "$L" "$D"
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "toplevel mismatch" >&2; exit 2; }
git -C "$D" config user.name r49-dev; git -C "$D" config user.email r49@dev.invalid
git -C "$D" checkout -q --detach "$BASE"
mkdir -p "$D/tools/round-49" "$D/plans"
cp -r "$L"/.ufo/waves/round-49/draft/tools/round-49/. "$D/tools/round-49/"
cp "$L"/.ufo/waves/round-49/draft/plans/round-49-claims.md "$D/plans/"
rm -rf "$D/tools/round-49/__pycache__"
git -C "$D" add tools/round-49 plans/round-49-claims.md
git -C "$D" commit -q -m "dev freeze"
echo "DEV_FREEZE=$(git -C "$D" rev-parse HEAD)"
