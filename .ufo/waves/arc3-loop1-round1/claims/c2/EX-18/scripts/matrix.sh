#!/usr/bin/env bash
# EX-18 absent-table injection matrix (arc3-loop1-round1, chain c2)
# Scratch lives in /dev/shm because /tmp hit the user quota (EDQUOT) — deviation recorded.
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
W=/dev/shm/ex18-absent
G=$W/gate
OUT=$W/out
PROBE=$G/citation-drift-probe.py
EXP=$G/expected.json
TBL=$G/pointer-table.json
mkdir -p "$OUT"

run_case() {
  local case="$1"
  echo "### CASE $case" >> "$OUT/matrix.log"
  echo "-- table object: $(stat -c '%F %s bytes' "$TBL" 2>&1)" >> "$OUT/matrix.log"
  echo "-- table sha256: $(sha256sum "$TBL" 2>&1 | cut -c1-64)" >> "$OUT/matrix.log"
  echo "-- readlink: $(readlink -f "$TBL" 2>&1)" >> "$OUT/matrix.log"
  python3 "$PROBE" --root "$REPO" --rev HEAD --table "$TBL" --expected "$EXP" \
      > "$OUT/$case.probe.txt" 2>&1
  local pe=$?
  python3 "$PROBE" --root "$REPO" --rev HEAD --table "$TBL" --expected "$EXP" --strict \
      > "$OUT/$case.gate.txt" 2>&1
  local ge=$?
  echo "-- probe-mode exit=$pe | gate-mode exit=$ge" >> "$OUT/matrix.log"
  echo "-- probe verdict: $(grep -h 'CITATION_DRIFT_VERDICT' "$OUT/$case.probe.txt")" >> "$OUT/matrix.log"
  echo "-- gate  verdict: $(grep -h 'CITATION_DRIFT_VERDICT' "$OUT/$case.gate.txt")" >> "$OUT/matrix.log"
  echo "-- probe findings: $(grep -c '^CITATION_DRIFT:' "$OUT/$case.probe.txt")" >> "$OUT/matrix.log"
  echo "" >> "$OUT/matrix.log"
}

# R0 baseline: pristine table copy
run_case R0-baseline

# R1 absent: delete the table
rm -f "$TBL"
run_case R1-absent

# R2 directory in the table's place
rm -rf "$TBL"; mkdir "$TBL"
run_case R2-directory

# R3 symlink -> stale copy (round-4-era table from git history)
rm -rf "$TBL"
ln -s "$W/stale/pointer-table-round4.json" "$TBL"
run_case R3-symlink-stale

# R4 dangling symlink (target does not exist)
rm -f "$TBL"
ln -s "$W/stale/does-not-exist.json" "$TBL"
run_case R4-symlink-dangling

# R5 control: symlink -> the live pinned table (real repo path, read-only)
rm -f "$TBL"
ln -s "$REPO/.ufo/gates/citation-drift/pointer-table.json" "$TBL"
run_case R5-symlink-live

# R6 tampered content in place (same path, same size class, one needle altered)
rm -f "$TBL"
python3 - "$W/stale/pointer-table-round4.json" "$TBL" <<'PY'
import json, sys
src, dst = sys.argv[1], sys.argv[2]
t = json.load(open(src))
t["entries"][0]["must_match"] = "NEEDLE-THAT-CANNOT-MATCH-ANYTHING"
json.dump(t, open(dst, "w"))
PY
run_case R6-tampered-content

# restore pristine copy for any later re-run
rm -f "$TBL"
cp -a "$REPO/.ufo/gates/citation-drift/pointer-table.json" "$TBL"
echo "DONE" >> "$OUT/matrix.log"
