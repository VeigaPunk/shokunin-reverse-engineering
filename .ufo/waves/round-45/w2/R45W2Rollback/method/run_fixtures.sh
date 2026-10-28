#!/bin/bash
# Fixture probes for block 22 rows 6 and 10, plus the row-count floor.
set -u
S=/fast/scratch/hyaku/kaidoku-r45/R45W2Rollback
export TMPDIR="$S" HYAKU_SCRATCH="$S/counterscratch"
mkdir -p "$S/receipts" "$S/counterscratch"
C="$S/clone"; cd "$C" || exit 9
[ "$(git rev-parse --show-toplevel)" = "$C" ] || { echo REFUSING; exit 9; }
PRE="$C/tools/round-45/frozen-path-preflight.py"

receipt() {
  local name=$1; shift
  local out="$S/receipts/$name.out" err="$S/receipts/$name.err"
  local utc; utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  "$@" >"$out" 2>"$err"; local rc=$?
  printf 'name=%s\nutc=%s\ncmd=' "$name" "$utc" >"$S/receipts/$name.receipt"
  printf '%q ' "$@" >>"$S/receipts/$name.receipt"
  printf '\nexit=%s\nstdout_sha256=%s\nstderr_sha256=%s\nstdout_bytes=%s\n' \
    "$rc" "$(sha256sum "$out" | cut -d' ' -f1)" "$(sha256sum "$err" | cut -d' ' -f1)" \
    "$(wc -c <"$out")" >>"$S/receipts/$name.receipt"
  echo "[$name] exit=$rc"
}

# --- fixture A: FREEZE == REV with the frozen worktree dirty (row 10) ----------
A="$S/fx-empty-dirty"; rm -rf "$A"; mkdir -p "$A"
git -C "$A" init -q
[ "$(git -C "$A" rev-parse --show-toplevel)" = "$A" ] || { echo "REFUSING fx A"; exit 9; }
git -C "$A" config user.email fx@scratch; git -C "$A" config user.name fx
mkdir -p "$A/frozen"; printf 'alpha\n' >"$A/frozen/a.txt"
git -C "$A" add -A; git -C "$A" commit -q -m freeze
printf 'dirty\n' >"$A/frozen/a.txt"
receipt preflight-empty-range-dirty python3 -I -B "$PRE" --root "$A" \
  --freeze HEAD --rev HEAD --pathspec frozen/ --freeze-path frozen --require-pathspec --check-dirty \
  --json-out "$S/receipts/preflight-empty-range-dirty.json"

# --- fixture B: the M45-1 bulk sweep (row 6) ----------------------------------
B="$S/fx-sweep"; rm -rf "$B"; mkdir -p "$B"
git -C "$B" init -q
[ "$(git -C "$B" rev-parse --show-toplevel)" = "$B" ] || { echo "REFUSING fx B"; exit 9; }
git -C "$B" config user.email fx@scratch; git -C "$B" config user.name fx
mkdir -p "$B/frozen"; printf 'alpha\n' >"$B/frozen/a.txt"
git -C "$B" add -A; git -C "$B" commit -q -m freeze; FB=$(git -C "$B" rev-parse HEAD)
mkdir -p "$B/frozen/control-fixtures"
for i in 0 1 2 3 4 5 6 7; do printf '%s\n' "$i" >"$B/frozen/control-fixtures/c$i.json"; done
printf 'swept\n' >"$B/outside.txt"
git -C "$B" add -A; git -C "$B" commit -q -m sweep; RB=$(git -C "$B" rev-parse HEAD)
receipt preflight-bulk-sweep python3 -I -B "$PRE" --root "$B" \
  --freeze "$FB" --rev "$RB" --pathspec frozen/ --freeze-path frozen --require-pathspec \
  --json-out "$S/receipts/preflight-bulk-sweep.json"

# --- fixture C: the selftest itself (11 cases) --------------------------------
receipt preflight-selftest python3 -I -B "$PRE" --selftest
