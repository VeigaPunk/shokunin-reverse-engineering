#!/usr/bin/env bash
# RV-5 extra cells: content-vs-path, stale pin, absent expected.json.
# Usage: cells-extra.sh <gate-dir> <label-prefix>
set -u
S=$(cd "$(dirname "$0")" && pwd)
. "$S/mutation-harness.sh"
GATEDIR=$1; PF=$2
P=$GATEDIR/probe.py; E=$GATEDIR/expected.json; T=$GATEDIR/pointer-table.json
echo "### $PF extra cells (probe=$(sha256sum "$P" | cut -c1-16) exp=$(sha256sum "$E" | cut -c1-16))"
run $PF-identical-copy "$P" "$E" "$S/fixtures/table-identical-copy.json"
run $PF-stale-pin-honest-table "$P" "$S/fixtures/expected-stale-pin.json" "$T"
run $PF-no-expected "$P" "$S/fixtures/no-such-expected.json" "$T"
