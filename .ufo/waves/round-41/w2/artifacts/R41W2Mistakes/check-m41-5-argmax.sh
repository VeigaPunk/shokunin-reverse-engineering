#!/usr/bin/env bash
# M41-5 check (R41W2Mistakes): c1-run.sh passes the envelope-data summary to
# jq through `--argjson summary "$summary"`, i.e. as ONE argv string.  Linux
# caps a single argument string at MAX_ARG_STRLEN = 32 * PAGE_SIZE = 131072
# bytes; anything longer fails execve with E2BIG ("Argument list too long")
# even though the total ARG_MAX here is 2097152.
#
# The real V4 summary (computed from the committed V4 after.json) is 146561
# bytes -- over the cap -- which is why the V4 run wrote after.json but died
# before writing run.json (run-harness-failure.log).
#
# RED: the exact harness pattern (receipt jq, c1-run.sh lines 543-547) on a
#   summary over the cap -> exit 126, "Argument list too long".
# GREEN: same data via `--slurpfile` (the R41-CL2 fix) -> exit 0.
#
# usage: check-m41-5-argmax.sh <summary.json>
#   <summary.json> is a JSON value whose compact serialization exceeds 131072 B.
set -u
JQ=${JQ:-$HOME/.local/bin/jq}
SUMMARY=${1:?need a summary.json path}
SZ=$(stat -c %s "$SUMMARY")
echo "summary bytes: $SZ (per-arg cap 131072)"

summary=$(cat "$SUMMARY")

# --- RED: harness receipt-jq pattern (c1-run.sh lines 543-547) --------------
receipt=$("$JQ" -n \
  --arg sha "0000000000000000000000000000000000000000000000000000000000000000" \
  --argjson bytes "$SZ" \
  --argjson summary "$summary" \
  '{path: "after.json", sha256: $sha, bytes: $bytes} + $summary' 2>red.err)
rc=$?
echo "RED  harness --argjson pattern rc=$rc stderr=$(head -c 80 red.err)"
[ "$rc" -ne 0 ] || { echo "RED FAILED (expected non-zero)"; exit 1; }

# --- GREEN: fix as routed R41-CL2 (--slurpfile) ----------------------------
receipt=$("$JQ" -n \
  --arg sha "0000000000000000000000000000000000000000000000000000000000000000" \
  --argjson bytes "$SZ" \
  --slurpfile summary "$SUMMARY" \
  '{path: "after.json", sha256: $sha, bytes: $bytes} + $summary[0]' 2>green.err)
rc=$?
echo "GREEN --slurpfile pattern rc=$rc"
[ "$rc" -eq 0 ] || { echo "GREEN FAILED (expected 0)"; exit 1; }

echo "check-m41-5: RED confirmed on mistaken pattern, GREEN confirmed on repair"
exit 0
