#!/usr/bin/env bash
# RV-6 proto attacks: independent verification of EX-21's guarded prototype
# (the closest thing to "the implemented code" while EX-16's real target is
# unlanded). Source is read-only; all work happens in this artifact dir.
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
W=$REPO/.ufo/waves/arc3-loop1-round1/claims/c2
S=$(cd "$(dirname "$0")" && pwd)
export TMPDIR=$S/tmp; mkdir -p "$TMPDIR"
PT=$S/proto-test; rm -rf "$PT"; mkdir -p "$PT"
cp "$W/EX-21/tmp/proto/probe.py" "$PT/probe.py"
cp "$W/EX-21/tmp/proto/pointer-table.json" "$PT/pointer-table.json"
cp "$W/EX-21/tmp/proto/expected.json" "$PT/expected-as-shipped.json"
P=$PT/probe.py
REAL_TABLE=$REPO/.ufo/gates/citation-drift/pointer-table.json

echo "### proto fingerprint + shipped expected state"
sha256sum "$PT/probe.py" "$PT/expected-as-shipped.json" | sed 's/^/  /'
python3 - "$PT/expected-as-shipped.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
print("  keys:",list(d.keys()), "table_sha256:", d.get("table_sha256"))
print("  selftest cases:", len(d.get("selftest",[])))
PY

echo
echo "### A. proto selftest with its OWN (as-shipped) expected.json"
python3 "$P" --selftest --expected "$PT/expected-as-shipped.json" 2>&1 | tail -2
echo "  rc=${PIPESTATUS[0]}  <- green while the pin is absent"

echo
echo "### build a properly pinned expected.json (13-case table)"
python3 - "$PT/expected-as-shipped.json" "$REAL_TABLE" "$PT/expected-pinned.json" <<'PY'
import hashlib,json,sys
d=json.load(open(sys.argv[1]))
d["table_sha256"]=hashlib.sha256(open(sys.argv[2],"rb").read()).hexdigest()
st=d.get("selftest",[])
names=[c["case"] for c in st]
if "table_tampered" not in names:
    st.append({"case":"table_tampered","exit_code":2,"finding":"pointer_table_tampered"})
if "table_absent" not in names:
    st.append({"case":"table_absent","exit_code":2,"finding":"pointer_table_unreadable"})
d["selftest"]=st
json.dump(d,open(sys.argv[3],"w"))
print("  pin:",d["table_sha256"])
print("  cases:",len(st))
PY
python3 "$P" --selftest --expected "$PT/expected-pinned.json" 2>&1 | tail -3
echo "  rc=${PIPESTATUS[0]}"

echo
echo "### fixture tables"
printf '{"_doc":"x","entries":[],"quoted":[]}' > "$PT/table-empty.json"
cp "$REAL_TABLE" "$PT/table-real.json"
printf '\n' >> "$PT/table-real.json.space" 2>/dev/null || true
cp "$REAL_TABLE" "$PT/table-space.json"; printf ' ' >> "$PT/table-space.json"
printf '{"_doc":"x","entries":[],"quoted":[]}' > "$PT/expected-unpinned-emptied-pair.json"

runc() { # runc <label> <table> <expected> [extra]
  local label=$1 table=$2 exp=$3; shift 3
  out=$(python3 "$P" --root "$REPO" --rev HEAD --table "$table" --expected "$exp" "$@" 2>&1); rc=$?
  echo "[$label] rc=$rc | $(echo "$out" | grep '^CITATION_DRIFT_VERDICT')"
  echo "$out" | grep '^CITATION_DRIFT:' | head -2 | sed 's/^/    /'
}

echo
echo "### B-G. pinned expected (guard in force)"
runc "B-pinned-real-table"     "$PT/table-real.json"   "$PT/expected-pinned.json"
runc "C-pinned-emptied-table"  "$PT/table-empty.json"  "$PT/expected-pinned.json"
runc "C2-pinned-emptied-strict" "$PT/table-empty.json" "$PT/expected-pinned.json" --strict
runc "D-pinned-absent-table"   "$PT/absent-table.json" "$PT/expected-pinned.json"
runc "E-pinned-space-tamper"   "$PT/table-space.json"  "$PT/expected-pinned.json"
runc "F-pinned-nondefault-path-real" "$REAL_TABLE"      "$PT/expected-pinned.json"

echo
echo "### H. THE HOLE: unpinned expected (pin key deleted) + emptied table"
python3 - "$PT/expected-pinned.json" "$PT/expected-unpinned.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1])); d.pop("table_sha256",None)
json.dump(d,open(sys.argv[2],"w"))
PY
runc "H-unpinned-emptied"      "$PT/table-empty.json"  "$PT/expected-unpinned.json"
runc "H2-unpinned-emptied-strict" "$PT/table-empty.json" "$PT/expected-unpinned.json" --strict
runc "H3-unpinned-real-table"  "$PT/table-real.json"   "$PT/expected-unpinned.json"

echo
echo "### I. expected.json absent entirely"
runc "I-absent-expected"       "$PT/table-empty.json"  "$PT/no-such-expected.json"

echo
echo "### J. row-token string comparison (code vs EX-20 patch text)"
echo "-- ids the proto code can emit on guard paths --"
grep -o 'pointer_table_tampered\|pointer_table_unreadable\|table_tampered' "$P" | sort | uniq -c | sed 's/^/    /'
echo "-- ids the row patch declares --"
grep -o '`table_tampered`\|`pointer_table_unreadable`\|`revision_unresolvable`\|unpinned' "$W/SC-4/scratch/patchtest/SKILL.md" | sort | uniq -c | sed 's/^/    /'
