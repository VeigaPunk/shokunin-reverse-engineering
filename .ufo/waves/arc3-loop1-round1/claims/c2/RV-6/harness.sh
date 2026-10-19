#!/usr/bin/env bash
# RV-6 seat harness: silent-rc-0 hunt on the citation-drift probe.
# Read-only over the real repo; all mutated inputs live in this artifact dir.
# TMPDIR is redirected here because /tmp hit the user quota this wave.
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
G=$REPO/.ufo/gates/citation-drift
S=$(cd "$(dirname "$0")" && pwd)
export TMPDIR=$S/tmp
mkdir -p "$TMPDIR"
PROBE=$G/citation-drift-probe.py
EXP=$G/expected.json

run() { # run <label> <table> [extra args...]
  local label=$1 table=$2; shift 2
  out=$(python3 "$PROBE" --root "$REPO" --rev HEAD --table "$table" --expected "$EXP" "$@" 2>&1)
  rc=$?
  last=$(echo "$out" | tail -1)
  echo "[$label] rc=$rc | $last"
  echo "$out" | grep -c "^CITATION_DRIFT:" | sed "s/^/[$label] finding_lines=/"
}

echo "### A: absent table path"
run "A-absent" "$S/does-not-exist.json"

echo "### B: tampered table = emptied entries (valid JSON)"
printf '{"_doc":"x","entries":[],"quoted":[]}' > "$S/table-empty.json"
run "B-emptied" "$S/table-empty.json"
run "B-emptied-strict" "$S/table-empty.json" --strict

echo "### C: tampered table = {} (no entries key at all)"
printf '{}' > "$S/table-brace.json"
run "C-brace" "$S/table-brace.json"
run "C-brace-strict" "$S/table-brace.json" --strict

echo "### D: table = valid JSON but a list (type confusion)"
printf '[]' > "$S/table-list.json"
run "D-list" "$S/table-list.json"

echo "### E: table truncated (invalid JSON)"
printf '{"entries": [{"id":"x"' > "$S/table-trunc.json"
run "E-trunc" "$S/table-trunc.json"

echo "### F: table entry must_match weakened to .* (suppression of real drift)"
python3 - "$G/pointer-table.json" "$S/table-weakened.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
for e in d.get("entries",[]):
    e["must_match"]=".*"
for q in d.get("quoted",[]):
    q["must_match"]=".*"
json.dump(d,open(sys.argv[2],"w"))
PY
run "F-weakened" "$S/table-weakened.json"
run "F-weakened-strict" "$S/table-weakened.json" --strict

echo "### G: table with all entries removed but quoted kept"
python3 - "$G/pointer-table.json" "$S/table-noentries.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
d["entries"]=[]
json.dump(d,open(sys.argv[2],"w"))
PY
run "G-noentries" "$S/table-noentries.json"

echo "### H: expected.json absent"
python3 "$PROBE" --root "$REPO" --rev HEAD --table "$G/pointer-table.json" --expected "$S/absent-expected.json" > "$S/H.out" 2>&1
echo "[H-absent-expected] rc=$? | $(tail -1 "$S/H.out")"

echo "### I: frozen-run rev existence check"
git -C "$REPO" cat-file -t 679af5d749f2fd48b9d543e3c99d348d5458f90f 2>&1
echo "### I2: real-table run at frozen rev (if it exists)"
if git -C "$REPO" cat-file -e 679af5d749f2fd48b9d543e3c99d348d5458f90f^{commit} 2>/dev/null; then
  run "I2-frozen-rev-real-table" "$G/pointer-table.json"
  run "I2-frozen-rev-real-table-strict" "$G/pointer-table.json" --strict
  run "I2-frozen-rev-emptied-table" "$S/table-empty.json"
fi

echo "### J: selftest still green under redirected TMPDIR"
python3 "$PROBE" --selftest > "$S/J-selftest.out" 2>&1
echo "[J-selftest] rc=$? | $(tail -1 "$S/J-selftest.out")"
