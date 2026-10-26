#!/usr/bin/env bash
# usage: run_rea.sh <name> <input> <depth|-> <arm: after|before> [extra args...]
set -u
S=/fast/scratch/hyaku/kaidoku-r42/R42C2ReconCombo
cd "$S" || exit 9
export TMPDIR="$S" HYAKU_SCRATCH=/fast/scratch/hyaku
NAME=$1; INPUT=$2; DEPTH=$3; ARM=$4; shift 4
OUT="$S/rea/out/$NAME"
rm -rf "$OUT" "$S/rea/logs/$NAME"; mkdir -p "$S/rea/logs/$NAME"
export REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob
if [ "$ARM" = before ]; then
  HOME_BIN=$(realpath "$HOME/.local/bin")
  KEPT=$(printf '%s' "$PATH" | tr ':' '\n' | grep -v "^$HOME_BIN$" | paste -sd:)
  export PATH="$KEPT"
fi
DEP_ARGS=()
if [ "$DEPTH" != - ]; then DEP_ARGS=(--max-depth "$DEPTH"); fi
set +e
npx -y rea-agents@6.5.0 extract-firmware --format json --full-output "${DEP_ARGS[@]}" "$INPUT" "$OUT" > "$S/rea/logs/$NAME/stdout.json" 2> "$S/rea/logs/$NAME/stderr.log"
RC=$?
set -e
echo "$RC" > "$S/rea/logs/$NAME/exitcode"
echo "name=$NAME input=$INPUT depth=${DEPTH:-default} arm=$ARM rc=$RC"
