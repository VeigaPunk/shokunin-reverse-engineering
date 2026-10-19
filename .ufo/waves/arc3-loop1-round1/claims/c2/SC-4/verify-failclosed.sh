#!/usr/bin/env bash
# SC-4: measure the fail-closed variant of EX-21's guard prototype — the option
# that would close the unpinned-table hole (P4). Scratch copies only; the real
# gate is untouched. TMPDIR redirected here (/tmp quota).
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
G=$REPO/.ufo/gates/citation-drift
S=$(cd "$(dirname "$0")" && pwd)
EX21=$REPO/.ufo/waves/arc3-loop1-round1/claims/c2/EX-21/tmp/proto
OUT=$S/verify-failclosed.txt
export TMPDIR=$S/scratch/tmp
mkdir -p "$TMPDIR" "$S/scratch/failclosed"
P=$S/scratch/failclosed/probe.py

python3 - "$EX21/probe.py" "$P" <<'PY'
import sys
src = open(sys.argv[1]).read()

old_cne = '''        if any(f in ("snapshot_tampered", "snapshot_missing",
                     "pointer_table_unreadable", "pointer_table_tampered",
                     "unpinned_legacy",
                     "root_unreadable", "revision_unresolvable", "internal_error")
               for f, _, _ in self.rows):'''
new_cne = '''        if any(f in ("snapshot_tampered", "snapshot_missing",
                     "pointer_table_unreadable", "pointer_table_tampered",
                     "table_pin_absent",
                     "unpinned_legacy",
                     "root_unreadable", "revision_unresolvable", "internal_error")
               for f, _, _ in self.rows):'''
assert old_cne in src, "CNE list not found"
src = src.replace(old_cne, new_cne)

old_guard = '''    pinned_table = expected.get("table_sha256")
    if pinned_table is not None and sha256_bytes(table_bytes) != pinned_table:
        findings.add("pointer_table_tampered", os.path.basename(table_path),
                     "sha256 %s != pinned %s" % (sha256_bytes(table_bytes), pinned_table))
        return findings'''
new_guard = '''    pinned_table = expected.get("table_sha256")
    if pinned_table is None:
        findings.add("table_pin_absent", os.path.basename(table_path),
                     "expected.json pins no table digest (fail-closed)")
        return findings
    if sha256_bytes(table_bytes) != pinned_table:
        findings.add("pointer_table_tampered", os.path.basename(table_path),
                     "sha256 %s != pinned %s" % (sha256_bytes(table_bytes), pinned_table))
        return findings'''
assert old_guard in src, "guard block not found"
src = src.replace(old_guard, new_guard)
open(sys.argv[2], "w").write(src)
print("fail-closed variant written to", sys.argv[2])
PY

run() { # run <label> <args...>
  local label=$1; shift
  local out rc
  out=$(python3 "$P" --root "$REPO" --rev HEAD "$@" 2>&1); rc=$?
  echo "### $label (rc=$rc)"
  echo "$out" | grep -E "^CITATION_DRIFT: |^CITATION_DRIFT_VERDICT" | tail -2
  echo
}

{
echo "### SC-4 verify-failclosed at $(date -Is)"
echo "### variant source: EX-21 probe.py + fail-closed unpinned branch"
sha256sum "$P"
echo
run "F1 pinned + real table (want 0/findings=0)" \
  --table "$G/pointer-table.json" --expected "$S/scratch/expected-pinned.json"
run "F2 pinned + weakened table (want 2/pointer_table_tampered)" \
  --table "$S/scratch/table-weakened.json" --expected "$S/scratch/expected-pinned.json"
run "F3 ATTACK unpinned expected + weakened table (want 2/table_pin_absent)" \
  --table "$S/scratch/table-weakened.json" --expected "$S/scratch/expected-unpinned.json"
run "F4 unpinned expected + real table (want 2/table_pin_absent)" \
  --table "$G/pointer-table.json" --expected "$S/scratch/expected-unpinned.json"
run "F5 absent table (want 2/pointer_table_unreadable)" \
  --table "$S/scratch/does-not-exist.json" --expected "$S/scratch/expected-pinned.json"
echo "### F6 selftest with EX-21's case table as it stands (pristine 11-case copy)"
out=$(python3 "$P" --selftest --expected "$EX21/expected.json" 2>&1); rc=$?
echo "$out" | tail -1
echo "rc=$rc"
echo
echo "### F6b selftest with the 13-case table SC-4 derives from EX-21's design"
echo "### (pristine table + case table_tampered/exit 2/pointer_table_tampered"
echo "###  + case table_absent/exit 2/pointer_table_unreadable; EX-21's own"
echo "###  13-case expected.json was overwritten by its 07:07 re-run)"
python3 - "$EX21/expected.json" "$S/scratch/expected-13.json" <<'PY'
import json,sys
e=json.load(open(sys.argv[1]))
e["selftest"]=e["selftest"]+[
 {"case":"table_tampered","exit_code":2,"finding":"pointer_table_tampered"},
 {"case":"table_absent","exit_code":2,"finding":"pointer_table_unreadable"}]
json.dump(e,open(sys.argv[2],"w"))
print("case_count=%d" % len(e["selftest"]))
PY
out=$(python3 "$P" --selftest --expected "$S/scratch/expected-13.json" 2>&1); rc=$?
echo "$out" | grep -E "SELFTEST_CASE: (CLEAN|FAILED) case=table_" 
echo "$out" | tail -1
echo "rc=$rc"
} > "$OUT" 2>&1
echo "wrote $OUT"
