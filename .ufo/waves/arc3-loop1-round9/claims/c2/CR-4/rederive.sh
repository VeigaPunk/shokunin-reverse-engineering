#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
SEAT="$ROOT/.ufo/waves/arc3-loop1-round9/claims/c2/CR-4"
EVID="$SEAT/evidence"
SRC="$ROOT/.ufo/waves/arc3-loop1-round4/claims/c1/CR-1/vy/K8.vy"
VYPER="$ROOT/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper"
PYTHON="$ROOT/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/python"
RUN="$(mktemp -d /var/tmp/kaidoku-cr4-r9.XXXXXX)"

mkdir -p "$RUN/tmp" "$EVID/compile" "$EVID/probe"
cp "$SRC" "$EVID/K8.vy"

{
  printf 'repo_head='
  git rev-parse HEAD
  printf 'source_path=%s\n' "$SRC"
  sha256sum "$SRC" "$EVID/K8.vy"
  printf 'compiler_path=%s\n' "$VYPER"
  sha256sum "$VYPER"
  "$VYPER" --version
  printf 'scratch=%s\nTMPDIR=%s\n' "$RUN" "$RUN/tmp"
} > "$EVID/identity.txt"

for mode in noopt none; do
  case "$mode" in
    noopt) args=(--no-optimize) ;;
    none) args=(-O none) ;;
  esac
  for pass in 1 2; do
    env TMPDIR="$RUN/tmp" "$VYPER" "${args[@]}" -f bytecode_runtime "$EVID/K8.vy" > "$EVID/compile/$mode.$pass.runtime.hex"
  done
  cmp "$EVID/compile/$mode.1.runtime.hex" "$EVID/compile/$mode.2.runtime.hex"
  cp "$EVID/compile/$mode.1.runtime.hex" "$EVID/compile/$mode.runtime.hex"
  env TMPDIR="$RUN/tmp" "$VYPER" "${args[@]}" -f abi "$EVID/K8.vy" > "$EVID/compile/$mode.abi.json"
  env TMPDIR="$RUN/tmp" "$VYPER" "${args[@]}" -f method_identifiers "$EVID/K8.vy" > "$EVID/compile/$mode.methodids.json"
  env TMPDIR="$RUN/tmp" "$VYPER" "${args[@]}" -f settings "$EVID/K8.vy" > "$EVID/compile/$mode.settings.json"
done

cmp "$EVID/compile/noopt.runtime.hex" "$EVID/compile/none.runtime.hex"
cmp "$EVID/compile/noopt.abi.json" "$EVID/compile/none.abi.json"
cmp "$EVID/compile/noopt.methodids.json" "$EVID/compile/none.methodids.json"
cmp "$EVID/compile/noopt.settings.json" "$EVID/compile/none.settings.json"

{
  printf 'REA version: '
  TMPDIR="$RUN/tmp" npx -y rea-agents@6.7.0 --version
} > "$EVID/rea-version.txt"
for mode in noopt none; do
  env TMPDIR="$RUN/tmp" npx -y rea-agents@6.7.0 inspect-evm-interface "$EVID/compile/$mode.runtime.hex" hex --format json > "$EVID/probe/$mode.json" 2> "$EVID/probe/$mode.stderr"
done

"$PYTHON" "$SEAT/measure.py" "$EVID" > "$EVID/measure.txt"
{
  printf 'measurement_utc='
  date -u +%Y-%m-%dT%H:%M:%SZ
  printf 'source=%s\ncompiler=%s\n' "$SRC" "$VYPER"
  printf 'scratch=%s\nTMPDIR=%s\n' "$RUN" "$RUN/tmp"
  printf 'two bytecode_runtime passes per form: cmp succeeded\n'
  printf 'cross-form runtime/ABI/method_identifiers/settings cmp: all succeeded\n'
  printf 'REA commands (rea-agents@6.7.0):\n'
  printf '  inspect-evm-interface %s/compile/noopt.runtime.hex hex --format json\n' "$EVID"
  printf '  inspect-evm-interface %s/compile/none.runtime.hex hex --format json\n' "$EVID"
} > "$EVID/reproduction.txt"
