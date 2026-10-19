#!/bin/bash
# VZ-4 C2 after-state suite — runs against a SCRATCH COPY of the tool under test
# plus the in-repo v1 receipt; never writes to a real target or a custody path
# except the tool's own read-only live capture.
# usage: c2-verify.sh <tool-path> <scratch-root> <out-file> [v1-receipt]
set -u
TOOL=$1; SCR=$2; OUT=$3
V1=${4:-}
PY=python3
mkdir -p "$SCR"
: > "$OUT"
say() { printf '%s\n' "$*" | tee -a "$OUT"; }
say "== VZ-4 C2 after-state suite =="
say "tool=$(sha256sum "$TOOL") lines=$(wc -l < "$TOOL") utc=$(date -u +%FT%TZ)"

say "-- selftest (expect cases>=17 passed==cases exit=0) --"
mkdir -p "$SCR/st"
o=$($PY "$TOOL" selftest --scratch "$SCR/st" 2>&1); rc=$?
printf 'exit=%d\n' "$rc" | tee -a "$OUT"
printf '%s\n' "$o" | tail -5 | tee -a "$OUT"
printf '%s\n' "$o" | grep -E '^SELFTEST_SUMMARY|^CUSTODY_PAIR_SELFTEST' | tee -a "$OUT" || true

say "-- live capture 5/5 with the tool under test (read-only over custody paths) --"
o=$($PY "$TOOL" capture --out "$SCR/vz4-after.json" --label "vz4-after-$(date -u +%FT%TZ)" 2>&1); rc=$?
printf 'exit=%d\n%s\n' "$rc" "$o" | tee -a "$OUT"

say "-- receipt self-pin: header tool sha256 vs computed --"
grep -iE '^#.*(tool|sha256).*' "$SCR/vz4-after.json" 2>/dev/null | head -8 | tee -a "$OUT" || true
computed=$(sha256sum "$TOOL" | cut -d' ' -f1)
say "computed tool sha256=$computed"
grep -q "$computed" "$SCR/vz4-after.json" 2>/dev/null && say "TOOL_SELF_PIN=YES" || say "TOOL_SELF_PIN=NO (or no header pin field)"

say "-- verify my capture against the live filesystem (expect MATCH 5/5 exit 0) --"
o=$($PY "$TOOL" verify "$SCR/vz4-after.json" --live 2>&1); rc=$?
printf 'exit=%d\n' "$rc" | tee -a "$OUT"
printf '%s\n' "$o" | grep -E 'VERDICT|CUSTODY_PAIR_VERIFY|SHA256-CONTRACT|drift' | tee -a "$OUT" || true

if [ -n "$V1" ]; then
  say "-- v1 canonical receipt (round-1 CU-1) vs live: field-level contract --"
  o=$($PY "$TOOL" verify "$V1" --live 2>&1); rc=$?
  printf 'exit=%d\n' "$rc" | tee -a "$OUT"
  printf '%s\n' "$o" | grep -E 'VERDICT|SHA256-CONTRACT|LABEL-DEFECT|v1' | head -12 | tee -a "$OUT" || true

  say "-- v1 sums-form receipt vs live (expect exit 0 + SHA256-CONTRACT) --"
  sums="$SCR/v1-sums.txt"
  : > "$sums"
  for p in $($PY "$TOOL" paths); do
    ep=$(eval echo "$p"); printf '%s  %s\n' "$(sha256sum "$ep" | cut -d' ' -f1)" "$ep" >> "$sums"
  done
  o=$($PY "$TOOL" verify "$sums" --live 2>&1); rc=$?
  printf 'exit=%d\n' "$rc" | tee -a "$OUT"
  printf '%s\n' "$o" | grep -E 'VERDICT|SHA256-CONTRACT|PARTIAL' | head -12 | tee -a "$OUT" || true
fi

say "-- injection suite (D2/D3/D6/write-guard) via c2-attacks.sh --"
bash "$(dirname "$0")/c2-attacks.sh" "$TOOL" "$SCR/atk" "$SCR/atk.txt" >>"$OUT" 2>&1
say "injection summary:"
grep -E '^CASE|clobbered=' "$SCR/atk.txt" | tee -a "$OUT" || true
say "== end $(date -u +%FT%TZ) =="