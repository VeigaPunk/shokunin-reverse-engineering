#!/usr/bin/env bash
# Differential containment probe: round-50 fetch-vendor.py vs round-41 fetch-vendor.py
# (the file the FROZEN counter docstring names).  Offline: a local tar + file:// URL.
set -u
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
S=/fast/scratch/hyaku/kaidoku-r50/w3-SentReceipts
SPEC=$S/containment/carriers-local.json
mkdir -p "$S/containment"

echo "== A: round-50 fetcher, file:// URL =="
python3 -I -B "$LANE/tools/round-50/fetch-vendor.py" --spec "$SPEC" --cache "$S/containment/c50-file" 2>&1 | tail -12
echo "exit=${PIPESTATUS[0]}"
echo "cache contents:"; ls -la "$S/containment/c50-file" 2>&1 | tail -3

echo
echo "== B: round-41 fetcher, file:// URL (the file the frozen counter names) =="
python3 -I -B "$LANE/tools/round-41/fetch-vendor.py" --spec "$SPEC" --cache "$S/containment/c41-file" 2>&1 | tail -12
echo "exit=${PIPESTATUS[0]}"
echo "cache contents:"; ls -la "$S/containment/c41-file" 2>&1 | tail -3

echo
echo "== C: round-50 fetcher, cache INSIDE the lane =="
python3 -I -B "$LANE/tools/round-50/fetch-vendor.py" --spec "$SPEC" --cache "$LANE/.ufo/waves/round-50/w3/SentReceipts/lanecache" 2>&1 | tail -6
echo "exit=${PIPESTATUS[0]}"

echo
echo "== D: round-41 fetcher, cache INSIDE the lane =="
python3 -I -B "$LANE/tools/round-41/fetch-vendor.py" --spec "$SPEC" --cache "$LANE/.ufo/waves/round-50/w3/SentReceipts/lanecache41" 2>&1 | tail -6
echo "exit=${PIPESTATUS[0]}"
echo "cache contents:"; ls -la "$LANE/.ufo/waves/round-50/w3/SentReceipts/lanecache41" 2>&1 | tail -3

echo
echo "== E: round-50 fetcher, cache = lane root itself (trailing-slash bypass?) =="
python3 -I -B "$LANE/tools/round-50/fetch-vendor.py" --spec "$SPEC" --cache "$LANE" 2>&1 | tail -4
echo "exit=${PIPESTATUS[0]}"

echo
echo "== F: round-50 fetcher, cache = lane root + '/.' =="
python3 -I -B "$LANE/tools/round-50/fetch-vendor.py" --spec "$SPEC" --cache "$LANE/." 2>&1 | tail -4
echo "exit=${PIPESTATUS[0]}"

echo
echo "== G: round-50 fetcher, cache = a SYMLINK inside the lane pointing at the lane =="
ln -sfn "$LANE" "$S/lanelink"
python3 -I -B "$LANE/tools/round-50/fetch-vendor.py" --spec "$SPEC" --cache "$S/lanelink" 2>&1 | tail -4
echo "exit=${PIPESTATUS[0]}"
echo "cache contents:"; ls -la "$S/lanelink" 2>&1 | tail -3
