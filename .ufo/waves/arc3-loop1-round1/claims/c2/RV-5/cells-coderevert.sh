#!/usr/bin/env bash
# RV-5 code-revert mutation: pre-guard PROBE + landed expected.json (pin present,
# guard code absent). Isolates the two halves of the fix:
#   - pin alone (data) with no guard code  -> do the injections stay silent?
#   - does the landed selftest catch the missing guard code?
set -u
S=$(cd "$(dirname "$0")" && pwd)
. "$S/mutation-harness.sh"
P=$SCRATCH/pre-gate/probe.py; E=$SCRATCH/post-gate/expected.json; T=$SCRATCH/post-gate/pointer-table.json
echo "### code-revert state probe=$(sha256sum "$P" | cut -c1-16) exp=$(sha256sum "$E" | cut -c1-16)"
run code-revert-selftest "$P" "$E" "$T" --selftest
run code-revert-clean "$P" "$E" "$T"
run code-revert-tampered-emptied "$P" "$E" "$S/fixtures/table-emptied.json"
run code-revert-tampered-emptied-strict "$P" "$E" "$S/fixtures/table-emptied.json" --strict
run code-revert-absent "$P" "$E" "$S/fixtures/no-such-table.json"
REV=679af5d749f2fd48b9d543e3c99d348d5458f90f run code-revert-frozenrev-emptied "$P" "$E" "$S/fixtures/table-emptied.json"
