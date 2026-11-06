#!/bin/bash
# usage: drive2.sh <id> <world-name> <rev>
S=/fast/scratch/hyaku/kaidoku-r100/MutationC2
id="$1"; w="$2"; r="$3"
if [ "$id" = orig ]; then f="$S/orig.py"; else f="$S/mut/$id.py"; fi
python3 -I -B "$f" --root "$S/worlds/$w" --rev "$r" --work "$S/runs/$id-$w" --json-out "$S/out/$id-$w.json" > "$S/out/$id-$w.txt" 2>&1; echo "rc=$?" >> "$S/out/$id-$w.txt"
rm -rf "$S/runs/$id-$w"
echo "done $id $w"
