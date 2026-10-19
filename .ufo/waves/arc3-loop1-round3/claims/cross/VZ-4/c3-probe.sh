#!/bin/bash
# VZ-4 C3 harness — citation-drift probe re-measurement (independent of seats' prose).
# usage: c3-probe.sh <probe.py> <table.json> <expected.json> <root> <out>
set -u
PROBE=$1; TABLE=$2; EXPECTED=$3; ROOT=$4; OUT=$5
export TMPDIR=/var/tmp/vz4r3/tmp; mkdir -p "$TMPDIR"
: > "$OUT"
say() { printf '%s\n' "$*" | tee -a "$OUT"; }
say "== VZ-4 C3 probe harness =="
say "probe=$(sha256sum "$PROBE")"
say "table=$(sha256sum "$TABLE") lines=$(wc -l < "$TABLE")"
say "expected=$(sha256sum "$EXPECTED")"
say "root=$ROOT rev=HEAD utc=$(date -u +%FT%TZ)"

say "-- entry count (mechanical) --"
python3 - "$TABLE" <<'PY' | tee -a "$OUT"
import json, sys
t = json.load(open(sys.argv[1]))
e = t.get('entries', [])
print(f"entries={len(e)}")
ids = [x.get('id') for x in e]
print(f"unique_ids={len(set(ids))}")
PY

say "-- digest pin: sha256(table) vs expected.pointer_table.sha256 --"
python3 - "$TABLE" "$EXPECTED" <<'PY' | tee -a "$OUT"
import hashlib, json, sys
table, exp = sys.argv[1], sys.argv[2]
h = hashlib.sha256(open(table, 'rb').read()).hexdigest()
pin = json.load(open(exp)).get('pointer_table', {}).get('sha256', '')
print(f"computed={h}")
print(f"pinned  ={pin}")
print(f"PIN_MATCH={'YES' if h == pin else 'NO'}")
PY

say "-- selftest --"
o=$(python3 "$PROBE" --selftest --expected "$EXPECTED" 2>&1); rc=$?
printf 'selftest exit=%d\n%s\n' "$rc" "$o" | tee -a "$OUT"

say "-- HEAD run, default mode --"
o=$(python3 "$PROBE" --root "$ROOT" --rev HEAD --table "$TABLE" --expected "$EXPECTED" 2>&1); rc=$?
printf 'run exit=%d\n%s\n' "$rc" "$o" | tee -a "$OUT"

say "-- HEAD run, --strict --"
o=$(python3 "$PROBE" --root "$ROOT" --rev HEAD --table "$TABLE" --expected "$EXPECTED" --strict 2>&1); rc=$?
printf 'strict exit=%d\n%s\n' "$rc" "$o" | tee -a "$OUT"

say "== end $(date -u +%FT%TZ) =="