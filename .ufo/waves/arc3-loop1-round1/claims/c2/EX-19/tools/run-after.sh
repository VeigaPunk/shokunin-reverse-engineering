#!/bin/bash
# EX-19 frozen-run byte-stability harness.
# usage: run-after.sh <new-probe> <new-expected> <new-table>
# Runs the post-guard probe against the ORIGINAL (pre-guard) expected+table
# and against the NEW pins; outputs land in $S/after/.
set -u
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
# self-locating: this kit lives in claims/c2/EX-19/tools/ (orig/, before-matrix/)
S=$(cd "$(dirname "$0")" && pwd)
NEW_PROBE=${1:?new probe path}
NEW_EXPECTED=${2:?new expected path}
NEW_TABLE=${3:?new table path}
mkdir -p "$S/tmp"
export TMPDIR=$S/tmp
A=${OUTDIR:-$S/after}; mkdir -p $A
cd "$R"

run() { # run <tag> <cmd...>
  local tag=$1; shift
  "$@" > "$A/$tag.txt" 2>&1
  local rc=$?
  echo "$rc" > "$A/$tag.exit"
  echo "[$tag] exit=$rc"
}

# A. frozen-run byte-stability: NEW probe + ORIGINAL expected/table
run selftest-newprobe-orgexpected python3 "$NEW_PROBE" --selftest --expected "$S/orig/expected.json"
run fullrun-newprobe-orgexpected python3 "$NEW_PROBE" --root "$R" --rev HEAD --table "$S/orig/pointer-table.json" --expected "$S/orig/expected.json"
run fullrun-strict-newprobe-orgexpected python3 "$NEW_PROBE" --root "$R" --rev HEAD --table "$S/orig/pointer-table.json" --expected "$S/orig/expected.json" --strict
run frozenrev-newprobe-orgexpected python3 "$NEW_PROBE" --root "$R" --rev 679af5d749f2fd48b9d543e3c99d348d5458f90f --table "$S/orig/pointer-table.json" --expected "$S/orig/expected.json"
run tamperedtable-newprobe-orgexpected python3 "$NEW_PROBE" --root "$R" --rev HEAD --table "$S/before/table-tampered.json" --expected "$S/orig/expected.json"
run emptytable-newprobe-orgexpected python3 "$NEW_PROBE" --root "$R" --rev HEAD --table "$S/before/table-empty.json" --expected "$S/orig/expected.json"
run absenttable-newprobe-orgexpected python3 "$NEW_PROBE" --root "$R" --rev HEAD --table "$S/before/no-such-table.json" --expected "$S/orig/expected.json"

# B. post-guard pins: NEW probe + NEW expected + NEW table
run selftest-newprobe-newexpected python3 "$NEW_PROBE" --selftest --expected "$NEW_EXPECTED"
run fullrun-newprobe-newexpected python3 "$NEW_PROBE" --root "$R" --rev HEAD --table "$NEW_TABLE" --expected "$NEW_EXPECTED"
run absenttable-newprobe-newexpected python3 "$NEW_PROBE" --root "$R" --rev HEAD --table "$S/before/no-such-table.json" --expected "$NEW_EXPECTED"
run tamperedtable-newprobe-newexpected python3 "$NEW_PROBE" --root "$R" --rev HEAD --table "$S/before/table-tampered.json" --expected "$NEW_EXPECTED"
# C. cross-compat attack: OLD probe + NEW expected (additive JSON must not break old readers)
run selftest-oldprobe-newexpected python3 "$S/orig/citation-drift-probe.py" --selftest --expected "$NEW_EXPECTED"
run fullrun-oldprobe-newexpected python3 "$S/orig/citation-drift-probe.py" --root "$R" --rev HEAD --table "$NEW_TABLE" --expected "$NEW_EXPECTED"

echo "=== byte-stability comparisons vs before-matrix (want: identical) ==="
for f in "$A"/*.txt; do
  tag=$(basename "$f" .txt)
  if [ -f "$S/before-matrix/$tag.txt" ]; then
    if cmp -s "$S/before-matrix/$tag.txt" "$f"; then echo "IDENTICAL: $tag"; else echo "DIVERGED:  $tag"; fi
  else
    echo "NEW-RUN:   $tag (no before counterpart)"
  fi
done
echo "=== exit-code comparisons ==="
for f in "$A"/*.exit; do
  tag=$(basename "$f" .exit)
  if [ -f "$S/before-matrix/$tag.exit" ]; then
    echo "$tag: before=$(cat $S/before-matrix/$tag.exit) after=$(cat $f)"
  fi
done
