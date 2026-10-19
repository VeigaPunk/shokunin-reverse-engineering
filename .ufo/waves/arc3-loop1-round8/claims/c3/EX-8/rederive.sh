#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SEAT="$ROOT/.ufo/waves/arc3-loop1-round8/claims/c3/EX-8"
OUT="$SEAT/evidence"
SRC="$ROOT/.ufo/waves/arc3-loop1-round4/claims/c1/CR-1/vy/K8.vy"
VYPER="$ROOT/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper"
PYTHON="$ROOT/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/python"
RUN="$(mktemp -d /var/tmp/kaidoku-ex8-r8.XXXXXX)"

mkdir -p "$RUN/tmp" "$RUN/out" "$RUN/probe" "$OUT/compile" "$OUT/probe"
cp "$SRC" "$OUT/K8.vy"

{
  printf 'repo_head='
  git rev-parse HEAD
  printf 'source_path=%s\n' "$SRC"
  sha256sum "$SRC" "$OUT/K8.vy"
  printf 'compiler_path=%s\n' "$VYPER"
  sha256sum "$VYPER"
  "$VYPER" --version
  printf 'scratch=%s\n' "$RUN"
  printf 'TMPDIR=%s\n' "$RUN/tmp"
} > "$OUT/identity.txt"

for mode in gas noopt none codesize; do
  case "$mode" in
    gas) args=() ;;
    noopt) args=(--no-optimize) ;;
    none) args=(-O none) ;;
    codesize) args=(-O codesize) ;;
  esac
  for pass in 1 2; do
    env TMPDIR="$RUN/tmp" "$VYPER" "${args[@]}" -f bytecode_runtime "$OUT/K8.vy" > "$RUN/out/$mode.$pass.runtime.hex"
  done
  cmp "$RUN/out/$mode.1.runtime.hex" "$RUN/out/$mode.2.runtime.hex"
  cp "$RUN/out/$mode.1.runtime.hex" "$RUN/out/$mode.runtime.hex"
  env TMPDIR="$RUN/tmp" "$VYPER" "${args[@]}" -f abi "$OUT/K8.vy" > "$RUN/out/$mode.abi.json"
  env TMPDIR="$RUN/tmp" "$VYPER" "${args[@]}" -f method_identifiers "$OUT/K8.vy" > "$RUN/out/$mode.methodids.json"
  env TMPDIR="$RUN/tmp" "$VYPER" "${args[@]}" -f settings "$OUT/K8.vy" > "$RUN/out/$mode.settings.json"
done

env TMPDIR="$RUN/tmp" "$VYPER" -O gas -f bytecode_runtime "$OUT/K8.vy" > "$RUN/out/gas-explicit.runtime.hex"
cmp "$RUN/out/gas.runtime.hex" "$RUN/out/gas-explicit.runtime.hex"
cmp "$RUN/out/noopt.runtime.hex" "$RUN/out/none.runtime.hex"
cp "$RUN"/out/* "$OUT/compile/"

TMPDIR="$RUN/tmp" npx -y rea-agents@6.7.0 --version > "$OUT/rea-version.txt"
for mode in gas noopt codesize; do
  env TMPDIR="$RUN/tmp" npx -y rea-agents@6.7.0 inspect-evm-interface "$OUT/compile/$mode.runtime.hex" hex --format json > "$RUN/probe/$mode.json" 2> "$RUN/probe/$mode.stderr"
  cp "$RUN/probe/$mode.json" "$OUT/probe/$mode.json"
  cp "$RUN/probe/$mode.stderr" "$OUT/probe/$mode.stderr"
done

"$PYTHON" "$SEAT/measure.py" "$OUT/compile" "$OUT/probe" > "$OUT/measure.txt"

{
  printf 'measurement_utc='
  date -u +%Y-%m-%dT%H:%M:%SZ
  printf 'scratch=%s\n' "$RUN"
  printf 'source_copy=%s\n' "$OUT/K8.vy"
  printf 'compile_commands (TMPDIR=%s):\n' "$RUN/tmp"
  printf '  %s -f bytecode_runtime K8.vy\n' "$VYPER"
  printf '  %s --no-optimize -f bytecode_runtime K8.vy\n' "$VYPER"
  printf '  %s -O none -f bytecode_runtime K8.vy\n' "$VYPER"
  printf '  %s -O codesize -f bytecode_runtime K8.vy\n' "$VYPER"
  printf '  %s -O gas -f bytecode_runtime K8.vy (compared with default)\n' "$VYPER"
  printf '  two bytecode_runtime passes per mode; cmp succeeded\n'
  printf 'REA commands (TMPDIR=%s):\n' "$RUN/tmp"
  for mode in gas noopt codesize; do
    printf '  npx -y rea-agents@6.7.0 inspect-evm-interface %s/compile/%s.runtime.hex hex --format json\n' "$SEAT" "$mode"
  done
} > "$OUT/reproduction.txt"
