#!/usr/bin/env bash
# EX-04 (arc3-loop1-round4, C1) — compile CarrierV.vy with the wave venv's vyper
# and capture bytecode + abi + runtime, with sha256s.
#
#   usage: compile-carrier.sh <venv-dir> <work-dir>
#
# Writes into <work-dir>: creation.hex, creation.bin, abi.json, runtime.hex,
# runtime.bin, opcodes.txt, method-identifiers.json, metadata.json, combined.txt
# (the literal `vyper -f bytecode,abi` capture), compile-receipt.txt.
set -u
VENV="$1"; WORK="$2"
VYPER="$VENV/bin/vyper"
SRC="$(cd "$(dirname "$0")" && pwd)/../src/CarrierV.vy"
mkdir -p "$WORK"

{
  echo "seat: EX-04  chain: c1  wave: arc3-loop1-round4"
  echo "recorded_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "host: $(uname -srmo)"
  echo "venv: $VENV"
  echo "vyper_path: $VYPER"
  echo "vyper_version: $("$VYPER" --version 2>&1)"
  echo "vyper_sha256: $(sha256sum "$(readlink -f "$VYPER")" | awk '{print $1}')"
  echo "python_in_venv: $("$VENV/bin/python" -V 2>&1)"
  echo "python_sha256: $(sha256sum "$(readlink -f "$VENV/bin/python")" | awk '{print $1}')"
  echo "source: $SRC"
  echo "source_sha256: $(sha256sum "$SRC" | awk '{print $1}')"
} > "$WORK/compile-receipt.txt"

# --- the literal command the seat task names: `vyper -f bytecode,abi` --------
"$VYPER" -f bytecode,abi "$SRC" > "$WORK/combined.txt" 2> "$WORK/combined.err"
echo "combined_exit=$?" >> "$WORK/compile-receipt.txt"

# --- the same outputs, one format per invocation (machine-parseable) --------
"$VYPER" -f bytecode          "$SRC" > "$WORK/creation.raw.txt" 2>&1 || exit 11
"$VYPER" -f bytecode_runtime  "$SRC" > "$WORK/runtime.raw.txt"  2>&1 || exit 12
"$VYPER" -f abi               "$SRC" > "$WORK/abi.json"        2>&1 || exit 13
"$VYPER" -f method_identifiers "$SRC" > "$WORK/method-identifiers.json" 2>&1 || exit 14
"$VYPER" -f opcodes_runtime   "$SRC" > "$WORK/opcodes.txt"     2>&1 || exit 15
"$VYPER" -f metadata          "$SRC" > "$WORK/metadata.json"   2>&1 || exit 16

strip0x() { sed -e 's/^0x//' -e '/^$/d' "$1" | tr -d '\n'; }
strip0x "$WORK/creation.raw.txt" > "$WORK/creation.hex"
strip0x "$WORK/runtime.raw.txt"  > "$WORK/runtime.hex"
printf '%s' "$(cat "$WORK/creation.hex")" | xxd -r -p > "$WORK/creation.bin"
printf '%s' "$(cat "$WORK/runtime.hex")"  | xxd -r -p > "$WORK/runtime.bin"

{
  echo "creation_bytes: $(stat -c%s "$WORK/creation.bin")"
  echo "runtime_bytes: $(stat -c%s "$WORK/runtime.bin")"
  for f in creation.hex creation.bin runtime.hex runtime.bin abi.json \
           method-identifiers.json metadata.json opcodes.txt combined.txt; do
    echo "$f sha256: $(sha256sum "$WORK/$f" | awk '{print $1}')"
  done
} >> "$WORK/compile-receipt.txt"
cat "$WORK/compile-receipt.txt"
