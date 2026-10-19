#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"
SRC="$SCRIPT_DIR/source/K8.vy"
VYPER="$ROOT/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper"
REA="$HOME/.npm/_npx/9b9809298fe40d2c/node_modules/rea-agents/scripts/rea.mjs"
JS_SHA3="$ROOT/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/js-sha3"
SCRATCH="$(mktemp -d /var/tmp/kaidoku-cr1-r10.XXXXXX)"
trap 'rm -rf "$SCRATCH"' EXIT
mkdir -p "$SCRATCH/tmp" "$SCRIPT_DIR/compiled" "$SCRIPT_DIR/probe"
export TMPDIR="$SCRATCH/tmp"

VYPER_VERSION="$("$VYPER" --version)"
REA_VERSION="$(node "$REA" --version)"
JS_SHA3_VERSION="$(node -e 'process.stdout.write(require(process.argv[1] + "/package.json").version)' "$JS_SHA3")"
test "$VYPER_VERSION" = "0.4.3+commit.bff19ea2"
test "$REA_VERSION" = "6.7.0"
test "$JS_SHA3_VERSION" = "0.8.0"
test "$(sha256sum "$SRC" | cut -d ' ' -f 1)" = "62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d"

{
  printf 'scratch=%s (removed on exit)\nTMPDIR=%s\n' "$SCRATCH" "$TMPDIR"
  printf 'source=%s\n' "$SRC"
  sha256sum "$SRC"
  printf 'compiler=%s\n' "$VYPER_VERSION"
  sha256sum "$VYPER"
  printf 'rea-agents=%s\n' "$REA_VERSION"
  sha256sum "$REA"
  printf 'js-sha3=%s\n' "$JS_SHA3_VERSION"
  sha256sum "$JS_SHA3/package.json"
  printf 'compile-form=vyper --evm-version FORK -f FORMAT %s\n' "$SRC"
  printf 'probe-form=node %s inspect-evm-interface COMPILED_RUNTIME hex --format json\n' "$REA"
} > "$SCRIPT_DIR/reproduction.txt"

for fork in paris prague; do
  mkdir -p "$SCRATCH/$fork-first" "$SCRATCH/$fork-second"
  for pass in first second; do
    OUT="$SCRATCH/$fork-$pass"
    for format in bytecode_runtime abi method_identifiers opcodes_runtime settings; do
      case "$format" in
        bytecode_runtime) name=runtime.hex ;;
        abi) name=abi.json ;;
        method_identifiers) name=method-identifiers.json ;;
        opcodes_runtime) name=runtime.opcodes.txt ;;
        settings) name=settings.json ;;
      esac
      "$VYPER" --evm-version "$fork" -f "$format" "$SRC" > "$OUT/$name"
    done
  done
  for name in runtime.hex abi.json method-identifiers.json runtime.opcodes.txt settings.json; do
    cmp "$SCRATCH/$fork-first/$name" "$SCRATCH/$fork-second/$name"
    cp "$SCRATCH/$fork-first/$name" "$SCRIPT_DIR/compiled/$fork.$name"
  done
  node "$REA" inspect-evm-interface "$SCRIPT_DIR/compiled/$fork.runtime.hex" hex --format json > "$SCRIPT_DIR/probe/$fork.rea.json"
done

python3 "$SCRIPT_DIR/measure.py" > "$SCRIPT_DIR/measurement.txt"
printf 'compile_reruns=PARIS byte-identical (5/5 outputs); PRAGUE byte-identical (5/5 outputs)\n' >> "$SCRIPT_DIR/reproduction.txt"
printf 'scratch_usage=all compiler and REA scratch under /var/tmp; removed on exit\n' >> "$SCRIPT_DIR/reproduction.txt"
