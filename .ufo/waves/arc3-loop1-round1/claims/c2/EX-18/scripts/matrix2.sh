#!/usr/bin/env bash
# EX-18 extra shapes: in-place tamper of the CURRENT table (R7) and a SHRUNK table (R8).
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
W=/dev/shm/ex18-absent
G=$W/gate
OUT=$W/out
PROBE=$G/citation-drift-probe.py
EXP=$G/expected.json
TBL=$G/pointer-table.json
REAL=$REPO/.ufo/gates/citation-drift/pointer-table.json

run_case() {
  local case="$1"
  echo "### CASE $case" >> "$OUT/matrix.log"
  echo "-- table object: $(stat -c '%F %s bytes' "$TBL" 2>&1)" >> "$OUT/matrix.log"
  echo "-- table sha256: $(sha256sum "$TBL" 2>&1 | cut -c1-64)" >> "$OUT/matrix.log"
  python3 "$PROBE" --root "$REPO" --rev HEAD --table "$TBL" --expected "$EXP" \
      > "$OUT/$case.probe.txt" 2>&1; local pe=$?
  python3 "$PROBE" --root "$REPO" --rev HEAD --table "$TBL" --expected "$EXP" --strict \
      > "$OUT/$case.gate.txt" 2>&1; local ge=$?
  echo "-- probe-mode exit=$pe | gate-mode exit=$ge" >> "$OUT/matrix.log"
  echo "-- probe verdict: $(grep -h 'CITATION_DRIFT_VERDICT' "$OUT/$case.probe.txt")" >> "$OUT/matrix.log"
  echo "-- gate  verdict: $(grep -h 'CITATION_DRIFT_VERDICT' "$OUT/$case.gate.txt")" >> "$OUT/matrix.log"
  echo "" >> "$OUT/matrix.log"
}

# R7: current table, one needle altered in place (same shape/size class as real)
rm -f "$TBL"
python3 - "$REAL" "$TBL" <<'PY'
import json, sys
t = json.load(open(sys.argv[1]))
t["entries"][0]["must_match"] = "NEEDLE-THAT-CANNOT-MATCH-ANYTHING"
json.dump(t, open(sys.argv[2], "w"))
PY
run_case R7-tampered-current-needle

# R8: current table with 5 entries dropped (contract silently weakened, all pins intact)
rm -f "$TBL"
python3 - "$REAL" "$TBL" <<'PY'
import json, sys
t = json.load(open(sys.argv[1]))
t["entries"] = t["entries"][:-5]
json.dump(t, open(sys.argv[2], "w"))
PY
run_case R8-shrunk-table

# restore pristine
rm -f "$TBL"
cp -a "$REAL" "$TBL"
echo "DONE2" >> "$OUT/matrix.log"
