#!/usr/bin/env bash
# RV-5 seat harness: mutation-test the citation-drift frozen-run guard.
#
# Question: is the guard load-bearing? Method: run the two injections
# (tampered table, absent table) against three states of the gate:
#   pre    = HEAD gate dir (no pin in expected.json, pre-guard probe)
#   post   = EX-16's landed gate dir (pin + guard in probe)
#   revert = post-guard probe + PRE-GUARD expected.json  (the mutation:
#            restoring the pre-guard expected.json must disable the guard)
# A guard is load-bearing iff the injections pass silently in `revert`
# while reading could-not-evaluate in `post`.
#
# Read-only over the real repo: --root is the real work tree (git objects
# only). All mutated inputs live in this artifact dir. TMPDIR is redirected
# because /tmp hit the vgpnk user quota this wave (EDQUOT at 37KB).
set -u
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
GATE=$REPO/.ufo/gates/citation-drift
S=$(cd "$(dirname "$0")" && pwd)
SCRATCH=${SCRATCH:-/home/vgpnk/.cache/kaidoku-rv5-arc3r1}
export TMPDIR=$SCRATCH/tmp
mkdir -p "$TMPDIR" "$S/logs" "$S/fixtures" "$SCRATCH/pre-gate" "$SCRATCH/post-gate"

run() { # run <label> <probe> <expected> <table> [extra args...]
  local label=$1 probe=$2 exp=$3 table=$4; shift 4
  local out rc last
  out=$(python3 "$probe" --root "$REPO" --rev "${REV:-HEAD}" --table "$table" \
        --expected "$exp" "$@" 2>&1)
  rc=$?
  last=$(echo "$out" | tail -1)
  printf '%s\n' "$out" > "$S/logs/$label.txt"
  echo "exit=$rc" >> "$S/logs/$label.txt"
  echo "[$label] rc=$rc | $last"
}
