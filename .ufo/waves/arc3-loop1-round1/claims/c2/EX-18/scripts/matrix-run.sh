#!/usr/bin/env bash
# EX-18 generic 8-shape injection matrix runner.
# env: PROBE EXP TBL OUTDIR LABEL REPO STALE
set -u
: "${PROBE:?}" "${EXP:?}" "${TBL:?}" "${OUTDIR:?}" "${LABEL:?}"
REPO=${REPO:-/home/vgpnk/Projects/shokunin/kaidoku-shokunin}
STALE=${STALE:-/dev/shm/ex18-absent/stale/pointer-table-round4.json}
REAL=$REPO/.ufo/gates/citation-drift/pointer-table.json
mkdir -p "$OUTDIR"
LOG=$OUTDIR/matrix-$LABEL.log
: > "$LOG"

run_case() {
  local case="$1"
  local tbl_obj; tbl_obj=$(stat -c '%F %s bytes' "$TBL" 2>&1)
  local tbl_sha; tbl_sha=$(sha256sum "$TBL" 2>&1 | cut -c1-64)
  local pe ge
  python3 "$PROBE" --root "$REPO" --rev HEAD --table "$TBL" --expected "$EXP" \
      > "$OUTDIR/$case.probe.txt" 2>&1; pe=$?
  python3 "$PROBE" --root "$REPO" --rev HEAD --table "$TBL" --expected "$EXP" --strict \
      > "$OUTDIR/$case.gate.txt" 2>&1; ge=$?
  {
    echo "### CASE $case  [label=$LABEL]"
    echo "-- probe: $PROBE"
    echo "-- expected: $EXP"
    echo "-- table object: $tbl_obj"
    echo "-- table sha256: $tbl_sha"
    echo "-- readlink: $(readlink -f "$TBL" 2>&1)"
    echo "-- probe-mode exit=$pe | gate-mode exit=$ge"
    echo "-- probe verdict: $(grep -h 'CITATION_DRIFT_VERDICT' "$OUTDIR/$case.probe.txt")"
    echo "-- gate  verdict: $(grep -h 'CITATION_DRIFT_VERDICT' "$OUTDIR/$case.gate.txt")"
    echo "-- probe findings:"
    grep -h '^CITATION_DRIFT:' "$OUTDIR/$case.probe.txt" | sed 's/^/     /'
    echo ""
  } >> "$LOG"
}

run_case R0-baseline

rm -f "$TBL"; run_case R1-absent

rm -rf "$TBL"; mkdir "$TBL"; run_case R2-directory

rm -rf "$TBL"; ln -s "$STALE" "$TBL"; run_case R3-symlink-stale

rm -f "$TBL"; ln -s /dev/shm/ex18-absent/stale/does-not-exist.json "$TBL"; run_case R4-symlink-dangling

rm -f "$TBL"; ln -s "$REAL" "$TBL"; run_case R5-symlink-live

rm -f "$TBL"
python3 - "$REAL" "$TBL" <<'PY'
import json, sys
t = json.load(open(sys.argv[1]))
t["entries"][0]["must_match"] = "NEEDLE-THAT-CANNOT-MATCH-ANYTHING"
json.dump(t, open(sys.argv[2], "w"))
PY
run_case R6-tampered-current-needle

rm -f "$TBL"
python3 - "$REAL" "$TBL" <<'PY'
import json, sys
t = json.load(open(sys.argv[1]))
t["entries"] = t["entries"][:-5]
json.dump(t, open(sys.argv[2], "w"))
PY
run_case R7-shrunk-table-5-dropped

rm -f "$TBL"; cp -a "$REAL" "$TBL"
echo "DONE label=$LABEL" >> "$LOG"
