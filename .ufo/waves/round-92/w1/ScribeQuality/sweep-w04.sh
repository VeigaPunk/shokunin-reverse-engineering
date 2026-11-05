#!/usr/bin/env bash
# Sweep for QUALITY 187: every "N W04" figure a report states must equal the
# W04 line count of the census receipt it cites.
# usage: sweep-w04.sh <report.md> <receipt.txt>
# exit 0 = every figure agrees; exit 1 = a figure disagrees; exit 2 = nothing
# checked (missing input, or no "N W04" figure in the report).
set -u
[ $# -eq 2 ] || { echo "usage: $0 <report.md> <receipt.txt>" >&2; exit 2; }
report=$1
receipt=$2
[ -f "$report" ] || { echo "no such report: $report" >&2; exit 2; }
[ -f "$receipt" ] || { echo "no such receipt: $receipt" >&2; exit 2; }
actual=$(grep -cP '\tW04\t' -- "$receipt")
claims=$(grep -oP '\b[0-9]+(?= W04)' -- "$report" | sort -un)
[ -n "$claims" ] || { echo "no 'N W04' figure in $report: nothing checked"; exit 2; }
rc=0
while read -r n; do
  if [ "$n" -eq "$actual" ]; then
    echo "agree: report $n == receipt $actual ($receipt)"
  else
    echo "DISAGREE: report $n != receipt $actual ($receipt)"
    rc=1
  fi
done <<< "$claims"
exit $rc
