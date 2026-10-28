#!/usr/bin/env bash
# R49-C1 run harness (kaidoku round 49; the AFTER-freeze data procedure).
#
# Thin wrapper around c1-run.py: it resolves the lane root, pins the child
# PATH and the scratch base, and refuses to run the data procedure into the
# committed evidence root unless the caller states that the freeze is in
# place. The receipt work is done by the Python sibling (same directory), which
# the L1 installs next to this script under tools/round-49/.
#
#   c1-run.sh --dry-run            print the commands that would run; write nothing
#   c1-run.sh [--data-run] ...     run the procedure (after the freeze)
#
# The L1 runs this AFTER the freeze; seats never run it (a pre-freeze receipt
# breaks the counter's receipt_fresh binding). The guard below is the second
# line of that defence - the first is that the receipt is only a receipt once
# it is committed after the freeze.
#
# Usage:
#   c1-run.sh [--lane-root DIR] [--carriers FILE] [--evidence-root DIR]
#              [--scratch BASE] [--carrier ID]... [--timeout SEC]
#              [--freeze REV] [--dry-run] [--data-run] [--keep-scratch]
#              [--force] [--no-unblob-log-tee]
#
# env:
#   HYAKU_SCRATCH        scratch base (default /fast/scratch/hyaku); the runner
#                        appends /kaidoku-r49
#   KAIDOKU_C1_DATA_RUN  set to 1 to assert that the freeze is in place
#   C1_UNBLOB_LOG_TEE    set to 0 to run unblob without the log tee
#
# Exit: 0 every carrier produced a receipt, 1 at least one carrier failed,
#       2 could not evaluate (usage/environment error).
set -euo pipefail

PROG=$(basename "$0")
SCRIPT_DIR=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd -P)

err() { echo "$PROG: $*" >&2; exit 2; }

# The Python sibling lives next to this script once the L1 installs both under
# tools/round-49/. Allow an override for a development run from the artifacts
# directory.
PY_TOOL=${C1_RUN_PY:-$SCRIPT_DIR/c1-run.py}
[[ -f $PY_TOOL ]] || err "c1-run.py not found next to this script: $PY_TOOL"\
"                     (set C1_RUN_PY to the installed tool)"
command -v python3 >/dev/null || err "python3 not found on PATH"

# The child PATH of the REA run. Identical to the round-42 counter's
# FIXED_PATH, so the extractor that resolves (`sasquatch`) is the same binary
# in the run and in the counter's own rerun.
FIXED_PATH="/usr/local/bin:/usr/bin:/bin:$HOME/.local/bin:$HOME/.local/share/fnm/node-versions/v24.21.0/installation/bin"
export PATH="$FIXED_PATH"
command -v npx >/dev/null || err "npx not found on the fixed PATH $FIXED_PATH"

exec python3 -I -B "$PY_TOOL" "$@"
