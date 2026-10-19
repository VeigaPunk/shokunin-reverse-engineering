#!/usr/bin/env bash
# RV-5: run the injection matrix against an arbitrary staged gate dir.
# Usage: cells-gate.sh <gate-dir> <label-prefix> [--revert]
#   <gate-dir> holds probe.py, expected.json, pointer-table.json
#   --revert swaps in the PRE-GUARD expected.json (the guard-off mutation)
set -u
S=$(cd "$(dirname "$0")" && pwd)
. "$S/mutation-harness.sh"
GATEDIR=$1; PF=$2; MODE=${3:-}
P=$GATEDIR/probe.py; T=$GATEDIR/pointer-table.json
if [ "$MODE" = "--revert" ]; then E=$SCRATCH/pre-gate/expected.json; PF="$PF-revert"; else E=$GATEDIR/expected.json; fi
echo "### $PF state probe=$(sha256sum "$P" | cut -c1-16) exp=$(sha256sum "$E" | cut -c1-16) table=$(sha256sum "$T" | cut -c1-16)"
run $PF-selftest "$P" "$E" "$T" --selftest
run $PF-clean "$P" "$E" "$T"
run $PF-clean-strict "$P" "$E" "$T" --strict
run $PF-tampered-emptied "$P" "$E" "$S/fixtures/table-emptied.json"
run $PF-tampered-emptied-strict "$P" "$E" "$S/fixtures/table-emptied.json" --strict
run $PF-tampered-space "$P" "$E" "$S/fixtures/table-space.json"
run $PF-tampered-weakened "$P" "$E" "$S/fixtures/table-weakened.json"
run $PF-absent "$P" "$E" "$S/fixtures/no-such-table.json"
REV=679af5d749f2fd48b9d543e3c99d348d5458f90f run $PF-frozenrev-real "$P" "$E" "$T"
REV=679af5d749f2fd48b9d543e3c99d348d5458f90f run $PF-frozenrev-emptied "$P" "$E" "$S/fixtures/table-emptied.json"
