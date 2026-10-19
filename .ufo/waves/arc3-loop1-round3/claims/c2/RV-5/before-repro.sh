#!/bin/bash
[ -z "$3" ] && { echo "need <tool> <outdir> <tag>"; exit 9; }
# RV-5 before-state reproduction battery — measure the four named defects on the
# tool revision present in the tree at run time. Scratch-local; custody paths are
# never touched except read-only (none here).
# usage: before-repro.sh <tool-path> <outdir> <tag>
TOOL="$1"; OUT="$2"; TAG="$3"
S="/var/tmp/rv5/scratch/$TAG"
rm -rf "$S"; mkdir -p "$S" "$OUT"
export PYTHONDONTWRITEBYTECODE=1
PY=python3

run() {  # run <name> <cmd...>
  local name="$1"; shift
  echo "### $name" | tee -a "$OUT/run.log"
  echo "\$ $*" | tee -a "$OUT/run.log"
  { "$PY" "$TOOL" "$@"; echo "exit=$?"; } >>"$OUT/run.log" 2>&1
  echo "---" | tee -a "$OUT/run.log"
}

echo "tool=$TOOL" | tee "$OUT/run.log"
sha256sum "$TOOL" >>"$OUT/run.log"
echo "tag=$TAG date=$(date -Is)" >>"$OUT/run.log"

# --- D2a: exists-but-EACCES parent dir -> exists=no + STAT-ERROR, then fail-open MATCH
mkdir -p "$S/eacces-dir"
printf 'custody fixture\n' >"$S/eacces-dir/inner.conf"
printf 'control\n' >"$S/control.conf"
chmod 000 "$S/eacces-dir"
run D2a-capture capture --out "$S/d2a-cap.txt" --paths "$S/eacces-dir/inner.conf" --label d2a
run D2a-verify-live verify "$S/d2a-cap.txt" --live
run D2a-verify-two-receipts verify "$S/d2a-cap.txt" "$S/d2a-cap.txt"
cat "$S/d2a-cap.txt" >>"$OUT/D2a-receipt.txt" 2>&1
chmod 755 "$S/eacces-dir"

# --- D2b: chmod-000 file (lstat ok, open EACCES) -> traceback on capture
printf 'unreadable\n' >"$S/unreadable.conf"
chmod 000 "$S/unreadable.conf"
run D2b-capture capture --out "$S/d2b-cap.txt" --paths "$S/unreadable.conf" --label d2b
run D2b-verify-live verify "$S/d2b-cap.txt" --live
chmod 644 "$S/unreadable.conf"

# --- D2c: readable receipt, candidate turned unreadable -> traceback on verify --live
printf 'readable-then-not\n' >"$S/toggle.conf"
run D2c-capture capture --out "$S/d2c-cap.txt" --paths "$S/toggle.conf" --label d2c
chmod 000 "$S/toggle.conf"
run D2c-verify-live verify "$S/d2c-cap.txt" --live
chmod 644 "$S/toggle.conf"

# --- D3: 1-of-5 reference verifies clean (partial-reference coverage)
run D3-capture-1of5 capture --out "$S/d3-one.txt" --paths "$S/control.conf" --label d3
run D3-verify-live verify "$S/d3-one.txt" --live
run D3-verify-require5 verify "$S/d3-one.txt" --live --require-paths 5

# --- write-guard scope: --out X --paths X clobbers X
printf 'precious measurement target\n' >"$S/self.conf"
sha256sum "$S/self.conf" >>"$OUT/run.log"
run guard-scope capture --out "$S/self.conf" --paths "$S/self.conf" --label guard
sha256sum "$S/self.conf" >>"$OUT/run.log"
head -3 "$S/self.conf" >>"$OUT/run.log" 2>&1
echo "=== run.log ends ===" >>"$OUT/run.log"

# --- D6: selftest --scratch <missing dir>
run D6-selftest-missing-scratch selftest --scratch "$S/does-not-exist"
run D6-selftest-existing-scratch selftest --scratch "$S"

exit 0