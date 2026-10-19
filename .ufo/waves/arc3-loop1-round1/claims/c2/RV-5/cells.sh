#!/usr/bin/env bash
# RV-5 cells: build fixtures, then run the injection matrix for a given state.
# Usage: cells.sh pre | post | revert   (post/revert need EX-16's landed gate)
set -u
S=$(cd "$(dirname "$0")" && pwd)
. "$S/mutation-harness.sh"
REPO=${REPO:-/home/vgpnk/Projects/shokunin/kaidoku-shokunin}
GATE=$REPO/.ufo/gates/citation-drift
SCRATCH=${SCRATCH:-/home/vgpnk/.cache/kaidoku-rv5-arc3r1}

# ---- fixtures (built from the real table bytes) ---------------------------
python3 - "$GATE/pointer-table.json" "$S/fixtures" <<'PY'
import json, sys
src, outdir = sys.argv[1], sys.argv[2]
raw = open(src, "rb").read()
d = json.loads(raw)
e = dict(d); e["entries"] = []; e["quoted"] = []
json.dump(e, open(outdir + "/table-emptied.json", "w"))
w = json.loads(raw)
for row in w.get("entries", []) + w.get("quoted", []):
    row["must_match"] = ".*"
json.dump(w, open(outdir + "/table-weakened.json", "w"))
open(outdir + "/table-space.json", "wb").write(raw + b" ")
PY
cp -a "$GATE/expected.json" "$S/fixtures/expected-pre.json" 2>/dev/null || true
sha256sum "$GATE/pointer-table.json" "$GATE/expected.json" "$GATE/citation-drift-probe.py" \
  > "$S/logs/provenance-$(date -u +%Y%m%dT%H%M%SZ).txt"

case "${1:-}" in
pre)
  P=$SCRATCH/pre-gate/citation-drift-probe.py; E=$SCRATCH/pre-gate/expected.json
  echo "### PRE state (HEAD gate dir; no pin) probe=$(sha256sum $P | cut -c1-16)"
  run pre-selftest "$P" "$E" "$SCRATCH/pre-gate/pointer-table.json" --selftest
  run pre-clean "$P" "$E" "$SCRATCH/pre-gate/pointer-table.json"
  run pre-clean-strict "$P" "$E" "$SCRATCH/pre-gate/pointer-table.json" --strict
  run pre-tampered-emptied "$P" "$E" "$S/fixtures/table-emptied.json"
  run pre-tampered-emptied-strict "$P" "$E" "$S/fixtures/table-emptied.json" --strict
  run pre-tampered-space "$P" "$E" "$S/fixtures/table-space.json"
  run pre-tampered-weakened "$P" "$E" "$S/fixtures/table-weakened.json"
  run pre-absent "$P" "$E" "$S/fixtures/no-such-table.json"
  REV=679af5d749f2fd48b9d543e3c99d348d5458f90f run pre-frozenrev-real "$P" "$E" "$SCRATCH/pre-gate/pointer-table.json"
  REV=679af5d749f2fd48b9d543e3c99d348d5458f90f run pre-frozenrev-emptied "$P" "$E" "$S/fixtures/table-emptied.json"
  ;;
post)
  P=$SCRATCH/post-gate/citation-drift-probe.py; E=$SCRATCH/post-gate/expected.json
  T=$SCRATCH/post-gate/pointer-table.json
  echo "### POST state (EX-16 landed) probe=$(sha256sum $P | cut -c1-16) exp=$(sha256sum $E | cut -c1-16)"
  run post-selftest "$P" "$E" "$T" --selftest
  run post-clean "$P" "$E" "$T"
  run post-clean-strict "$P" "$E" "$T" --strict
  run post-tampered-emptied "$P" "$E" "$S/fixtures/table-emptied.json"
  run post-tampered-emptied-strict "$P" "$E" "$S/fixtures/table-emptied.json" --strict
  run post-tampered-space "$P" "$E" "$S/fixtures/table-space.json"
  run post-tampered-weakened "$P" "$E" "$S/fixtures/table-weakened.json"
  run post-absent "$P" "$E" "$S/fixtures/no-such-table.json"
  run post-copy-same-bytes "$P" "$E" "$S/fixtures/table-identical-copy.json"
  run post-stale-pin-honest-table "$P" "$S/fixtures/expected-stale-pin.json" "$T"
  run post-no-expected "$P" "$S/fixtures/no-such-expected.json" "$T"
  REV=679af5d749f2fd48b9d543e3c99d348d5458f90f run post-frozenrev-real "$P" "$E" "$T"
  REV=679af5d749f2fd48b9d543e3c99d348d5458f90f run post-frozenrev-emptied "$P" "$E" "$S/fixtures/table-emptied.json"
  ;;
revert)
  P=$SCRATCH/post-gate/citation-drift-probe.py; E=$SCRATCH/pre-gate/expected.json
  T=$SCRATCH/post-gate/pointer-table.json
  echo "### REVERT state (post-guard probe + PRE-GUARD expected.json) probe=$(sha256sum $P | cut -c1-16) exp=$(sha256sum $E | cut -c1-16)"
  run revert-selftest "$P" "$E" "$T" --selftest
  run revert-clean "$P" "$E" "$T"
  run revert-tampered-emptied "$P" "$E" "$S/fixtures/table-emptied.json"
  run revert-tampered-emptied-strict "$P" "$E" "$S/fixtures/table-emptied.json" --strict
  run revert-tampered-space "$P" "$E" "$S/fixtures/table-space.json"
  run revert-tampered-weakened "$P" "$E" "$S/fixtures/table-weakened.json"
  run revert-absent "$P" "$E" "$S/fixtures/no-such-table.json"
  REV=679af5d749f2fd48b9d543e3c99d348d5458f90f run revert-frozenrev-emptied "$P" "$E" "$S/fixtures/table-emptied.json"
  ;;
*) echo "usage: cells.sh pre|post|revert" >&2; exit 2;;
esac
