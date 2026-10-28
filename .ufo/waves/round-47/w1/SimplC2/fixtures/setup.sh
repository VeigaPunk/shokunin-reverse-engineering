#!/bin/sh
# Rebuild the SimplC2 mutation variants from the lane's counter, then rerun the probes.
#
#   sh fixtures/setup.sh /home/vgpnk/Projects/shokunin/kaidoku-shokunin
#   python3 -I -B fixtures/harness.py
#   python3 -I -B fixtures/probe2.py
#
# Nothing here writes outside this directory. The lane tree is read-only input.
set -eu
LANE=${1:?usage: setup.sh <lane root>}
HERE=$(cd "$(dirname "$0")" && pwd)
rm -rf "$HERE/mut"
mkdir -p "$HERE/mut/round-46"
cp "$LANE/tools/round-46/gate.py" "$HERE/mut/round-46/"
for v in base dead cut min1 bypass; do
    mkdir -p "$HERE/mut/$v"
    cp "$LANE/tools/round-47/record.py" "$HERE/mut/$v/record.py"
done
for v in dead cut min1 bypass; do
    patch -s -d "$HERE/mut/$v" < "$HERE/patches/$v.diff"
done
echo "variants rebuilt: $(ls "$HERE/mut" | tr '\n' ' ')"
