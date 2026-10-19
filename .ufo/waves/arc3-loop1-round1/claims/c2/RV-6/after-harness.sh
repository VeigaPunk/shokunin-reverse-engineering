#!/usr/bin/env bash
# RV-6 after-state matrix: run once EX-16's guard lands.
# Uses a private copy of the gates dir (so "default path" tampering is testable
# without touching the repo), with --root pointed read-only at the real repo.
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
S=$(cd "$(dirname "$0")" && pwd)
export TMPDIR=$S/tmp; mkdir -p "$TMPDIR"
AH=$S/after; rm -rf "$AH"; mkdir -p "$AH"
cp -r "$REPO/.ufo/gates/citation-drift/." "$AH/"
P=$AH/citation-drift-probe.py
G=$REPO/.ufo/gates/citation-drift

echo "### fingerprints (after-state)"
sha256sum "$AH"/* | sed 's|^|  |'
echo "### expected.json keys + selftest case table"
python3 - "$AH/expected.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
print("  keys:",list(d.keys()))
for k,v in d.items():
    if k not in ("_doc","selftest"):
        print("  %s: %s" % (k, json.dumps(v)[:300]))
st=d.get("selftest",[])
print("  selftest cases: %d" % len(st))
for c in st: print("    %-22s exit=%s finding=%s" % (c.get("case"),c.get("exit_code"),c.get("finding")))
PY

runc() { # runc <label> [args...]
  local label=$1; shift
  out=$(python3 "$P" --root "$REPO" --rev HEAD "$@" 2>&1); rc=$?
  echo "[$label] rc=$rc findings=$(echo "$out" | grep -c '^CITATION_DRIFT:')"
  echo "$out" | grep '^CITATION_DRIFT' | sed 's/^/    /'
  echo "$out" | grep '^CITATION_DRIFT_VERDICT' | sed 's/^/    /'
}

echo "### 1. selftest (copy)"
python3 "$P" --selftest 2>&1 | tail -2; echo "  rc=${PIPESTATUS[0]}"

echo "### 2. clean run at HEAD, defaults (copy)"
runc "2-clean-defaults"

echo "### 3. repo-native clean run (real gates dir, real defaults)"
out=$(python3 "$G/citation-drift-probe.py" --root "$REPO" --rev HEAD 2>&1); rc=$?
echo "[3-repo-clean] rc=$rc"; echo "$out" | tail -1 | sed 's/^/    /'

echo "### 4. absent table path (--table)"
runc "4-absent-table" --table "$AH/absent-table.json" --expected "$AH/expected.json"

echo "### 5. tampered table at NON-default path (--table)"
printf '{"_doc":"x","entries":[],"quoted":[]}' > "$S/table-empty.json"
runc "5-tampered-nondefault" --table "$S/table-empty.json" --expected "$AH/expected.json"

echo "### 6. tampered table at DEFAULT path (emptied entries)"
cp "$AH/pointer-table.json" "$S/after-table-orig.json"
printf '{"_doc":"x","entries":[],"quoted":[]}' > "$AH/pointer-table.json"
runc "6-tampered-default-emptied"
echo "### 6b. tampered default + --strict"
runc "6b-tampered-default-strict" --strict
cp "$S/after-table-orig.json" "$AH/pointer-table.json"

echo "### 7. weakened must_match at DEFAULT path"
python3 - "$AH/pointer-table.json" "$AH/pointer-table.json.tmp" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
for e in d.get("entries",[]): e["must_match"]=".*"
for q in d.get("quoted",[]): q["must_match"]=".*"
json.dump(d,open(sys.argv[2],"w"))
PY
cp "$AH/pointer-table.json.tmp" "$AH/pointer-table.json"
runc "7-weakened-default"
cp "$S/after-table-orig.json" "$AH/pointer-table.json"

echo "### 8. whitespace-only reformat at DEFAULT path (semantic no-op)"
python3 -c "import json,sys;json.dump(json.load(open(sys.argv[1])),open(sys.argv[2],'w'),indent=1)" "$S/after-table-orig.json" "$AH/pointer-table.json"
runc "8-whitespace-reformat"
cp "$S/after-table-orig.json" "$AH/pointer-table.json"

echo "### 9. absent table at DEFAULT path"
mv "$AH/pointer-table.json" "$S/after-table-orig2.json"
runc "9-absent-default"
mv "$S/after-table-orig2.json" "$AH/pointer-table.json"

echo "### 10. expected.json digest key removed (legacy/unpinned expected)"
python3 - "$AH/expected.json" "$S/expected-unpinned.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
for k in list(d.keys()):
    if "table" in k: del d[k]
json.dump(d,open(sys.argv[2],"w"))
PY
runc "10-expected-unpinned" --expected "$S/expected-unpinned.json"

echo "### 11. expected.json absent"
runc "11-expected-absent" --expected "$AH/absent-expected.json"

echo "### 12. table = valid JSON list at DEFAULT path"
cp "$AH/pointer-table.json" "$S/after-table-orig3.json"
printf '[]' > "$AH/pointer-table.json"
runc "12-default-list"
cp "$S/after-table-orig3.json" "$AH/pointer-table.json"

echo "### 13. frozen-run reproduction attempt at recorded rev with current table"
runc "13-frozen-rev-current-table" --rev 679af5d749f2fd48b9d543e3c99d348d5458f90f

echo "### 14. the suppression pair, re-run against the guarded probe (bypass check)"
python3 - "$G/pointer-table.json" "$S/table-with-dead.json" "$S/table-with-dead-emptied.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
d["entries"]=d["entries"]+[{"id":"rv6-injected-dead","kind":"exact","file":"SKILL.md","line":1,"must_match":"ZZZ-rv6-no-such-text"}]
json.dump(d,open(sys.argv[2],"w"))
e=dict(d); e["entries"]=[]; json.dump(e,open(sys.argv[3],"w"))
PY
runc "14a-dead-table-nondefault" --table "$S/table-with-dead.json" --expected "$AH/expected.json"
runc "14b-dead-emptied-nondefault" --table "$S/table-with-dead-emptied.json" --expected "$AH/expected.json"
echo "### 14c: same, at DEFAULT path (guarded run must not be silent)"
cp "$S/table-with-dead-emptied.json" "$AH/pointer-table.json"
runc "14c-dead-emptied-default"
cp "$S/after-table-orig.json" "$AH/pointer-table.json"
