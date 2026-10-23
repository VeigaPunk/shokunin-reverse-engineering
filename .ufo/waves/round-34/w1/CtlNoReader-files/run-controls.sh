#!/usr/bin/env bash
# CtlNoReader: bounded control run harness (consolidated final pass).
#
# Runs the FROZEN counter (tools/round-34/version-needs-counter.py, unmodified,
# at the frozen revision) with --control-reader against each adversarial
# no-reader control, capturing exact argv, UTC timestamps, stdout, stderr and
# exit code into per-control receipt files.
#
# The production reader tools/round-34/elf-version-needs.py is NEVER executed:
# every invocation passes --control-reader, so the counter never loads it.
#
# All runs are bounded by timeout(1).
set -u

SANDBOX=/fast/scratch/hyaku/kaidoku-r34/w1/CtlNoReader
FREEZE=54a87a51a865ab931fd355e767303337b05cccf4
SEATDIR="$SANDBOX/.ufo/waves/round-34/w1/CtlNoReader-files"
COUNTER="$SANDBOX/tools/round-34/version-needs-counter.py"

unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE

run_control () {
  local name="$1"
  local reader="$2"
  local out="$SEATDIR/receipt-${name}.json"
  local meta="$SEATDIR/receipt-${name}.meta"
  local started ended
  started=$(date -u +%Y-%m-%dT%H:%M:%S.%NZ)
  local argv=("python3" "$COUNTER" "--root" "$SANDBOX" "--rev" "$FREEZE" "--freeze" "$FREEZE" "--control-reader" "$reader")
  timeout 180 "${argv[@]}" >"$out" 2>"$SEATDIR/receipt-${name}.stderr"
  local code=$?
  ended=$(date -u +%Y-%m-%dT%H:%M:%S.%NZ)
  {
    echo "name=${name}"
    echo "argv=${argv[*]}"
    echo "started_utc=${started}"
    echo "ended_utc=${ended}"
    echo "exit_code=${code}"
    echo "reader_sha256=$(sha256sum "$reader" | cut -d' ' -f1)"
    echo "counter_sha256=$(sha256sum "$COUNTER" | cut -d' ' -f1)"
    echo "stdout_sha256=$(sha256sum "$out" | cut -d' ' -f1)"
    echo "stderr_bytes=$(wc -c <"$SEATDIR/receipt-${name}.stderr")"
  } >"$meta"
  echo "== ${name} exit=${code}"
}

run_control constant-e01 "$SEATDIR/control-reader-constant-e01.py"
run_control constant-empty "$SEATDIR/control-reader-constant-empty.py"
run_control plausible-synthetic "$SEATDIR/control-reader-plausible-synthetic.py"
run_control oracle-by-size "$SEATDIR/control-reader-oracle-by-size.py"
run_control oracle-root-discovered "$SEATDIR/control-reader-oracle-root-discovered.py"
