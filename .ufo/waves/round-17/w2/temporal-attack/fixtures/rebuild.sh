#!/bin/sh
# Rebuilds the /tmp fixture repo used in TemporalSweepAttack.md. Stdlib+git only.
set -eu
D=${1:-/tmp/tsw-attack-rebuilt}; rm -rf "$D"; mkdir -p "$D/lane"; cd "$D/lane"
git init -q; git config user.email a@b.c; git config user.name t
SRC=$(dirname "$0")
mkdir -p corpus/lessons corpus/knowledge .ufo/waves/round-16
for f in LOG.md corpus/lessons/round-16.md corpus/knowledge/note.md corpus/knowledge/newknowledge.md .ufo/waves/round-16/verification.json; do cp "$SRC/rev1/$f" "$f"; done
git add -A && git commit -qm rev1; R1=$(git rev-parse HEAD)
for f in LOG.md SCORECARD.md corpus/lessons/round-16.md corpus/lessons/round-17.md corpus/knowledge/note.md corpus/knowledge/newknowledge.md .ufo/waves/round-16/verification.json; do cp "$SRC/rev4/$f" "$f"; done
git add -A && git commit -qm rev4; R4=$(git rev-parse HEAD)
echo "R1=$R1 R4=$R4"
python3 -B -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/temporal-sweep.py --root "$D/lane" --rev "$R4" --sites-rev "$R1"
