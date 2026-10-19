#!/usr/bin/env bash
# RV-7 mutation matrix: run the harness over a tool revision plus its reverts.
# usage: run-matrix.sh <tool-path> <label>
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
TOOL=$1; LABEL=$2
RUNROOT=/dev/shm/rv7/runs
mkdir -p "$RUNROOT"
for spec in clean M1-guard-revert M1a-scoped-arm-revert M1b-inode-arm-revert M2-coverage-revert; do
  tag="$LABEL-$spec"
  if [ "$spec" = clean ]; then
    python3 "$HERE/mutants.py" --tool "$TOOL" --root "$RUNROOT" --tag "$tag" \
      --note "landed revision, unmutated" --out "$HERE/$tag.json" > "$RUNROOT/$tag.log" 2>&1 \
      || { echo "RUN FAILED: $tag"; tail -5 "$RUNROOT/$tag.log"; }
  else
    python3 "$HERE/mutants.py" --tool "$TOOL" --root "$RUNROOT" --tag "$tag" \
      --note "revert spec $spec" --mutate-spec "$HERE/specs/$spec.json" --out "$HERE/$tag.json" \
      > "$RUNROOT/$tag.log" 2>&1 \
      || { echo "RUN FAILED: $tag"; tail -5 "$RUNROOT/$tag.log"; }
  fi
done
echo "matrix done: $LABEL  $(date -u +%H:%M:%SZ)"
ls -1 "$HERE/$LABEL"-*.json | wc -l