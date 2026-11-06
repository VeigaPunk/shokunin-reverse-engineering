#!/bin/bash
# usage: drive1.sh <mutant-id>
S=/fast/scratch/hyaku/kaidoku-r100/MutationC2
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
B0=6371c88633f6ce6692eaeff17e256b80ad21ece0
A2=cbd224ef9b9d2271f415d823bdc4d1e70a0d281c
id="$1"; f="$S/mut/$id.py"
python3 -I -B "$f" --selftest > "$S/out/$id.selftest.txt" 2>&1; echo "rc=$?" >> "$S/out/$id.selftest.txt"
python3 -I -B "$f" --root "$LANE" --rev "$B0" --work "$S/runs/$id-b0" --json-out "$S/out/$id-b0.json" > "$S/out/$id-b0.txt" 2>&1; echo "rc=$?" >> "$S/out/$id-b0.txt"
python3 -I -B "$f" --root "$LANE" --rev "$A2" --work "$S/runs/$id-a2" --json-out "$S/out/$id-a2.json" > "$S/out/$id-a2.txt" 2>&1; echo "rc=$?" >> "$S/out/$id-a2.txt"
rm -rf "$S/runs/$id-b0" "$S/runs/$id-a2"
echo "done $id"
